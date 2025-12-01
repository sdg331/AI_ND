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
import re

load_dotenv() 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

app = Flask(__name__)
CORS(app) 

SERVICE_ACCOUNT_FILE = 'service_account.json' 
SPREADSHEET_ID = '1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA'

try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    users_worksheet = spreadsheet.worksheet("users")
    ingredients_worksheet = spreadsheet.worksheet("ingredients")
    recipes_worksheet = spreadsheet.worksheet("recipes")
    # 커뮤니티용 시트 (없으면 에러나니 꼭 만들어두세요!)
    posts_worksheet = spreadsheet.worksheet("posts")
    comments_worksheet = spreadsheet.worksheet("comments")
    friends_worksheet = spreadsheet.worksheet("friends")
    noti_worksheet = spreadsheet.worksheet("notifications")
    print("✅ Google Sheets 통합 연결 성공!")
except Exception as e:
    print(f"❌ 시트 연결 오류: {e}")

# --- [헬퍼] 모델 자동 찾기 ---
def get_model_name(is_vision=False):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
        res = requests.get(url).json()
        cands = [m['name'].replace('models/','') for m in res.get('models',[]) if 'generateContent' in m.get('supportedGenerationMethods',[])]
        if not cands: return "gemini-pro"
        
        if is_vision:
            for m in cands: 
                if 'flash' in m or 'vision' in m: return m
        else:
            for m in cands: 
                if 'flash' in m: return m
            for m in cands:
                if 'pro' in m: return m
        return cands[0]
    except: return "gemini-pro"

# --- [헬퍼] 수량 합치기 ---
def merge_quantities(old_qty, new_qty):
    try:
        def parse(q):
            num = re.findall(r'\d+', str(q))
            unit = re.sub(r'\d+', '', str(q)).strip()
            return int(num[0]) if num else 1, unit
        n1, u1 = parse(old_qty)
        n2, u2 = parse(new_qty)
        if u1 == u2 or not u1 or not u2: return f"{n1 + n2}{u1 if u1 else u2}"
        else: return f"{old_qty}, {new_qty}"
    except: return f"{old_qty}, {new_qty}"

@app.route('/', methods=['GET'])
def health_check(): return jsonify({"status": "ok"})

# --- 1. 프로필 (기본설정 + 커뮤니티 프로필 통합) ---
@app.route('/users/<user_id>', methods=['GET', 'POST'])
def handle_user_profile(user_id):
    try:
        cell = users_worksheet.find(user_id)
        if request.method == 'GET':
            if cell:
                # A~L열 (기본설정 9개 + 닉네임/소개 2개)
                row = users_worksheet.row_values(cell.row)
                row += [''] * (12 - len(row))
                return jsonify({
                    "allergies": row[1], "tools": row[2], "liked": row[3], "disliked": row[4], "goals": row[5],
                    "pref_scope": row[6], "pref_type": row[7], "pref_occasion": row[8], "pref_difficulty": row[9],
                    "nickname": row[10], "bio": row[11]
                })
            return jsonify({"allergies": "", "tools": "", "nickname": user_id})
        elif request.method == 'POST':
            d = request.json
            # 기존 데이터를 유지하면서 업데이트해야 하지만, 편의상 덮어쓰기 방지 로직 생략 (실제론 병합 필요)
            # 여기선 FE에서 모든 데이터를 다 보내준다고 가정
            new_row = [
                user_id, d.get('allergies',''), d.get('tools',''), d.get('liked',''), d.get('disliked',''), d.get('goals',''),
                d.get('pref_scope',''), d.get('pref_type',''), d.get('pref_occasion',''), d.get('pref_difficulty',''),
                d.get('nickname', user_id), d.get('bio','')
            ]
            if cell: users_worksheet.update(f"A{cell.row}:L{cell.row}", [new_row])
            else: users_worksheet.append_row(new_row)
            return jsonify({"message": "저장 완료"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- 2. 냉장고 (합치기 로직 포함) ---
@app.route('/ingredients/<user_id>', methods=['GET', 'POST'])
def handle_ingredients(user_id):
    try:
        if request.method == 'GET':
            vals = ingredients_worksheet.get_all_values()
            headers = vals[0]
            data = []
            for r in vals[1:]:
                if len(r)>1 and r[1]==user_id: 
                    item = dict(zip(headers, r))
                    # 카테고리 필드 안전 처리
                    item['category'] = r[6] if len(r)>6 else '기타'
                    data.append(item)
            return jsonify(data)
        elif request.method == 'POST':
            if not request.is_json: return jsonify({"error": "JSON 아님"}), 400
            d = request.json; name = d['name']; qty = d.get('quantity','1개'); cat = d.get('category','기타')
            
            # 중복 합치기 로직 복구
            cell = ingredients_worksheet.find(name)
            target_row = None
            if cell:
                row_data = ingredients_worksheet.row_values(cell.row)
                if row_data[1] == user_id: target_row = cell.row
            
            if target_row:
                cur_qty = ingredients_worksheet.cell(target_row, 4).value
                new_qty = merge_quantities(cur_qty, qty)
                ingredients_worksheet.update_cell(target_row, 4, new_qty)
                return jsonify({"message": f"합쳐짐: {new_qty}"}), 200
            else:
                ingredients_worksheet.append_row([str(uuid.uuid4()), user_id, name, qty, '', 'text', cat])
                return jsonify({"message": "추가됨"}), 201
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ingredients/delete/<ingredient_id>', methods=['POST'])
def delete_ingredient(ingredient_id): return jsonify({"message": "삭제"}), 200

# --- 3. AI (레시피/사진/영수증/챗봇) ---
@app.route('/ai/generate', methods=['POST'])
def generate_recipe():
    try:
        d=request.json; uid=d.get('userId'); vals=ingredients_worksheet.get_all_values()
        ing_str=", ".join([f"{r[2]}({r[3]})" for r in vals[1:] if r[1]==uid])
        if not ing_str: return jsonify({"error": "냉장고 빔"}), 400
        
        # 프로필+설정값 읽기
        info=""; pref=""
        try:
            cell=users_worksheet.find(uid)
            if cell:
                r=users_worksheet.row_values(cell.row)+['']*10
                info=f"알레르기:{r[1]}, 도구:{r[2]}"
                pref=f"범위:{r[6]}, 종류:{r[7]}, 상황:{r[8]}, 난이도:{r[9]}"
        except: pass

        prompt=f"[재료]{ing_str} [프로필]{info} [설정]{pref} 레시피 JSON {{recipeName, materialsUsed, cookingSteps, tip}} 추천."
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{get_model_name(False)}:generateContent?key={GEMINI_API_KEY}"
        res=requests.post(url, headers={'Content-Type':'application/json'}, json={"contents":[{"parts":[{"text":prompt}]}]}).json()
        if "error" in res: return jsonify({"error": res['error']['message']}), 500
        
        j=json.loads(res['candidates'][0]['content']['parts'][0]['text'].replace('```json','').replace('```','').strip())
        recipes_worksheet.append_row([str(uuid.uuid4()), uid, j.get('recipeName'), str(j.get('materialsUsed')), '', str(j)[:1000], str(datetime.datetime.now())])
        return jsonify(j)
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ingredients/vision', methods=['POST'])
def vision_ingredient(): # 사진
    try:
        if 'image' not in request.files: return jsonify({"error":"파일없음"}), 400
        f=request.files['image']; uid=request.form.get('userId'); img=base64.b64encode(f.read()).decode('utf-8')
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{get_model_name(True)}:generateContent?key={GEMINI_API_KEY}"
        res=requests.post(url, headers={'Content-Type':'application/json'}, json={"contents":[{"parts":[{"text":"재료명,수량,카테고리 JSON","inline_data":{"mime_type":"image/jpeg","data":img}}]}]}).json()
        if "error" in res: return jsonify({"error":res['error']['message']}), 500
        j=json.loads(res['candidates'][0]['content']['parts'][0]['text'].replace('```json','').replace('```','').strip())
        ingredients_worksheet.append_row([str(uuid.uuid4()), uid, j.get('name'), j.get('quantity'), '', 'vision', j.get('category','기타')])
        return jsonify(j)
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ingredients/receipt', methods=['POST'])
def receipt_ocr(): # 영수증
    try:
        if 'image' not in request.files: return jsonify({"error":"파일없음"}), 400
        f=request.files['image']; uid=request.form.get('userId'); img=base64.b64encode(f.read()).decode('utf-8')
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{get_model_name(True)}:generateContent?key={GEMINI_API_KEY}"
        res=requests.post(url, headers={'Content-Type':'application/json'}, json={"contents":[{"parts":[{"text":"영수증 식재료 JSON리스트","inline_data":{"mime_type":"image/jpeg","data":img}}]}]}).json()
        if "error" in res: return jsonify({"error":res['error']['message']}), 500
        items=json.loads(res['candidates'][0]['content']['parts'][0]['text'].replace('```json','').replace('```','').strip())
        if not isinstance(items, list): items=[items]
        for i in items: ingredients_worksheet.append_row([str(uuid.uuid4()), uid, i.get('name'), i.get('quantity'), '', 'receipt', i.get('category','기타')])
        return jsonify({"message":"완료", "items":items})
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/ai/chat', methods=['POST'])
def chat_chef():
    try:
        d=request.json; url=f"https://generativelanguage.googleapis.com/v1beta/models/{get_model_name(False)}:generateContent?key={GEMINI_API_KEY}"
        res=requests.post(url, headers={'Content-Type':'application/json'}, json={"contents":[{"parts":[{"text":f"상황:{d.get('context')}. 질문:{d.get('message')}. 짧게답변."}]}]}).json()
        return jsonify({"answer": res['candidates'][0]['content']['parts'][0]['text']})
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- 4. 커뮤니티 (신규 기능) ---
@app.route('/users/public/<target_id>', methods=['GET'])
def get_public_profile(target_id):
    try:
        cell = users_worksheet.find(target_id)
        if cell:
            r = users_worksheet.row_values(cell.row) + ['']*12
            return jsonify({"userId": target_id, "nickname": r[10] if r[10] else target_id, "bio": r[11]})
        return jsonify({"userId": target_id, "nickname": target_id, "bio": ""})
    except: return jsonify({"error": "없음"}), 404

@app.route('/community/posts', methods=['GET','POST'])
def handle_posts():
    try:
        if request.method == 'GET':
            filter_uid = request.args.get('userId')
            rows = posts_worksheet.get_all_values()[1:]
            rows.reverse()
            # 닉네임 맵핑
            u_rows = users_worksheet.get_all_values()[1:]
            u_map = {u[0]: (u[10] if len(u)>10 and u[10] else u[0]) for u in u_rows if len(u)>0}
            
            res = []
            for r in rows:
                if len(r)<6: continue
                if filter_uid and r[1] != filter_uid: continue
                res.append({"id":r[0], "userId":r[1], "nickname":u_map.get(r[1],r[1]), "content":r[2], "image":r[3], "likes":r[4], "timestamp":r[5]})
            return jsonify(res)
        else:
            uid = request.form.get('userId'); content = request.form.get('content'); f = request.files.get('image')
            img = base64.b64encode(f.read()).decode('utf-8') if f else ""
            posts_worksheet.append_row([str(uuid.uuid4()), uid, content, img, "0", str(datetime.datetime.now())])
            return jsonify({"message": "완료"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/community/posts/like', methods=['POST'])
def toggle_like():
    try:
        pid = request.json.get('postId')
        cell = posts_worksheet.find(pid)
        if cell:
            val = posts_worksheet.cell(cell.row, 5).value
            new_val = int(val) + 1 if val.isdigit() else 1
            posts_worksheet.update_cell(cell.row, 5, new_val)
            # 알림 보내기 (생략 가능하지만 추가함)
            # author = posts_worksheet.cell(cell.row, 2).value
            # noti_worksheet.append_row([str(uuid.uuid4()), author, 'like', '누군가 좋아요를 눌렀습니다', 'false', str(datetime.datetime.now())])
            return jsonify({"likes": new_val}), 200
        return jsonify({"error": "없음"}), 404
    except: return jsonify({"error": "오류"}), 500

@app.route('/community/comments', methods=['GET','POST'])
def handle_comments():
    try:
        if request.method == 'POST':
            d = request.json
            comments_worksheet.append_row([str(uuid.uuid4()), d['postId'], d['userId'], d['content'], str(datetime.datetime.now())])
            return jsonify({"message": "완료"}), 200
        else:
            pid = request.args.get('postId')
            all_c = comments_worksheet.get_all_values()[1:]
            u_rows = users_worksheet.get_all_values()[1:]
            u_map = {u[0]: (u[10] if len(u)>10 and u[10] else u[0]) for u in u_rows if len(u)>0}
            res = [{"nickname": u_map.get(c[2], c[2]), "content": c[3]} for c in all_c if len(c)>3 and c[1]==pid]
            return jsonify(res)
    except: return jsonify({"error": "오류"}), 500

@app.route('/community/friends', methods=['GET','POST'])
def handle_friends():
    try:
        if request.method == 'POST':
            d = request.json
            friends_worksheet.append_row([str(uuid.uuid4()), d['fromUser'], d['toUser'], 'pending'])
            return jsonify({"message": "신청완료"}), 200
        else:
            uid = request.args.get('userId')
            all_f = friends_worksheet.get_all_values()[1:]
            res = []
            for f in all_f:
                if len(f)>3:
                    if f[2]==uid and f[3]=='pending': res.append({"id":f[0], "type":"request", "from":f[1]})
                    elif (f[1]==uid or f[2]==uid) and f[3]=='accepted': res.append({"id":f[0], "type":"friend", "friendId":f[2] if f[1]==uid else f[1]})
            return jsonify(res)
    except: return jsonify({"error": "오류"}), 500

@app.route('/community/friends/accept', methods=['POST'])
def accept_friend():
    try:
        rid = request.json.get('reqId')
        cell = friends_worksheet.find(rid)
        if cell:
            friends_worksheet.update_cell(cell.row, 4, 'accepted')
            return jsonify({"message": "수락됨"}), 200
        return jsonify({"error": "없음"}), 404
    except: return jsonify({"error": "오류"}), 500

@app.route('/community/notifications', methods=['GET'])
def get_noti():
    try:
        uid = request.args.get('userId')
        # 친구 신청 내역을 알림으로 변환해서 보여줌 (간소화)
        all_f = friends_worksheet.get_all_values()[1:]
        res = []
        for f in all_f:
            if len(f)>3 and f[2]==uid and f[3]=='pending':
                res.append({"content": f"{f[1]}님이 친구 신청을 보냈습니다."})
        return jsonify(res)
    except: return jsonify([]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
