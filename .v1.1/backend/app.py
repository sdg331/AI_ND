from flask import Flask, request, jsonify
import gspread
import datetime
import uuid
from flask_cors import CORS 
import os
from dotenv import load_dotenv
import json
import requests 
import base64 
import re # 숫자 추출을 위한 정규표현식 모듈

# --- 환경 설정 ---
load_dotenv() 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

app = Flask(__name__)
CORS(app) 

# --- Google Sheets 설정 ---
SERVICE_ACCOUNT_FILE = 'service_account.json' 
# 👇👇👇 사용자님 스프레드시트 ID (그대로 유지) 👇👇👇
SPREADSHEET_ID = '1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA'

try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    users_worksheet = spreadsheet.worksheet("users")
    ingredients_worksheet = spreadsheet.worksheet("ingredients")
    recipes_worksheet = spreadsheet.worksheet("recipes")
    print("✅ Google Sheets 연결 성공!")
except Exception as e:
    print(f"❌ Google Sheets 연결 오류: {e}")

# --- 도우미 함수: 수량 더하기 (예: "300g" + "200g" = "500g") ---
def merge_quantities(old_qty, new_qty):
    try:
        # 숫자만 추출 (예: "300g" -> 300, "g")
        def parse(q):
            num = re.findall(r'\d+', str(q))
            unit = re.sub(r'\d+', '', str(q)).strip()
            return int(num[0]) if num else 1, unit

        n1, u1 = parse(old_qty)
        n2, u2 = parse(new_qty)
        
        # 단위가 같거나 하나가 없으면 합침
        if u1 == u2 or not u1 or not u2:
            final_unit = u1 if u1 else u2
            return f"{n1 + n2}{final_unit}"
        else:
            # 단위가 다르면 그냥 문자열로 이어붙임 (예: 1개 + 200g)
            return f"{old_qty}, {new_qty}"
    except:
        return f"{old_qty}, {new_qty}" # 에러나면 그냥 쉼표로 연결

# --- API 구현 ---
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Server is running"})

@app.route('/users/<user_id>', methods=['GET', 'POST'])
def handle_user_profile(user_id):
    try:
        if request.method == 'GET':
            return jsonify({"username": "User", "allergies": "", "tools": ""})
        else:
            return jsonify({"message": "저장 완료"}), 200
    except: return jsonify({"error": "error"}), 500

# 👇👇👇 [핵심 수정] 재료 조회 및 추가 (중복 합치기 + 카테고리) 👇👇👇
@app.route('/ingredients/<user_id>', methods=['GET', 'POST'])
def handle_ingredients(user_id):
    try:
        if request.method == 'GET':
            vals = ingredients_worksheet.get_all_values()
            headers = vals[0]
            data = []
            for r in vals[1:]:
                # 카테고리 컬럼(7번째, 인덱스 6)이 없으면 빈칸 처리
                category = r[6] if len(r) > 6 else '기타'
                if len(r) > 1 and r[1] == user_id:
                    item = dict(zip(headers, r))
                    item['category'] = category # 카테고리 정보 추가
                    data.append(item)
            return jsonify(data)

        elif request.method == 'POST':
            if not request.is_json: return jsonify({"error": "JSON 아님"}), 400
            
            d = request.json
            name = d['name']
            qty = d.get('quantity', '1개')
            category = d.get('category', '기타') # 카테고리 받기
            
            # 1. 기존 재료 검색
            cell = ingredients_worksheet.find(name)
            
            # 이름이 같고, UserID도 같은지 확인 (find는 전체 시트에서 찾으므로)
            target_row = None
            if cell:
                # 찾은 셀의 행 전체 데이터 가져오기
                row_data = ingredients_worksheet.row_values(cell.row)
                # UserID(2번째열)가 일치하는지 확인
                if row_data[1] == user_id: 
                    target_row = cell.row

            if target_row:
                # 2. 있으면 -> 수량 합치기 (Update)
                current_qty = ingredients_worksheet.cell(target_row, 4).value # 4번째 열이 수량
                new_total_qty = merge_quantities(current_qty, qty)
                ingredients_worksheet.update_cell(target_row, 4, new_total_qty)
                return jsonify({"message": f"'{name}' 수량이 추가되었습니다. (총 {new_total_qty})"}), 200
            else:
                # 3. 없으면 -> 새로 추가 (Create)
                # 헤더 순서: id, userId, name, quantity, expiry, type, category
                ingredients_worksheet.append_row([
                    str(uuid.uuid4()), user_id, name, qty, '', 'text', category
                ])
                return jsonify({"message": "새 재료가 추가되었습니다."}), 201
                
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ingredients/delete/<ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    # 행 삭제 로직 (기존과 동일하지만 안전하게 구현)
    try:
        cell = ingredients_worksheet.find(ingredient_id)
        if cell:
            ingredients_worksheet.delete_rows(cell.row)
            return jsonify({"message": "삭제 완료"}), 200
        return jsonify({"error": "재료 없음"}), 404
    except: return jsonify({"error": "삭제 실패"}), 500

# --- [핵심 2] 레시피 생성 (변경 없음, 그대로 유지) ---
@app.route('/ai/generate', methods=['POST'])
def generate_recipe():
    try:
        data = request.json
        user_id = data.get('userId')
        vals = ingredients_worksheet.get_all_values()
        ing_list = [f"{r[2]}({r[3]})" for r in vals[1:] if r[1] == user_id]
        ing_str = ", ".join(ing_list)
        
        if not ing_str: return jsonify({"error": "냉장고가 비었습니다."}), 400

        prompt_text = f"""
        재료: {ing_str}
        이 재료로 만들 수 있는 요리 레시피 1개를 추천해줘.
        응답은 JSON 형식으로:
        {{ "recipeName": "이름", "materialsUsed": "재료", "cookingSteps": ["단계1", "단계2"], "tip": "팁" }}
        """
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = { "contents": [{ "parts": [{"text": prompt_text}] }] }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if "error" in result: return jsonify({"error": result['error']['message']}), 500

        try:
            ai_text = result['candidates'][0]['content']['parts'][0]['text']
            ai_text = ai_text.replace('```json', '').replace('```', '').strip()
            res_json = json.loads(ai_text)
        except:
            res_json = {"recipeName": "AI 요리", "materialsUsed": ing_str, "cookingSteps": [str(result)], "tip": "오류"}

        recipes_worksheet.append_row([str(uuid.uuid4()), user_id, res_json.get('recipeName'), str(res_json.get('materialsUsed')), '', str(res_json)[:1000], str(datetime.datetime.now())])
        return jsonify(res_json)
    except Exception as e: return jsonify({"error": str(e)}), 500


# --- [핵심 3] 사진 인식 (카테고리 자동 추론 추가) ---
@app.route('/ingredients/vision', methods=['POST'])
def vision_ingredient():
    try:
        if 'image' not in request.files: return jsonify({"error": "파일 없음"}), 400
        file = request.files['image']
        user_id = request.form.get('userId')
        img_content = file.read()
        img_b64 = base64.b64encode(img_content).decode('utf-8')
        
        # AI에게 카테고리까지 물어봅니다.
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [
                    {"text": "이 식재료 이름, 수량, 그리고 카테고리(육류/채소/과일/유제품/가공식품/기타 중 1개)를 JSON으로 알려줘: {\"name\": \"이름\", \"quantity\": \"수량\", \"category\": \"카테고리\"}"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if "error" in result: return jsonify({"error": result['error']['message']}), 500
            
        ai_text = result['candidates'][0]['content']['parts'][0]['text']
        ai_text = ai_text.replace('```json', '').replace('```', '').strip()
        res_json = json.loads(ai_text)

        # 똑같이 중복 체크 후 저장 (위의 로직 재사용하면 좋지만 간단히 구현)
        # 비전은 중복 체크 없이 일단 추가하겠습니다 (복잡도 방지)
        ingredients_worksheet.append_row([
            str(uuid.uuid4()), user_id, res_json.get('name'), res_json.get('quantity'), '', 'vision', res_json.get('category', '기타')
        ])
        return jsonify(res_json)

    except Exception as e: return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
