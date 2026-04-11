# 🪄 LangChain RAG AI Web Application (Luxury Earth Tone Edition)

이 프로젝트는 LangChain과 OpenAI의 언어 모델을 결합하여 데이터 기반 질문에 논리적으로 응답하는 **RAG (Retrieval-Augmented Generation) 기반의 풀스택 AI 채팅 웹 애플리케이션**입니다. 

---

## 🛠️ 기술 스택 (Tech Stack)

### **Frontend**
*   **Framework**: React 19 (Vite 번들러, 기본 포트: `5173`)
*   **Routing & Auth**: `react-router-dom`, `jwt-decode`, Custom Protected Routes
*   **UI/UX**: 
    *   순수 CSS Variables 기반
    *   커스텀 팝업 모달 체계 (native window.alert/prompt/confirm 완벽 대체)
*   **Markdown Parsing**: `react-markdown`, `remark-gfm`
*   **API 통신**: `axios`

### **Backend**
*   **Framework**: FastAPI, Uvicorn (기본 포트: `8000`)
*   **AI/LLM Core**: LangChain, OpenAI (`gpt-4.1-nano`, `text-embedding-3-small`)
*   **Database**: MongoDB (비동기 Motor/Pymongo 연동, 포트: `27017`)
*   **Security**: JWT 기반 인증 체계 (OAuth2PasswordBearer)

---

## ✨ 핵심 기능 (Key Features)

### 1. 🤖 지능형 RAG 문서 검색 체계
*   **고성능 임베딩**: 사용자의 텍스트를 `text-embedding-3-small`로 임베딩하여 Numpy를 활용한 코사인 유사도 연산으로 가장 관련성 높은 문서를 즉시 찾습니다.
*   **컨텍스트 융합 답변**: 검색된 문서를 바탕으로 프롬프트 템플릿(Prompt Template)을 엮어 `gpt-4.1-nano`가 높은 도메인 정확도를 가진 응답을 반환합니다.

### 2. 🎨 UI/UX & 마크다운 렌더링
*   **자연스러운 스크롤 (Infinite Scroll)**: 최신 상용 메신저(카카오톡 등)와 동일하게, 화면 최상단 도달 시 과거 대화를 시야 끊김 없이 자연스럽게 프리페치(Prefetching) 해옵니다.
*   **완벽한 마크다운 지원**: AI가 전송하는 볼드체, 테이블, 리스트 등의 마크다운 포맷팅 텍스트가 깨지지 않고 채팅창에 예쁘게 파싱(`react-markdown`)되어 출력됩니다.

### 3. 🛡️ 완벽한 RBAC 보안 통제 (Role-Based Access Control)
*   가입 시 기본적으로 `user` 권한이 부여되며, 쿠키(JWT 토큰)의 `role` 값을 기반으로 프론트엔드 라우터 가드(`ProtectedRoute.jsx`)가 작동합니다.
*   일반 유저가 어드민 라우트(`/admin`)로 무단 침입을 시도할 경우, 단순 403 에러가 아닌 전용 `NotFound (404)` 페이지로 돌려보내어 시스템 구조(경로)를 완벽히 숨깁니다.
*   백엔드 API(`api/admin/*`) 레벨에서도 JWT 의존성 주입을 통해 악의적인 다이렉트 API 호출을 원천 차단합니다.

### 4. 👑 탭(Tab) 기반 관리자 대시보드 (Admin Panel)
*   **모델 업로드**: 새로운 AI 모델 이름, 성격 및 학습 데이터 파일(.txt, .pdf)을 서버에 업로드합니다.
*   **모델 관리 (CRUD)**: 현재 활성화된 AI 모델 리스트를 조회하고, 세련된 커스텀 모달 오버레이를 통해 이름 재설정(Update)과 폐기(Delete)를 수행합니다.
*   **유저 권한 관리**: 가입된 사용자 목록을 표시하고, 직관적인 `<select>` 박스를 통해 즉석에서 일반 유저(`user`)를 플랫폼 최고 관리자(`admin`)로 승격시킬 수 있습니다.

---

## 🚀 설치 및 가동 가이드 (Getting Started)

프로젝트를 구동하기 위해선 백엔드(FastAPI), 프론트엔드(React), 그리고 MongoDB 데몬이 동작 중이어야 합니다.

### 1. MongoDB 구동
*   로컬 혹은 원격망에 MongoDB가 `27017` 포트로 띄워져 있어야 합니다.
*   벡터 데이터와 유저 정보가 저장될 `aichat` 데이터베이스를 필요로 합니다.

### 2. 환경 변수 설정 (.env)
`backend/` 폴더 내에 `.env` 파일을 구성하여 OpenAI API 키를 연결해 줍니다.
```env
OPENAI_API_KEY="sk-여러분들의-OPENAI-키를-입력하세요"
```

### 3. Backend (API 서버) 기동
가능하면 가상 환경(Virtualenv 등) 위에서 패키지를 설치하신 후 서버를 구동하십시오.
```bash
cd backend
pip install -r requirements.txt
python main.py
```
> 서버가 성공적으로 켜지면 터미널 상에 `http://localhost:8000` 주소가 나타납니다.

### 4. Frontend (Vite) 기동
Node.js 필수 모듈들을 설치하고 프론트엔드를 실행합니다.
```bash
cd frontend
npm install
npm run dev
```
> 브라우저를 열고 터미널에 표시된 `http://localhost:5173` 으로 접속하시면 즉시 럭셔리 채팅 UI와 만나실 수 있습니다!

---

## 📂 아키텍처 개요 (Directory Structure)

```text
LangChain-RAG/
├── backend/                  
│   ├── routers/              # 도메인별 분리된 API 라우터 (admin, chat, login)
│   ├── services/             # RAG 및 Numpy 코사인 유사도 벡터 연산 비즈니스 계층
│   ├── main.py               # FastAPI 통합 진입점 및 CORS 인증 미들웨어
│   └── common.py             # 실행 속도 타이밍 계측 데코레이터 등 유틸 모음
├── frontend/                 
│   ├── src/
│   │   ├── components/       # ProtectedRoute 등 글로벌 공유 컴포넌트
│   │   ├── page/             # Home(채팅창), Admin(대시보드), NotFound 뷰 집합
│   │   ├── api.js            # 백엔드 연동 통신망 (axios base 인스턴스)
│   │   └── App.jsx           # 리액트 다이내믹 통합 라우터 (RBAC 가드 내장)
│   └── package.json          
└── README.md                 # 본 가이드라인
```
