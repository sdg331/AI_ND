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

# --- 환경 설정 ---
load_dotenv() 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

app = Flask(__name__)
CORS(app) 

# --- Google Sheets 설정 ---
SERVICE_ACCOUNT_FILE = 'service_account.json' 
# 👇👇👇 [필수] 본인의 구글 시트 ID 입력 👇👇👇
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


# 👇👇👇 [새로운 방법] 사용 가능한 모델을 직접 조회하는 함수 👇👇👇
def get_dynamic_model_name():
    try:
        # 1. 구글에 "내가 쓸 수 있는 모델 목록" 요청 (ListModels)
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # 2. 목록에서 'generateContent'(채팅/생성) 기능이 있는 모델 찾기
        if 'models' in data:
            # 우선순위 1: 1.5-flash (가장 빠르고 다재다능함)
            for m in data['models']:
                if 'gemini-1.5-flash' in m['name'] and 'generateContent' in m['supportedGenerationMethods']:
                    return m['name'].replace("models/", "")
            
            # 우선순위 2: gemini-pro (가장 기본)
            for m in data['models']:
                if 'gemini-pro' in m['name'] and 'generateContent' in m['supportedGenerationMethods']:
                    return m['name'].replace("models/", "")
            
            # 우선순위 3: 아무거나 되는 거 하나 잡기
            for m in data['models']:
                if 'generateContent' in m['supportedGenerationMethods']:
                    return m['name'].replace("models/", "")
        
        # 목록 조회 실패 시 어쩔 수 없이 기본값 반환
        return "gemini-1.5-flash"
    except:
        return "gemini-1.5-flash"

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

@app.route('/ingredients/<user_id>', methods=['GET', 'POST'])
def handle_ingredients(user_id):
    try:
        if request.method == 'GET':
            vals = ingredients_worksheet.get_all_values()
            headers = vals[0]
            data = []
            for r in vals[1:]:
                if len(r)>1 and r[1]==user_id: data.append(dict(zip(headers, r)))
            return jsonify(data)
        elif request.method == 'POST':
            if request.is_json:
                d = request.json
                ingredients_worksheet.append_row([str(uuid.uuid4()), user_id, d['name'], d.get('quantity','1개'), '', 'text', ''])
                return jsonify({"message": "추가 완료"}), 201
            else:
                return jsonify({"error": "JSON 형식이 아닙니다"}), 400
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ingredients/delete/<ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    return jsonify({"message": "삭제 완료"}), 200

# --- [핵심 1] 레시피 생성 (동적 모델 적용) ---
@app.route('/ai/generate', methods=['POST'])
def generate_recipe():
    try:
        data = request.json
        user_id = data.get('userId')
        
        vals = ingredients_worksheet.get_all_values()
        ing_list = [f"{r[2]}({r[3]})" for r in vals[1:] if r[1] == user_id]
        ing_str = ", ".join(ing_list)
        
        if not ing_str: return jsonify({"error": "냉장고가 비었습니다."}), 400

        # 👇 [중요] 사용할 모델 이름을 실시간으로 받아옵니다.
        current_model = get_dynamic_model_name()
        print(f"🤖 레시피 생성에 사용된 모델: {current_model}")

        prompt_text = f"""
        재료: {ing_str}
        이 재료로 만들 수 있는 요리 레시피 1개를 추천해줘.
        응답은 JSON 형식으로:
        {{ "recipeName": "이름", "materialsUsed": "재료", "cookingSteps": ["단계1", "단계2"], "tip": "팁" }}
        """
        
        # 찾아낸 모델로 요청 주소 생성
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = { "contents": [{ "parts": [{"text": prompt_text}] }] }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if "error" in result:
             return jsonify({"error": f"AI 오류: {result['error']['message']}"}), 500

        try:
            ai_text = result['candidates'][0]['content']['parts'][0]['text']
            ai_text = ai_text.replace('```json', '').replace('```', '').strip()
            res_json = json.loads(ai_text)
        except:
            res_json = {"recipeName": "AI 요리", "materialsUsed": ing_str, "cookingSteps": [str(result)], "tip": "오류"}

        recipes_worksheet.append_row([str(uuid.uuid4()), user_id, res_json.get('recipeName'), str(res_json.get('materialsUsed')), '', str(res_json)[:1000], str(datetime.datetime.now())])
        return jsonify(res_json)
    except Exception as e:
        return jsonify({"error": f"실패: {str(e)}"}), 500


# --- [핵심 2] 사진 인식 (동적 모델 적용) ---
@app.route('/ingredients/vision', methods=['POST'])
def vision_ingredient():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "이미지 파일이 없습니다."}), 400
        
        file = request.files['image']
        user_id = request.form.get('userId')
        
        img_content = file.read()
        img_b64 = base64.b64encode(img_content).decode('utf-8')
        
        # 👇 [중요] 사진도 똑같이 조회된 모델 사용
        current_model = get_dynamic_model_name()
        print(f"📸 사진 분석에 사용된 모델: {current_model}")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{current_model}:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [
                    {"text": "이 사진에 있는 식재료 이름과 수량을 JSON으로 알려줘: {\"name\": \"이름\", \"quantity\": \"수량\"}. 재료가 여러개면 가장 메인 재료 1개만."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if "error" in result:
            return jsonify({"error": f"사진 분석 실패: {result['error']['message']}"}), 500
            
        ai_text = result['candidates'][0]['content']['parts'][0]['text']
        ai_text = ai_text.replace('```json', '').replace('```', '').strip()
        
        try:
            res_json = json.loads(ai_text)
        except:
            res_json = {"name": "사진재료", "quantity": "1개"}

        ingredients_worksheet.append_row([str(uuid.uuid4()), user_id, res_json.get('name','알수없음'), res_json.get('quantity','1개'), '', 'vision', ''])
        return jsonify(res_json)

    except Exception as e:
        return jsonify({"error": f"오류 발생: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
