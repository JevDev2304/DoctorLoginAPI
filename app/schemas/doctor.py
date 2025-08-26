from pydantic import BaseModel
from datetime import date

class DoctorRegisterRequest(BaseModel):
    id: str
    name: str
    last_name: str
    email: str
    password: str

class DoctorResponse(BaseModel):
    id: str
    name: str
    last_name: str

class DoctorLoginRequest(BaseModel):
    id: str
    password: str

class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer" 
