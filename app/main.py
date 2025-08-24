from fastapi import FastAPI
from app.routes import admin_routes, doctor_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(doctor_routes.router, prefix="/doctor")
app.include_router(admin_routes.router, prefix="/admin")

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
