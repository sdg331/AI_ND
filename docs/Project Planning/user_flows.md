# cookmake 사용자 흐름도 (User Flows)

## 전체 프로세스

flowchart TD
%% 스타일 정의
classDef startend fill:#4CAF50,stroke:#333,stroke-width:2px,color:white,rx:10,ry:10;
classDef proc fill:#E3F2FD,stroke:#2196F3,stroke-width:1px,color:black,rx:4,ry:4;
classDef decision fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:black,rx:4,ry:4;
classDef subproc fill:#F5F5F5,stroke:#9E9E9E,stroke-width:1px,color:black,stroke-dasharray: 5 5;
classDef api fill:#E8F5E8,stroke:#4CAF50,stroke-width:2px,color:black;

text
%% 노드 정의
Start([cookmake 앱 시작]):::startend
Finish([요리 완료]):::startend

%% 1. 온보딩 프로세스
subgraph Onboarding [앱 진입 및 초기 설정]
    direction TB
    A[앱 첫 실행]:::proc --> B[Expo Splash → 온보딩]:::proc
    B --> C[카메라 권한 요청]:::proc
    C --> D[프로필 설정<br/>선호도/도구/수준]:::proc
    D --> E[홈 화면 진입<br/>하단 탭바 활성화]:::proc
end

%% 메인 분기점
E --> F{재료 등록 필요?}:::decision

%% 2. 재료 관리 프로세스 (cookmake 핵심)
subgraph Fridge [나의 냉장고 - 재료 관리]
    direction TB
    F -- 예 --> G[Scan 탭 이동]:::proc
    G --> I{등록 방식 선택}:::decision
    
    %% Gemini Vision 등록 (핵심)
    I -- 사진 촬영 --> J[Expo Camera 열기]:::proc
    J --> K[냉장고 사진 촬영]:::proc
    K --> L[Flask /ingredients POST<br/>Gemini Vision 호출]:::api
    L --> M[인식 결과 검토<br/>['계란','양파','간장']]:::proc
    
    %% 텍스트 입력 (간편)
    I -- 직접 입력 --> R[재료명/수량 입력]:::proc
    R --> S[Flask /ingredients POST<br/>Google Sheets 저장]:::api
    
    M --> N[수정 후 저장]:::proc
    N --> T[재료 목록 갱신<br/>Real-time UI]:::proc
    S --> T
    T --> U[Home 탭으로 복귀]:::proc
end

%% 3. 요리 및 AI 프로세스 (cookmake 핵심)
subgraph Cooking [AI 셰프 - 레시피 & 챗봇]
    direction TB
    F -- 아니오 --> H[레시피 생성 버튼]:::proc
    U --> H
    
    H --> V[Flask /recipe POST<br/>Gemini Flash 호출]:::api
    V --> W[레시피 카드 리스트<br/>'간장 계란볶음밥']:::proc
    W --> X[레시피 선택]:::proc
    X --> Y[레시피 상세 화면]:::proc
    Y --> Z[쿠킹 모드 진입]:::proc
    
    Z --> AA{AI 챗봇 필요?}:::decision
    
    %% AI 챗봇 루프 (cookmake 핵심)
    AA -- 예 --> BB[Chat 탭 또는 모달]:::proc
    BB --> CC[질문 입력<br/>"간이 너무 짜요"]:::proc
    CC --> DD[Flask /chat POST<br/>Gemini Flash 호출]:::api
    DD --> EE[실시간 답변<br/>"물을 추가하세요"]:::proc
    EE -.-> FF
    
    AA -- 아니오 --> FF[요리 진행]:::proc
    FF --> GG[요리 완료 체크]:::proc
end

%% 4. 로그 저장 (cookmake DB)
subgraph Logging [Google Sheets 로그 저장]
    GG --> HH[자동 로그 저장<br/>레시피/챗봇 기록]:::api
    HH --> II[다음 요리 추천<br/>캐시 활용]:::proc
end

Start --> A
II --> Finish
text

## 핵심 데이터 흐름 상세

### 1. /ingredients 엔드포인트
사진 업로드 → Gemini Vision → ["계란","양파"] → Google Sheets Row 추가

text

### 2. /recipe 엔드포인트  
재료+프로필 → Gemini Flash 프롬프트 → {"title":"계란볶음밥","steps":[...]} → UI 렌더링

text

### 3. /chat 엔드포인트
"간이 짜요" → 컨텍스트(현재레시피)+질문 → Gemini Flash → "물을 1스푼 추가하세요"

text

---
