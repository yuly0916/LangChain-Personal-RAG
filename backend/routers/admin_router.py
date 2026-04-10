from fastapi import APIRouter, HTTPException, Depends
from fastapi import UploadFile, File
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo.synchronous.database import Database

from db import get_db

from services.admin_service import AdminService

admin = APIRouter(prefix="/admin")
service = AdminService()

@admin.post("/upload")
async def upload_file(file:UploadFile, db:Database=Depends(get_db)):
    if service.check_extension(file.filename):
        content_bytes = await file.read()
        text_content = content_bytes.decode("utf-8")
        text_split = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_split.create_documents([text_content])
        # 임베딩 한걸 디비에 저장(텍스트포함)
        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

        for t in texts:
            embedded_text = embeddings_model.embed_query(t.page_content)
            col = db["data"]
            data = {"text": t.page_content, "vector_text": embedded_text}
            col.insert_one(data)

    else:
        raise HTTPException(415, detail=".txt파일을 올려주세요.")





