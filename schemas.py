# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class FarmerProfileRequest(BaseModel):
    crops: Optional[str] = None
    soil_type: Optional[str] = None
    location_pref: Optional[str] = None
    irrigation_method: Optional[str] = None
    acreage: Optional[str] = None
    custom_notes: Optional[str] = None

class FarmerProfileResponse(FarmerProfileRequest):
    pass

class QuestionRequest(BaseModel):
    question: str
    location: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
