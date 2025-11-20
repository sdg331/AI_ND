import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ .env 파일에서 API 키를 못 찾았어요!")
else:
    print(f"✅ API 키 확인됨: {api_key[:5]}...")
    try:
        client = genai.Client(api_key=api_key)
        print("\n🔍 사용 가능한 모델 목록을 조회합니다...")
        
        # 모델 목록 가져오기
        for m in client.models.list(config={"page_size": 100}):
            # 요리 추천(generateContent)이 가능한 모델만 표시
            if "generateContent" in m.supported_actions:
                print(f"👉 모델 이름: {m.name}")
                
        print("\n✅ 조회가 끝났습니다. 위 목록에 있는 이름 중 하나를 쓰면 무조건 됩니다!")
        
    except Exception as e:
        print(f"❌ 조회 실패: {e}")
