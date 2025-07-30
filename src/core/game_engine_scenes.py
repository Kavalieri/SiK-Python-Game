"""
Game Engine Scenes - Configuración de Escenas y Transiciones
===========================================================

Autor: SiK Team
Fecha: 2024
Descripción: Configuración de escenas del juego y sus transiciones.
"""

from ..utils.logger import get_logger


class GameEngineScenes:
    """Configuración de escenas del juego y transiciones."""

    def __init__(self, core, events):
        """
        Inicializa el configurador de escenas.

        Args:
            core: Instancia de GameEngineCore
            events: Instancia de GameEngineEvents
        """
        self.core = core
        self.events = events
        self.logger = get_logger("SiK_Game")

    def setup_scenes(self):
        """Configura las escenas iniciales del juego y documenta el flujo avanzado de menús y guardado."""
        try:
            from ..scenes.character_select_scene import CharacterSelectScene
            from ..scenes.game_scene_core import GameScene
            from ..scenes.loading_scene import LoadingScene
            from ..scenes.main_menu_scene import MainMenuScene
            from ..scenes.options_scene import OptionsScene
            from ..scenes.pause_scene import PauseScene
            from ..scenes.slot_selection_scene import SlotSelectionScene

            # Crear todas las escenas
            loading_scene = LoadingScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
                self._on_loading_complete,
            )
            main_menu_scene = MainMenuScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
            )
            game_scene = GameScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
            )
            pause_scene = PauseScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
            )
            character_select_scene = CharacterSelectScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
            )
            slot_selection_scene = SlotSelectionScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
            )
            options_scene = OptionsScene(
                self.core.screen,
                self.core.config,
                self.core.game_state,
                self.core.save_manager,
            )

            # Añadir escenas al gestor
            self.core.scene_manager.add_scene("loading", loading_scene)
            self.core.scene_manager.add_scene("main_menu", main_menu_scene)
            self.core.scene_manager.add_scene("game", game_scene)
            self.core.scene_manager.add_scene("pause", pause_scene)
            self.core.scene_manager.add_scene(
                "character_select", character_select_scene
            )
            self.core.scene_manager.add_scene("slot_selection", slot_selection_scene)
            self.core.scene_manager.add_scene("options", options_scene)

            # Configurar callbacks para transiciones entre escenas
            self.setup_scene_transitions()

            # Establecer escena de carga como inicial
            self.core.scene_manager.change_scene("loading")
            self.logger.info(
                "Escenas configuradas correctamente (flujo avanzado de menús y guardado)"
            )
        except RuntimeError as e:
            self.logger.error("Error al configurar escenas: %s", e)
            raise

    def setup_scene_transitions(self):
        """Configura las transiciones entre escenas y documenta la diferenciación de botón Salir y cierre de ventana."""
        try:
            main_menu_scene = self.core.scene_manager.scenes["main_menu"]
            slot_selection_scene = self.core.scene_manager.scenes["slot_selection"]
            options_scene = self.core.scene_manager.scenes["options"]
            character_select_scene = self.core.scene_manager.scenes["character_select"]
            pause_scene = self.core.scene_manager.scenes["pause"]

            # Menú principal - callbacks condensados
            main_callbacks = main_menu_scene.menu_manager.callbacks
            main_callbacks.on_new_game = lambda: self.core.scene_manager.change_scene(
                "slot_selection"
            )
            main_callbacks.on_continue_game = self.events.handle_continue_game
            main_callbacks.on_load_game = lambda: self.core.scene_manager.change_scene(
                "slot_selection"
            )
            main_callbacks.on_options = lambda: self.core.scene_manager.change_scene(
                "options"
            )
            main_callbacks.on_exit = self.events.log_and_quit_menu

            # Selección de slots - callbacks condensados
            slot_callbacks = slot_selection_scene.menu_manager.callbacks
            slot_callbacks.on_select_slot = self.events.handle_slot_selection
            slot_callbacks.on_clear_slot = self.events.handle_clear_slot
            slot_callbacks.on_back_to_main_from_slots = (
                lambda: self.core.scene_manager.change_scene("main_menu")
            )

            # Otros callbacks
            options_scene.menu_manager.callbacks.on_back_to_main = (
                lambda: self.core.scene_manager.change_scene("main_menu")
            )
            character_select_scene.menu_manager.callbacks.on_character_selected = (
                self.events.handle_character_selection
            )

            # Pausa - callbacks condensados
            pause_callbacks = pause_scene.menu_manager.callbacks
            pause_callbacks.on_resume_game = (
                lambda: self.core.scene_manager.change_scene("game")
            )
            pause_callbacks.on_save_game = self.events.handle_save_game
            pause_callbacks.on_main_menu = lambda: self.core.scene_manager.change_scene(
                "main_menu"
            )
            pause_callbacks.on_exit = self.events.log_and_quit_menu

            self.logger.info("Transiciones entre escenas configuradas (flujo avanzado)")
        except RuntimeError as e:
            self.logger.error("Error configurando transiciones: %s", e)

    def _on_loading_complete(self):
        """Callback cuando la carga está completa."""
        self.core.scene_manager.change_scene("main_menu")

    def _quit_game(self):
        """Cierra el juego desde menú."""
        self.core.running = False

    # Métodos delegados eliminados ya que ahora se usan desde events
