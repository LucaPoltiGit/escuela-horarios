from pydantic import BaseModel
from typing import Optional

class EscuelaCreate(BaseModel):
    nombre: str
    numero: Optional[str] = None

class EscuelaResponse(BaseModel):
    id: int
    nombre: str
    numero: Optional[str] = None

    class Config:
        from_attributes = True