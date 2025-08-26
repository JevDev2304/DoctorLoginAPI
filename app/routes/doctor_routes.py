import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.doctor import DoctorLoginRequest, DoctorRegisterRequest, DoctorResponse, TokenResponse
from app.schemas.double_auth import ChangePasswordRequest, DoubleAuthRequest, EmailValidationResponse, UserEmailRequest
from app.services.doctor_service import change_password, register_doctor
from app.models import Doctor

from datetime import date, datetime, timedelta, timezone
import bcrypt
from jose import jwt
import os
from dotenv import load_dotenv
from jose.exceptions import JWTError

from app.services.double_auth_service import create_2fa_token, send_2fa_token, verify_2fa_token

router = APIRouter()

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", "cambia_esto_por_una_clave_secreta_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 12

@router.post("/register", response_model=DoctorResponse)
def register_doctor_endpoint(request: DoctorRegisterRequest, db: Session = Depends(get_db)):
    try:
        doctor = register_doctor(
            db=db,
            id=request.id,
            name=request.name,
            last_name=request.last_name,
            email=request.email,
            birth_date=request.birth_date,
            password=request.password
        )
        return DoctorResponse(
            id=str(doctor.id),
            name=str(doctor.name),
            last_name=str(doctor.last_name),
            birth_date=doctor.birth_date if isinstance(doctor.birth_date, date) else date.fromisoformat(str(doctor.birth_date))
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor {e}")

@router.post("/login", response_model=TokenResponse)
def login_doctor(request: DoctorLoginRequest, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == request.id).first()
    if not doctor or not bcrypt.checkpw(request.password.encode(), doctor.password.encode()):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {"sub": doctor.id, 
                 "name": f"{doctor.name} {doctor.last_name}",
                 "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Validar el token generado
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=500, detail="Error al validar el token generado")
    return TokenResponse(token=token)

@router.post("/change_password", response_model="")
def change_password_endpoint(request: ChangePasswordRequest, db:Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == request.id).first()
    if not doctor:
        raise HTTPException(status_code=400, detail="No existe ese ID")
    if bcrypt.checkpw(request.new_password.encode(), doctor.password.encode()):
        raise HTTPException(status_code=400, detail="Esa contraseña es la actual")
    else:
        doctor = change_password(db, request.id, request.new_password)
        return DoctorResponse(
                id=str(doctor.id),
                name=str(doctor.name),
                last_name=str(doctor.last_name),
                birth_date=doctor.birth_date if isinstance(doctor.birth_date, date) else date.fromisoformat(str(doctor.birth_date))
            )


@router.post("/validate_email", response_model=EmailValidationResponse)
def validate_email(request: UserEmailRequest, db:Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == request.id).first()
    if not doctor:
        raise HTTPException(status_code=401, detail="ID inválido")
    if not doctor.email:
        raise HTTPException(status_code=500, detail="El doctor no cuenta con correo")
    assertion = doctor.email == request.email
    return EmailValidationResponse(existance=assertion)

@router.post("/send-2fa", response_model=TokenResponse)
def send_2fa(request: UserEmailRequest, db:Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == request.id).first()
    if not doctor:
        raise HTTPException(status_code=401, detail="ID inválido")
    if not doctor.email:
        raise HTTPException(status_code=500, detail="El doctor no cuenta con correo")
    token, code = create_2fa_token(request.id)
    send_2fa_token(request.email, code)
    return TokenResponse(token=token)

@router.post("/verify-2fa")
def verify_2fa(request: DoubleAuthRequest):
    result = verify_2fa_token(request.token, request.code)
    if not result["valid"]:
        if result["reason"] == "expired":
            raise HTTPException(status_code=400, detail="El código ha expirado")
        elif result["reason"] == "wrong_code":
            raise HTTPException(status_code=400, detail="El código es incorrecto")
        else:
            raise HTTPException(status_code=400, detail="Token inválido")
    return {"message": "Autenticación completada", "user_id": result["user_id"]}



