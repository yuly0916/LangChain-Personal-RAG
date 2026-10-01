
from pymongo.synchronous.database import Database

from db import get_db
from fastapi import APIRouter, Depends, Body, HTTPException, Request

from response.dto import ModelDto, User, ChatResponseDto
from routers.login_router import get_current_user
from services.chat_service import ChatService
chat = APIRouter(prefix="/api/chat", dependencies=[Depends(get_current_user)])
service = ChatService()


@chat.post("")
def chatting(request: Request,model_name:str, text: str=Body(...), db:Database=Depends(get_db), user:User=Depends(get_current_user)):
    return service.post_chat(model_name, text, db, user, request)


@chat.get("", responses={400:{"description":"요청이 올바르지 않습니다. page는 0초과, limit은 100 미만이어야합니다."}})
def get_history(page: int = 1, limit: int = 10, db:Database=Depends(get_db), user:User=Depends(get_current_user)) -> list[ChatResponseDto]:# 토큰 (티켓)을 시크릿키로 해석해서 가져올거임
    if page <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="요청이 올바르지 않습니다. page는 0초과, limit은 100 미만이어야합니다.")
    return service.get_chat(page,limit,db,user)

@chat.get("/models")
def get_models(db=Depends(get_db)) -> list[ModelDto]:
    return list(service.get_model(db["model"]))

