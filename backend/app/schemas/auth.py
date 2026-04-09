from pydantic import BaseModel, EmailStr
from typing import Optional

class RegistroRequest(BaseModel):
    email: EmailStr
    nombre: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UsuarioResponse(BaseModel):
    id: int
    email: str
    nombre: str
    escuela_id: Optional[int] = None

    class Config:
        from_attributes = True