from pymongo import MongoClient
from pymongo.synchronous.database import Database

client = MongoClient("mongodb://localhost:27017")
db = client["aichat"]
def get_db()-> Database:
    return db