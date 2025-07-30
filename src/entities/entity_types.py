"""
Entity Types - Tipos y Estructuras de Datos de Entidades
======================================================

Autor: SiK Team
Fecha: 2024
Descripción: Definiciones de tipos, estados y estadísticas para entidades.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


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

    def to_dict(self) -> Dict[str, Any]:
        """Convierte las estadísticas a diccionario para guardado."""
        return {
            "health": self.health,
            "max_health": self.max_health,
            "speed": self.speed,
            "damage": self.damage,
            "armor": self.armor,
            "attack_speed": self.attack_speed,
            "attack_range": self.attack_range,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EntityStats":
        """Crea estadísticas desde diccionario."""
        return cls(
            health=data.get("health", 100.0),
            max_health=data.get("max_health", 100.0),
            speed=data.get("speed", 1.0),
            damage=data.get("damage", 10.0),
            armor=data.get("armor", 0.0),
            attack_speed=data.get("attack_speed", 1.0),
            attack_range=data.get("attack_range", 50.0),
        )
