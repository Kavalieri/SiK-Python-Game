"""
Game Engine - Fachada del Motor Principal del Juego
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Fachada que integra todos los componentes del motor del juego.
"""

import pygame
from .game_engine_core import GameEngineCore
from .game_engine_scenes import GameEngineScenes
from .game_engine_events import GameEngineEvents
from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger


class GameEngine:
    """
    Motor principal del juego que integra todos los componentes.
    """

    def __init__(self, config: ConfigManager):
        """
        Inicializa el motor del juego.

        Args:
            config: Gestor de configuración del juego
        """
        self.logger = get_logger("SiK_Game")

        # Inicializar componentes
        self.core = GameEngineCore(config)
        self.events = GameEngineEvents(self.core)
        self.scenes = GameEngineScenes(self.core, self.events)

        # Configurar escenas
        self.scenes.setup_scenes()

        self.logger.info("GameEngine completamente inicializado")

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
        """Ejecuta el bucle principal del juego."""
        self.running = True
        self.logger.info("Iniciando bucle principal del juego...")

        try:
            while self.running:
                self.events.handle_events()
                self._update()
                self._render()
                if self.clock:
                    self.clock.tick(self.config.get_fps())

        except RuntimeError as e:
            self.logger.error("Error en el bucle principal: %s", e)
            raise
        finally:
            self._cleanup()

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
