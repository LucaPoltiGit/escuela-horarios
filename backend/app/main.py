from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import escuela

app = FastAPI(title="Escuela Horarios API", version="0.1.0")

app.include_router(escuela.router)

@app.get("/")
def root():
    return {"message": "Escuela Horarios API funcionando"}