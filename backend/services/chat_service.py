from datetime import datetime

from langchain_core.messages import AIMessage

from pymongo.synchronous.collection import Collection
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import numpy as np


from common import timing



class ChatService:
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)
        self.llm = ChatOpenAI(model="gpt-4.1-nano")
    @timing
    def embed(self, text: str)->list[float]:
        """
        사용자의 질문을 입력받아 임베딩된 텍스트로 변환하는 함수
        :param text: 사용자 질문
        :return: 임베딩된 결과 값
        """
        return self.embeddings_model.embed_query(text)

    def _cosine_similarity(self ,a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @timing
    def vector_search(self, embedded_text:list[float], model_name:str, data:Collection, limit:int)->list[str]:
        """
        벡터DB에 임베딩된 텍스트로 유사도 검색을 수행하는 함수
        :param limit: 유사도 기반 순위 n개
        :param embedded_text: 임베딩된 텍스트
        :param data: data 컬렉션
        :return: 유사도 검색 결과 값 (일반 텍스트)
        """
        data_doc = list(data.find({"model":model_name}, {"text":1, "vector_text":1, "model":1}))
        query_vec = np.array(embedded_text)
        results = []
        for doc in data_doc:
            emb = np.array(doc["vector_text"])
            score = self._cosine_similarity(query_vec, emb)
            results.append((doc["text"], score))
        results.sort(key=lambda x: x[1], reverse=True)
        top = results[:limit]
        return top

    @timing
    def vector_search_chat_history(self,user_k_id, embed_query, chat_history:Collection, limit:int)->list[set]:
        """
        개발중 유저 챗 히스토리 RAG검색 : 위 vector_search() 함수랑 기능이 동일하여 통합 가능성 높음
        :param embedded_text:
        :param data:
        :param limit:
        :param user_k_id:
        :return:
        """
        # content: str,
        # role: str,
        # vector_text: list[float]
        data_doc:list[dict] = list(chat_history.find({"user_k_id": user_k_id},{"_id":0,"user_k_id":0,"model":0,"timestamp":0}).sort([("timestamp", -1), ("_id", -1)]))

        # query_vec = np.array(embedded_text)
        results = []
        for doc in data_doc:
            emb = np.array(doc["vector_text"])
            score = self._cosine_similarity(embed_query, emb)
            results.append((f"({doc["role"]}의 대화 기록입니다.\n 내용:{doc["content"]})", score))
        results.sort(key=lambda x: x[1], reverse=True)
        top = results[:limit]
        return top
    # 답변이나 질문이 비슷하면 chat_history 에서 백터 텍스트 검사해서 전에 했던 내용 3개 정도

    @timing
    def send_to_model(
        self,
        text: str,
        data_vector_search_result: list[str],
        chat_history_vector_search_result: list[set],
        chat_history_top: list[str],
        model_description: str = "",
    ) -> AIMessage:
        """
        사용자 질문과 유사도 검색 결과로 LLM에게 전달할 프롬프트를 만드는 함수.
        시스템 프롬프트를 통해 모델 범위 외 질문에 대한 안내를 LLM이 직접 처리합니다.

        :param text: 사용자 질문
        :param data_vector_search_result: RAG 전문 기술 벡터 유사도 검색 결과 [(text, score), ...]
        :param chat_history_vector_search_result: RAG 사용자 대화 벡터 유사도 검색 결과
        :param chat_history_top: 사용자 대화중 최신 10개
        :param model_description: 모델 설명 (시스템 프롬프트 페르소나 설정용)
        :return: AIMessage
        """
        system_prompt = (
            "마크다운 문법으로 답변하세요.\n"
            f"당신은 다음 설명에 해당하는 전문 AI입니다: {model_description}\n"
            # "위에서 안내한 당신의 전문 분야와 전혀 다른 질문이라고 생각이 든다면, 답변을 거부하세요."
        )

        context_texts = [item[0] for item in data_vector_search_result]
        template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human",
             "다음은 사용자 질문에 대한 관련 검색 결과입니다. 참고하여 답변하세요:\n"
             "{data_vector_search_result}\n\n"
             "다음은 사용자와 이전에 했던 대화 내용 중 관련이 높은 대화 내용 검색입니다. 참고하여 답변하세요.\n"
             "{chat_history_vector_search_result}\n\n"
             "다음은 사용자와 이 대화 직전에 했던 대화들입니다. 참고하여 답변하세요."
             "{chat_history_top}\n\n"
             "사용자 질문: {q}")
        ])
        chain = template | self.llm
        return chain.invoke({"data_vector_search_result": context_texts, "chat_history_vector_search_result":chat_history_vector_search_result,"chat_history_top": chat_history_top, "q": text})

    @timing
    def insert_db(self,user_id:int, q:str, a:str,  chat:Collection, embedded_text, model_name)-> bool:
        """
        사용자 질문과, LLM 응답을 벡터DB에 저장하는 함수
        :param chat: chat_history 컬렉션
        :param q: 사용자 질문
        :param a: LLM 응답
        :return: None
        """
        try:
            user_data = {
                "user_k_id": user_id,
                "content": q,
                "role":"human",
                "vector_text": embedded_text,
                "model": model_name,
                "timestamp": datetime.now()
            }
            chat.insert_one(user_data)

            ai_data = {
                "user_k_id": user_id,
                "content": a,
                "role": "ai",
                "vector_text": self.embeddings_model.embed_query(a),
                "model": model_name,
                "timestamp": datetime.now()
            }
            chat.insert_one(ai_data)

            return True
        except Exception as e:
            print(f"저장 실패:{e}")
            return False
    def get_model(self, model:Collection):
        return model.find({},{"_id":0})

    def get_chat_history_top(self, user_k_id, history_col:Collection) -> list[str]:
        chats = history_col.find({"user_k_id": user_k_id}, {"content": 1, "role": 1, "_id": 0}).sort(
            [("timestamp", -1), ("_id", -1)]).limit(10)
        result: list[str] = []
        for chat in chats:
            result.append(f"({chat["role"]}의 대화 기록입니다.\n 내용:{chat["content"]})")
        return result


