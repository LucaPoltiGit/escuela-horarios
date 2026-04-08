from fastapi import FastAPI
from app.database import engine, Base
from app import models

app = FastAPI(title="Escuela Horarios API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "Escuela Horarios API funcionando"}