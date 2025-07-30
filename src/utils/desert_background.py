"""
Desert Background - Sistema de Fondo de Desierto Refactorizado
=============================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada del sistema de fondo dinámico de desierto tras refactorización modular.
"""

import pygame
from typing import Tuple
import logging

from .sand_particles import SandParticleSystem
from .dune_renderer import DuneRenderer
from .atmospheric_effects import AtmosphericEffects


class DesertBackground:
    """
    Sistema de fondo dinámico de desierto refactorizado.

    Actúa como fachada unificada que integra:
    - SandParticleSystem: Partículas de arena
    - DuneRenderer: Sistema de dunas
    - AtmosphericEffects: Efectos atmosféricos y cielo
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Inicializa el fondo de desierto.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)

        # Inicializar sistemas modulares
        self._init_systems()

    def _init_systems(self):
        """Inicializa todos los sistemas del fondo de desierto."""
        try:
            # Sistema de partículas de arena
            self.particle_system = SandParticleSystem(
                self.screen_width, self.screen_height, particle_count=50
            )

            # Sistema de dunas
            self.dune_renderer = DuneRenderer(self.screen_width, self.screen_height)

            # Sistema de efectos atmosféricos
            self.atmospheric_effects = AtmosphericEffects(
                self.screen_width, self.screen_height
            )

            self.logger.info("Sistemas de fondo de desierto inicializados")

        except Exception as e:
            self.logger.error("Error inicializando sistemas de desierto: %s", e)
            raise

    def update(self, delta_time: float):
        """
        Actualiza todos los sistemas del fondo de desierto.

        Args:
            delta_time: Tiempo transcurrido desde la última actualización
        """
        # Actualizar efectos atmosféricos
        self.atmospheric_effects.update(delta_time)

        # Obtener datos del viento para aplicar a las partículas
        wind_strength, wind_angle = self.atmospheric_effects.get_wind_data()
        self.particle_system.set_wind_effect(wind_strength, wind_angle)

        # Actualizar partículas
        self.particle_system.update(delta_time)

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """
        Renderiza el fondo completo del desierto.

        Args:
            screen: Superficie donde renderizar
            camera_offset: Offset de la cámara para efectos de parallax
        """
        # 1. Renderizar gradiente del cielo
        self.atmospheric_effects.render_sky_gradient(screen)

        # 2. Renderizar nubes de polvo en el horizonte
        self.atmospheric_effects.render_dust_clouds(screen, camera_offset)

        # 3. Renderizar dunas del fondo
        self.dune_renderer.render(screen, camera_offset)

        # 4. Renderizar efectos de las dunas (brillos)
        self.dune_renderer.render_dune_effects(screen, camera_offset)

        # 5. Renderizar efectos de viento
        self.atmospheric_effects.render_wind_effect(screen)

        # 6. Renderizar partículas de arena
        self.particle_system.render(screen, camera_offset)

        # 7. Renderizar efectos de calor (heat shimmer)
        self.atmospheric_effects.render_heat_shimmer(screen)

    # === MÉTODOS DE CONFIGURACIÓN ===

    def set_particle_count(self, count: int):
        """
        Configura el número de partículas de arena.

        Args:
            count: Número de partículas
        """
        self.particle_system.set_particle_count(count)

    def set_wind_parameters(self, strength: float, angle: float):
        """
        Configura los parámetros del viento.

        Args:
            strength: Fuerza del viento (0.0 - 1.0)
            angle: Ángulo del viento en radianes
        """
        self.atmospheric_effects.set_wind_parameters(strength, angle)

    def set_heat_shimmer_intensity(self, intensity: float):
        """
        Configura la intensidad del efecto de calor.

        Args:
            intensity: Intensidad del shimmer (0.0 - 1.0)
        """
        self.atmospheric_effects.set_heat_shimmer_strength(intensity)

    def add_dune(self, x: float, y: float, width: float, height: float):
        """
        Añade una nueva duna al sistema.

        Args:
            x: Posición X de la duna
            y: Posición Y de la duna
            width: Ancho de la duna
            height: Alto de la duna
        """
        return self.dune_renderer.add_dune(x, y, width, height)

    def regenerate_dunes(self):
        """Regenera todas las dunas del sistema."""
        self.dune_renderer.regenerate_dunes()

    # === MÉTODOS DE INFORMACIÓN ===

    def get_system_info(self) -> dict:
        """
        Obtiene información de todos los sistemas.

        Returns:
            Diccionario con información de los sistemas
        """
        return {
            "particle_count": len(self.particle_system.particles),
            "dune_count": self.dune_renderer.get_dune_count(),
            "wind_strength": self.atmospheric_effects.wind_strength,
            "wind_angle": self.atmospheric_effects.wind_angle,
            "heat_shimmer_strength": self.atmospheric_effects.heat_shimmer_strength,
        }

    def get_performance_metrics(self) -> dict:
        """
        Obtiene métricas de rendimiento del sistema.

        Returns:
            Diccionario con métricas de rendimiento
        """
        info = self.get_system_info()

        # Calcular carga estimada de rendering
        particle_load = info["particle_count"] * 0.1  # Factor estimado por partícula
        dune_load = info["dune_count"] * 0.5  # Factor estimado por duna
        effect_load = 1.0  # Carga base de efectos atmosféricos

        total_load = particle_load + dune_load + effect_load

        return {
            "total_rendering_load": total_load,
            "particle_load": particle_load,
            "dune_load": dune_load,
            "effect_load": effect_load,
            "performance_level": (
                "high" if total_load < 10 else "medium" if total_load < 20 else "low"
            ),
        }

    # === MÉTODOS DE OPTIMIZACIÓN ===

    def optimize_for_performance(self, target_fps: int = 60):
        """
        Optimiza el sistema para alcanzar el FPS objetivo.

        Args:
            target_fps: FPS objetivo para optimización
        """
        current_metrics = self.get_performance_metrics()

        if current_metrics["performance_level"] == "low":
            # Reducir partículas si el rendimiento es bajo
            current_particles = len(self.particle_system.particles)
            optimized_particles = max(20, int(current_particles * 0.7))
            self.set_particle_count(optimized_particles)

            # Reducir intensidad de efectos
            self.set_heat_shimmer_intensity(0.3)

            self.logger.info(
                "Sistema optimizado para rendimiento: %d partículas",
                optimized_particles,
            )

    def reset_to_defaults(self):
        """Resetea todos los sistemas a sus valores por defecto."""
        # Reinicializar sistemas
        self._init_systems()
        self.logger.info("Sistemas de desierto reseteados a valores por defecto")
