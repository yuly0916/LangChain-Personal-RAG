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
        print(model_name)
        data_doc = list(data.find({"model":model_name}, {"text":1, "vector_text":1, "model":1}))
        for d in data_doc:
            print(d["model"])
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
    def vector_search_chat_history(self,user_k_id,embedded_text, data:Collection, limit:int):
        """
        개발중 유저 챗 히스토리 RAG검색 : 위 vector_search() 함수랑 기능이 동일하여 통합 가능성 높음
        :param embedded_text:
        :param data:
        :param limit:
        :param user_k_id:
        :return:
        """
        data_doc = list(data.find({"user_k_id": user_k_id}))
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
    def send_to_model(self, text:str, vector_search_result:list[str]) -> AIMessage:
        """
        사용자 질문과, 유사도 검색 결과로 LLM에게 전달할 프롬프트를 만드는 함수
        :param text: 시용자 질문
        :param vector_search_result: 벡터 유사도 검색 결과
        :return: 프롬프트 객체 (Langchain 객체)
        """
        print(vector_search_result)
        template = ChatPromptTemplate.from_messages([("system","마크다운 문법으로 답변하세요"), ("human","이 것은 사용자 질문에 대한 검색 결과입니다. 참고하여 답변하세요.:{vector_search_result}\n 사용자 질문:{q}")])
        chain = template | self.llm
        return chain.invoke({"vector_search_result":vector_search_result,"q":text})

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


