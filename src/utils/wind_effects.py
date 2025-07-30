# -*- coding: utf-8 -*-
"""
Wind Effects - Sistema de efectos visuales del viento.
Módulo especializado extraído de atmospheric_effects.py (optimización de líneas).
"""

import math
import random

import pygame


class WindEffects:
    """Sistema de efectos visuales del viento para el desierto."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Estado del viento
        self.wind_time = 0.0
        self.wind_strength = 0.2
        self.wind_angle = 0.0

    def update(self, delta_time: float):
        """Actualiza el tiempo del viento."""
        self.wind_time += delta_time

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
            wind_surface = pygame.Surface((50, 30))
            wind_surface.set_alpha(20)
            pygame.draw.line(wind_surface, wind_color[:3], (0, 10), (30, 20), 1)

            # Verificar límites antes de dibujar
            if (
                0 <= start_pos[0] < self.screen_width
                and 0 <= start_pos[1] < self.screen_height
            ):
                screen.blit(wind_surface, (start_pos[0] - 10, start_pos[1] - 10))

    def render_dust_clouds(self, screen: pygame.Surface, camera_offset=(0, 0)):
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
            cloud_surface = pygame.Surface((100, 40))
            cloud_surface.set_alpha(30)

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

    def set_wind_parameters(self, strength: float, base_angle: float):
        """Configura los parámetros del viento."""
        self.wind_strength = max(0.0, min(1.0, strength))
        self.wind_angle = base_angle

    def get_wind_data(self):
        """Obtiene los datos actuales del viento."""
        return (self.wind_strength, self.wind_angle)
