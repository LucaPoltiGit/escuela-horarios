from pydantic import BaseModel
from typing import Optional
from datetime import time
from app.models.models import TipoModulo

class ModuloCreate(BaseModel):
    numero: int
    hora_inicio: time
    hora_fin: time
    tipo: TipoModulo = TipoModulo.clase

class ModuloResponse(BaseModel):
    id: int
    numero: int
    hora_inicio: time
    hora_fin: time
    tipo: TipoModulo
    escuela_id: int

    class Config:
        from_attributes = True