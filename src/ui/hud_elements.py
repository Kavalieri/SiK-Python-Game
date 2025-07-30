"""
HUD Elements - Elementos y Configuración del HUD
===============================================

Autor: SiK Team
Fecha: 2024
Descripción: Elementos UI, configuración y estructuras de datos para el sistema HUD.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

from ..entities.powerup import PowerupType


@dataclass
class HUDElement:
    """Elemento del HUD con su posición y configuración."""

    name: str
    x: int
    y: int
    width: int
    height: int
    visible: bool = True


class HUDConfiguration:
    """Configuración centralizada del HUD."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Paleta de colores del HUD
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 165, 0),
            "purple": (128, 0, 128),
            "gray": (128, 128, 128),
            "dark_gray": (64, 64, 64),
            "light_gray": (192, 192, 192),
        }

        # Configuración de fuentes
        self.font_sizes = {"small": 14, "medium": 18, "large": 24, "huge": 32}

    def get_hud_elements(self) -> Dict[str, HUDElement]:
        """Inicializa y retorna todos los elementos del HUD con sus posiciones."""
        elements = {}

        # Barra superior
        elements["top_bar"] = HUDElement("top_bar", 0, 0, self.screen_width, 60)

        # Información del jugador (izquierda)
        elements["player_info"] = HUDElement("player_info", 10, 10, 200, 40)
        elements["health_bar"] = HUDElement("health_bar", 10, 50, 200, 20)
        elements["shield_bar"] = HUDElement("shield_bar", 10, 75, 200, 15)

        # Información del juego (centro superior)
        elements["game_info"] = HUDElement(
            "game_info", self.screen_width // 2 - 150, 10, 300, 40
        )
        elements["level_info"] = HUDElement(
            "level_info", self.screen_width // 2 - 100, 50, 200, 20
        )
        elements["time_info"] = HUDElement(
            "time_info", self.screen_width // 2 - 100, 75, 200, 15
        )

        # Información del score (derecha)
        elements["score_info"] = HUDElement(
            "score_info", self.screen_width - 210, 10, 200, 40
        )
        elements["combo_info"] = HUDElement(
            "combo_info", self.screen_width - 210, 50, 200, 20
        )

        # Mini-mapa (derecha inferior)
        elements["minimap"] = HUDElement(
            "minimap", self.screen_width - 160, 100, 150, 150
        )

        # Inventario/powerups (izquierda inferior)
        elements["inventory"] = HUDElement("inventory", 10, 100, 150, 100)

        # Barra de progreso de nivel (inferior)
        elements["level_progress"] = HUDElement(
            "level_progress", 200, self.screen_height - 30, self.screen_width - 400, 20
        )

        # Elementos de overlay
        elements["crosshair"] = HUDElement(
            "crosshair",
            self.screen_width // 2 - 10,
            self.screen_height // 2 - 10,
            20,
            20,
        )

        return elements


class HUDEffectUtils:
    """Utilidades para efectos y powerups en el HUD."""

    @staticmethod
    def get_effect_name(effect_type: PowerupType) -> str:
        """Obtiene el nombre legible del efecto."""
        names = {
            PowerupType.SPEED: "Velocidad",
            PowerupType.DAMAGE: "Daño",
            PowerupType.SHIELD: "Escudo",
            PowerupType.RAPID_FIRE: "Disparo Rápido",
            PowerupType.DOUBLE_SHOT: "Doble Disparo",
            PowerupType.HEALTH: "Vida",
        }
        return names.get(effect_type, effect_type.value)

    @staticmethod
    def get_effect_color(effect_type: PowerupType) -> Tuple[int, int, int]:
        """Obtiene el color para el tipo de efecto."""
        colors = {
            PowerupType.SPEED: (0, 255, 0),  # Verde
            PowerupType.DAMAGE: (255, 0, 0),  # Rojo
            PowerupType.SHIELD: (0, 0, 255),  # Azul
            PowerupType.RAPID_FIRE: (255, 255, 0),  # Amarillo
            PowerupType.DOUBLE_SHOT: (255, 0, 255),  # Magenta
            PowerupType.HEALTH: (255, 165, 0),  # Naranja
        }
        return colors.get(effect_type, (255, 255, 255))
