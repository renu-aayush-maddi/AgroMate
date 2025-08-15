# db_mongo.py
import os
from dotenv import load_dotenv
import motor.motor_asyncio

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "agri_advisor")

_client = None
_db = None

async def get_db():
    global _client, _db
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
        _db = _client[MONGO_DB_NAME]
    return _db

async def close_db():
    global _client
    if _client:
        _client.close()
        _client = None
