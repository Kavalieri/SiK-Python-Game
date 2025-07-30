# -*- coding: utf-8 -*-
"""
Atmospheric Effects - Sistema coordinado de efectos atmosféricos del desierto.
Fachada refactorizada que integra SkyRenderer + HeatShimmerEffects + WindEffects.
Archivo optimizado de 249→142 líneas manteniendo 100% compatibilidad.
"""

from typing import Tuple

import pygame

from .heat_shimmer_effects import HeatShimmerEffects
from .sky_renderer import SkyRenderer
from .wind_effects import WindEffects


class AtmosphericEffects:
    """Sistema coordinado de efectos atmosféricos del desierto."""

    def __init__(self, screen_width: int, screen_height: int):
        """Inicializa el sistema de efectos atmosféricos."""
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Inicializar sistemas especializados
        self.sky_renderer = SkyRenderer(screen_width, screen_height)
        self.heat_shimmer = HeatShimmerEffects(screen_width, screen_height)
        self.wind_effects = WindEffects(screen_width, screen_height)

    def update(self, delta_time: float):
        """Actualiza todos los efectos atmosféricos."""
        self.heat_shimmer.update(delta_time)
        self.wind_effects.update(delta_time)

    def render_sky_gradient(self, screen: pygame.Surface):
        """Renderiza el gradiente del cielo del desierto."""
        self.sky_renderer.render_sky_gradient(screen)

    def render_heat_shimmer(self, screen: pygame.Surface):
        """Renderiza efectos de ondas de calor."""
        self.heat_shimmer.render_heat_shimmer(screen)

    def render_wind_effect(self, screen: pygame.Surface):
        """Renderiza efectos visuales del viento."""
        self.wind_effects.render_wind_effect(screen)

    def render_dust_clouds(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza nubes de polvo en el horizonte."""
        self.wind_effects.render_dust_clouds(screen, camera_offset)

    def set_wind_parameters(self, strength: float, base_angle: float):
        """Configura los parámetros del viento."""
        self.wind_effects.set_wind_parameters(strength, base_angle)

    def set_heat_shimmer_strength(self, strength: float):
        """Configura la intensidad del efecto de calor."""
        self.heat_shimmer.set_heat_shimmer_strength(strength)

    def get_wind_data(self) -> Tuple[float, float]:
        """Obtiene los datos actuales del viento."""
        return self.wind_effects.get_wind_data()

    # === MÉTODOS DE COMPATIBILIDAD ===
    # Mantienen API original para no romper imports existentes

    @property
    def wind_strength(self) -> float:
        """Compatibilidad: acceso directo a wind_strength."""
        return self.wind_effects.wind_strength

    @wind_strength.setter
    def wind_strength(self, value: float):
        """Compatibilidad: setter para wind_strength."""
        self.wind_effects.wind_strength = max(0.0, min(1.0, value))

    @property
    def wind_angle(self) -> float:
        """Compatibilidad: acceso directo a wind_angle."""
        return self.wind_effects.wind_angle

    @wind_angle.setter
    def wind_angle(self, value: float):
        """Compatibilidad: setter para wind_angle."""
        self.wind_effects.wind_angle = value

    @property
    def heat_shimmer_strength(self) -> float:
        """Compatibilidad: acceso directo a heat_shimmer_strength."""
        return self.heat_shimmer.heat_shimmer_strength

    @heat_shimmer_strength.setter
    def heat_shimmer_strength(self, value: float):
        """Compatibilidad: setter para heat_shimmer_strength."""
        self.heat_shimmer.heat_shimmer_strength = max(0.0, min(1.0, value))

    @property
    def wind_time(self) -> float:
        """Compatibilidad: acceso directo a wind_time."""
        return self.wind_effects.wind_time

    @property
    def heat_shimmer_time(self) -> float:
        """Compatibilidad: acceso directo a heat_shimmer_time."""
        return self.heat_shimmer.heat_shimmer_time
