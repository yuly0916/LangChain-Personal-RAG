from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi import UploadFile
from langchain_core.documents import Document
from pymongo.synchronous.database import Database

from db import get_db

from services.admin_service import AdminService
from routers.login_router import get_current_user

admin = APIRouter(prefix="/api/admin")
service = AdminService()

def get_admin_user(current_user: dict = Depends(get_current_user)):
    role = current_user.get("role")
    if role != "admin":
        raise HTTPException(status_code=403, detail="어드민 권한이 필요합니다.")
    return current_user

@admin.post("/upload")
async def upload_file(file: UploadFile, db: Database = Depends(get_db), admin_user: dict = Depends(get_admin_user), model_name:str="이름 없는 모델", model_description: str="설명이 없습니다."):
    if service.check_extension(file.filename):
        text:str = await service.load_file(file)
        chunks:list[Document] = service.chunk_texts(text)
        service.insert_db_model_collection(model_name, model_description,db["model"])
        service.insert_db_data_collection(chunks, model_name, db["data"])

    else:
        raise HTTPException(415, detail=".txt파일을 올려주세요.")

@admin.get("/users")
def get_users_infor(db: Database = Depends(get_db)):
    users = service.get_users(user=db["user"])
    return users

@admin.put("/users/{user_k_id}/role")
def update_role(user_k_id:int, role:str=Body(..., embed=True),db:Database = Depends(get_db), admin_user:dict = Depends(get_users_infor)):
    # 업데이트 할 정보를 디비에 다시 넣기
    update = db["user"]
    update.update_one({'user_k_id':user_k_id},{'$set':{'role':role}})


