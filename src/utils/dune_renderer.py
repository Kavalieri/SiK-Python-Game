"""
Dune Renderer - Sistema de Renderizado de Dunas
==============================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Sistema de renderizado de dunas y terreno del desierto.
"""

import pygame
import random
import math
from typing import List, Tuple
import logging


class Dune:
    """Duna de arena para el fondo."""

    def __init__(
        self, x: float, y: float, width: float, height: float, screen_width: int
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width

        # Propiedades de la duna
        self.points = self._generate_dune_points()
        self.color = (
            random.randint(180, 220),  # R
            random.randint(160, 200),  # G
            random.randint(100, 140),  # B
        )

        # Efecto de sombra
        self.shadow_color = (
            max(0, self.color[0] - 40),  # R más oscuro
            max(0, self.color[1] - 40),  # G más oscuro
            max(0, self.color[2] - 40),  # B más oscuro
        )

    def _generate_dune_points(self) -> List[Tuple[float, float]]:
        """Genera puntos para dibujar la duna."""
        points = []
        num_points = 20

        for i in range(num_points + 1):
            x = self.x + (i / num_points) * self.width

            # Función sinusoidal para crear la forma de duna
            progress = i / num_points
            wave = math.sin(progress * math.pi) * 0.3
            noise = random.uniform(-0.1, 0.1)

            y = self.y + self.height * (1 - wave + noise)
            points.append((x, y))

        return points

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza la duna."""
        # Aplicar offset de cámara
        offset_points = []
        for x, y in self.points:
            offset_x = x - camera_offset[0]
            offset_y = y - camera_offset[1]
            offset_points.append((offset_x, offset_y))

        # Dibujar duna principal
        if len(offset_points) > 2:
            pygame.draw.polygon(screen, self.color, offset_points)

        # Dibujar sombra
        shadow_points = []
        for x, y in offset_points:
            shadow_points.append((x, y + 5))  # Sombra desplazada hacia abajo

        if len(shadow_points) > 2:
            pygame.draw.polygon(screen, self.shadow_color, shadow_points)


class DuneRenderer:
    """Sistema de renderizado de dunas del desierto."""

    def __init__(self, screen_width: int, screen_height: int):
        """
        Inicializa el renderizador de dunas.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dunes: List[Dune] = []
        self.logger = logging.getLogger(__name__)

        self._create_dunes()

    def _create_dunes(self):
        """Crea las dunas del fondo."""
        self.dunes = []

        # Crear dunas en el fondo
        num_dunes = random.randint(3, 6)
        for i in range(num_dunes):
            x = random.uniform(-50, self.screen_width - 100)
            y = random.uniform(self.screen_height * 0.6, self.screen_height * 0.9)
            width = random.uniform(150, 300)
            height = random.uniform(50, 120)

            dune = Dune(x, y, width, height, self.screen_width)
            self.dunes.append(dune)

        # Ordenar dunas por profundidad (y más grande = más al fondo)
        self.dunes.sort(key=lambda d: d.y, reverse=True)

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza todas las dunas."""
        for dune in self.dunes:
            dune.render(screen, camera_offset)

    def render_dune_effects(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza efectos adicionales de las dunas."""
        # Añadir brillos en los picos de las dunas
        for dune in self.dunes:
            if len(dune.points) > 0:
                # Encontrar el punto más alto de la duna
                highest_point = min(dune.points, key=lambda p: p[1])

                # Aplicar offset de cámara
                highlight_x = highest_point[0] - camera_offset[0]
                highlight_y = highest_point[1] - camera_offset[1]

                # Dibujar brillo
                highlight_color = (
                    min(255, dune.color[0] + 50),
                    min(255, dune.color[1] + 50),
                    min(255, dune.color[2] + 50),
                )

                # Crear superficie para el brillo con transparencia
                highlight_surface = pygame.Surface((20, 5), pygame.SRCALPHA)
                pygame.draw.ellipse(
                    highlight_surface, (*highlight_color, 100), (0, 0, 20, 5)
                )

                screen.blit(highlight_surface, (highlight_x - 10, highlight_y - 2))

    def add_dune(self, x: float, y: float, width: float, height: float) -> Dune:
        """
        Añade una nueva duna al sistema.

        Args:
            x: Posición X de la duna
            y: Posición Y de la duna
            width: Ancho de la duna
            height: Alto de la duna

        Returns:
            La duna creada
        """
        dune = Dune(x, y, width, height, self.screen_width)
        self.dunes.append(dune)

        # Re-ordenar por profundidad
        self.dunes.sort(key=lambda d: d.y, reverse=True)

        return dune

    def remove_dune(self, dune: Dune):
        """
        Remueve una duna del sistema.

        Args:
            dune: La duna a remover
        """
        if dune in self.dunes:
            self.dunes.remove(dune)

    def get_dune_count(self) -> int:
        """
        Obtiene el número de dunas en el sistema.

        Returns:
            Número de dunas
        """
        return len(self.dunes)

    def clear_dunes(self):
        """Limpia todas las dunas del sistema."""
        self.dunes.clear()

    def regenerate_dunes(self):
        """Regenera todas las dunas del sistema."""
        self.clear_dunes()
        self._create_dunes()
