# 11주차 과제 - cookmake

## 목차
- [1. 프로젝트 한눈에 보기](#1-프로젝트-한눈에-보기-overview)
- [2. 주요 목표](#2-주요-목표)
- [3. 기술 스택](#3-기술-스택)
- [4. 전체 구조 및 아키텍처](#4-전체-구조-및-아키텍처)
- [5. 주요 기능 및 데이터 흐름](#5-주요-기능-및-데이터-흐름)
- [6. 백엔드 API 설계](#6-백엔드-api-설계)
- [7. 프런트엔드 구조 및 예시](#7-프런트엔드-구조-및-예시)
- [8. Google Sheets 연동](#8-google-sheets-연동)
- [9. 비용 절감 및 제한 대응 전략](#9-비용-절감-및-제한-대응-전략)
- [10. 과제 제출 안내](#10-과제-제출-안내)

---

## 1. 프로젝트 한눈에 보기 (Overview)

프로젝트명: cookmake (내 냉장고 속 AI 셰프)  
대상: 20~30대 1인 가구(자취생)  
플랫폼: React Native + Python Flask  
핵심 아이디어:  
냉장고 속 재료를 텍스트 또는 사진으로 입력하면 AI가 맞춤 레시피를 제안하고, 실시간 요리 가이드를 제공합니다.

---

## 2. 주요 목표

- 재료 낭비를 줄이고 식비 절감
- 초보자도 쉽게 시도할 수 있는 요리 추천
- 음식 취향, 알레르기, 기구 기반으로 개인 맞춤화
- 무료 인프라 환경에서 효율적 구현

---

## 3. 기술 스택

| 구분 | 기술/서비스 | 주요 역할 |
|------|--------------|------------|
| 프런트엔드 | React Native (Expo) | iOS/Android 동시 지원, 빠른 빌드 |
| 백엔드 | Google Gemini API | 경량 REST API 서버 |
| DB | Google Sheets | 무료 데이터베이스 대체 (CRUD) |
| AI | Google Gemini API / Vision | 재료 인식 및 레시피 생성 |
| 호스팅 | Render / Railway / PythonAnywhere | 무료 또는 저비용 배포 |
| 인증/보안 | dotenv, CORS | 환경 변수 및 기본 보안 유지 |

---

## 4. 전체 구조 및 아키텍처

```
사용자 입력 (텍스트/이미지)
        ↓
React Native App (Expo)
        ↓
Flask API 서버
        ↓
Gemini Flash / Vision (AI 요청)
        ↓
Google Sheets (데이터 저장)
        ↓
결과(레시피 및 챗봇 응답) → 앱 UI
```

---

## 5. 주요 기능 및 데이터 흐름

1. 사용자가 냉장고 재료를 입력하거나 사진 업로드  
2. 앱에서 Gemini Vision 호출 → 재료 텍스트로 변환  
3. Flask 서버가 Google Sheets에 결과 저장  
4. 사용자가 레시피 요청 → Flask가 Gemini Flash 호출  
5. 맞춤 레시피 응답을 받아 앱에서 카드 형태로 표시  
6. 요리 단계별 AI 챗봇 가이드 제공  

---

## 6. 백엔드 API 설계

### 6.1 /recipe

**요청**
```
{
  "ingredients": ["계란", "양파", "간장"],
  "user_profile": { "allergy": [], "tools": ["프라이팬"], "level": "초급" }
}
```

**응답**
```
{
  "recipeTitle": "간장 계란 볶음밥",
  "steps": [
    "양파를 잘게 썬다.",
    "계란을 풀어 익힌다.",
    "간장을 넣고 볶는다."
  ],
  "time": "10분",
  "difficulty": "초급"
}
```

---

### 6.2 /chat

AI 요리 챗봇용 엔드포인트.  
입력된 진행 상황이나 질문에 대해 AI가 단계별 답변 제공.

**요청**
```
{ "message": "양파 대신 어떤 걸 써도 될까?" }
```

**응답**
```
{ "reply": "양파 대신 파나 마늘을 사용해도 풍미를 살릴 수 있습니다." }
```

---

### 6.3 /ingredients

이미지 업로드 또는 텍스트 기반 재료 인식용.  
Google Gemini Vision API를 통해 재료명 추출.

**응답 예시**
```
{ "ingredients": ["달걀", "당근", "대파"] }
```

---

## 7. 프런트엔드 구조 및 예시

### 폴더 구조

```
cookmake-app/
  ├── screens/
  │   ├── HomeScreen.js
  │   ├── ScanScreen.js
  │   ├── RecipesScreen.js
  │   └── ProfileScreen.js
  ├── components/
  │   ├── RecipeCard.js
  │   ├── IngredientCard.js
  │   └── ChatBotCard.js
  ├── services/
  │   ├── api.js
  │   └── gemini.js
  └── App.js
```

### API 호출 예시

```
import axios from "axios";

export async function getRecipe(data) {
  try {
    const res = await axios.post("https://cookmake-api.onrender.com/recipe", data);
    return res.data;
  } catch (e) {
    console.error(e);
    return null;
  }
}
```

---

## 8. Google Sheets 연동

```
import gspread
from datetime import datetime

def save_recipe_log(title, ingredients):
    sa = gspread.service_account(filename="credentials.json")
    sh = sa.open("cookmake-db")
    worksheet = sh.worksheet("recipes")
    worksheet.append_row([datetime.now().isoformat(), title, ", ".join(ingredients)])
```

---

## 9. 비용 절감 및 제한 대응 전략

- Gemini 호출 최소화: 동일 입력 캐싱, 최근 결과 재활용  
- Google Sheets 쓰기 빈도 최소화: batch append 사용  
- 무료 호스팅 비용 절약: 서버 콜드스타트 대비 헬스 체크 라우트 추가  
- 오프라인 모드: 간단한 로컬 JSON 기반 임시 결과 표시  
- `.env`로 API 키 보관, 클라이언트 노출 금지  
