from fastapi import FastAPI, Depends
from app.database import engine, Base
from app import models
from app.routers import escuela, profesor, maestra, auth
from app.core.dependencies import get_current_user

app = FastAPI(title="Escuela Horarios API", version="0.1.0")

app.include_router(auth.router)
app.include_router(escuela.router, dependencies=[Depends(get_current_user)])
app.include_router(profesor.router, dependencies=[Depends(get_current_user)])
app.include_router(maestra.router, dependencies=[Depends(get_current_user)])

@app.get("/")
def root():
    return {"message": "Escuela Horarios API funcionando"}