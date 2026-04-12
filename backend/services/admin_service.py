from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database


class AdminService:
    def __init__(self):
        self.embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
    def check_extension(self, file_name: str) -> bool:
        """
        확장자 검사
        :param file_name:
        :return:
        """
        if file_name.split(".")[-1] == "txt":
            return True
        else:
            return False
    async def load_file(self, file:UploadFile) -> str:
        content_bytes:bytes = await file.read()
        return content_bytes.decode("utf-8")

    def chunk_texts(self, text:str) ->list[Document]:
        text_split:RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_split.create_documents([text])

    def insert_db_model_collection(self, model_name:str, description:str, model:Collection):
        about_model:dict = {"name": model_name, "description": description}
        model["model"].insert_one(about_model)

    def insert_db_data_collection(self, chunks:list[Document], model:str, data:Collection):
        for chunk in chunks:
            embed:list[float] = self.embed_model.embed_query(chunk.page_content)
            data.insert_one({"text":chunk.page_content, "vector_text": embed, "model":model})

    def get_users(self, user:Collection):
        users= user.find({},{'_id':0,'user_k_id':1, 'name':1, 'role':1})
        return list(users)

