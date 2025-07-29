"""
Options Scene - Escena de Opciones
=================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Escena para configurar opciones del juego.
"""

import pygame
from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..ui.menu_manager import MenuManager
from ..utils.logger import get_logger


class OptionsScene(Scene):
    """
    Escena de opciones del juego.
    """

    def __init__(
        self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager
    ):
        super().__init__(screen, config)
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")
        # Inicializar menú
        self.menu_manager = MenuManager(screen, config, game_state, save_manager)
        self.logger.info("[OptionsScene] Escena de opciones inicializada")

    def enter(self):
        super().enter()
        self.menu_manager.show_menu("options")
        self.logger.info("[OptionsScene] Entrando en escena de opciones")

    def exit(self):
        super().exit()
        self.menu_manager.hide_current_menu()
        self.logger.info("[OptionsScene] Saliendo de escena de opciones")

    def handle_event(self, event: pygame.event.Event) -> bool:
        # Manejar eventos del menú
        self.menu_manager.update([event])
        # Manejar eventos específicos de la escena
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.logger.info(
                    "[OptionsScene] ESC presionado - volviendo al menú principal"
                )
                self.game_state.scene_manager.change_scene("main_menu")
                return True
        return False

    def update(self, dt: float = 0):
        self.menu_manager.update([])

    def render(self):
        self.screen.fill((0, 0, 0))
        self.menu_manager.render()
