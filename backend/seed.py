import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models.models import (
    Escuela, Modulo, Grado, MaestraDeGrado,
    ProfesorCurricular, DisponibilidadProfesor,
    AsignacionCurricular, TipoModulo, DiaSemana
)

def seed():
    db = SessionLocal()

    # ── Escuela ───────────────────────────────────────────
    escuela = Escuela(nombre="Escuela Normal Superior", numero="3")
    db.add(escuela)
    db.flush()

    # ── Módulos ───────────────────────────────────────────
    from datetime import time
    modulos_data = [
        (1, time(7, 30), time(8, 10), TipoModulo.clase),
        (2, time(8, 10), time(8, 50), TipoModulo.clase),
        (3, time(8, 50), time(9, 10), TipoModulo.recreo),
        (4, time(9, 10), time(9, 50), TipoModulo.clase),
        (5, time(9, 50), time(10, 30), TipoModulo.clase),
        (6, time(10, 30), time(11, 10), TipoModulo.clase),
        (7, time(11, 10), time(11, 50), TipoModulo.clase),
        (8, time(11, 50), time(12, 10), TipoModulo.comedor),
    ]
    modulos = []
    for numero, inicio, fin, tipo in modulos_data:
        m = Modulo(escuela_id=escuela.id, numero=numero, hora_inicio=inicio, hora_fin=fin, tipo=tipo)
        db.add(m)
        modulos.append(m)
    db.flush()

    # ── Grados ────────────────────────────────────────────
    nombres_grados = [
        "1° A", "1° B",
        "2° A", "2° B",
        "3° A", "3° B",
        "4° A", "4° B",
        "5° A", "5° B",
        "6° A", "6° B",
    ]
    grados = []
    for nombre in nombres_grados:
        g = Grado(escuela_id=escuela.id, nombre=nombre)
        db.add(g)
        grados.append(g)
    db.flush()

    # ── Maestras de grado ─────────────────────────────────
    maestras_nombres = [
        "Roxana García", "Julia Pérez",
        "Laura Martínez", "Claudia López",
        "Sandra Rodríguez", "Patricia Gómez",
        "Marcela Díaz", "Silvia Fernández",
        "Carolina Torres", "Valeria Ruiz",
        "Natalia Sánchez", "Mónica Herrera",
    ]
    for grado, nombre in zip(grados, maestras_nombres):
        db.add(MaestraDeGrado(nombre=nombre, grado_id=grado.id))
    db.flush()

    # ── Profesores curriculares ───────────────────────────
    profesores_data = [
        {
            "nombre": "Carlos Méndez",
            "materia": "Música",
            "modulos_cargo": 16,
            "disponibilidad": [
                (DiaSemana.lunes, 4),
                (DiaSemana.miercoles, 4),
                (DiaSemana.viernes, 4),
            ],
            "asignaciones": [0, 1, 2, 3],  # índices de grados
            "modulos_por_grado": 2,
        },
        {
            "nombre": "Ana López",
            "materia": "Inglés",
            "modulos_cargo": 32,
            "disponibilidad": [
                (DiaSemana.lunes, 5),
                (DiaSemana.martes, 5),
                (DiaSemana.miercoles, 5),
                (DiaSemana.jueves, 5),
            ],
            "asignaciones": [0, 1, 2, 3, 4, 5],
            "modulos_por_grado": 2,
        },
        {
            "nombre": "Roberto Silva",
            "materia": "Educación Física",
            "modulos_cargo": 16,
            "disponibilidad": [
                (DiaSemana.martes, 4),
                (DiaSemana.jueves, 4),
                (DiaSemana.viernes, 4),
            ],
            "asignaciones": [4, 5, 6, 7],
            "modulos_por_grado": 2,
        },
        {
            "nombre": "Fernanda Castro",
            "materia": "Plástica",
            "modulos_cargo": 14,
            "disponibilidad": [
                (DiaSemana.lunes, 3),
                (DiaSemana.miercoles, 3),
                (DiaSemana.viernes, 3),
            ],
            "asignaciones": [8, 9, 10, 11],
            "modulos_por_grado": 2,
        },
        {
            "nombre": "Diego Romero",
            "materia": "Inglés",
            "modulos_cargo": 16,
            "disponibilidad": [
                (DiaSemana.martes, 4),
                (DiaSemana.jueves, 4),
            ],
            "asignaciones": [6, 7, 8, 9],
            "modulos_por_grado": 2,
        },
    ]

    for data in profesores_data:
        prof = ProfesorCurricular(
            escuela_id=escuela.id,
            nombre=data["nombre"],
            materia=data["materia"],
            modulos_cargo=data["modulos_cargo"]
        )
        db.add(prof)
        db.flush()

        for dia, cantidad in data["disponibilidad"]:
            db.add(DisponibilidadProfesor(
                profesor_id=prof.id,
                dia=dia,
                modulos_ese_dia=cantidad
            ))

        for idx in data["asignaciones"]:
            db.add(AsignacionCurricular(
                profesor_id=prof.id,
                grado_id=grados[idx].id,
                modulos_semanales=data["modulos_por_grado"]
            ))

    db.commit()
    db.close()
    print("✅ Seed completado: escuela, módulos, grados, maestras y profesores cargados.")

if __name__ == "__main__":
    seed()