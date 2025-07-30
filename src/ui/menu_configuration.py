"""
Menu Configuration - Configuración de Widgets y Opciones
======================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo para configuración de widgets y opciones de menús.
"""

from typing import Any, Callable, Dict, List

import pygame_menu

from ..utils.logger import get_logger


class MenuConfiguration:
    """
    Gestor de configuración de widgets y opciones para menús.
    """

    def __init__(self, config_manager=None, save_manager=None):
        """
        Inicializa configuración de menús.

        Args:
            config_manager: Gestor de configuración del juego
            save_manager: Gestor de guardado
        """
        self.config = config_manager
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")

    def get_resolution_options(self) -> List[str]:
        """Obtiene opciones de resolución disponibles."""
        return ["800x600", "1024x768", "1280x720", "1920x1080"]

    def get_character_options(self) -> List[Dict[str, str]]:
        """Obtiene opciones de personajes disponibles."""
        return [
            {"name": "Guerrero", "id": "guerrero"},
            {"name": "Arquera", "id": "adventureguirl"},
            {"name": "Robot", "id": "robot"},
        ]

    def get_upgrade_options(self) -> List[Dict[str, Any]]:
        """Obtiene opciones de mejoras disponibles."""
        return [
            {"name": "Velocidad", "cost": 1},
            {"name": "Daño", "cost": 1},
            {"name": "Vida", "cost": 1},
            {"name": "Escudo", "cost": 1},
        ]

    def get_inventory_categories(self) -> List[str]:
        """Obtiene categorías de inventario."""
        return ["Armas", "Armaduras", "Accesorios", "Consumibles"]

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

    def add_save_slot_buttons(
        self, menu: pygame_menu.Menu, callback: Callable[[int], None]
    ) -> None:
        """Añade botones de slots de guardado."""
        try:
            if self.save_manager:
                save_infos = self.save_manager.get_save_files_info()
                for i, info in enumerate(save_infos, 1):
                    if info["exists"]:
                        label = (
                            f"Slot {i} | {info.get('player_name', 'Sin nombre')} | "
                            f"Nivel: {info.get('level', 1)} | Puntos: {info.get('score', 0)}"
                        )
                    else:
                        label = f"Slot {i} | VACÍO"
                    menu.add.button(label, lambda slot=i: callback(slot), font_size=20)
                    menu.add.vertical_margin(5)
            else:
                self.logger.warning("SaveManager no disponible para slots de guardado")
        except (AttributeError, KeyError, ValueError) as e:
            self.logger.error("Error añadiendo botones de slot de guardado: %s", str(e))

    def get_audio_volume_values(self) -> Dict[str, float]:
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

    def get_display_settings(self) -> Dict[str, Any]:
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
