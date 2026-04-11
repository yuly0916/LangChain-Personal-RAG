from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi import UploadFile, File
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
        content_bytes = await file.read()
        text_content = content_bytes.decode("utf-8")
        text_split = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_split.create_documents([text_content])
        # 임베딩 한걸 디비에 저장(텍스트포함)
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")
        model_col = db["model"]
        data = {"name": model_name, "description": model_description}
        model_col.insert_one(data)
        for t in texts:
            embedded_text = embeddings_model.embed_query(t.page_content)
            col = db["data"]
            data = {"text": t.page_content, "vector_text": embedded_text, "model": model_name}
            col.insert_one(data)

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


