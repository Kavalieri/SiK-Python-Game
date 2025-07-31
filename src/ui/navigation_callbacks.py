"""
Callbacks de navegación y transiciones de menús.
Módulo especializado extraído de MenuCallbacks para mantener límite de 150 líneas.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.game_state import GameState
    from src.utils.save_manager import SaveManager

logger = logging.getLogger(__name__)


class NavigationCallbacks:
    """
    Gestiona los callbacks de navegación entre menús y escenas.
    """

    def __init__(self, game_state: "GameState", save_manager: "SaveManager"):
        """
        Inicializa el gestor de callbacks de navegación.

        Args:
            game_state: Estado del juego
            save_manager: Gestor de archivos de guardado
        """
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = logger

    def on_new_game(self):
        """Callback para iniciar un nuevo juego."""
        try:
            self.logger.info("Iniciando nuevo juego")
            self.game_state.slot_selection_mode = "new_game"
            self.game_state.set_scene("slot_selection")
        except (AttributeError, ValueError) as e:
            self.logger.error("Error iniciando nuevo juego: %s", str(e))

    def on_continue_game(self):
        """Callback para continuar la última partida guardada."""
        try:
            save_files = self.save_manager.get_save_files_info()

            # Buscar el último guardado con timestamp más reciente
            latest_save = None
            latest_timestamp = 0

            for save_file in save_files:
                if save_file.get("exists", False):
                    timestamp = save_file.get("timestamp", 0)
                    if timestamp > latest_timestamp:
                        latest_timestamp = timestamp
                        latest_save = save_file

            if latest_save:
                self.logger.info(
                    "Continuando desde archivo de guardado %s", latest_save["slot"]
                )

                # Cargar el estado del juego
                game_data = self.save_manager.load_save(latest_save["slot"])
                if game_data:
                    self.game_state.load_state(game_data)
                    self.game_state.set_scene("game")
                else:
                    self.logger.error("Error cargando datos del guardado")
                    self.game_state.set_scene("main_menu")
            else:
                self.logger.warning("No hay guardados para continuar")
                self.game_state.set_scene("slot_selection")

        except (AttributeError, ValueError, KeyError) as e:
            self.logger.error("Error continuando juego: %s", str(e))
            self.game_state.set_scene("main_menu")

    def on_load_game(self):
        """Callback para cargar un juego específico."""
        try:
            self.logger.info("Navegando a selección de guardado")
            self.game_state.slot_selection_mode = "load_game"
            self.game_state.set_scene("slot_selection")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error navegando a carga: %s", str(e))

    def on_options(self):
        """Callback para acceder a opciones."""
        try:
            self.logger.info("Navegando a opciones")
            self.game_state.set_scene("options")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error navegando a opciones: %s", str(e))

    def on_exit(self):
        """Callback para salir del juego."""
        try:
            self.logger.info("Saliendo del juego desde menú")
            self.game_state.quit_game()
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error saliendo del juego: %s", str(e))

    def on_resume_game(self):
        """Callback para reanudar el juego desde pausa."""
        try:
            self.logger.info("Reanudando juego")
            self.game_state.set_scene("game")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error reanudando juego: %s", str(e))

    def on_main_menu(self):
        """Callback para volver al menú principal."""
        try:
            self.logger.info("Volviendo al menú principal")
            self.game_state.set_scene("main_menu")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error volviendo al menú principal: %s", str(e))

    def on_character_selected(self, character_name: str):
        """
        Callback para cuando se selecciona un personaje.

        Args:
            character_name: Nombre del personaje seleccionado
        """
        try:
            self.logger.info("Personaje seleccionado: %s", character_name)

            # Configurar el personaje en el estado del juego
            self.game_state.selected_character = character_name

            # Navegar al juego
            self.game_state.set_scene("game")

        except (AttributeError, ValueError, OSError) as e:
            self.logger.error(
                "Error seleccionando personaje %s: %s", character_name, str(e)
            )

    def on_back_to_main(self):
        """Callback para volver al menú principal desde cualquier lugar."""
        try:
            self.logger.info("Navegando de vuelta al menú principal")
            self.game_state.set_scene("main_menu")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error volviendo al menú principal: %s", str(e))

    def on_back_to_previous(self):
        """Callback para volver a la escena anterior."""
        try:
            # Por simplicidad, volver al menú principal
            # En el futuro se podría implementar un stack de escenas
            self.logger.info("Navegando a escena anterior (menú principal)")
            self.game_state.set_scene("main_menu")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error("Error volviendo a escena anterior: %s", str(e))

    def on_new_game_with_slot(self, slot: int):
        """Callback para nueva partida en slot específico - ir a selección de personajes."""
        try:
            self.logger.info(
                "Nueva partida en slot %d - ir a selección de personajes", slot
            )
            # Establecer el slot activo
            if hasattr(self.game_state, "set_active_slot"):
                self.game_state.set_active_slot(slot)
            # Ir directamente a selección de personajes
            self.game_state.set_scene("character_select")
        except (AttributeError, ValueError, OSError) as e:
            self.logger.error(
                "Error iniciando nueva partida en slot %d: %s", slot, str(e)
            )
