```mermaid
flowchart TD
    %% 스타일 최소화 (GitHub 호환 위주)
    classDef startend fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    classDef proc fill:#E3F2FD,stroke:#2196F3,stroke-width:1px
    classDef decision fill:#FFF3E0,stroke:#FF9800,stroke-width:1px
    classDef api fill:#E8F5E8,stroke:#4CAF50,stroke-width:1px

    %% 앱 시작 & 온보딩
    Start([cookmake 앱 시작]):::startend
    A[앱 첫 실행]:::proc
    B[권한 요청]:::proc
    C[프로필 설정]:::proc
    D[홈 화면 진입]:::proc

    %% 재료 등록
    I{재료 등록 방식}:::decision
    J[카메라 촬영]:::proc
    K[사진 캡처]:::proc
    L[API /ingredients 호출]:::api
    M[인식 결과 확인]:::proc
    R[텍스트 직접 입력]:::proc
    N[재료 저장 (Sheets)]:::api
    T[재료 목록 갱신]:::proc

    %% 레시피 생성
    H[레시피 생성 버튼]:::proc
    V[API /recipe 호출]:::api
    W[레시피 리스트 표시]:::proc
    X[레시피 선택]:::proc
    Y[쿠킹 모드]:::proc

    %% 챗봇
    AA{챗봇 사용 여부}:::decision
    BB[질문 입력]:::proc
    DD[API /chat 호출]:::api
    EE[AI 답변 표시]:::proc
    FF[요리 진행]:::proc

    %% 로그 & 종료
    HH[사용 로그 저장]:::api
    II[다음 추천 준비]:::proc
    Finish([요리 완료]):::startend

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
    FF --> HH --> II --> Finish
undefined
