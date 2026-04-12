from langchain_core.messages import AIMessage
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.cursor import Cursor

from db import get_db
from fastapi import APIRouter, Depends, Body

from routers.login_router import get_current_user
from services.chat_service import ChatService
from langchain_core.prompts import ChatPromptTemplate
chat = APIRouter(prefix="/api/chat", dependencies=[Depends(get_current_user)])
service = ChatService()


@chat.post("")
def chatting(model_name:str, text: str=Body(...), db=Depends(get_db), user=Depends(get_current_user)):

    embedded_text:list[float] = service.embed(text)
    vector_search_result:list[str] = service.vector_search(embedded_text, model_name, db['data'], limit=10)

    response:AIMessage = service.send_to_model(text, vector_search_result, model_name)

    service.insert_db(user["user_k_id"], text, response.text,  db['chat_history'], embedded_text, model_name)
    return response

@chat.get("")
def get_history(page: int = 1, limit: int = 10, db=Depends(get_db), user=Depends(get_current_user)):# 토큰 (티켓)을 시크릿키로 해석해서 가져올거임
    col = db["chat_history"]
    skip = (page - 1) * limit
    hi:Cursor =  col.find({"user_k_id":user["user_k_id"]},{"content": 1, "role": 1, "_id":0}).sort([("timestamp", -1), ("_id", -1)]).skip(skip).limit(limit)
    # 최신순으로 가져와서 이전 대화가 위에 보이도록 정렬
    return list(hi)[::-1]

@chat.get("/models")
def get_models(db=Depends(get_db)):
    return list(service.get_model(db["model"]))