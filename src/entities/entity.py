"""
Entity - Puente de Compatibilidad (Refactorizado)
================================================

Este archivo actúa como puente de compatibilidad tras la refactorización modular.
La funcionalidad se ha dividido en módulos especializados:

- entity_types.py: Enums y dataclasses
- entity_effects.py: Sistema de efectos y estados especiales
- entity_rendering.py: Sistema de renderizado y animaciones
- entity_core.py: Clase base Entity refactorizada

Importaciones para mantener compatibilidad con código existente.
"""

# Importar todo para compatibilidad
from .entity_core import Entity
from .entity_effects import EntityEffectsSystem
from .entity_rendering import EntityRenderingSystem
from .entity_types import EntityState, EntityStats, EntityType

# Mantener las exportaciones existentes
__all__ = [
    "EntityType",
    "EntityState",
    "EntityStats",
    "Entity",
    "EntityEffectsSystem",
    "EntityRenderingSystem",
]
