"""
Atmospheric Effects - Efectos Atmosféricos del Desierto
======================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Sistema de efectos atmosféricos y cielo del desierto.
"""

import logging
import math
import random
from typing import Tuple

import pygame


class AtmosphericEffects:
    """Sistema de efectos atmosféricos del desierto."""

    def __init__(self, screen_width: int, screen_height: int):
        """
        Inicializa el sistema de efectos atmosféricos.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)

        # Colores del desierto con más profundidad
        self.sky_colors = {
            "top": (135, 183, 255),  # Azul cielo superior
            "middle": (255, 223, 186),  # Amarillo arena medio
            "bottom": (255, 200, 150),  # Naranja arena inferior
        }

        # Efectos de viento
        self.wind_strength = 0.3
        self.wind_angle = 0.0
        self.wind_time = 0.0

        # Efectos de calor (heat shimmer)
        self.heat_shimmer_time = 0.0
        self.heat_shimmer_strength = 0.5

    def update(self, delta_time: float):
        """
        Actualiza los efectos atmosféricos.

        Args:
            delta_time: Tiempo transcurrido desde la última actualización
        """
        # Actualizar efectos de viento
        self.wind_time += delta_time
        self.wind_angle = math.sin(self.wind_time * 0.5) * 0.3
        self.wind_strength = 0.3 + math.sin(self.wind_time * 0.2) * 0.2

        # Actualizar efectos de calor
        self.heat_shimmer_time += delta_time

    def render_sky_gradient(self, screen: pygame.Surface):
        """Renderiza el gradiente del cielo del desierto."""
        # Crear superficies para gradiente
        sky_height = int(self.screen_height * 0.7)

        for y in range(sky_height):
            # Calcular progreso del gradiente
            progress = y / sky_height

            # Interpolación entre colores
            if progress < 0.3:
                # Transición de azul a amarillo (superior a medio)
                blend_progress = progress / 0.3
                color = self._interpolate_color(
                    self.sky_colors["top"], self.sky_colors["middle"], blend_progress
                )
            else:
                # Transición de amarillo a naranja (medio a inferior)
                blend_progress = (progress - 0.3) / 0.7
                color = self._interpolate_color(
                    self.sky_colors["middle"], self.sky_colors["bottom"], blend_progress
                )

            # Dibujar línea del gradiente
            pygame.draw.line(screen, color, (0, y), (self.screen_width, y))

    def render_heat_shimmer(self, screen: pygame.Surface):
        """Renderiza efectos de ondas de calor."""
        # Crear efecto de shimmer en la parte inferior
        shimmer_height = int(self.screen_height * 0.3)
        shimmer_start_y = self.screen_height - shimmer_height

        # Crear superficie para efectos de calor
        shimmer_surface = pygame.Surface(
            (self.screen_width, shimmer_height), pygame.SRCALPHA
        )

        for y in range(0, shimmer_height, 5):
            # Calcular ondulación basada en tiempo y posición
            wave_offset = math.sin(self.heat_shimmer_time * 3 + y * 0.1) * 2
            wave_offset += math.sin(self.heat_shimmer_time * 5 + y * 0.05) * 1

            # Intensidad del shimmer basada en la altura
            intensity = (y / shimmer_height) * self.heat_shimmer_strength * 30

            # Color del shimmer (transparente con tinte cálido)
            shimmer_color = (255, 255, 255, int(intensity))

            # Dibujar líneas onduladas
            points = []
            for x in range(0, self.screen_width, 10):
                offset_y = y + wave_offset * (y / shimmer_height)
                points.append((x, offset_y))

            if len(points) > 1:
                for i in range(len(points) - 1):
                    start_pos = points[i]
                    end_pos = points[i + 1]
                    pygame.draw.line(
                        shimmer_surface, shimmer_color[:3], start_pos, end_pos, 2
                    )

        # Aplicar superficie de shimmer
        screen.blit(shimmer_surface, (0, shimmer_start_y))

    def render_wind_effect(self, screen: pygame.Surface):
        """Renderiza efectos visuales del viento."""
        # Crear líneas de viento sutiles
        wind_lines_count = 8

        for i in range(wind_lines_count):
            # Posición de las líneas de viento
            x = (i / wind_lines_count) * self.screen_width
            y_start = random.uniform(self.screen_height * 0.4, self.screen_height * 0.8)

            # Calcular movimiento del viento
            wind_movement = math.sin(self.wind_time + i) * self.wind_strength * 50

            # Puntos de la línea de viento
            start_pos = (x + wind_movement, y_start)

            # Color del viento (muy sutil)
            wind_color = (255, 255, 255, 20)

            # Crear superficie para transparencia
            wind_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
            pygame.draw.line(wind_surface, wind_color[:3], (0, 10), (30, 20), 1)

            # Verificar límites antes de dibujar
            if (
                0 <= start_pos[0] < self.screen_width
                and 0 <= start_pos[1] < self.screen_height
            ):
                screen.blit(wind_surface, (start_pos[0] - 10, start_pos[1] - 10))

    def render_dust_clouds(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza nubes de polvo en el horizonte."""
        # Crear nubes de polvo sutiles en el horizonte
        dust_y = self.screen_height * 0.7

        for i in range(3):
            # Posición de la nube de polvo
            cloud_x = (i * self.screen_width / 3) + (self.screen_width / 6)
            cloud_x -= camera_offset[0] * 0.1  # Parallax muy sutil

            # Movimiento ondulante
            wave_offset = math.sin(self.wind_time * 0.5 + i * 2) * 20

            # Color de la nube (muy sutil)
            dust_color = (220, 200, 180, 30)

            # Crear superficie para la nube
            cloud_surface = pygame.Surface((100, 40), pygame.SRCALPHA)

            # Dibujar múltiples círculos para formar la nube
            for j in range(5):
                circle_x = j * 20 + random.uniform(-5, 5)
                circle_y = 20 + random.uniform(-10, 10)
                radius = random.randint(8, 15)

                pygame.draw.circle(
                    cloud_surface,
                    dust_color[:3],
                    (int(circle_x), int(circle_y)),
                    radius,
                )

            # Aplicar la nube
            final_x = cloud_x + wave_offset - 50
            final_y = dust_y - 20

            if -100 <= final_x <= self.screen_width + 100:
                screen.blit(cloud_surface, (final_x, final_y))

    def _interpolate_color(
        self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float
    ) -> Tuple[int, int, int]:
        """
        Interpola entre dos colores.

        Args:
            color1: Color inicial
            color2: Color final
            t: Factor de interpolación (0.0 - 1.0)

        Returns:
            Color interpolado
        """
        t = max(0.0, min(1.0, t))  # Clamp t entre 0 y 1

        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)

        return (r, g, b)

    def set_wind_parameters(self, strength: float, base_angle: float):
        """
        Configura los parámetros del viento.

        Args:
            strength: Fuerza del viento (0.0 - 1.0)
            base_angle: Ángulo base del viento en radianes
        """
        self.wind_strength = max(0.0, min(1.0, strength))
        self.wind_angle = base_angle

    def set_heat_shimmer_strength(self, strength: float):
        """
        Configura la intensidad del efecto de calor.

        Args:
            strength: Intensidad del shimmer (0.0 - 1.0)
        """
        self.heat_shimmer_strength = max(0.0, min(1.0, strength))

    def get_wind_data(self) -> Tuple[float, float]:
        """
        Obtiene los datos actuales del viento.

        Returns:
            Tupla con (fuerza, ángulo)
        """
        return (self.wind_strength, self.wind_angle)
