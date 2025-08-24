from pydantic import BaseModel
from datetime import date

class DoctorRegisterRequest(BaseModel):
    id: str
    name: str
    last_name: str
    email: str
    birth_date: date
    password: str

class DoctorResponse(BaseModel):
    id: str
    name: str
    last_name: str
    birth_date: date

class DoctorLoginRequest(BaseModel):
    id: str
    password: str

class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer" 
