"""
Callbacks de guardado y gestión de slots.
Módulo especializado extraído de MenuCallbacks para mantener límite de 150 líneas.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game_state import GameState
    from utils.save_manager import SaveManager

logger = logging.getLogger(__name__)


class SaveCallbacks:
    """
    Gestiona los callbacks de guardado y slots del juego.
    """

    def __init__(self, game_state: "GameState", save_manager: "SaveManager"):
        """
        Inicializa el gestor de callbacks de guardado.

        Args:
            game_state: Estado del juego
            save_manager: Gestor de archivos de guardado
        """
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = logger

    def on_save_game(self):
        """Callback para guardar el juego actual."""
        self.logger.info("Guardando juego")
        self._handle_engine_action("_handle_save_game")

    def _handle_engine_action(self, action_name: str, *args):
        """Método helper para acciones del motor de juego."""
        try:
            if (
                hasattr(self.game_state, "scene_manager")
                and self.game_state.scene_manager
            ):
                if hasattr(self.game_state.scene_manager, "game_engine"):
                    engine = self.game_state.scene_manager.game_engine
                    method = getattr(engine, action_name, None)
                    if method:
                        return method(*args)
                self.logger.warning("Método %s no disponible en motor", action_name)
            else:
                self.logger.warning("Scene manager no disponible")
        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error en %s: %s", action_name, str(e))

    def on_select_slot(self, slot: int):
        """Callback para seleccionar un slot de guardado."""
        self.logger.info("Seleccionar Slot %d", slot)
        self._handle_engine_action("_handle_slot_selection", slot)

    def on_clear_slot(self, slot: int):
        """Callback para vaciar un slot de guardado."""
        self.logger.info("Vaciar Slot %d", slot)
        self._handle_engine_action("_handle_clear_slot", slot)

    def on_back_to_main_from_slots(self):
        """Callback para volver al menú principal desde selección de slots."""
        try:
            self.logger.info("Volver desde Slots")
            if (
                hasattr(self.game_state, "scene_manager")
                and self.game_state.scene_manager
            ):
                self.game_state.scene_manager.change_scene("main_menu")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error volviendo al menú: %s", str(e))

    def on_select_save_file(self, file_number: int):
        """Callback para seleccionar archivo de guardado."""
        try:
            self.logger.info("Seleccionando archivo de guardado: %d", file_number)
            info_list = self.save_manager.get_save_files_info()

            if file_number < 1 or file_number > len(info_list):
                self.logger.error("Número de archivo inválido: %d", file_number)
                self._show_save_menu_feedback("Número de archivo inválido.")
                return

            info = info_list[file_number - 1]
            if not info.get("exists", False):
                self._show_save_menu_feedback("Slot vacío. No se puede continuar.")
                self.logger.warning("Slot vacío. No se puede continuar.")
                self._refresh_save_menu()
                return

            self.save_manager.load_save(file_number)
            self.game_state.set_scene("game")
            self.logger.info("Archivo de guardado %d cargado", file_number)
            self._show_save_menu_feedback("")
            self._refresh_save_menu()

        except (IndexError, KeyError, AttributeError, ValueError, OSError) as e:
            self._show_save_menu_feedback(f"Error cargando slot: {e}")
            self.logger.error(
                "Error cargando archivo de guardado %d: %s", file_number, str(e)
            )
            self._refresh_save_menu()

    def on_new_save(self):
        """Callback para crear nuevo archivo de guardado."""
        try:
            save_files_info = self.save_manager.get_save_files_info()
            for i, info in enumerate(save_files_info, 1):
                if not info.get("exists", False):
                    self.save_manager.create_new_save(i)
                    self.logger.info("Nuevo guardado creado en slot %d", i)
                    self._show_save_menu_feedback(f"Nuevo guardado en slot {i}")
                    return
            self.logger.warning("No hay slots vacíos")
            self._show_save_menu_feedback("No hay slots vacíos.")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error creando guardado: %s", str(e))

    def on_delete_save(self):
        """Callback para eliminar archivo de guardado."""
        try:
            save_files_info = self.save_manager.get_save_files_info()
            for i, info in enumerate(save_files_info, 1):
                if info.get("exists", False):
                    self.save_manager.delete_save(i)
                    self.logger.info("Guardado eliminado en slot %d", i)
                    self._show_save_menu_feedback(f"Eliminado slot {i}")
                    return
            self.logger.warning("No hay guardados para eliminar")
            self._show_save_menu_feedback("No hay guardados para eliminar.")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error eliminando guardado: %s", str(e))

    def _show_save_menu_feedback(self, msg: str):
        """Muestra mensaje de feedback en el menú de guardado."""
        try:
            # Implementación simplificada - en el futuro se podría mejorar
            self.logger.info("Feedback: %s", msg)
        except (AttributeError, ValueError):
            pass  # Evitar errores en feedback

    def _refresh_save_menu(self):
        """Actualiza el menú de guardado."""
        try:
            # Implementación simplificada - en el futuro se podría mejorar
            self.logger.debug("Refrescando menú de guardado")
        except (AttributeError, ValueError):
            pass  # Evitar errores en refresh

    def get_save_callbacks(self) -> dict:
        """
        Obtiene todos los callbacks de guardado disponibles.

        Returns:
            Diccionario con callbacks de guardado
        """
        return {
            "save_game": self.on_save_game,
            "select_slot": self.on_select_slot,
            "clear_slot": self.on_clear_slot,
            "back_to_main_from_slots": self.on_back_to_main_from_slots,
            "select_save_file": self.on_select_save_file,
            "new_save": self.on_new_save,
            "delete_save": self.on_delete_save,
        }
