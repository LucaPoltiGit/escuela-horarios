from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

@dataclass
class SlotHorario:
    """Un módulo en un día específico"""
    dia: str
    modulo_numero: int

@dataclass
class AsignacionSlot:
    """Una asignación resuelta: quién da clase, a quién, cuándo"""
    profesor_id: int
    profesor_nombre: str
    materia: str
    grado_id: int
    grado_nombre: str
    dia: str
    modulo_numero: int

@dataclass
class EstadoScheduler:
    """El estado completo del proceso de scheduling"""
    # Slots ya ocupados por profesor: (profesor_id, dia, modulo_numero)
    ocupado_profesor: Set[Tuple[int, str, int]] = field(default_factory=set)
    # Slots ya ocupados por grado: (grado_id, dia, modulo_numero)
    ocupado_grado: Set[Tuple[int, str, int]] = field(default_factory=set)
    # Resultado final
    asignaciones: List[AsignacionSlot] = field(default_factory=list)

    def hay_conflicto(self, profesor_id: int, grado_id: int, dia: str, modulo: int) -> bool:
        return (
            (profesor_id, dia, modulo) in self.ocupado_profesor or
            (grado_id, dia, modulo) in self.ocupado_grado
        )

    def asignar(self, slot: AsignacionSlot):
        self.ocupado_profesor.add((slot.profesor_id, slot.dia, slot.modulo_numero))
        self.ocupado_grado.add((slot.grado_id, slot.dia, slot.modulo_numero))
        self.asignaciones.append(slot)

    def desasignar(self, slot: AsignacionSlot):
        self.ocupado_profesor.discard((slot.profesor_id, slot.dia, slot.modulo_numero))
        self.ocupado_grado.discard((slot.grado_id, slot.dia, slot.modulo_numero))
        self.asignaciones.remove(slot)