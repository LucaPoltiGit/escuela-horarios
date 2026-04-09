from pydantic import BaseModel
from typing import List, Optional

class SlotAsignado(BaseModel):
    profesor_id: int
    profesor_nombre: str
    materia: str
    grado_id: int
    grado_nombre: str
    dia: str
    modulo_numero: int

class HorarioResponse(BaseModel):
    escuela_id: int
    exitoso: bool
    mensaje: Optional[str] = None
    asignaciones: List[SlotAsignado] = []