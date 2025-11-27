# 🍳 FridgeChef - 내 냉장고 속 AI 셰프

> **AI와 멀티모달 분석으로, 냉장고 재료 기반 맞춤 레시피를 추천받는 모바일 쿠킹 솔루션**

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![React Native](https://img.shields.io/badge/React%20Native-Latest-blue) ![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Active-red) ![Status](https://img.shields.io/badge/Status-Active%20Development-green)

---

## 📋 프로젝트 개요

**FridgeChef**는 냉장고 속 재료와 사용자의 요리 프로필을 기반으로 **AI가 생성한 맞춤형 레시피**를 제공합니다.

### 🎯 핵심 가치

| 문제 | 해결책 |
|------|--------|
| 💰 식비 낭비 | 냉장고 재료를 최대한 활용하는 레시피 생성 |
| ⏰ 시간 소비 | 사진 한 장으로 자동 재료 인식 & 레시피 추천 |
| 😰 요리 초보자 불안감 | AI 쿠킹 어시스턴트가 실시간으로 도움 제공 |
| 🚫 식단/알레르기 관리 | 개인 프로필 기반 완전 맞춤형 레시피 |

### 💡 "내 손안의 AI 셰프 + 요리 코치"

```
냉장고 사진 인식 → 맞춤 프로필 반영 → AI 레시피 생성 → 실시간 요리 지원
```

---

## 🚀 빠른 시작

### 필수 조건

- Python 3.9+
- Windows / macOS / Linux
- 인터넷 연결

### 로컬 실행 (3단계)

```bash
# 1️⃣ 가상환경 생성
python -m venv venv

# 2️⃣ 가상환경 활성화
# Windows CMD
venv\Scripts\activate.bat
# Windows PowerShell (오류 시 docs/TERMINAL_GUIDE.md 참고)
venv\Scripts\Activate.ps1

# 3️⃣ 패키지 설치 & 서버 실행
pip install -r requirements.txt
cd backend
python app.py
```

✅ 성공 메시지:
```
✅ Google Sheets 연결 성공!
✅ Gemini API 준비 완료!
 * Running on http://127.0.0.1:5000
```

---

## 🏗️ 프로젝트 구조

```
FridgeChef/
├── backend/
│   ├── app.py              # Flask 메인 서버
│   ├── config.py           # 설정 파일
│   ├── requirements.txt     # Python 패키지
│   └── service_account.json # Google Cloud 인증 (git ignored)
│
├── frontend/
│   ├── index.html          # React Native Web 진입점
│   ├── style.css           # 스타일
│   └── app.js              # 메인 컴포넌트
│
├── docs/                   # 📚 설정 및 가이드 문서
│   ├── PROJECT_SETUP.md
│   ├── CLOUD_CONFIG.md
│   ├── SHEETS_CONFIG.md
│   ├── ENV_EXAMPLE.md
│   └── TERMINAL_GUIDE.md
│
├── .env                    # 환경 변수 (git ignored)
├── .gitignore
├── README.md
├── CHANGELOG.md            # 버전 변경사항
└── FridgeChef-발표자료.pptx # 프레젠테이션
```

---

## ✨ 주요 기능

### 1️⃣ 나의 냉장고 (재료 등록)

```
냉장고 사진 촬영
├─ Vision AI가 자동으로 재료 인식
├─ OCR 영수증 스캔 → 마트 구매 물품 자동 추출
└─ 직접 텍스트 입력 → 유통기한/수량 함께 기록
```

**지원 방식:**
- 📷 냉장고 내부 이미지 분석
- 🧾 영수증 OCR 스캔
- ⌨️ 직접 입력 (재료명, 수량)

---

### 2️⃣ 프로필 설정 (맞춤화)

사용자의 식단 정보를 저장하면, AI가 이를 반영해 레시피를 생성합니다.

| 설정 항목 | 예시 |
|----------|------|
| 🚫 알레르기 | 땅콩, 새우, 계란 |
| ❤️ 좋아하는 재료 | 치즈, 고기, 마늘 |
| 💔 싫어하는 재료 | 오이, 당근, 고수 |
| 🔪 보유 조리도구 | 에어프라이어, 오븐, 전자레인지 |
| 🎯 건강 목표 | 다이어트, 비건, 저염식, 고단백 |

---

### 3️⃣ AI 레시피 생성

**"오늘 뭐 해먹지?" 버튼 클릭 → AI가 자동 생성**

```
냉장고 재료 ＋ 개인 프로필 → Gemini API → 맞춤 레시피 제안
```

**생성되는 정보:**
- 📝 요리명 & 설명
- ⏱️ 예상 조리 시간
- 📊 난이도 (초간단 / 중간 / 고급)
- 🛒 사용할 재료 (냉장고 vs 추가 구매)
- 👨‍🍳 단계별 조리 방법
- (P1) 영양 정보 & 팁

---

### 4️⃣ 쿠킹 모드 & AI 어시스턴트

**선택한 레시피로 "요리 시작" → 단계별 가이드 제공**

```
[Step 1] 재료 준비
    ↓
[Step 2] 기본 손질
    ↓
[Step 3] 조리 시작
    ↓
💬 "어? 이 부분 이렇게 하는 게 맞아?" 
   → AI가 즉시 해결책 제안
```

**AI 쿠킹 어시스턴트 (P1 확장):**
- 🔥 "간이 짜요" → 대처 방법 제안
- 🥒 "이 재료 없어요" → 대체 재료 추천
- ⏱️ "얼마나 더 익혀야 해?" → 타이밍 조언
- 🎵 음성 질문 지원 (손 더러울 때 유용)

---

## 🛠️ 기술 스택

### 프론트엔드
- **React Native** - iOS/Android 동시 지원
- **HTML/CSS/JavaScript** - 웹 버전

### 백엔드
- **Python Flask** - REST API 서버
- **Google Cloud Vision API** - 이미지 인식 (냉장고 사진, 영수증 OCR)
- **Google Gemini API** - 레시피 생성 & AI 챗봇

### 데이터 & 저장소
- **Google Sheets** - 사용자 데이터 & 레시피 저장
- **환경 변수 (.env)** - API 키 관리

---

## 📚 설정 및 실행 가이드

### 📖 문서 구조

본격적인 설정이나 실행에 문제가 있다면 **docs 폴더의 문서들**을 참고하세요.

| 문서 | 내용 |
|------|------|
| `docs/PROJECT_SETUP.md` | 전체 설정 개요 및 흐름 |
| `docs/CLOUD_CONFIG.md` | Google Cloud 프로젝트 & 서비스 계정 설정 |
| `docs/SHEETS_CONFIG.md` | Google Sheets 연동 & 공유 권한 설정 |
| `docs/ENV_EXAMPLE.md` | 환경 변수(.env) 작성 방법 |
| `docs/TERMINAL_GUIDE.md` | 터미널 명령어 & 오류 해결 |

### ⚡ 핵심 설정 체크리스트

- [ ] Google Cloud 프로젝트 생성 (`fridgechef-478716`)
- [ ] 서비스 계정 키(JSON) 발급 → `backend/service_account.json` 저장
- [ ] Google Sheets ID 확인 → 서비스 계정에 편집자 권한 부여
- [ ] `.env` 파일 생성 및 API 키 입력
- [ ] 가상환경 생성 & 활성화
- [ ] `python app.py` 실행 → 서버 정상 작동 확인

**자세한 설정은 `docs/PROJECT_SETUP.md`를 참고하세요.**

---

## 🚀 로드맵 (향후 확장)

### P0 (현재 진행 중)
- ✅ 냉장고 재료 등록 (사진/영수증/텍스트)
- ✅ 프로필 설정 & 맞춤 레시피 생성
- ✅ 3개 탭 UI (냉장고 / AI 셰프 / 프로필)

### P1 (다음 버전)
- 🔄 OCR 영수증 스캔 고도화
- 🔄 AI 쿠킹 어시스턴트 (실시간 챗봇)
- 🔄 음성 질문 기능
- 🔄 커뮤니티 레시피 공유

### P2 (장기 계획)
- 제휴 식재료 커머스 연동
- 프리미엄 구독 모델
  - 광고 제거
  - 음성 질문 무제한 이용
  - 고급 레시피 접근
- 건강 데이터 연동 (칼로리 추적 등)

---

## 📊 프로젝트 정보

| 항목 | 값 |
|------|-----|
| **프로젝트명** | FridgeChef |
| **설명** | 내 냉장고 속 AI 셰프 |
| **타겟** | 20~30대 자취생 |
| **Google Cloud 프로젝트 ID** | fridgechef-478716 |
| **Google Sheets ID** | 1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA |
| **상태** | Active Development 🟢 |
| **최근 업데이트** | 2025-11-27 |

---

## 📝 커밋 컨벤션

깃허브 커밋 메시지는 다음 형식을 따릅니다:

```
type(scope): subject

body

footer
```

### 타입 정의

- `feat` - 새 기능 추가
- `fix` - 버그 수정
- `docs` - 문서 수정
- `style` - 코드 스타일 (기능 변화 X)
- `refactor` - 코드 리팩토링
- `test` - 테스트 추가/수정
- `chore` - 빌드, 의존성 등

### 예시

```
feat(recipe): Gemini API 레시피 생성 기능 구현

- 사용자 냉장고 재료 분석
- 개인 프로필 반영
- JSON 형식 응답

Closes #12
```

---

## 🔐 보안 & 민감 정보

### ⚠️ 절대 커밋하지 말 것

```
❌ .env
❌ service_account.json
❌ API 키 (하드코딩)
```

### ✅ 대신 사용할 것

```
✅ .env.example (형식만 포함)
✅ docs에 "어디서 생성하는지" 기록
✅ 환경 변수로 관리
```

### .gitignore 확인

```
.env
service_account.json
venv/
__pycache__/
*.pyc
.vscode/
.DS_Store
```

---

## 🤝 기여 및 문의

### 버그 리포트 & 기능 요청

GitHub Issues를 통해 보고해 주세요.

### 커뮤니케이션

- 📧 이메일: [your-email@example.com]
- 💬 Slack: [workspace-link]

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

## 🎯 버전 정보

현재 버전: **v1.0.0** (2025-11-27)

자세한 변경사항은 `CHANGELOG.md`를 참고하세요.

---

## 🙏 감사의 말

- 🏫 Google Cloud 무료 크레딧 제공
- 🤖 Gemini API 팀
- 📊 Google Sheets API 팀

---

**"냉장고를 열면, AI 셰프가 준비되어 있어요"** 🍳✨
