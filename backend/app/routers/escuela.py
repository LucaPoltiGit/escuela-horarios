from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from io import BytesIO
from typing import List

from app.database import get_db
from app.models.models import Escuela, Modulo, Grado
from app.schemas.escuela import EscuelaCreate, EscuelaResponse, EscuelaResumen, GradoConMaestra
from app.schemas.modulo import ModuloCreate, ModuloResponse
from app.schemas.grado import GradoCreate, GradoResponse
from app.schemas.horario import HorarioResponse, SlotAsignado
from app.services.scheduler.engine import generar_horario
from app.services.pdf.generator import generar_pdfs_horario

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

@router.get("/{escuela_id}/resumen", response_model=EscuelaResumen)
def resumen_escuela(escuela_id: int, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    grados_con_maestra = [
        GradoConMaestra(
            id=grado.id,
            nombre=grado.nombre,
            maestra=grado.maestra.nombre if grado.maestra else None
        )
        for grado in escuela.grados
    ]

    return EscuelaResumen(
        id=escuela.id,
        nombre=escuela.nombre,
        numero=escuela.numero,
        modulos=escuela.modulos,
        grados=grados_con_maestra,
        profesores=escuela.profesores
    )

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

# ── Scheduler ─────────────────────────────────────────────

@router.post("/{escuela_id}/generar-horario", response_model=HorarioResponse)
def generar_horario_escuela(escuela_id: int, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    resultado = generar_horario(
        profesores=escuela.profesores,
        modulos=escuela.modulos,
        grados=escuela.grados
    )

    if not resultado:
        return HorarioResponse(
            escuela_id=escuela_id,
            exitoso=False,
            mensaje="No se encontró una combinación válida de horarios"
        )

    return HorarioResponse(
        escuela_id=escuela_id,
        exitoso=True,
        asignaciones=[SlotAsignado(**vars(a)) for a in resultado.asignaciones]
    )

# ── PDF ───────────────────────────────────────────────────

@router.post("/{escuela_id}/generar-pdf")
def generar_pdf_horario(escuela_id: int, db: Session = Depends(get_db)):
    escuela = db.query(Escuela).filter(Escuela.id == escuela_id).first()
    if not escuela:
        raise HTTPException(status_code=404, detail="Escuela no encontrada")

    resultado = generar_horario(
        profesores=escuela.profesores,
        modulos=escuela.modulos,
        grados=escuela.grados
    )

    if not resultado:
        raise HTTPException(status_code=400, detail="No se pudo generar un horario válido")

    grados_map = {
        g.id: {
            "nombre": g.nombre,
            "maestra": g.maestra.nombre if g.maestra else "Sin maestra"
        }
        for g in escuela.grados
    }

    profesores_map = {
        p.id: {"nombre": p.nombre, "materia": p.materia}
        for p in escuela.profesores
    }

    pdf_bytes = generar_pdfs_horario(
        escuela_nombre=escuela.nombre,
        asignaciones=resultado.asignaciones,
        modulos=escuela.modulos,
        grados_map=grados_map,
        profesores_map=profesores_map
    )

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=horario.pdf"}
    )