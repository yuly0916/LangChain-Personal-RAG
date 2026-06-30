import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.synchronous.database import Database

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("MONGO_DB", "aichat")]

def get_db() -> Database:
    return db