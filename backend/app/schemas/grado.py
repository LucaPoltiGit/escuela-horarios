from pydantic import BaseModel

class GradoCreate(BaseModel):
    nombre: str

class GradoResponse(BaseModel):
    id: int
    nombre: str
    escuela_id: int

    class Config:
        from_attributes = True