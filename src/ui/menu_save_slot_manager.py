"""
MenuSaveSlotManager - Gestión de Slots de Guardado en Menús
==========================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Gestión especializada de slots de guardado para menús.

Responsabilidades:
- Botones de slots de guardado dinámicos
- Gestión de partidas por slot
- Botones de inicio de partida
- Callbacks especializados
"""

from collections.abc import Callable

import pygame_menu

from utils.logger import get_logger


class MenuSaveSlotManager:
    """
    Gestor especializado de slots de guardado para menús.
    """

    def __init__(self, save_manager=None, game_state=None):
        """
        Inicializa gestor de slots de guardado.

        Args:
            save_manager: Gestor de guardado
            game_state: Estado del juego
        """
        self.save_manager = save_manager
        self.game_state = game_state
        self.logger = get_logger("SiK_Game")

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
