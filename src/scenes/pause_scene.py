"""
Pause Scene - Escena de Pausa
============================

Autor: SiK Team
Fecha: 2024
Descripción: Escena de pausa del juego.
"""

import sys

import pygame

from ..core.scene_manager import Scene
from ..ui.menu_manager import MenuManager
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger


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
        self.logger.info("[PauseScene] Escena de pausa inicializada")

        # Inicializar menú
        self.menu_manager = MenuManager(screen, config, game_state, save_manager)
        self.menu_manager.show_menu("pause")

        # Configurar callbacks
        self._configurar_callbacks()

        self.logger.info("Escena de pausa inicializada")

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
        # Método vacío, pero necesario para la estructura.
        return

    def render(self):
        """
        Renderiza la escena de pausa.
        """
        # Fondo semi-transparente
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Renderizar menú
        self.menu_manager.render()

    def _on_resume_game(self):
        """Callback para reanudar juego."""
        self.logger.info("Reanudando juego")
        # Aquí se volvería a la escena del juego
        self.menu_manager.hide_current_menu()

    def _on_save_game(self):
        """Callback para guardar juego."""
        self.logger.info("Guardando juego")
        # Aquí se guardaría la partida actual
        # Por ahora solo mostramos un mensaje
        self.menu_manager.hide_current_menu()

    def _on_main_menu(self):
        """Callback para volver al menú principal."""
        self.logger.info("Volviendo al menú principal")
        # Aquí se cambiaría a la escena del menú principal
        self.menu_manager.hide_current_menu()

    def _on_exit(self):
        """
        Callback para salir.
        """
        self.logger.info("Saliendo del juego")
        pygame.display.quit()
        pygame.quit()  # pylint: disable=no-member
        sys.exit()
