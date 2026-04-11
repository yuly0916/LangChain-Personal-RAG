from traceback import print_exception

from fastapi import APIRouter
import requests
from pymongo.synchronous.collection import Collection

from jose import jwt
import datetime
from starlette.responses import RedirectResponse
from db import get_db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import os

login = APIRouter(prefix="/api")
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
LOGIN_SUCCESS_PAGE = os.environ.get('LOGIN_SUCCESS_PAGE')


def create_token(name, profile_img, kakao_user_id, role="user"):
    """
    티켓 발행 하는 함수
    """
    payload = {
        "name": name,
        "profile_img": profile_img,
        "user_k_id": kakao_user_id,
        "role": role,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

class KakaoAccessTokenResponseException(Exception):
    pass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@login.get("/login/redirect")
def kakao_login_redirect(db=Depends(get_db), code: str | None = None, error: str | None=None, error_description:str|None=None):
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "client_secret": CLIENT_SECRET
    }
    kakao_access_token_response = None

    try:
        # Step1
        kakao_access_token_response = requests.post("https://kauth.kakao.com/oauth/token",data)
        kakao_response_data: dict = kakao_access_token_response.json()
        access_token = kakao_response_data.get("access_token")
        if access_token is None:
            raise KakaoAccessTokenResponseException("엑세스 토큰 받아오기 실패!")

        # Step2
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content_Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        kakao_user_data = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
        user_infor :dict = kakao_user_data.json()
        user_detail :dict = user_infor.get("properties")

        # Step 3
        # DB 입출력, 토큰 생성 부분
        user_col:Collection = db["user"]
        user = user_col.find_one({"user_k_id": user_infor.get("id")},{"_id":0,"name":1,"profile_img":1,"user_k_id":1,"role":1})
        if user is None:
            print("유저가 존재하지 않아 회원가입을 진행합니다. : ",user)
            user = {
                "name": user_detail.get("nickname"),
                "profile_img": user_detail.get("profile_image"),
                "user_k_id": user_infor.get("id"),
                "role": "user"
            }
            user_col.insert_one(user)
            
        token = create_token(
            name=user.get("name") or user_detail.get("nickname"), 
            profile_img=user.get("profile_img") or user_detail.get("profile_image"), 
            kakao_user_id=user.get("user_k_id"),
            role=user.get("role", "user")
        )
        # --end

        #Step4
        res = RedirectResponse(url=LOGIN_SUCCESS_PAGE)
        res.set_cookie(key="jwt_token", value=token)
        return res
    except KakaoAccessTokenResponseException as e:
        print_exception(e)
        print("KaKaoAccessToken Response : ",kakao_access_token_response.json())
        raise HTTPException(500, kakao_access_token_response.json())



