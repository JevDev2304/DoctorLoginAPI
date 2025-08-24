from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
import random
from jose import ExpiredSignatureError, jwt, JWTError
import smtplib
from email.mime.text import MIMEText

# Clave secreta (debería venir de variables de entorno)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def create_2fa_token(user_id: int, expires_minutes: int = 5):
    otp_code = str(random.randint(100000, 999999))
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {
        "sub": str(user_id),
        "otp_code": otp_code,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, otp_code


def verify_2fa_token(token: str, code: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        return {"valid": False, "reason": "expired"}
    except JWTError:
        return {"valid": False, "reason": "invalid_token"}

    if payload.get("otp_code") != code:
        return {"valid": False, "reason": "wrong_code"}

    return {"valid": True, "user_id": payload.get("sub")}


def send_2fa_token(email, code):
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; padding:20px;">
        <div style="max-width:500px; margin:0 auto; background:#ffffff; padding:20px; border-radius:10px; box-shadow:0 2px 5px rgba(0,0,0,0.1); text-align:center;">
          <h2 style="color:#333;">🔐 Tu código de verificación</h2>
          <p style="color:#555;">Usa este código para completar tu autenticación:</p>
          <div style="margin:30px 0;">
            <span style="font-size:32px; font-weight:bold; color:#2196F3; background:#f1f1f1; padding:15px 30px; border-radius:8px; letter-spacing:4px; display:inline-block;">
              {code}
            </span>
          </div>
          <p style="font-size:14px; color:#777;">⚠️ Este código expira en 5 minutos.</p>
          <p style="font-size:12px; color:#aaa; margin-top:20px;">Si no solicitaste este código, ignora este correo.</p>
        </div>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Tu código de verificación 2FA"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)


