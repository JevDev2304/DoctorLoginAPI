from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    id: str
    password: str