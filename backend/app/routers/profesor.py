from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import ProfesorCurricular, DisponibilidadProfesor, AsignacionCurricular, Escuela
from app.schemas.profesor import ProfesorCreate, ProfesorResponse
from typing import List

router = APIRouter(prefix="/escuelas", tags=["Profesores"])

@router.post("/{escuela_id}/profesores", response_model=ProfesorResponse)
def crear_profesor(escuela_id: int, profesor: ProfesorCreate, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")
    
    nuevo = ProfesorCurricular(
        nombre=profesor.nombre,
        materia=profesor.materia,
        modulos_cargo=profesor.modulos_cargo,
        escuela_id=escuela_id
    )
    db.add(nuevo)
    db.flush()

    for d in profesor.disponibilidad:
        db.add(DisponibilidadProfesor(
            profesor_id=nuevo.id,
            dia=d.dia,
            modulos_ese_dia=d.modulos_ese_dia
        ))

    for a in profesor.asignaciones:
        db.add(AsignacionCurricular(
            profesor_id=nuevo.id,
            grado_id=a.grado_id,
            modulos_semanales=a.modulos_semanales
        ))

    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/{escuela_id}/profesores", response_model=List[ProfesorResponse])
def listar_profesores(escuela_id: int, db: Session = Depends(get_db)):
    return db.query(ProfesorCurricular).filter(ProfesorCurricular.escuela_id == escuela_id).all()

@router.get("/{escuela_id}/profesores/{profesor_id}", response_model=ProfesorResponse)
def obtener_profesor(escuela_id: int, profesor_id: int, db: Session = Depends(get_db)):
    profesor = db.query(ProfesorCurricular).filter(
        ProfesorCurricular.id == profesor_id,
        ProfesorCurricular.escuela_id == escuela_id
    ).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor