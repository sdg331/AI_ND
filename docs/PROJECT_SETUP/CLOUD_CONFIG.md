# 1. Google Cloud / AI 설정

## 1-1. 프로젝트 정보

- 프로젝트 이름: FridgeChef
- 프로젝트 ID: fridgechef-478716

## 1-2. Google AI Studio

- URL: https://aistudio.google.com/app/projects
- 사용 중인 프로젝트명: createapi

## 1-3. 서비스 계정

- 이메일: fridge-chef-bot@fridgechef-478716.iam.gserviceaccount.com
- 권한: 편집자(Editor)

### 서비스 계정 키(JSON) 만들기

1. Google Cloud Console 접속
2. 프로젝트: `fridgechef-478716` 선택
3. “IAM 및 관리자” → “서비스 계정”
4. `fridge-chef-bot@fridgechef-478716.iam.gserviceaccount.com` 선택
5. “키” 탭 → “키 추가” → “새 키 만들기” → JSON 선택
6. 다운로드된 JSON 파일을 `backend/service_account.json` 으로 저장

※ 이 JSON 파일은 절대 깃허브에 올리지 말 것. `.gitignore`에 포함.

## 1-4. API 및 서비스 → 인증 정보

- URL: https://console.cloud.google.com/apis/credentials?project=fridgechef-478716

여기에서 생성/관리하는 것들:
- API 키 (브라우저용)
- OAuth 클라이언트 (필요 시)
- 서비스 계정 키(JSON)
