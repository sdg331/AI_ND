# 2. Google Sheets 설정

## 2-1. 스프레드시트 정보

- 스프레드시트 ID  
  - 1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA

- 스프레드시트 URL  
  - https://docs.google.com/spreadsheets/d/1tn2npx2hvbwVkpndUYW8y-V3qIVoV4sYgNcdCnkhKqA/edit

## 2-2. 공유 설정

1. 위 링크로 접속
2. “공유” 버튼 클릭
3. `fridge-chef-bot@fridgechef-478716.iam.gserviceaccount.com` 추가
4. 권한을 “편집자”로 설정
5. 저장

이 설정이 되어야만 Flask 서버에서 Sheets에 읽기/쓰기 할 수 있습니다.
