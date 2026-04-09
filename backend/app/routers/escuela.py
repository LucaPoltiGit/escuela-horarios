from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Escuela, Modulo, Grado
from app.schemas.escuela import EscuelaCreate, EscuelaResponse
from app.schemas.modulo import ModuloCreate, ModuloResponse
from app.schemas.grado import GradoCreate, GradoResponse
from typing import List

router = APIRouter(prefix="/escuelas", tags=["Escuelas"])

# ── Escuela ───────────────────────────────────────────────

@router.post("/", response_model=EscuelaResponse)
def crear_escuela(escuela: EscuelaCreate, db: Session = Depends(get_db)):
    nueva = Escuela(**escuela.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=List[EscuelaResponse])
def listar_escuelas(db: Session = Depends(get_db)):
    return db.query(Escuela).all()

@router.get("/{escuela_id}", response_model=EscuelaResponse)
def obtener_escuela(escuela_id: int, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    return escuela

# ── Módulos ───────────────────────────────────────────────

@router.post("/{escuela_id}/modulos", response_model=ModuloResponse)
def agregar_modulo(escuela_id: int, modulo: ModuloCreate, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    nuevo = Modulo(**modulo.model_dump(), escuela_id=escuela_id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/{escuela_id}/modulos", response_model=List[ModuloResponse])
def listar_modulos(escuela_id: int, db: Session = Depends(get_db)):
    return db.query(Modulo).filter(Modulo.escuela_id == escuela_id).all()

# ── Grados ────────────────────────────────────────────────

@router.post("/{escuela_id}/grados", response_model=GradoResponse)
def agregar_grado(escuela_id: int, grado: GradoCreate, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    nuevo = Grado(**grado.model_dump(), escuela_id=escuela_id)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/{escuela_id}/grados", response_model=List[GradoResponse])
def listar_grados(escuela_id: int, db: Session = Depends(get_db)):
    return db.query(Grado).filter(Grado.escuela_id == escuela_id).all()