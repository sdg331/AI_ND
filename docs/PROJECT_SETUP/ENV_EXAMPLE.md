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
# 기본 정보
### google cloud 프로젝트
###### 이름:FridgeChef 
###### ID:fridgechef-478716

# 백업
### 스프레드시트
###### https://docs.google.com/spreadsheets/d/1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA/edit?gid=2064129858#gid=2064129858
###### 공유-ai에게 편집자 권한 줄것.

### API 
###### https://aistudio.google.com/app/projects
###### 프로젝트
###### 이름:createapi

### API 및 서비스->인증정보에서 확인
###### 사용자 인증 정보
###### https://console.cloud.google.com/apis/credentials?project=fridgechef-478716
###### 서비스 계정-편집자 이메일
###### fridge-chef-bot@fridgechef-478716.iam.gserviceaccount.com


```text

권장:
- `.env.example` 파일을 루트에 두고 위 내용을 복사해 두기
- 팀원은 `.env.example`를 복사해서 `.env`를 만든 후 자신의 키만 채워 넣기
```
