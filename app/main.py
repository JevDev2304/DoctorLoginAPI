from fastapi import FastAPI
from app.routes import doctor_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(doctor_routes.router, prefix="/doctor")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*"
)

@app.get("/")
def root():
    return {"msg": "API de login"}
