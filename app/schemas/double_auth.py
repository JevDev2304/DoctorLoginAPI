from pydantic import BaseModel

class EmailValidationResponse(BaseModel):
    existance: bool

class UserEmailRequest(BaseModel):
    id: str
    email: str

class DoubleAuthRequest(BaseModel):
    token: str
    code: str

class ChangePasswordRequest(BaseModel):
    id: str
    new_password: str