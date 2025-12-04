# cookmake 사용자 흐름도 (User Flows)

## 전체 프로세스

flowchart TD
%% 스타일 정의 (GitHub Mermaid 호환)
classDef startend fill:#4CAF50,stroke:#333,stroke-width:3px,color:#fff
classDef proc fill:#E3F2FD,stroke:#2196F3,stroke-width:2px
classDef decision fill:#FFF3E0,stroke:#FF9800,stroke-width:2px
classDef api fill:#E8F5E8,stroke:#4CAF50,stroke-width:2px
classDef subproc fill:#F3E5F5,stroke:#9C27B0,stroke-width:1px,stroke-dasharray: 5 5

text
%% 1. 앱 시작 & 온보딩
Start([cookmake 앱 시작]):::startend
A[Expo Splash 화면]:::proc
B[카메라 권한 요청]:::proc
C[프로필 설정<br/>선호도/도구/수준]:::proc
D[홈 화면 진입<br/>하단 탭바]:::proc

%% 2. 재료 등록 (핵심 MVP)
subgraph "📸 나의 냉장고 (Scan 탭)"
    I{등록 방식}:::decision
    J[카메라 열기]:::proc
    K[냉장고 사진]:::proc
    L[Flask /ingredients<br/>Gemini Vision 호출]:::api
    M[인식 결과 확인<br/>'계란, 양파, 간장']:::proc
    R[텍스트 직접 입력]:::proc
    N[Google Sheets 저장]:::api
    T[재료 목록 갱신]:::proc
end

%% 3. 레시피 생성 (핵심 MVP)
subgraph "🍳 AI 셰프 (Home 탭)"
    H[레시피 생성 버튼]:::proc
    V[Flask /recipe POST<br/>Gemini Flash 호출]:::api
    W[레시피 카드 리스트]:::proc
    X[레시피 선택]:::proc
    Y[상세 화면 & 쿠킹 모드]:::proc
end

%% 4. AI 챗봇 (핵심 MVP)
subgraph "💬 AI 챗봇 (Chat 탭)"
    AA{챗봇 필요?}:::decision
    BB[질문 입력<br/>"간이 짜요"]:::proc
    DD[Flask /chat POST<br/>Gemini Flash]:::api
    EE[실시간 답변<br/>"물 1스푼 추가"]:::proc
    FF[요리 계속]:::proc
end

%% 5. 로그 저장
subgraph "💾 Google Sheets 로그"
    HH[자동 로그 저장<br/>레시피/챗봇 기록]:::api
    II[다음 요리 추천]:::proc
    Finish([요리 완료]):::startend
end

%% 연결
Start --> A --> B --> C --> D
D --> I
I -->|사진| J --> K --> L --> M --> N --> T
I -->|텍스트| R --> N
T --> H
D --> H
H --> V --> W --> X --> Y --> AA
AA -->|예| BB --> DD --> EE --> FF
AA -->|아니오| FF
Y --> FF
FF --> HH --> II --> Finish
text

## 🔄 핵심 API 데이터 흐름

| 단계 | API 엔드포인트 | 입력 | AI 호출 | 출력 | 저장소 |
|------|----------------|------|---------|------|--------|
| 재료 등록 | `POST /ingredients` | 이미지/텍스트 | Gemini **Vision** | `["계란","양파"]` | Google Sheets |
| 레시피 생성 | `POST /recipe` | 재료+프로필 | Gemini **Flash** | `{"title":"계란볶음밥","steps":[...]}` | Google Sheets |
| 요리 챗봇 | `POST /chat` | 질문+컨텍스트 | Gemini **Flash** | `"물을 1스푼 추가하세요"` | Google Sheets |

## 📱 React Native 화면 흐름

App.js (Bottom Tab Navigator)
├── HomeScreen (레시피 생성)
├── ScanScreen (재료 등록)
├── RecipesScreen (레시피 리스트)
├── ChatScreen (AI 챗봇)
└── ProfileScreen (설정)

text
