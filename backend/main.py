import uvicorn
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

load_dotenv()
from fastapi import FastAPI
from routers.admin_router import admin
from routers.chat_router import chat
from routers.login_router import login
from routers.web_router import web


app = FastAPI()

origin = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(login)
app.include_router(chat)
app.include_router(admin)
app.include_router(web)

@app.get('/test')
def test():
    return True


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
