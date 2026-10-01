from pydantic import BaseModel

class ModelDto(BaseModel):
    name: str
    description: str

class User(BaseModel):
    name:str
    profile_img: str |None
    user_k_id: int | None
    role: str
    login_type:int

class ChatResponseDto(BaseModel):
    content: str
    role: str

class InforMessageDto(BaseModel):
    message: str