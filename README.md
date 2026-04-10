# LangChain RAG AI Web Application

이 프로젝트는 LangChain과 OpenAI의 언어 모델을 활용하여 데이터 기반 질문에 응답할 수 있는 **RAG (Retrieval-Augmented Generation)** 기반의 AI 채팅 웹 애플리케이션입니다. React 기반의 프론트엔드 모델과 FastAPI로 구축된 백엔드로 구성된 풀스택 웹 앱입니다.

## 🛠️ 기술 스택 (Tech Stack)

### **Backend**
*   **Framework**: FastAPI, Uvicorn (포트: `8000`)
*   **AI/LLM**: LangChain, OpenAI (`gpt-4.1-nano`, `text-embedding-3-small`)
*   **Database**: MongoDB (`pymongo`, 데이터베이스명: `aichat`, 포트: `27017`)
*   **Other Libraries**: `numpy` (코사인 유사도 연산 로직 등), `python-dotenv`, `starlette` (CORS)

### **Frontend**
*   **Framework**: React 19 (개발 환경: Vite, 포트: `5173`)
*   **Routing**: `react-router-dom`
*   **API 통신**: `axios`
*   **기타 라이브러리**: `react-icons`

---

## ✨ 주요 기능 (Features)

1.  **사용자 대화 기반 RAG 검색**:
    *   사용자의 텍스트 데이터를 받아 OpenAI `text-embedding-3-small`을 통해 벡터값으로 임베딩(Embedding)합니다.
    *   Numpy를 활용하여 MongoDB에 저장된 기존 문서들 중 코사인 유사도(Cosine Similarity)를 통해 사용자 질문과 관련성이 가장 높은 문서(Top-K)를 추출합니다.
    *   추출된 문서를 바탕으로 LangChain의 프롬프트 템플릿(PromptTemplate)을 구성하여 `gpt-4.1-nano` 모델에게 컨텍스트가 포함된 높은 정확도의 텍스트 응답을 기대합니다.
2.  **대화 기록(Chat History) 저장**:
    *   유저의 질문과 AI의 응답 내용, 그에 상응하는 벡터값을 DB에 저장하여 추후 대화 내역 조회 및 히스토리를 데이터로 쓸 수 있게 구축되어 있습니다.
3.  **도메인별 라우터 아키텍처**:
    *   단순한 서버 구성을 넘어 `login`, `chat`, `admin`, `web` 형태의 여러 도메인별 라우터로 모듈화하여 관리 및 유지 보수의 효율성을 높였습니다.

---

## 🚀 설치 및 실행 방법 (Getting Started)

프로젝트를 로컬 환경에서 실행하려면 프론트엔드, 백엔드 서버 및 Database(MongoDB)가 모두 동작해야 합니다.

### 1. MongoDB 설정
* 로컬 `27017` 포트에 MongoDB가 설치되어 실행 중이어야 합니다.
* 벡터(Vector)와 텍스트(Text) 데이터를 저장할 로컬 데이터베이스(`aichat`)를 필요로 합니다.

### 2. 환경 변수 설정 (.env)
백엔드 폴더(`backend/`) 내에 `.env` 파일을 생성하거나 수정하여 필수 환경변수를 설정합니다. OpenAI 모델 사용에 필요한 키가 요구됩니다.
```env
OPENAI_API_KEY="sk-..."
```

### 3. Backend (FastAPI 서버) 실행
Python 환경이 구성되어있어야 동작합니다. 가상 환경 위에서 구동하는 것을 추천합니다.

```bash
cd backend

# 의존성 패키지 설치 (requirements.txt 활용)
pip install -r requirements.txt

# 서버 실행 (API 주소: http://127.0.0.1:8000)
python main.py
```

### 4. Frontend (React) 실행

```bash
cd frontend

# 의존성 패키지 설치
npm install

# 개발용 테스트 프론트 프록시 서버 실행 (기본 포트: http://127.0.0.1:5173)
npm run dev
```

---

## 📂 주요 구조 (Directory Structure)

```text
LangChain-RAG/
├── backend/                  # FastAPI 기반의 백엔드 서버
│   ├── routers/              # API 라우팅 파일 (admin, chat, login, web 등)
│   ├── services/             # 비즈니스 로직 및 RAG 벡터 검색 로직 (chat_service.py 등)
│   ├── main.py               # 백엔드 서버 애플리케이션 진입점 (CORS 미들웨어 적용 포함)
│   ├── db.py                 # MongoDB 데이터베이스 연결 헬퍼 함수
│   ├── common.py             # 공통 유틸리티 (timing 데코레이터 등)
│   └── requirements.txt      # 파이썬 의존성 패키지 목록
├── frontend/                 # React (Vite) 프론트엔드 웹 SPA
│   ├── public/             
│   ├── src/                  # 프론트 화면 및 컴포넌트 (App.jsx, /page 등)
│   ├── package.json          # NPM 패키지 목록
│   └── vite.config.js        # Vite 번들러 설정
└── README.md
```
