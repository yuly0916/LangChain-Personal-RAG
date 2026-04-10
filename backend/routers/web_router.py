
from fastapi import APIRouter
from fastapi.params import Depends

from services.web_service import WebService
from db import get_db


web = APIRouter()


