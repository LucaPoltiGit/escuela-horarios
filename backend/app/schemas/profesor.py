from pydantic import BaseModel
from typing import List, Optional
from app.models.models import DiaSemana

class DisponibilidadCreate(BaseModel):
    dia: DiaSemana
    modulos_ese_dia: int

class AsignacionCreate(BaseModel):
    grado_id: int
    modulos_semanales: int

class ProfesorCreate(BaseModel):
    nombre: str
    materia: str
    modulos_cargo: int
    disponibilidad: List[DisponibilidadCreate]
    asignaciones: List[AsignacionCreate]

class DisponibilidadResponse(BaseModel):
    id: int
    dia: DiaSemana
    modulos_ese_dia: int
    class Config:
        from_attributes = True

class AsignacionResponse(BaseModel):
    id: int
    grado_id: int
    modulos_semanales: int
    class Config:
        from_attributes = True

class ProfesorResponse(BaseModel):
    id: int
    nombre: str
    materia: str
    modulos_cargo: int
    escuela_id: int
    disponibilidad: List[DisponibilidadResponse]
    asignaciones: List[AsignacionResponse]
    class Config:
        from_attributes = True