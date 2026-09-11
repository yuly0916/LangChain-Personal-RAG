from pydantic import BaseModel

class ModelDto(BaseModel):
    name: str
    description: str

class User(BaseModel):
    name:str
    profile_img: str
    user_k_id: int
    role: str

class ChatResponseDto(BaseModel):
    content: str
    role: str

class InforMessageDto(BaseModel):
    message: str