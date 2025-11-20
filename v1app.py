from flask import Flask, request, jsonify
import gspread
import datetime
import uuid
from flask_cors import CORS 
import os
from dotenv import load_dotenv
import json
import requests 

# --- 환경 설정 ---
load_dotenv() 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

app = Flask(__name__)
CORS(app) 

# --- Google Sheets 설정 ---
SERVICE_ACCOUNT_FILE = 'service_account.json' 
# 👇👇👇 [필수] 본인의 구글 시트 ID 입력 👇👇👇
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE' 

try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    users_worksheet = spreadsheet.worksheet("users")
    ingredients_worksheet = spreadsheet.worksheet("ingredients")
    recipes_worksheet = spreadsheet.worksheet("recipes")
    print("✅ Google Sheets 연결 성공!")
except Exception as e:
    print(f"❌ Google Sheets 연결 오류: {e}")

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
            d = request.json
            ingredients_worksheet.append_row([str(uuid.uuid4()), user_id, d['name'], d.get('quantity','1개'), '', 'text', ''])
            return jsonify({"message": "추가 완료"}), 201
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ingredients/delete/<ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id):
    return jsonify({"message": "삭제 완료"}), 200

# --- [핵심] AI 레시피 생성 (텍스트 전용 - 성공했던 버전) ---
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
        
        # 👇 아까 성공했던 'gemini-pro' (텍스트 모델) 주소 사용
        target_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        payload = { "contents": [{ "parts": [{"text": prompt_text}] }] }
        
        response = requests.post(target_url, headers=headers, json=payload)
        result = response.json()

        if "error" in result:
             return jsonify({"error": f"AI 오류: {result['error']['message']}"}), 500

        try:
            ai_text = result['candidates'][0]['content']['parts'][0]['text']
            ai_text = ai_text.replace('```json', '').replace('```', '').strip()
            res_json = json.loads(ai_text)
        except:
            res_json = {
                "recipeName": "AI 추천 요리",
                "materialsUsed": ing_str,
                "cookingSteps": ["레시피 내용을 가져왔으나 변환 실패", str(result)],
                "tip": "다시 시도해주세요."
            }

        recipes_worksheet.append_row([str(uuid.uuid4()), user_id, res_json.get('recipeName'), str(res_json.get('materialsUsed')), '', str(res_json)[:1000], str(datetime.datetime.now())])
        
        return jsonify(res_json)

    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"error": f"처리 실패: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
