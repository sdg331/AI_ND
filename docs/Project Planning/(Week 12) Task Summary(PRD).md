# PRD - cookmate (내 냉장고 속 AI 셰프)

## 프로젝트 개요 (The "Vibe" in Spec)

**프로젝트 명:** cookmate (내 냉장고 속 AI 셰프)

**핵심 컨셉:** AI가 냉장고 속 재료와 개인 프로필을 분석해 최적의 맞춤형 레시피를 생성하고, 요리 과정의 문제 해결까지 실시간으로 지원하는 초개인화 쿠킹 솔루션. **'절약', '맞춤', '성공적인 경험'**을 Vibe로 한다.

**핵심 목표:** 사용자가 냉장고 재료를 효율적으로 활용하여 음식물 낭비를 줄이고, 요리 초보자도 쉽게 요리에 성공하여 자신감을 얻도록 한다.

**타겟 페르소나:**

이름: 김지금  
나이: 23세  
직업: 대학생 (현재 대학교 근처에서 자취 중)  
상황: 주머니 사정이 넉넉하지 않고, 집에 있는 재료를 최대한 활용해 식비를 줄이고자 함. 냉장고 안 재료가 많지 않으며, 요리 정보가 부족한 초보자.

---

## 상세 기능 명세 P0 (Core Features - MVP)

### 나의 냉장고: 간편 재료 등록 시스템

[User Story] 사용자는 세 가지 방법으로 식재료를 등록할 수 있다:

1. 냉장고 사진 촬영 → AI 인식 후 자동 등록
2. 영수증 스캔 → OCR로 구매한 식재료 일괄 등록
3. 텍스트 입력 → 직접 재료명 입력

[Spec]  
- DB 구조: Google Sheets "냉장고 재료" 워크시트에 id, user_id, item_name, quantity, expiry_date, registered_at 열 생성
- API: POST /api/fridge/items/image (Base64 이미지 전송) → Gemini-Pro-Vision API로 재료 목록 및 수량 추출 → Google Sheets에 저장
- GET /api/fridge/items → user_id별 재료 목록 JSON 반환

### 개인 프로필 설정 및 관리

[User Story]  
- 알레르기 정보, 보유 조리 도구, 개인 목표를 설정 가능  
- 예: 알레르기 체크, 에어프라이어 보유 여부, 다이어트/비건/저염식 목표 선택

[Spec]  
- DB: Google Sheets "사용자 프로필" 워크시트에 user_id, preferences, dislikes, allergies, equipments, dietary_goals 열 생성  
- API: GET/POST /api/users/profile  
- JSON 문자열로 복잡 데이터 저장 및 파싱

### AI 셰프: 맞춤 레시피 생성 및 추천

[User Story]  
- 등록 재료와 개인 프로필 기반 맞춤형 레시피 추천 및 단계별 조리 가이드 제공  
- 요리 시작 시 요리 화면으로 이동

[Spec]  
- 요청: POST /api/chef/recipe/generate  
- 작업: 보유 재료 및 프로필 데이터 Google Sheets에서 조회 → 종합 프롬프트 구성 → Gemini-Pro API 호출 → JSON/마크다운 형태 응답 파싱 → 보유 재료 소진율 계산 → 레시피 목록 JSON 반환

### AI 쿠킹 어시스턴트: 실시간 조리 지원 챗봇

[User Story]  
- 요리 중 돌발 상황 시 실시간 질문 및 맞춤 해결책 수신 가능  
- 챗봇은 메뉴선택 및 요리 시작 단계 진입 시 활성화, 채팅형 인터페이스 제공

[Spec]  
- 요청: POST /api/chat/assistant (질문과 current_recipe_id, current_step 포함)  
- 관리: 대화 기록 유지 (Gemini Chat API 활용)  
- 시스템 프롬프트로 전문 셰프 역할 수행  
- 실시간 문제 해결 답변 생성 및 반환

---

## 미래 확장 기능 (P1)

### 커뮤니티: 레시피 후기 공유  
- 사진, 별점, 추천 내용 커뮤니티 공유  
- POST /api/recipes/{id}/review, GET /api/recipes/{id}/reviews API 제공

### 제휴 / 커머스 연동  
- 부족한 재료 바로 구매 링크 제공 (쿠팡, 마켓컬리 등 연동)

### 프리미엄 구독 모델 (Freemium)  
- 광고 제거, 무제한 AI 챗봇, 고급 레시피 접근 권한  
- 음성 문의 기능 추가 예정

---

## 식재료 등록 기능 상세명세

- 세 가지 등록 방식: 사진 촬영 / 영수증 OCR / 직접 입력  
- 등록 후 DB(예: Google Sheets) 자동 저장  
- UI는 따뜻한 웜톤 기반, 사용자 편의 최우선 설계  

---

## UX/UI 원칙

- 미니멀리즘 + 웜톤 색상과 부드러운 모서리  
- 명조체 + 산세리프 폰트 병용으로 가독성 상승  
- 효과음 최소화 및 단순 애니메이션 사용

---

**본 문서는 GitHub Markdown 형식으로 작성되었으며, 프로젝트 리드미 파일 등 깃허브 내 문서로 바로 활용 가능합니다.**
