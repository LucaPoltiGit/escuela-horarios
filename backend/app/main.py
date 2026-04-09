from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import escuela, profesor, maestra

app = FastAPI(title="Escuela Horarios API", version="0.1.0")

app.include_router(escuela.router)
app.include_router(profesor.router)
app.include_router(maestra.router)

@app.get("/")
def root():
    return {"message": "Escuela Horarios API funcionando"}