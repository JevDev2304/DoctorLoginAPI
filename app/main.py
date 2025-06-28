from fastapi import FastAPI
from app.routes import doctor_routes

app = FastAPI()

app.include_router(doctor_routes.router, prefix="/doctor")

@app.get("/")
def root():
    return {"msg": "API de login"}
