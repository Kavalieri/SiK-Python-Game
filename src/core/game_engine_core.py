"""
Game Engine Core - Núcleo de Inicialización del Motor
====================================================

Autor: SiK Team
Fecha: 2024
Descripción: Núcleo del motor con inicialización de componentes y configuración.
"""

import pygame

from ..ui.menu_manager import MenuManager
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger
from ..utils.save_manager import SaveManager
from .game_state import GameState
from .scene_manager import SceneManager


class GameEngineCore:
    """Núcleo del motor con inicialización y configuración básica."""

    def __init__(self, config: ConfigManager):
        """
        Inicializa el núcleo del motor del juego.

        Args:
            config: Gestor de configuración del juego
        """
        self.logger = get_logger("SiK_Game")
        self.logger.info("[GameEngine] Motor principal inicializado")
        self.config = config

        # Componentes principales
        self.running = False
        self.clock = None
        self.screen = None
        self.game_state = None
        self.scene_manager = None
        self.save_manager = None
        self.menu_manager = None

        # Inicialización completa
        self.logger.info("Inicializando motor del juego...")
        self._initialize_pygame()
        self._initialize_components()
        self.logger.info("Motor del juego inicializado correctamente")

    def _initialize_pygame(self):
        """Inicializa Pygame y configura la pantalla."""
        try:
            pygame.init()  # pylint: disable=no-member
            pygame.mixer.init()  # pylint: disable=no-member

            # Configurar pantalla
            screen_width, screen_height = self.config.get_resolution()
            title = self.config.get("game", "title", "SiK Python Game")

            self.screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption(title)

            # Configurar reloj
            fps = self.config.get_fps()
            self.clock = pygame.time.Clock()

            self.logger.info(
                "Pygame inicializado - Resolución: %dx%d, FPS: %d",
                screen_width,
                screen_height,
                fps,
            )

        except RuntimeError as e:
            self.logger.error("Error al inicializar Pygame: %s", e)
            raise

    def _initialize_components(self):
        """Inicializa los componentes principales del juego."""
        try:
            # Verificar que screen esté inicializada
            if not self.screen:
                raise RuntimeError("Screen no inicializada")

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

            # Configurar referencias entre componentes (si scene_manager tiene setter)
            # self.game_state.scene_manager = self.scene_manager

            self.logger.info("Componentes del juego inicializados")

        except RuntimeError as e:
            self.logger.error("Error al inicializar componentes: %s", e)
            raise

    def cleanup(self):
        """Limpia recursos del motor."""
        try:
            self.logger.info("Cerrando motor del juego...")
            # Solo limpiar si game_state tiene método cleanup
            if hasattr(self.game_state, "cleanup"):
                self.game_state.cleanup()  # type: ignore
            pygame.quit()  # pylint: disable=no-member
            self.logger.info("Motor del juego cerrado")
        except RuntimeError as e:
            self.logger.error("Error en cleanup: %s", e)

    def get_fps(self) -> int:
        """Obtiene los FPS configurados."""
        return self.config.get_fps()

    def get_screen_size(self) -> tuple:
        """Obtiene el tamaño de pantalla configurado."""
        return self.config.get_resolution()

    def get_screen(self):
        """Obtiene la superficie de pantalla."""
        return self.screen

    def get_clock(self):
        """Obtiene el reloj del juego."""
        return self.clock
