from langchain_core.messages import AIMessage
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.cursor import Cursor

from db import get_db
from fastapi import APIRouter, Depends

from routers.login_router import get_current_user
from services.chat_service import ChatService
from langchain_core.prompts import ChatPromptTemplate
chat = APIRouter(prefix="/chat", dependencies=[Depends(get_current_user)])
service = ChatService()


@chat.post("")
def chatting(text: str, db=Depends(get_db)):
    user_k_id = "17469876"

    embedded_text:list[float] = service.embed(text)
    vector_search_result:list[str] = service.vector_search(embedded_text, db['data'], limit=2)  # 조건 없이 다
    # chat_history = service.vector_search_chat_history(user_k_id,embedded_text, db['chat_history'], limit=10) # 유저 것만 조건

    response:AIMessage = service.send_to_model(text, vector_search_result)

    service.insert_db(user_k_id, text, response.text,  db['chat_history'], embedded_text)
    return response

@chat.get("")
def get_history(db=Depends(get_db), user=Depends(get_current_user)):# 토큰 (티켓)을 시크릿키로 해석해서 가져올거임
    col = db["chat_history"]
    hi:Cursor =  col.find({"user_k_id":str(user["user_k_id"])},{"content": 1, "role": 1, "_id":0}).sort("timestamp",-1)
    return list(hi)

# 깃허브 액션 테스트