# -*- coding: utf-8 -*-
"""
Heat Shimmer Effects - Sistema de efectos de ondas de calor.
Módulo especializado extraído de atmospheric_effects.py (optimización de líneas).
"""

import pygame
import math


class HeatShimmerEffects:
    """Sistema de efectos de ondas de calor para el desierto."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Estado de efectos de calor
        self.heat_shimmer_time = 0.0
        self.heat_shimmer_strength = 0.3

    def update(self, delta_time: float):
        """Actualiza el tiempo para efectos de calor."""
        self.heat_shimmer_time += delta_time

    def render_heat_shimmer(self, screen: pygame.Surface):
        """Renderiza efectos de ondas de calor."""
        # Crear efecto de shimmer en la parte inferior
        shimmer_height = int(self.screen_height * 0.3)
        shimmer_start_y = self.screen_height - shimmer_height

        # Crear superficie para efectos de calor
        shimmer_surface = pygame.Surface((self.screen_width, shimmer_height))
        shimmer_surface.set_alpha(128)

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

    def set_heat_shimmer_strength(self, strength: float):
        """Configura la intensidad del efecto de calor."""
        self.heat_shimmer_strength = max(0.0, min(1.0, strength))
