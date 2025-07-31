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

    def __init__(self, config_manager=None, save_manager=None, game_state=None):
        """
        Inicializa configuración de menús.

        Args:
            config_manager: Gestor de configuración del juego
            save_manager: Gestor de guardado
            game_state: Estado del juego
        """
        self.config = config_manager
        self.save_manager = save_manager
        self.game_state = game_state
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
        """Añade botones de slots de guardado con modo dinámico."""
        try:
            # Obtener modo de selección desde game_state
            mode = getattr(self.game_state, "slot_selection_mode", "load_game")

            if mode == "new_game":
                menu.add.label("Selecciona slot para NUEVO JUEGO:", font_size=18)
            else:
                menu.add.label("Selecciona slot para CARGAR:", font_size=18)
            menu.add.vertical_margin(10)

            if self.save_manager:
                save_infos = self.save_manager.get_save_files_info()
                for i, info in enumerate(save_infos, 1):
                    if info["exists"]:
                        if mode == "new_game":
                            label = f"Slot {i} | SOBRESCRIBIR | {info.get('player_name', 'Sin nombre')}"
                        else:
                            label = (
                                f"Slot {i} | {info.get('player_name', 'Sin nombre')} | "
                                f"Nivel: {info.get('level', 1)} | Puntos: {info.get('score', 0)}"
                            )
                    else:
                        if mode == "new_game":
                            label = f"Slot {i} | CREAR NUEVA PARTIDA"
                        else:
                            label = f"Slot {i} | VACÍO - No disponible"

                    # Solo crear botón si es apropiado para el modo
                    if mode == "new_game" or (mode == "load_game" and info["exists"]):
                        menu.add.button(
                            label, lambda slot=i: callback(slot), font_size=20
                        )
                    else:
                        # Slot vacío en modo cargar - solo mostrar como label
                        menu.add.label(label, font_size=16)
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

    def add_slot_management_buttons(self, menu, callbacks) -> None:
        """Añade botones de gestión de partidas por slot."""
        try:
            if self.save_manager:
                save_infos = self.save_manager.get_save_files_info()
                for i, info in enumerate(save_infos, 1):
                    # Título del slot
                    if info["exists"]:
                        slot_title = f"--- SLOT {i}: {info.get('player_name', 'Sin nombre')} (Nivel {info.get('level', 1)}) ---"
                    else:
                        slot_title = f"--- SLOT {i}: VACÍO ---"

                    menu.add.label(slot_title, font_size=18)
                    menu.add.vertical_margin(5)

                    # Botones para cada slot
                    if info["exists"]:
                        # Slot con datos: Continuar + Nuevo + Eliminar
                        menu.add.button(
                            f"Continuar Slot {i}",
                            lambda slot=i: callbacks.on_continue_slot(slot),
                            font_size=16,
                        )
                        menu.add.button(
                            f"Nueva Partida en Slot {i}",
                            lambda slot=i: callbacks.on_new_game_slot(slot),
                            font_size=16,
                        )
                        menu.add.button(
                            f"Eliminar Slot {i}",
                            lambda slot=i: callbacks.on_clear_slot(slot),
                            font_size=16,
                        )
                    else:
                        # Slot vacío: Solo Nueva Partida
                        menu.add.button(
                            f"Nueva Partida en Slot {i}",
                            lambda slot=i: callbacks.on_new_game_slot(slot),
                            font_size=16,
                        )

                    menu.add.vertical_margin(15)  # Separación entre slots
            else:
                self.logger.warning(
                    "SaveManager no disponible para gestión de partidas"
                )
        except (AttributeError, KeyError, ValueError) as e:
            self.logger.error(
                "Error añadiendo botones de gestión de partidas: %s", str(e)
            )

    def add_start_game_slot_buttons(self, menu, callbacks) -> None:
        """Añade botones simples para iniciar partidas por slot."""
        try:
            if self.save_manager:
                saves_info = self.save_manager.get_save_files_info()
                for i, info in enumerate(saves_info, 1):
                    # Título del slot
                    if info["exists"]:
                        slot_title = f"--- SLOT {i}: {info.get('player_name', 'Sin nombre')} (Nivel {info.get('level', 1)}) ---"
                        menu.add.label(slot_title, font_size=16)
                        menu.add.vertical_margin(5)

                        # Botón para cargar partida existente
                        menu.add.button(
                            "CARGAR PARTIDA",
                            self._create_continue_callback(callbacks, i),
                            font_size=18,
                        )
                        menu.add.vertical_margin(5)

                        # Botón para nueva partida (sobreescribir)
                        menu.add.button(
                            "NUEVA PARTIDA (Sobreescribir)",
                            self._create_new_game_callback(callbacks, i),
                            font_size=16,
                        )
                    else:
                        # Slot vacío
                        slot_title = f"--- SLOT {i}: VACÍO ---"
                        menu.add.label(slot_title, font_size=16)
                        menu.add.vertical_margin(5)

                        # Solo botón para nueva partida
                        menu.add.button(
                            "NUEVA PARTIDA",
                            self._create_new_game_callback(callbacks, i),
                            font_size=18,
                        )

                    menu.add.vertical_margin(15)  # Separación entre slots
            else:
                self.logger.warning("SaveManager no disponible para iniciar partidas")
        except (AttributeError, KeyError, ValueError) as e:
            self.logger.error(
                "Error añadiendo botones de inicio de partida: %s", str(e)
            )

    def _create_continue_callback(self, callbacks, slot):
        """Crea callback para continuar partida específica."""

        def continue_callback():
            callbacks.on_continue_slot(slot)

        return continue_callback

    def _create_new_game_callback(self, callbacks, slot):
        """Crea callback para nueva partida específica."""

        def new_game_callback():
            callbacks.on_new_game_slot(slot)

        return new_game_callback
