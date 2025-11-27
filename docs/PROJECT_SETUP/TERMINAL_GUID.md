# 4. 로컬 실행 / 터미널 가이드

## 4-1. 가상환경 생성 (최초 1회)
```text
프로젝트 루트에서
python -m venv venv
```

## 4-2. 가상환경 활성화
```text
PowerShell: venv\Scripts\Activate.ps1
CMD(명령 프롬프트): venv\Scripts\activate.bat
```

## 4-3. 패키지 설치 (최초 1회)
```text
pip install -r requirements.txt
또는
pip install flask flask-cors google-cloud-vision python-dotenv google-generativeai openpyxl
```

## 4-4. 백엔드 실행
```text
cd backend
python app.py
```
정상 실행 시: Running on http://127.0.0.1:5000


## 4-5. 자주 발생하는 오류와 해결

- ❌ `service_account.json` 파일 없음  
  - 해결: `CLOUD_CONFIG.md`를 참고하여 서비스 계정 키(JSON)를 만들고  
    `backend/service_account.json` 이름으로 저장

- ❌ venv 활성화 안 됨 (`Activate.ps1 인식 안 됨`)  
  - 해결:
    - `python -m venv venv`로 다시 생성
    - PowerShell에서는  
      `venv\Scripts\Activate.ps1`  
      CMD에서는  
      `venv\Scripts\activate.bat`
