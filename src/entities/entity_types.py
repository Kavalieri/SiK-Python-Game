"""
Entity Types - Tipos y Estructuras de Datos de Entidades
======================================================

Autor: SiK Team
Fecha: 2024
Descripción: Definiciones de tipos, estados y estadísticas para entidades.
"""

from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
    """Tipos de entidades en el juego."""

    PLAYER = "player"
    ENEMY = "enemy"
    PROJECTILE = "projectile"
    POWERUP = "powerup"
    CHARACTER = "character"
    TILE = "tile"


class EntityState(Enum):
    """Estados posibles de una entidad."""

    IDLE = "idle"
    MOVING = "moving"
    ATTACKING = "attacking"
    HURT = "hurt"
    DEAD = "dead"
    INVULNERABLE = "invulnerable"


@dataclass
class EntityStats:
    """Estadísticas base de una entidad."""

    health: float = 100.0
    max_health: float = 100.0
    speed: float = 1.0
    damage: float = 10.0
    armor: float = 0.0
    attack_speed: float = 1.0
    attack_range: float = 50.0
