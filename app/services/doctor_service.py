from sqlalchemy.orm import Session
from app.models import Doctor
import bcrypt
from sqlalchemy.exc import IntegrityError

def register_doctor(db: Session, id: str, name: str, last_name: str, birth_date, password: str):
    # Verificar si el doctor ya existe
    existing = db.query(Doctor).filter(Doctor.id == id).first()
    if existing:
        raise ValueError("El id ya está registrado")
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    doctor = Doctor(
        id=id,  # El id viene del frontend
        name=name,
        last_name=last_name,
        birth_date=birth_date,
        eliminated=False,
        password=hashed_password
    )
    db.add(doctor)
    try:
        db.commit()
        db.refresh(doctor)
    except IntegrityError:
        db.rollback()
        raise ValueError("Error de integridad al registrar el doctor")
    return doctor 