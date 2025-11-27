# 3. 환경 변수 예시 (.env 형식)

프로젝트 루트에 `.env` 파일을 생성하고 아래 형식으로 작성합니다.  
이 파일은 깃허브에 커밋하지 않고, `.env.example`만 공유용으로 둡니다.

```text
Google Gemini / AI
GEMINI_API_KEY=AIzaSyDBoHyvmWs6caj9KNCMDrLJ9nBv3rm5SaI

Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA
GOOGLE_PROJECT_ID=fridgechef-478716
GOOGLE_SERVICE_ACCOUNT_EMAIL=fridge-chef-bot@fridgechef-478716.iam.gserviceaccount.com
```

```text
권장:
- `.env.example` 파일을 루트에 두고 위 내용을 복사해 두기
- 팀원은 `.env.example`를 복사해서 `.env`를 만든 후 자신의 키만 채워 넣기
```
