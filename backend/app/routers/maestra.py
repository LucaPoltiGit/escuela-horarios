from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import MaestraDeGrado, Grado
from app.schemas.maestra import MaestraCreate, MaestraResponse

router = APIRouter(prefix="/escuelas", tags=["Maestras de Grado"])

@router.post("/{escuela_id}/grados/{grado_id}/maestra", response_model=MaestraResponse)
def asignar_maestra(escuela_id: int, grado_id: int, maestra: MaestraCreate, db: Session = Depends(get_db)):
    grado = db.query(Grado).filter(Grado.id == grado_id, Grado.escuela_id == escuela_id).first()
    if not grado:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    if grado.maestra:
        raise HTTPException(status_code=400, detail="El grado ya tiene una maestra asignada")
    nueva = MaestraDeGrado(nombre=maestra.nombre, grado_id=grado_id)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/{escuela_id}/grados/{grado_id}/maestra", response_model=MaestraResponse)
def obtener_maestra(escuela_id: int, grado_id: int, db: Session = Depends(get_db)):
    grado = db.query(Grado).filter(Grado.id == grado_id, Grado.escuela_id == escuela_id).first()
    if not grado or not grado.maestra:
        raise HTTPException(status_code=404, detail="Maestra no encontrada")
    return grado.maestra