"""
Pause Scene - Escena de Pausa
============================

Autor: SiK Team
Fecha: 2024
Descripción: Escena de pausa del juego.
"""

import sys

import pygame
import pygame_gui

from core.scene_manager import Scene
from ui.menu_manager import MenuManager
from utils.config_manager import ConfigManager
from utils.logger import get_logger


class PauseScene(Scene):
    """
    Escena de pausa del juego.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        """
        Inicializa la escena de pausa.

        Args:
                screen: Superficie de Pygame donde renderizar
                config: Configuración del juego
                game_state: Estado del juego
                save_manager: Gestor de guardado
        """
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")

        # Configurar pygame-gui
        self.ui_manager = pygame_gui.UIManager(
            (screen.get_width(), screen.get_height()), theme_path="assets/ui/theme.json"
        )

        self.logger.info("[PauseScene] Escena de pausa inicializada")

        # Inicializar menú
        self.menu_manager = MenuManager(screen, config, game_state, save_manager)
        self.menu_manager.show_menu("pause")

        # Configurar callbacks
        self._configurar_callbacks()

        # Configurar elementos pygame-gui
        self._setup_pygame_gui_elements()

        self.logger.info("Escena de pausa inicializada")

    def _setup_pygame_gui_elements(self):
        """
        Configura los elementos de pygame-gui para la escena de pausa.
        """
        screen_width, screen_height = self.screen.get_size()

        # Panel central de pausa
        panel_width, panel_height = 400, 500
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        # Ventana/Panel principal
        self.pause_window = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.ui_manager,
        )

        # Título
        self.titulo_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_width // 2 - 50, 20), (100, 50)),
            text="PAUSA",
            manager=self.ui_manager,
            container=self.pause_window,
        )

        # Botones del menú de pausa
        button_width = 300
        button_height = 50
        button_x = (panel_width - button_width) // 2

        self.resume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 100), (button_width, button_height)),
            text="Reanudar Juego",
            manager=self.ui_manager,
            container=self.pause_window,
        )

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 170), (button_width, button_height)),
            text="Guardar Partida",
            manager=self.ui_manager,
            container=self.pause_window,
        )

        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 240), (button_width, button_height)),
            text="Opciones",
            manager=self.ui_manager,
            container=self.pause_window,
        )

        self.main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 310), (button_width, button_height)),
            text="Menú Principal",
            manager=self.ui_manager,
            container=self.pause_window,
        )

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, 380), (button_width, button_height)),
            text="Salir del Juego",
            manager=self.ui_manager,
            container=self.pause_window,
        )

    def _configurar_callbacks(self):
        """
        Configura los callbacks del menú de pausa.
        """
        self.menu_manager.add_callback("resume_game", self._on_resume_game)
        self.menu_manager.add_callback("save_game", self._on_save_game)
        self.menu_manager.add_callback("main_menu", self._on_main_menu)
        self.menu_manager.add_callback("exit", self._on_exit)

    def handle_event(self, event: pygame.event.Event):
        """
        Procesa eventos de Pygame.

        Args:
            event: Evento de Pygame a procesar.
        """
        # Procesar eventos de pygame-gui primero
        self.ui_manager.process_events(event)

        # Eventos específicos de pygame-gui
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.resume_button:
                self._on_resume_game()
                return
            elif event.ui_element == self.save_button:
                self._on_save_game()
                return
            elif event.ui_element == self.options_button:
                self._on_options()
                return
            elif event.ui_element == self.main_menu_button:
                self._on_main_menu()
                return
            elif event.ui_element == self.exit_button:
                self._on_exit()
                return

        self.logger.info("[PauseScene] Evento recibido: %s - %s", event.type, event)
        if event.type == 768:  # pygame.KEYDOWN
            self.logger.info("[PauseScene] Tecla pulsada: %s", event.key)
        elif event.type == 1025:  # pygame.MOUSEBUTTONDOWN
            self.logger.info(
                "[PauseScene] Click ratón: %s en %s", event.button, event.pos
            )
        if event.type == 768 and event.key == 27:  # KEYDOWN and K_ESCAPE
            # Reanudar juego con ESC
            self._on_resume_game()
        else:
            self.menu_manager.update([event])

    def update(self):
        """
        Actualiza la lógica de la escena de pausa.
        """
        time_delta = pygame.time.Clock().tick(60) / 1000.0
        self.ui_manager.update(time_delta)

    def render(self):
        """
        Renderiza la escena de pausa.
        """
        # Fondo semi-transparente
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Comentar menú original para evitar superposición
        # self.menu_manager.render()

        # Solo renderizar UI de pygame-gui
        self.ui_manager.draw_ui(self.screen)

    def _on_resume_game(self):
        """Callback para reanudar juego."""
        self.logger.info("Reanudando juego")
        # Cambiar de vuelta a la escena del juego
        self.game_state.scene_manager.change_scene("game")

    def _on_save_game(self):
        """Callback para guardar juego."""
        self.logger.info("Guardando juego")
        # Aquí se guardaría la partida actual
        # Por ahora solo mostramos un mensaje
        self.menu_manager.hide_current_menu()

    def _on_options(self):
        """Callback para ir a opciones."""
        self.logger.info("Abriendo opciones desde pausa")
        # Cambiar a la escena de opciones
        self.game_state.scene_manager.change_scene("options")

    def _on_main_menu(self):
        """Callback para volver al menú principal."""
        self.logger.info("Volviendo al menú principal")
        # Aquí se cambiaría a la escena del menú principal
        self.game_state.scene_manager.change_scene("main_menu")
        self.menu_manager.hide_current_menu()

    def _on_exit(self):
        """
        Callback para salir.
        """
        self.logger.info("Saliendo del juego")
        pygame.display.quit()
        pygame.quit()  # pylint: disable=no-member
        sys.exit()
