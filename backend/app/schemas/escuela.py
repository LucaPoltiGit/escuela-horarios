from pydantic import BaseModel
from typing import Optional, List
from app.schemas.modulo import ModuloResponse
from app.schemas.profesor import ProfesorResponse

class GradoConMaestra(BaseModel):
    id: int
    nombre: str
    maestra: Optional[str] = None

    class Config:
        from_attributes = True

class EscuelaCreate(BaseModel):
    nombre: str
    numero: Optional[str] = None

class EscuelaResponse(BaseModel):
    id: int
    nombre: str
    numero: Optional[str] = None

    class Config:
        from_attributes = True

class EscuelaResumen(BaseModel):
    id: int
    nombre: str
    numero: Optional[str] = None
    modulos: List[ModuloResponse]
    grados: List[GradoConMaestra]
    profesores: List[ProfesorResponse]

    class Config:
        from_attributes = True