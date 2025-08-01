"""
Game Engine - Fachada del Motor Principal del Juego
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Fachada que integra todos los componentes del motor del juego.
"""

import sys

import pygame

from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger
from .game_engine_core import GameEngineCore
from .game_engine_events import GameEngineEvents
from .game_engine_scenes import GameEngineScenes


class GameEngine:
    """
    Motor principal del juego que integra todos los componentes.
    """

    def __init__(self, config: ConfigManager):
        """Inicializa el motor del juego.

        Args:
            config (ConfigManager): Instancia del gestor de configuración.
        """
        self.logger = get_logger("SiK_Game")
        self.logger.info("Inicializando GameEngine...")

        self.core = GameEngineCore(config)
        self.events = GameEngineEvents(self.core)
        self.scenes = GameEngineScenes(self.core, self.events)

        self.logger.info("GameEngine inicializado.")

    @property
    def running(self) -> bool:
        """Acceso a running del core."""
        return self.core.running

    @running.setter
    def running(self, value: bool):
        """Setter para running del core."""
        self.core.running = value

    # Delegación de propiedades para compatibilidad
    @property
    def config(self):
        """Acceso a configuración."""
        return self.core.config

    @property
    def screen(self):
        """Acceso a pantalla."""
        return self.core.screen

    @property
    def clock(self):
        """Acceso a reloj."""
        return self.core.clock

    @property
    def game_state(self):
        """Acceso a estado del juego."""
        return self.core.game_state

    @property
    def scene_manager(self):
        """Acceso a gestor de escenas."""
        return self.core.scene_manager

    @property
    def save_manager(self):
        """Acceso a gestor de guardado."""
        return self.core.save_manager

    @property
    def menu_manager(self):
        """Acceso a gestor de menús."""
        return self.core.menu_manager

    def run(self):
        """Bucle principal del juego."""
        self.logger.info("Iniciando bucle principal del motor del juego.")

        # Asegurar que la escena inicial se configure y renderice antes del bucle principal
        self.scenes.setup_scenes()
        self._update()  # Forzar una actualización inicial para procesar cambios de escena
        self._render()  # Forzar un renderizado inicial para mostrar la escena

        while self.core.running:
            self.events.handle_events()
            self._update()
            self._render()
            self.core.clock.tick(self.core.get_fps())

        self.logger.info("Saliendo del bucle principal. Limpiando y cerrando...")
        pygame.quit()
        sys.exit()

    def _update(self):
        """Actualiza la lógica del juego."""
        if self.scene_manager:
            self.scene_manager.update()

    def _render(self):
        """Renderiza el juego en pantalla."""
        if self.scene_manager:
            self.scene_manager.render()
            pygame.display.flip()  # pylint: disable=no-member

    def _cleanup(self):
        """Limpia recursos y cierra el motor."""
        self.logger.info("Limpiando recursos del juego...")
        self.core.cleanup()
        self.logger.info("Juego cerrado correctamente")
