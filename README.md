# FridgeChef

냉장고 속 재료로 AI가 맞춤 레시피를 추천해주는 모바일 앱

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Flask](https://img.shields.io/badge/Flask-Latest-green) ![Status](https://img.shields.io/badge/Status-Development-yellow)

## 개요

FridgeChef는 냉장고 재료를 인식하고 사용자 프로필을 반영해 개인화된 레시피를 제안한다. 

**주요 기능:**
- 냉장고 사진/영수증 OCR/직접 입력으로 재료 관리
- 사용자 맞춤 프로필 (알레르기, 보유 도구, 식단 목표)
- Google Gemini API 기반 AI 레시피 생성
- (향후) 요리 중 실시간 AI 도움

**타겟:** 20-30대 자취생 (식비 절감 + 요리 성공률 향상)

## 빠른 시작

### 요구사항
- Python 3.9+
- Google Cloud 계정 (Vision API, Gemini API)

### 설치 및 실행

```bash
# 가상환경 생성
python -m venv venv

# 활성화 (Windows)
venv\Scripts\activate.bat

# 패키지 설치
pip install -r requirements.txt

# 백엔드 실행
cd backend
python app.py
```

정상 실행 시:
```
✅ Google Sheets 연결 성공!
✅ Gemini API 준비 완료!
 * Running on http://127.0.0.1:5000
```

## 구조

```
FridgeChef/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── service_account.json (git ignored)
├── frontend/
│   ├── index.html
│   └── style.css
├── docs/
│   ├── PROJECT_SETUP.md
│   ├── CLOUD_CONFIG.md
│   ├── SHEETS_CONFIG.md
│   ├── ENV_EXAMPLE.md
│   └── TERMINAL_GUIDE.md
├── README.md
└── .gitignore
```

## 기능

### 냉장고 관리
- **사진 촬영:** Vision AI로 이미지 내 재료 자동 인식
- **영수증 스캔:** OCR로 구매 물품 목록 추출
- **직접 입력:** 수량, 유통기한과 함께 수동 등록

### 프로필 설정
| 항목 | 설정 예시 |
|------|----------|
| 알레르기 | 땅콩, 새우 |
| 좋아하는 재료 | 치즈, 고기 |
| 싫어하는 재료 | 오이, 고수 |
| 보유 도구 | 에어프라이어, 오븐 |
| 건강 목표 | 다이어트, 비건 |

### 레시피 생성
- 냉장고 재료 + 프로필 정보 → Gemini API → 맞춤 레시피
- 각 레시피별 조리시간, 난이도, 단계별 가이드 제공

### 향후 기능 (P1)
- AI 쿠킹 어시스턴트: 요리 중 실시간 Q&A
- 음성 질문 지원
- 커뮤니티 레시피 공유
- 식재료 커머스 연동

## 기술 스택

| 계층 | 기술 |
|------|------|
| Frontend | React Native, HTML/CSS/JS |
| Backend | Python Flask |
| AI | Google Vision API, Google Gemini API |
| Database | Google Sheets |

## 설정

### 사전 준비
Google Cloud 프로젝트 ID: `fridgechef-478716`

### 환경 변수
프로젝트 루트에 `.env` 파일 생성:

```env
GEMINI_API_KEY=your_api_key
GOOGLE_SHEETS_SPREADSHEET_ID=1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA
GOOGLE_PROJECT_ID=fridgechef-478716
GOOGLE_SERVICE_ACCOUNT_EMAIL=fridge-chef-bot@fridgechef-478716.iam.gserviceaccount.com
```

### 서비스 계정 설정
1. Google Cloud Console에서 서비스 계정 생성
2. JSON 키 발급 → `backend/service_account.json` 저장
3. Google Sheets 공유 권한 부여

**자세한 설정은 `docs/PROJECT_SETUP.md` 참고**

## 사용 방법

### 터미널 명령어
# 백엔드 진입
cd backend

```bash
# 가상환경 활성화
.\venv\Scripts\Activate.ps1


# 서버 실행
python app.py

문제 발생 시 `docs/TERMINAL_GUIDE.md` 참고

## 버전 관리

현재: **v1.2** (2025-11-27)

### 커밋 규칙
```
feat(feature-name): 기능 추가
fix(bug-name): 버그 수정
docs: 문서 수정
```

## 보안

아래 파일들은 커밋하지 않음:
- `.env`
- `service_account.json`
- API 키 하드코딩

`.gitignore`에 포함되어 있음.

## 팀원 가이드

처음 프로젝트를 받았다면:

1. `docs/PROJECT_SETUP.md` 읽기
2. `docs/CLOUD_CONFIG.md`에서 Google Cloud 설정 완료
3. `.env` 파일 생성 (`.env.example` 참고)
4. `python -m venv venv` → `venv\Scripts\activate.bat`
5. `pip install -r requirements.txt`
6. `cd backend && python app.py`

문제는 `docs/TERMINAL_GUIDE.md`에서 찾기

## 라이선스

MIT

---

**FridgeChef** - "냉장고를 열면 AI 셰프가 대기 중입니다"
