from fastapi import APIRouter
from sqlalchemy.orm import Session
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routes.doctor_routes import ACCESS_TOKEN_EXPIRE_HOURS, ALGORITHM, SECRET_KEY
from app.schemas.admin import AdminLoginRequest
from app.schemas.doctor import TokenResponse
from app.models import Admin

from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from jose.exceptions import JWTError

router = APIRouter()

@router.post("/login")
def admin_login(request:AdminLoginRequest , db: Session = Depends(get_db)):
	admin = db.query(Admin).filter(Admin.id == request.id).first()
	if not admin or not bcrypt.checkpw(request.password.encode(), admin.password.encode()):
		raise HTTPException(status_code=401, detail="Credenciales inválidas")
	expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
	to_encode = {"sub": admin.id, 
                 "exp": expire}
	token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
	except JWTError:
		raise HTTPException(status_code=500, detail="Error al validar el token generado")
	return TokenResponse(token=token)