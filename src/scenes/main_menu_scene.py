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
        # Procesar eventos de menú aquí
        if event.type == pg_constants.KEYDOWN:  # pylint: disable=c-extension-no-member
            self.logger.info("[MainMenuScene] Tecla pulsada: %s", event.key)
        elif event.type == pg_constants.MOUSEBUTTONDOWN:  # pylint: disable=c-extension-no-member
            self.logger.info(
                "[MainMenuScene] Click ratón: %s en %s", event.button, event.pos
            )
        self.menu_manager.update([event])

    def update(self):
        """
        Actualiza la lógica de la escena.
        """
        # Método vacío, pero necesario para la estructura.
        return

    def render(self):
        """Renderiza la escena."""
        # Fondo negro
        self.screen.fill((0, 0, 0))

        # Renderizar menú
        self.menu_manager.render()

    def _on_new_game(self):
        """Callback para nuevo juego."""
        self.logger.info(
            "[MainMenuScene] Acción: Nuevo Juego - mostrando menú de guardado para nueva partida"
        )
        self.menu_manager.show_menu("save")

    def _on_continue_game(self):
        """Callback para continuar juego."""
        self.logger.info(
            "[MainMenuScene] Acción: Continuar Juego - mostrando menú de guardado para continuar"
        )
        self.menu_manager.show_menu("save")

    def _on_load_game(self):
        """
        Callback para cargar partida.

        Nota:
            Este método aún no está implementado.
        """
        self.logger.warning("[MainMenuScene] Acción: Cargar Juego - NO IMPLEMENTADO")
        # El menú sigue operativo

    def _on_options(self):
        """
        Callback para opciones.

        Nota:
            Este método aún no está implementado.
        """
        self.logger.warning("[MainMenuScene] Acción: Opciones - NO IMPLEMENTADO")
        # El menú sigue operativo

    def _on_exit(self):
        """
        Callback para salir.
        """
        self.logger.info("[MainMenuScene] Acción: Salir - cerrando juego")
        self.menu_manager.hide_current_menu()
        pygame.display.quit()
        pygame.quit()  # pylint: disable=no-member
        sys.exit()
