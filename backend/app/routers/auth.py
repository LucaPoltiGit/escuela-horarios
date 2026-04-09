from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Usuario
from app.schemas.auth import RegistroRequest, LoginRequest, TokenResponse, UsuarioResponse
from app.core.security import hash_password, verify_password, crear_token
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registro", response_model=UsuarioResponse)
def registro(data: RegistroRequest, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    usuario = Usuario(
        email=data.email,
        nombre=data.nombre,
        hashed_password=hash_password(data.password)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario or not verify_password(data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = crear_token({"sub": str(usuario.id)})
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UsuarioResponse)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user