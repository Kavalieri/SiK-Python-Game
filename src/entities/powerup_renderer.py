"""
Powerup Renderer - Renderizado de powerups
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Renderizado y sprites de powerups.
"""

import logging
import math

import pygame

from .powerup_types import PowerupConfiguration, PowerupType


class PowerupRenderer:
    """Manejador de renderizado de powerups."""

    def __init__(self, powerup_type: PowerupType, width: int = 30, height: int = 30):
        """
        Inicializa el renderizador de powerup.

        Args:
            powerup_type: Tipo de powerup
            width: Ancho del sprite
            height: Alto del sprite
        """
        self.powerup_type = powerup_type
        self.width = width
        self.height = height
        self.logger = logging.getLogger(__name__)
        self.config = PowerupConfiguration()

        # Efecto de flotación
        self.float_offset = 0
        self.float_speed = 2.0

        # Sprite
        self.sprite: pygame.Surface | None = None
        self._setup_sprite()

    def _setup_sprite(self):
        """Configura el sprite del powerup."""
        try:
            # Crear superficie con transparencia
            self.sprite = pygame.Surface((self.width, self.height))
            self.sprite = self.sprite.convert_alpha()

            # Obtener configuración del powerup
            powerup_config = self.config.get_config(self.powerup_type)
            color = powerup_config.get("color", (255, 255, 255))

            # Crear círculo de fondo
            center = (self.width // 2, self.height // 2)
            radius = min(self.width, self.height) // 2 - 2
            pygame.draw.circle(self.sprite, color, center, radius)

            # Borde más oscuro
            darker_color = tuple(max(0, c - 50) for c in color)
            pygame.draw.circle(self.sprite, darker_color, center, radius, 2)

            # Agregar símbolo
            self._add_symbol()

        except (AttributeError, ValueError) as e:
            self.logger.error("Error configurando sprite: %s", e)

    def _add_symbol(self):
        """Agrega el símbolo al sprite."""
        if not self.sprite:
            return

        try:
            # Obtener símbolo
            symbol = self.config.get_symbol(self.powerup_type)

            # Crear fuente
            try:
                font = pygame.font.Font(None, 20)
            except (FileNotFoundError, OSError):
                font = pygame.font.SysFont("arial", 20)

            # Renderizar símbolo
            text = font.render(symbol, True, (255, 255, 255))

            # Centrar el símbolo
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.sprite.blit(text, text_rect)

        except (AttributeError, ValueError) as e:
            self.logger.warning("Error agregando símbolo: %s", e)

    def update_animation(self, delta_time: float):
        """Actualiza la animación de flotación."""
        self.float_offset += self.float_speed * delta_time
        if self.float_offset > 2 * math.pi:
            self.float_offset = 0

    def render(
        self, screen: pygame.Surface, x: float, y: float, camera_offset: tuple = (0, 0)
    ):
        """
        Renderiza el powerup con efecto de flotación.

        Args:
            screen: Superficie donde renderizar
            x: Posición X
            y: Posición Y
            camera_offset: Offset de la cámara
        """
        if not self.sprite:
            return

        try:
            # Calcular posición con flotación
            float_y = math.sin(self.float_offset) * 3
            render_x = x - camera_offset[0]
            render_y = y - camera_offset[1] + float_y

            # Renderizar sprite
            screen.blit(self.sprite, (render_x, render_y))

        except (AttributeError, TypeError) as e:
            self.logger.debug("Error renderizando powerup: %s", e)

    def render_debug(
        self, screen: pygame.Surface, x: float, y: float, camera_offset: tuple = (0, 0)
    ):
        """Renderiza información de debug."""
        try:
            debug_rect = pygame.Rect(
                x - camera_offset[0], y - camera_offset[1], self.width, self.height
            )
            pygame.draw.rect(screen, (255, 255, 0), debug_rect, 2)
        except (AttributeError, TypeError) as e:
            self.logger.debug("Error en renderizado debug: %s", e)

    def get_sprite(self) -> pygame.Surface | None:
        """Obtiene el sprite del powerup."""
        return self.sprite

    def set_size(self, width: int, height: int):
        """Cambia el tamaño del powerup."""
        self.width = width
        self.height = height
        self._setup_sprite()

    def get_color(self) -> tuple:
        """Obtiene el color del powerup."""
        powerup_config = self.config.get_config(self.powerup_type)
        return powerup_config.get("color", (255, 255, 255))
