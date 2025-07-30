# -*- coding: utf-8 -*-
"""
Sky Renderer - Sistema de renderizado del cielo del desierto.
Módulo especializado extraído de atmospheric_effects.py (optimización de líneas).
"""

from typing import Tuple

import pygame


class SkyRenderer:
    """Renderizador especializado del gradiente del cielo del desierto."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Configuración de colores del cielo del desierto
        self.sky_colors = {
            "horizon": (245, 222, 179),  # Arena clara
            "mid": (135, 206, 235),  # Azul cielo
            "top": (70, 130, 180),  # Azul más profundo
            "sunset_horizon": (255, 165, 0),  # Naranja atardecer
            "sunset_mid": (255, 99, 71),  # Rojo atardecer
            "sunset_top": (25, 25, 112),  # Azul noche
        }

    def render_sky_gradient(self, screen: pygame.Surface):
        """Renderiza el gradiente del cielo del desierto."""
        # Dibujar gradiente vertical del cielo
        for y in range(self.screen_height):
            # Calcular ratio de interpolación (0.0 en la parte superior, 1.0 en el horizonte)
            t = y / self.screen_height

            # Interpolar entre colores del cielo
            horizon_color = self.sky_colors["horizon"]
            mid_color = self.sky_colors["mid"]
            top_color = self.sky_colors["top"]

            if t < 0.5:
                # Parte superior del cielo
                ratio = t * 2
                color = self._interpolate_color(top_color, mid_color, ratio)
            else:
                # Parte inferior hacia el horizonte
                ratio = (t - 0.5) * 2
                color = self._interpolate_color(mid_color, horizon_color, ratio)

            pygame.draw.line(screen, color, (0, y), (self.screen_width, y))

    def _interpolate_color(
        self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float
    ) -> Tuple[int, int, int]:
        """Interpola entre dos colores."""
        t = max(0.0, min(1.0, t))  # Clamp t entre 0 y 1

        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)

        return (r, g, b)
