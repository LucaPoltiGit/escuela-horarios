from typing import List, Optional, Dict
from app.models.models import ProfesorCurricular, Modulo, Grado
from app.services.scheduler.models import EstadoScheduler, AsignacionSlot, SlotHorario

def generar_slots_disponibles(profesor: ProfesorCurricular, modulos: List[Modulo]) -> List[SlotHorario]:
    """Genera todos los slots posibles para un profesor según sus días y módulos disponibles"""
    slots = []
    modulos_clase = [m for m in modulos if m.tipo == "clase"]
    numeros_modulos = sorted([m.numero for m in modulos_clase])

    for disponibilidad in profesor.disponibilidad:
        dia = disponibilidad.dia.value
        cantidad = disponibilidad.modulos_ese_dia
        for modulo_num in numeros_modulos[:cantidad]:
            slots.append(SlotHorario(dia=dia, modulo_numero=modulo_num))

    return slots

def backtrack(
    tareas: List[dict],
    indice: int,
    estado: EstadoScheduler,
    slots_por_profesor: Dict[int, List[SlotHorario]]
) -> bool:
    """
    Intenta asignar todas las tareas recursivamente.
    Cada tarea es: { profesor, grado, modulos_a_asignar }
    """
    if indice == len(tareas):
        return True  # todas las tareas asignadas

    tarea = tareas[indice]
    profesor = tarea["profesor"]
    grado = tarea["grado"]
    modulos_a_asignar = tarea["modulos_a_asignar"]
    slots_disponibles = slots_por_profesor[profesor.id]

    # Intentá encontrar `modulos_a_asignar` slots sin conflicto
    asignados = []

    for slot in slots_disponibles:
        if len(asignados) == modulos_a_asignar:
            break
        if not estado.hay_conflicto(profesor.id, grado.id, slot.dia, slot.modulo_numero):
            nuevo_slot = AsignacionSlot(
                profesor_id=profesor.id,
                profesor_nombre=profesor.nombre,
                materia=profesor.materia,
                grado_id=grado.id,
                grado_nombre=grado.nombre,
                dia=slot.dia,
                modulo_numero=slot.modulo_numero
            )
            estado.asignar(nuevo_slot)
            asignados.append(nuevo_slot)

    if len(asignados) < modulos_a_asignar:
        # No encontró suficientes slots — retrocedé
        for slot in asignados:
            estado.desasignar(slot)
        return False

    # Seguí con la siguiente tarea
    if backtrack(tareas, indice + 1, estado, slots_por_profesor):
        return True

    # Si falló hacia adelante, deshacé esta tarea y retrocedé
    for slot in asignados:
        estado.desasignar(slot)
    return False

def generar_horario(
    profesores: List[ProfesorCurricular],
    modulos: List[Modulo],
    grados: List[Grado]
) -> Optional[EstadoScheduler]:
    """Punto de entrada del scheduler"""

    grados_map = {g.id: g for g in grados}
    estado = EstadoScheduler()
    slots_por_profesor = {
        p.id: generar_slots_disponibles(p, modulos)
        for p in profesores
    }

    # Construí la lista de tareas: una por cada (profesor, grado) con módulos a asignar
    tareas = []
    for profesor in profesores:
        for asignacion in profesor.asignaciones:
            grado = grados_map.get(asignacion.grado_id)
            if not grado:
                continue
            tareas.append({
                "profesor": profesor,
                "grado": grado,
                "modulos_a_asignar": asignacion.modulos_semanales
            })

    # Ordená por el más restrictivo primero (menos slots disponibles)
    tareas.sort(key=lambda t: len(slots_por_profesor[t["profesor"].id]))

    exito = backtrack(tareas, 0, estado, slots_por_profesor)

    if not exito:
        return None

    return estado