from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.doctor_service import register_doctor
from app.models import Doctor
from app.schemas.doctor import DoctorRegisterRequest, DoctorResponse, DoctorLoginRequest, TokenResponse
from datetime import date, datetime, timedelta, timezone
import bcrypt
from jose import jwt
import os
from dotenv import load_dotenv
from jose.exceptions import JWTError

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
        raise HTTPException(status_code=500, detail="Error interno del servidor")

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
    return TokenResponse(access_token=token)