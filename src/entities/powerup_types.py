"""
Powerup Types - Tipos y configuraciones de powerups
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Tipos de powerups y sus configuraciones.
"""

from dataclasses import dataclass
from enum import Enum


class PowerupType(Enum):
    """Tipos de powerups disponibles."""

    SPEED = "speed"
    DAMAGE = "damage"
    SHIELD = "shield"
    RAPID_FIRE = "rapid_fire"
    DOUBLE_SHOT = "double_shot"
    HEALTH = "health"
    SPREAD = "spread"
    EXPLOSIVE = "explosive"
    SHRAPNEL = "shrapnel"


@dataclass
class PowerupEffect:
    """Efecto de un powerup."""

    type: PowerupType
    duration: float  # Duración en segundos
    value: float  # Valor del efecto
    description: str


class PowerupConfiguration:
    """Configuración de powerups con sus propiedades."""

    POWERUP_CONFIGS = {
        PowerupType.SPEED: {
            "name": "Velocidad",
            "color": (0, 255, 255),  # Cyan
            "duration": 8.0,
            "value": 1.5,  # Multiplicador de velocidad
            "description": "Aumenta la velocidad de movimiento",
        },
        PowerupType.DAMAGE: {
            "name": "Daño",
            "color": (255, 0, 0),  # Rojo
            "duration": 10.0,
            "value": 2.0,  # Multiplicador de daño
            "description": "Duplica el daño de ataque",
        },
        PowerupType.SHIELD: {
            "name": "Escudo",
            "color": (0, 0, 255),  # Azul
            "duration": 15.0,
            "value": 1.0,  # Absorbe daño
            "description": "Absorbe daño por un tiempo limitado",
        },
        PowerupType.RAPID_FIRE: {
            "name": "Fuego Rápido",
            "color": (255, 165, 0),  # Naranja
            "duration": 8.0,
            "value": 3.0,  # Multiplicador de velocidad de ataque
            "description": "Triplica la velocidad de disparo",
        },
        PowerupType.DOUBLE_SHOT: {
            "name": "Disparo Doble",
            "color": (255, 20, 147),  # Rosa
            "duration": 12.0,
            "value": 2,  # Número de proyectiles
            "description": "Dispara dos proyectiles a la vez",
        },
        PowerupType.HEALTH: {
            "name": "Salud",
            "color": (0, 255, 0),  # Verde
            "duration": 0.0,  # Instantáneo
            "value": 50.0,  # Cantidad de salud
            "description": "Restaura salud inmediatamente",
        },
        PowerupType.SPREAD: {
            "name": "Dispersión",
            "color": (255, 255, 0),  # Amarillo
            "duration": 10.0,
            "value": 3,  # Número de proyectiles en abanico
            "description": "Dispara proyectiles en abanico",
        },
        PowerupType.EXPLOSIVE: {
            "name": "Explosivo",
            "color": (255, 69, 0),  # Rojo-naranja
            "duration": 12.0,
            "value": 2.0,  # Radio de explosión
            "description": "Los proyectiles explotan al impactar",
        },
        PowerupType.SHRAPNEL: {
            "name": "Metralla",
            "color": (105, 105, 105),  # Gris
            "duration": 10.0,
            "value": 5,  # Número de fragmentos
            "description": "Los proyectiles se dividen en fragmentos",
        },
    }

    @classmethod
    def get_config(cls, powerup_type: PowerupType) -> dict:
        """Obtiene la configuración de un tipo de powerup."""
        return cls.POWERUP_CONFIGS.get(powerup_type, {})

    @classmethod
    def get_all_configs(cls) -> dict:
        """Obtiene todas las configuraciones de powerups."""
        return cls.POWERUP_CONFIGS.copy()

    @classmethod
    def get_symbol(cls, powerup_type: PowerupType) -> str:
        """Obtiene el símbolo para el tipo de powerup."""
        symbols = {
            PowerupType.SPEED: "⚡",
            PowerupType.DAMAGE: "⚔",
            PowerupType.SHIELD: "🛡",
            PowerupType.RAPID_FIRE: "🔥",
            PowerupType.DOUBLE_SHOT: "⚡⚡",
            PowerupType.HEALTH: "❤",
            PowerupType.SPREAD: "🎯",
            PowerupType.EXPLOSIVE: "💥",
            PowerupType.SHRAPNEL: "🔫",
        }
        return symbols.get(powerup_type, "?")

    @classmethod
    def get_all_types(cls) -> list:
        """Obtiene todos los tipos de powerups disponibles."""
        return list(PowerupType)
