from pydantic import BaseModel

class MaestraCreate(BaseModel):
    nombre: str

class MaestraResponse(BaseModel):
    id: int
    nombre: str
    grado_id: int

    class Config:
        from_attributes = True