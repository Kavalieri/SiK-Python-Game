"""
MenuWidgetConfig - Configuración de Widgets de Menú
===================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Configuración especializada de widgets para menús.

Responsabilidades:
- Configuración de sliders de volumen
- Selectores de resolución
- Toggles de pantalla completa
- Widgets básicos de configuración
"""

from collections.abc import Callable
from typing import Any

import pygame_menu

from utils.logger import get_logger


class MenuWidgetConfig:
    """
    Configurador especializado de widgets para menús.
    """

    def __init__(self, config_manager=None):
        """
        Inicializa configurador de widgets.

        Args:
            config_manager: Gestor de configuración del juego
        """
        self.config = config_manager
        self.logger = get_logger("SiK_Game")

    def get_resolution_options(self) -> list[str]:
        """Obtiene opciones de resolución disponibles."""
        return ["800x600", "1024x768", "1280x720", "1920x1080"]

    def configure_volume_slider(
        self,
        menu: pygame_menu.Menu,
        label: str,
        default_value: float,
        callback: Callable[[float], None],
    ) -> None:
        """Configura slider de volumen en menú."""
        try:
            menu.add.label(f"Volumen de {label}:", font_size=20)
            menu.add.range_slider(
                label,
                range_values=(0, 100),
                default=int(default_value * 100),
                increment=1,
                onchange=lambda value: callback(value / 100),
                font_size=18,
            )
            menu.add.vertical_margin(10)
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error(
                "Error configurando slider de volumen '%s': %s", label, str(e)
            )

    def configure_resolution_selector(
        self, menu: pygame_menu.Menu, callback: Callable[[str, int], None]
    ) -> None:
        """Configura selector de resolución."""
        try:
            menu.add.label("Resolución:", font_size=20)
            menu.add.selector(
                "Resolución",
                self.get_resolution_options(),
                onchange=callback,
                font_size=18,
            )
            menu.add.vertical_margin(10)
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error configurando selector de resolución: %s", str(e))

    def configure_fullscreen_toggle(
        self,
        menu: pygame_menu.Menu,
        default_value: bool,
        callback: Callable[[bool], None],
    ) -> None:
        """Configura toggle de pantalla completa."""
        try:
            menu.add.toggle_switch(
                "Pantalla Completa", default_value, onchange=callback, font_size=18
            )
            menu.add.vertical_margin(10)
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error configurando toggle pantalla completa: %s", str(e))

    def get_audio_volume_values(self) -> dict[str, float]:
        """Obtiene valores de volumen de audio desde configuración."""
        if not self.config:
            return {"music": 0.7, "sfx": 0.8}
        try:
            audio_config = self.config.get_audio_config()
            volumes = audio_config.get("volúmenes", {})
            return {
                "music": volumes.get("música_fondo", 0.7),
                "sfx": volumes.get("efectos_sonido", 0.8),
            }
        except (AttributeError, KeyError, TypeError) as e:
            self.logger.error("Error obteniendo valores de volumen: %s", str(e))
            return {"music": 0.7, "sfx": 0.8}

    def get_display_settings(self) -> dict[str, Any]:
        """Obtiene configuración de pantalla."""
        if not self.config:
            return {"fullscreen": False, "resolution": "1024x768"}
        try:
            return {
                "fullscreen": self.config.get_fullscreen(),
                "resolution": f"{self.config.get_width()}x{self.config.get_height()}",
            }
        except (AttributeError, TypeError) as e:
            self.logger.error("Error obteniendo configuración de pantalla: %s", str(e))
            return {"fullscreen": False, "resolution": "1024x768"}
