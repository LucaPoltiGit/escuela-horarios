from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Time
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TipoModulo(str, enum.Enum):
    clase = "clase"
    recreo = "recreo"
    comedor = "comedor"

class DiaSemana(str, enum.Enum):
    lunes = "lunes"
    martes = "martes"
    miercoles = "miercoles"
    jueves = "jueves"
    viernes = "viernes"

# ── Escuela ──────────────────────────────────────────────
class Escuela(Base):
    __tablename__ = "escuelas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    numero = Column(String, nullable=True)  # ej: "Escuela N°3"

    modulos = relationship("Modulo", back_populates="escuela")
    grados = relationship("Grado", back_populates="escuela")
    profesores = relationship("ProfesorCurricular", back_populates="escuela")

# ── Módulos horarios ──────────────────────────────────────
class Modulo(Base):
    __tablename__ = "modulos"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    numero = Column(Integer, nullable=False)        # 1, 2, 3...
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    tipo = Column(Enum(TipoModulo), default=TipoModulo.clase)

    escuela = relationship("Escuela", back_populates="modulos")

# ── Grados ────────────────────────────────────────────────
class Grado(Base):
    __tablename__ = "grados"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    nombre = Column(String, nullable=False)   # ej: "1° A"

    escuela = relationship("Escuela", back_populates="grados")
    maestra = relationship("MaestraDeGrado", back_populates="grado", uselist=False)
    asignaciones = relationship("AsignacionCurricular", back_populates="grado")

# ── Maestra de grado ──────────────────────────────────────
class MaestraDeGrado(Base):
    __tablename__ = "maestras_de_grado"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    grado_id = Column(Integer, ForeignKey("grados.id"), nullable=False, unique=True)

    grado = relationship("Grado", back_populates="maestra")

# ── Profesor curricular ───────────────────────────────────
class ProfesorCurricular(Base):
    __tablename__ = "profesores_curriculares"

    id = Column(Integer, primary_key=True, index=True)
    escuela_id = Column(Integer, ForeignKey("escuelas.id"), nullable=False)
    nombre = Column(String, nullable=False)
    materia = Column(String, nullable=False)        # ej: "Música"
    modulos_cargo = Column(Integer, nullable=False) # total de módulos semanales del cargo

    escuela = relationship("Escuela", back_populates="profesores")
    disponibilidad = relationship("DisponibilidadProfesor", back_populates="profesor")
    asignaciones = relationship("AsignacionCurricular", back_populates="profesor")

# ── Días que viene el profesor ────────────────────────────
class DisponibilidadProfesor(Base):
    __tablename__ = "disponibilidad_profesores"

    id = Column(Integer, primary_key=True, index=True)
    profesor_id = Column(Integer, ForeignKey("profesores_curriculares.id"), nullable=False)
    dia = Column(Enum(DiaSemana), nullable=False)
    modulos_ese_dia = Column(Integer, nullable=False)  # cuántos módulos viene ese día

    profesor = relationship("ProfesorCurricular", back_populates="disponibilidad")

# ── A qué grados le da y cuántos módulos ─────────────────
class AsignacionCurricular(Base):
    __tablename__ = "asignaciones_curriculares"

    id = Column(Integer, primary_key=True, index=True)
    profesor_id = Column(Integer, ForeignKey("profesores_curriculares.id"), nullable=False)
    grado_id = Column(Integer, ForeignKey("grados.id"), nullable=False)
    modulos_semanales = Column(Integer, nullable=False)  # cuántos módulos le da a ese grado

    profesor = relationship("ProfesorCurricular", back_populates="asignaciones")
    grado = relationship("Grado", back_populates="asignaciones")