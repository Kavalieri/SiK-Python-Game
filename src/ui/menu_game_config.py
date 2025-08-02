"""
MenuGameConfig - Configuración de Elementos de Juego en Menús
=============================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Configuración especializada de elementos de juego para menús.

Responsabilidades:
- Botones de selección de personajes
- Botones de mejoras/upgrades
- Opciones de inventario
- Configuración de elementos de gameplay
"""

from collections.abc import Callable
from typing import Any

import pygame_menu

from ..utils.logger import get_logger


class MenuGameConfig:
    """
    Configurador especializado de elementos de juego para menús.
    """

    def __init__(self):
        """Inicializa configurador de elementos de juego."""
        self.logger = get_logger("SiK_Game")

    def get_character_options(self) -> list[dict[str, str]]:
        """Obtiene opciones de personajes disponibles."""
        return [
            {"name": "Guerrero", "id": "guerrero"},
            {"name": "Arquera", "id": "adventureguirl"},
            {"name": "Robot", "id": "robot"},
        ]

    def get_upgrade_options(self) -> list[dict[str, Any]]:
        """Obtiene opciones de mejoras disponibles."""
        return [
            {"name": "Velocidad", "cost": 1},
            {"name": "Daño", "cost": 1},
            {"name": "Vida", "cost": 1},
            {"name": "Escudo", "cost": 1},
        ]

    def get_inventory_categories(self) -> list[str]:
        """Obtiene categorías de inventario."""
        return ["Armas", "Armaduras", "Accesorios", "Consumibles"]

    def add_character_buttons(
        self, menu: pygame_menu.Menu, callback: Callable[[str], None]
    ) -> None:
        """Añade botones de selección de personaje."""
        try:
            for char in self.get_character_options():
                menu.add.button(
                    char["name"],
                    lambda char_id=char["id"]: callback(char_id),
                    font_size=20,
                )
                menu.add.vertical_margin(5)
        except (AttributeError, KeyError, TypeError) as e:
            self.logger.error("Error añadiendo botones de personaje: %s", str(e))

    def add_upgrade_buttons(
        self, menu: pygame_menu.Menu, callback: Callable[[str], None]
    ) -> None:
        """Añade botones de mejoras."""
        try:
            for upgrade in self.get_upgrade_options():
                button_text = f"Mejorar {upgrade['name']} ({upgrade['cost']} punto)"
                menu.add.button(
                    button_text,
                    lambda ut=upgrade["name"].lower(): callback(ut),
                    font_size=20,
                )
                menu.add.vertical_margin(5)
        except (AttributeError, KeyError, TypeError) as e:
            self.logger.error("Error añadiendo botones de mejora: %s", str(e))
