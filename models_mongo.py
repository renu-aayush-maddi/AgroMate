# models_mongo.py
from datetime import datetime

# Logical “models” as helpers for collection names and basic docs
USERS_COLL = "users"
PROFILES_COLL = "farmer_profiles"
SESSIONS_COLL = "session_contexts"

def user_doc(email: str, password_hash: str, name: str | None):
    now = datetime.utcnow()
    return {
        "email": email,
        "password_hash": password_hash,
        "name": name,
        "created_at": now,
    }

def profile_doc(user_id, fields: dict):
    now = datetime.utcnow()
    base = {
        "user_id": user_id,  # email used as stable foreign key
        "updated_at": now
    }
    base.update(fields)
    return base

def session_context_doc(session_id: str):
    now = datetime.utcnow()
    return {
        "session_id": session_id,
        "data": {},
        "updated_at": now
    }
