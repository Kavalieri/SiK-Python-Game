"""
Game Engine - Motor principal del juego
======================================

Autor: SiK Team
Fecha: 2024
Descripción: Motor principal que gestiona el bucle del juego, renderizado y eventos.
"""

import pygame

from ..ui.menu_manager import MenuManager
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger
from ..utils.save_manager import SaveManager
from .game_state import GameState
from .scene_manager import SceneManager


class GameEngine:
    """
    Motor principal del juego que gestiona el bucle principal, renderizado y eventos.
    """

    def __init__(self, config: ConfigManager):
        """
        Inicializa el motor del juego.

        Args:
                config: Gestor de configuración del juego
        """
        self.logger = get_logger("SiK_Game")
        self.logger.info("[GameEngine] Motor principal inicializado")
        self.config = config
        self.running = False
        self.clock = None
        self.screen = None
        self.game_state = None
        self.scene_manager = None
        self.save_manager = None
        self.menu_manager = None

        self.logger.info("Inicializando motor del juego...")
        self._initialize_pygame()
        self._initialize_components()
        self.logger.info("Motor del juego inicializado correctamente")

    def _initialize_pygame(self):
        """Inicializa Pygame y configura la pantalla."""
        try:
            pygame.init()
            pygame.mixer.init()

            # Configurar pantalla
            screen_width, screen_height = self.config.get_resolution()
            title = self.config.get("game", "title", "SiK Python Game")

            self.screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption(title)

            # Configurar reloj
            fps = self.config.get_fps()
            self.clock = pygame.time.Clock()

            self.logger.info(
                f"Pygame inicializado - Resolución: {screen_width}x{screen_height}, FPS: {fps}"
            )

        except Exception as e:
            self.logger.error(f"Error al inicializar Pygame: {e}")
            raise

    def _initialize_components(self):
        """Inicializa los componentes principales del juego."""
        try:
            # Inicializar estado del juego
            self.game_state = GameState()

            # Inicializar gestor de guardado
            self.save_manager = SaveManager(self.config)

            # Inicializar gestor de menús
            self.menu_manager = MenuManager(
                self.screen, self.config, self.game_state, self.save_manager
            )

            # Inicializar gestor de escenas
            self.scene_manager = SceneManager(self.screen, self.config)

            # Configurar referencias entre componentes
            self.game_state.scene_manager = self.scene_manager

            # Configurar escenas iniciales
            self._setup_scenes()

            self.logger.info("Componentes del juego inicializados")

        except Exception as e:
            self.logger.error(f"Error al inicializar componentes: {e}")
            raise

    def _setup_scenes(self):
        """Configura las escenas iniciales del juego y documenta el flujo avanzado de menús y guardado."""
        try:
            from ..scenes.character_select_scene import CharacterSelectScene
            from ..scenes.game_scene import GameScene
            from ..scenes.loading_scene import LoadingScene
            from ..scenes.main_menu_scene import MainMenuScene
            from ..scenes.options_scene import OptionsScene
            from ..scenes.pause_scene import PauseScene
            from ..scenes.slot_selection_scene import SlotSelectionScene

            # Crear todas las escenas
            loading_scene = LoadingScene(
                self.screen,
                self.config,
                self.game_state,
                self.save_manager,
                self._on_loading_complete,
            )
            main_menu_scene = MainMenuScene(
                self.screen, self.config, self.game_state, self.save_manager
            )
            game_scene = GameScene(
                self.screen, self.config, self.game_state, self.save_manager
            )
            pause_scene = PauseScene(
                self.screen, self.config, self.game_state, self.save_manager
            )
            character_select_scene = CharacterSelectScene(
                self.screen, self.config, self.game_state, self.save_manager
            )
            slot_selection_scene = SlotSelectionScene(
                self.screen, self.config, self.game_state, self.save_manager
            )
            options_scene = OptionsScene(
                self.screen, self.config, self.game_state, self.save_manager
            )

            # Añadir escenas al gestor
            self.scene_manager.add_scene("loading", loading_scene)
            self.scene_manager.add_scene("main_menu", main_menu_scene)
            self.scene_manager.add_scene("game", game_scene)
            self.scene_manager.add_scene("pause", pause_scene)
            self.scene_manager.add_scene("character_select", character_select_scene)
            self.scene_manager.add_scene("slot_selection", slot_selection_scene)
            self.scene_manager.add_scene("options", options_scene)

            # Configurar callbacks para transiciones entre escenas
            self._setup_scene_transitions()

            # Establecer escena de carga como inicial
            self.scene_manager.change_scene("loading")
            self.logger.info(
                "Escenas configuradas correctamente (flujo avanzado de menús y guardado)"
            )
        except Exception as e:
            self.logger.error(f"Error al configurar escenas: {e}")
            raise

    def _setup_scene_transitions(self):
        """Configura las transiciones entre escenas y documenta la diferenciación de botón Salir y cierre de ventana."""
        try:
            main_menu_scene = self.scene_manager.scenes["main_menu"]
            slot_selection_scene = self.scene_manager.scenes["slot_selection"]
            options_scene = self.scene_manager.scenes["options"]
            character_select_scene = self.scene_manager.scenes["character_select"]
            pause_scene = self.scene_manager.scenes["pause"]

            # Menú principal
            main_menu_scene.menu_manager.callbacks.on_new_game = (
                lambda: self.scene_manager.change_scene("slot_selection")
            )
            main_menu_scene.menu_manager.callbacks.on_continue_game = (
                lambda: self._handle_continue_game()
            )
            main_menu_scene.menu_manager.callbacks.on_load_game = (
                lambda: self.scene_manager.change_scene("slot_selection")
            )
            main_menu_scene.menu_manager.callbacks.on_options = (
                lambda: self.scene_manager.change_scene("options")
            )
            main_menu_scene.menu_manager.callbacks.on_exit = (
                lambda: self._log_and_quit_menu()
            )

            # Selección de slots
            slot_selection_scene.menu_manager.callbacks.on_select_slot = (
                lambda slot: self._handle_slot_selection(slot)
            )
            slot_selection_scene.menu_manager.callbacks.on_clear_slot = (
                lambda slot: self._handle_clear_slot(slot)
            )
            slot_selection_scene.menu_manager.callbacks.on_back_to_main_from_slots = (
                lambda: self.scene_manager.change_scene("main_menu")
            )

            # Opciones
            options_scene.menu_manager.callbacks.on_back_to_main = (
                lambda: self.scene_manager.change_scene("main_menu")
            )

            # Selección de personaje
            character_select_scene.menu_manager.callbacks.on_character_selected = (
                lambda char: self._handle_character_selection(char)
            )

            # Pausa
            pause_scene.menu_manager.callbacks.on_resume_game = (
                lambda: self.scene_manager.change_scene("game")
            )
            pause_scene.menu_manager.callbacks.on_save_game = (
                lambda: self._handle_save_game()
            )
            pause_scene.menu_manager.callbacks.on_main_menu = (
                lambda: self.scene_manager.change_scene("main_menu")
            )
            pause_scene.menu_manager.callbacks.on_exit = (
                lambda: self._log_and_quit_menu()
            )

            self.logger.info("Transiciones entre escenas configuradas (flujo avanzado)")
        except Exception as e:
            self.logger.error(f"Error configurando transiciones: {e}")

    def _quit_game(self):
        """Método para salir del juego."""
        self.logger.info("[GameEngine] Saliendo del juego...")
        self.running = False

    def _on_loading_complete(self):
        """Callback cuando termina la carga."""
        self.logger.info("Carga completada, cambiando a menú principal")
        self.scene_manager.change_scene("main_menu")

    def run(self):
        """Ejecuta el bucle principal del juego."""
        self.running = True
        self.logger.info("[GameEngine] Iniciando bucle principal del juego...")

        try:
            while self.running:
                self._handle_events()
                self._update()
                self._render()
                self.clock.tick(self.config.get_fps())

        except Exception as e:
            self.logger.error(f"Error en el bucle principal: {e}")
            raise
        finally:
            self._cleanup()

    def _handle_events(self):
        """Procesa todos los eventos de Pygame."""
        for event in pygame.event.get():
            self.logger.info(f"[GameEngine] Evento global: {event.type} - {event}")
            # Logging detallado de eventos
            self._log_event(event)

            if event.type == pygame.QUIT:
                self.logger.info("Evento QUIT detectado - Cerrando juego")
                self.running = False
            else:
                self.scene_manager.handle_event(event)

    def _log_event(self, event: pygame.event.Event):
        """Registra eventos de Pygame para debug."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.logger.debug(
                f"MOUSE CLICK: {event.button} en ({event.pos[0]}, {event.pos[1]})"
            )
        elif event.type == pygame.MOUSEBUTTONUP:
            self.logger.debug(
                f"MOUSE RELEASE: {event.button} en ({event.pos[0]}, {event.pos[1]})"
            )
        elif event.type == pygame.MOUSEMOTION:
            # Solo loggear movimiento cada 10 frames para no saturar
            if hasattr(self, "_mouse_log_counter"):
                self._mouse_log_counter += 1
            else:
                self._mouse_log_counter = 0

            if self._mouse_log_counter % 10 == 0:
                self.logger.debug(f"MOUSE MOTION: ({event.pos[0]}, {event.pos[1]})")
        elif event.type == pygame.KEYDOWN:
            self.logger.debug(
                f"KEY DOWN: {pygame.key.name(event.key)} (scancode: {event.scancode})"
            )
        elif event.type == pygame.KEYUP:
            self.logger.debug(
                f"KEY UP: {pygame.key.name(event.key)} (scancode: {event.scancode})"
            )
        elif event.type == pygame.MOUSEWHEEL:
            self.logger.debug(f"MOUSE WHEEL: {event.y} en ({event.x}, {event.y})")

    def _update(self):
        """Actualiza la lógica del juego."""
        self.scene_manager.update()

    def _render(self):
        """Renderiza el juego en pantalla."""
        self.scene_manager.render()
        pygame.display.flip()

    def _cleanup(self):
        """Limpia recursos y cierra Pygame."""
        self.logger.info("Limpiando recursos del juego...")
        pygame.quit()
        self.logger.info("Juego cerrado correctamente")

    def _log_and_quit_menu(self):
        """Diferencia el cierre por botón Salir del menú y el cierre de ventana."""
        self.logger.info(
            "[Menu] Botón Salir pulsado - Cierre solicitado por el usuario desde el menú"
        )
        self._quit_game()

    def _handle_continue_game(self):
        """Maneja la acción de continuar juego desde el último slot activo."""
        last_save = self.save_manager.get_last_save_file()
        if last_save:
            self.logger.info(f"[GameEngine] Continuando juego desde: {last_save}")
            self.save_manager.load_save(last_save, self.game_state)
            self.scene_manager.change_scene("game")
        else:
            self.logger.warning("[GameEngine] No hay partida guardada para continuar")

    def _handle_slot_selection(self, slot: int):
        """Maneja la selección de un slot de guardado."""
        self.logger.info(f"[GameEngine] Slot seleccionado: {slot}")
        # Lógica para activar el slot y navegar a selección de personaje
        self.save_manager.set_active_slot(slot)
        self.scene_manager.change_scene("character_select")

    def _handle_clear_slot(self, slot: int):
        """Maneja el vaciado de un slot de guardado."""
        self.logger.info(f"[GameEngine] Vaciar slot: {slot}")
        self.save_manager.clear_slot(slot)
        self.scene_manager.change_scene("slot_selection")

    def _handle_character_selection(self, character: str):
        """Maneja la selección de personaje tras elegir slot."""
        self.logger.info(f"[GameEngine] Personaje seleccionado: {character}")
        self.game_state.selected_character = character
        self.scene_manager.change_scene("game")

    def _handle_save_game(self):
        """Maneja el guardado manual desde el menú de pausa."""
        self.logger.info("[GameEngine] Guardando partida manualmente en slot activo")
        self.save_manager.save_game()
