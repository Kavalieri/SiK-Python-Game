"""
Main Menu Scene - Escena del Menú Principal
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Escena del menú principal del juego.
"""

import logging
import sys

import pygame
import pygame.constants as pg_constants  # pylint: disable=no-member
import pygame_gui

from ..core.scene_manager import Scene
from ..ui.menu_manager import MenuManager
from ..utils.config_manager import ConfigManager


class MainMenuScene(Scene):
    """
    Escena del menú principal del juego.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        """
        Inicializa la escena del menú principal.

        Args:
                screen: Superficie de Pygame donde renderizar
                config: Configuración del juego
                game_state: Estado del juego
                save_manager: Gestor de guardado
        """
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = logging.getLogger(__name__)

        # Inicializar pygame-gui
        self.ui_manager = pygame_gui.UIManager(screen.get_size())
        self.setup_pygame_gui_elements()

        # Inicializar menú
        self.menu_manager = MenuManager(screen, config, game_state, save_manager)
        self.menu_manager.show_menu("main")

        # Configurar callbacks
        self._configurar_callbacks()

        self.logger.info("Escena del menú principal inicializada")

    def _configurar_callbacks(self):
        """
        Configura los callbacks del menú principal.
        """
        self.menu_manager.add_callback("new_game", self._on_new_game)
        self.menu_manager.add_callback("continue_game", self._on_continue_game)
        self.menu_manager.add_callback("load_game", self._on_load_game)
        self.menu_manager.add_callback("options", self._on_options)
        self.menu_manager.add_callback("exit", self._on_exit)

    def handle_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.

        Args:
            event: Evento de Pygame a procesar.
        """
        self.logger.debug("[MainMenuScene] Evento recibido: %s - %s", event.type, event)

        # Procesar eventos de pygame-gui primero
        self.ui_manager.process_events(event)

        # Manejar eventos de botones pygame-gui
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.new_game_button:
                    self._on_new_game()
                elif event.ui_element == self.continue_button:
                    self._on_continue_game()
                elif event.ui_element == self.options_button:
                    self._on_options()
                elif event.ui_element == self.exit_button:
                    self._on_exit()

        # Procesar eventos de menú aquí
        if event.type == pg_constants.KEYDOWN:  # pylint: disable=c-extension-no-member
            self.logger.info("[MainMenuScene] Tecla pulsada: %s", event.key)
        elif event.type == pg_constants.MOUSEBUTTONDOWN:  # pylint: disable=c-extension-no-member
            self.logger.info(
                "[MainMenuScene] Click ratón: %s en %s", event.button, event.pos
            )
        self.menu_manager.update([event])

    def setup_pygame_gui_elements(self):
        """Configura los elementos de la interfaz con pygame-gui"""
        screen_size = self.screen.get_size()

        # Botón principal mejorado
        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(screen_size[0] // 2 - 100, 200, 200, 50),
            text="Nuevo Juego",
            manager=self.ui_manager,
        )

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(screen_size[0] // 2 - 100, 270, 200, 50),
            text="Continuar",
            manager=self.ui_manager,
        )

        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(screen_size[0] // 2 - 100, 340, 200, 50),
            text="Opciones",
            manager=self.ui_manager,
        )

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(screen_size[0] // 2 - 100, 410, 200, 50),
            text="Salir",
            manager=self.ui_manager,
        )

    def update(self):
        """
        Actualiza la lógica de la escena.
        """
        # Actualizar pygame-gui
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        self.ui_manager.update(time_delta)

        # Método vacío, pero necesario para la estructura.
        return

    def render(self):
        """Renderiza la escena."""
        # Fondo negro
        self.screen.fill((0, 0, 0))

        # Comentar el menú tradicional para evitar superposición
        # self.menu_manager.render()

        # Solo renderizar elementos pygame-gui
        self.ui_manager.draw_ui(self.screen)

    def _on_new_game(self):
        """Callback para nuevo juego."""
        self.logger.info(
            "[MainMenuScene] Acción: Nuevo Juego - navegando a selección de personaje"
        )
        try:
            # Usar el sistema de escenas apropiado
            if hasattr(self, "game_state") and self.game_state:
                self.game_state.set_scene("character_select")
            else:
                self.logger.error("game_state no disponible en MainMenuScene")
        except (AttributeError, ValueError, RuntimeError) as e:
            self.logger.error("Error iniciando nuevo juego: %s", e)

    def _on_continue_game(self):
        """Callback para continuar juego."""
        self.logger.info(
            "[MainMenuScene] Acción: Continuar Juego - navegando a selección de slot"
        )
        try:
            # Usar el sistema de escenas apropiado
            if hasattr(self, "game_state") and self.game_state:
                self.game_state.set_scene("slot_selection")
            else:
                self.logger.error("game_state no disponible en MainMenuScene")
        except (AttributeError, ValueError, RuntimeError) as e:
            self.logger.error("Error continuando juego: %s", e)

    def _on_load_game(self):
        """Callback para cargar partida."""
        self.logger.info(
            "[MainMenuScene] Acción: Cargar Juego - navegando a selección de slot"
        )
        try:
            # Usar el sistema de escenas apropiado
            if hasattr(self, "game_state") and self.game_state:
                self.game_state.set_scene("slot_selection")
            else:
                self.logger.error("game_state no disponible en MainMenuScene")
        except (AttributeError, ValueError, RuntimeError) as e:
            self.logger.error("Error cargando juego: %s", e)

    def _on_options(self):
        """Callback para opciones."""
        self.logger.info("[MainMenuScene] Acción: Opciones - navegando a opciones")
        try:
            # Usar el sistema de escenas apropiado
            if hasattr(self, "game_state") and self.game_state:
                self.game_state.set_scene("options")
            else:
                self.logger.error("game_state no disponible en MainMenuScene")
        except (AttributeError, ValueError, RuntimeError) as e:
            self.logger.error("Error accediendo a opciones: %s", e)

    def _on_exit(self):
        """
        Callback para salir.
        """
        self.logger.info("[MainMenuScene] Acción: Salir - cerrando juego")
        self.menu_manager.hide_current_menu()
        pygame.display.quit()
        pygame.quit()  # pylint: disable=no-member
        sys.exit()
