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

@admin.put("/models/{model_name}")
def update_role(model_name: str, body:dict = Body(...),db:Database = Depends(get_db), admin_user:dict = Depends(get_users_infor)):
    # 업데이트 할 정보를 디비에 다시 넣기
    new_name = body.get("model_name")
    new_name = new_name.strip()

    if new_name == model_name:
        return{
            "messege":"변경된 내용이 없습니다.",
            "old_name": model_name,
            "new_name": new_name
        }
    same_name_model = db["model"].find_one({"name": new_name})

    if same_name_model:
        raise HTTPException(status_code=409, detail="이미 같은 이름의 모델이 존재합니다.")

    result = db["model"].update_one(
        {"name": model_name},
        {"$set":{"name":new_name}}
    )

    if result.matched_count == 0:
        raise  HTTPException(staus_code=404, detail="해당 모델을 찾을 수 없습니다.")

    db["data"].update_many(
        {"model": model_name},
        {"$set": {"model": new_name}}
    )

    db["chat_history"].update_many(
        {"model": model_name},
        {"$set": {"model": new_name}}
    )
    return {
        "message": "모델 이름이 수정되었습니다.",
        "old_name": model_name,
        "new_name": new_name
    }

@admin.delete("/models/{model_name}")
def delete_model(
    model_name: str,
    db: Database = Depends(get_db),
    admin_user: dict = Depends(get_admin_user)
):
    model_result = db["model"].delete_one({"name": model_name})

    if model_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="해당 모델을 찾을 수 없습니다.")

    data_result = db["data"].delete_many({"model": model_name})

    chat_result = db["chat_history"].delete_many({"model": model_name})

    return {
        "message": "모델이 삭제되었습니다.",
        "model_name": model_name,
        "deleted_model_count": model_result.deleted_count,
        "deleted_data_count": data_result.deleted_count,
        "deleted_chat_count": chat_result.deleted_count
    }

