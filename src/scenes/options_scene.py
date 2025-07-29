"""
Options Scene - Escena de Opciones
=================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Escena para configurar opciones del juego.
"""

import pygame

from ..core.scene_manager import Scene
from ..ui.menu_manager import MenuManager
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger


class OptionsScene(Scene):
    """
    Escena de opciones del juego.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        """
        Inicializa la escena de opciones.

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
        self._inicializar_menu()
        self.logger.info("[OptionsScene] Escena de opciones inicializada")

    def _inicializar_menu(self):
        """
        Inicializa el menú de opciones.
        """
        try:
            self.menu_manager = MenuManager(
                self.screen, self.config, self.game_state, self.save_manager
            )
        except Exception as e:
            self.logger.error("Error al inicializar el menú de opciones: %s", e)
            raise

    def enter(self):
        super().enter()
        self.menu_manager.show_menu("options")
        self.logger.info("[OptionsScene] Entrando en escena de opciones")

    def exit(self):
        super().exit()
        self.menu_manager.hide_current_menu()
        self.logger.info("[OptionsScene] Saliendo de escena de opciones")

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Maneja eventos de la escena de opciones.

        Args:
            event: Evento de Pygame a procesar.

        Returns:
            bool: True si el evento fue manejado, False en caso contrario.
        """
        self.menu_manager.update([event])
        if event.type == pygame.constants.KEYDOWN:
            if event.key == pygame.constants.K_ESCAPE:
                self.logger.info(
                    "[OptionsScene] ESC presionado - volviendo al menú principal"
                )
                self.game_state.scene_manager.change_scene("main_menu")
                return True
        return False

    def update(self):
        """
        Actualiza la lógica de la escena de opciones.
        """
        self.menu_manager.update([])

    def render(self):
        """
        Renderiza la escena de opciones.
        """
        self.screen.fill((0, 0, 0))
        self.menu_manager.render()
