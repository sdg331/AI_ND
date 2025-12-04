flowchart TD
    %% ============================
    %% Mermaid 스타일 정의
    %% (GitHub 호환 버전)
    %% ============================
    classDef startend fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    classDef proc fill:#E3F2FD,stroke:#2196F3,stroke-width:1.5px
    classDef decision fill:#FFF3E0,stroke:#FF9800,stroke-width:1.5px
    classDef api fill:#E8F5E8,stroke:#4CAF50,stroke-width:1.5px
    classDef subproc fill:#F3E5F5,stroke:#9C27B0,stroke-width:1px,stroke-dasharray:5 5

    %% ============================
    %% 1. 앱 시작 & 온보딩
    %% ============================
    Start([cookmake 앱 시작]):::startend
    A[Expo Splash 화면]:::proc
    B[카메라 권한 요청]:::proc
    C[프로필 설정<br/>선호도 · 도구 · 요리 수준 입력]:::proc
    D[홈 화면 진입<br/>하단 탭바 표시]:::proc

    %% ============================
    %% 2. 재료 등록 (Scan 탭)
    %% ============================
    subgraph SCAN["나의 냉장고 (Scan 탭)"]
        I{등록 방식 선택}:::decision
        J[카메라 열기]:::proc
        K[냉장고 사진 촬영]:::proc
        L[Flask /ingredients POST<br/>→ Gemini Vision 분석]:::api
        M[인식 결과 확인<br/>예: 계란, 양파, 간장]:::proc
        R[텍스트 직접 입력]:::proc
        N[Google Sheets 저장]:::api
        T[재료 목록 갱신]:::proc
    end

    %% ============================
    %% 3. 레시피 생성 (Home 탭)
    %% ============================
    subgraph HOME["AI 셰프 (Home 탭)"]
        H[레시피 생성 버튼 클릭]:::proc
        V[Flask /recipe POST<br/>→ Gemini Flash 호출]:::api
        W[레시피 카드 리스트 표시]:::proc
        X[레시피 선택]:::proc
        Y[레시피 상세 · 쿠킹 모드 진입]:::proc
    end

    %% ============================
    %% 4. AI 요리 챗봇 (Chat 탭)
    %% ============================
    subgraph CHAT["AI 요리 챗봇 (Chat 탭)"]
        AA{챗봇 사용 여부}:::decision
        BB[질문 입력<br/>예: "간이 짜요"]:::proc
        DD[Flask /chat POST<br/>→ Gemini Flash 호출]:::api
        EE[AI 답변<br/>예: "물을 조금 추가하세요"]:::proc
        FF[요리 계속 진행]:::proc
    end

    %% ============================
    %% 5. 로그 저장 및 완료
    %% ============================
    subgraph LOGS["Google Sheets 로그 저장"]
        HH[레시피/챗봇 사용 기록 저장]:::api
        II[다음 추천 요리 준비<br/>(캐시 활용)]:::proc
        Finish([요리 완료]):::startend
    end

    %% ============================
    %% 연결 라인
    %% ============================
    Start --> A --> B --> C --> D

    D --> I
    I -->|사진| J --> K --> L --> M --> N --> T
    I -->|텍스트| R --> N --> T

    T --> H
    D --> H

    H --> V --> W --> X --> Y --> AA

    AA -->|예| BB --> DD --> EE --> FF
    AA -->|아니오| FF

    Y --> FF
    FF --> HH --> II --> Finish
