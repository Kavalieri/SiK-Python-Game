"""
Powerup System - Sistema de Powerups (FACHADA)
==============================================

Autor: SiK Team
Fecha: 2024
Descripción: Fachada del sistema modular de powerups.
Mantiene API original para compatibilidad con delegación a módulos especializados.
"""

import logging
import random

import pygame

from .entity import Entity, EntityStats, EntityType
from .powerup_effects import PowerupEffects
from .powerup_renderer import PowerupRenderer
from .powerup_types import PowerupConfiguration, PowerupEffect, PowerupType


class Powerup(Entity):
    """
    Powerup que mejora temporalmente al jugador (FACHADA).
    Mantiene 100% compatibilidad con API original.
    """

    # Configuración para compatibilidad
    POWERUP_CONFIGS = PowerupConfiguration.POWERUP_CONFIGS

    def __init__(self, x: float, y: float, powerup_type: PowerupType):
        """
        Inicializa un powerup modular.

        Args:
            x: Posición X
            y: Posición Y
            powerup_type: Tipo de powerup
        """
        # Crear estadísticas básicas
        stats = EntityStats(
            health=1.0,
            max_health=1.0,
            speed=0.0,
            damage=0.0,
            armor=0.0,
            attack_speed=0.0,
            attack_range=0.0,
        )

        super().__init__(
            entity_type=EntityType.POWERUP, x=x, y=y, width=30, height=30, stats=stats
        )

        self.powerup_type = powerup_type
        self.logger = logging.getLogger(__name__)

        # Inicializar módulos especializados
        self.config_manager = PowerupConfiguration()
        self.effects_manager = PowerupEffects()
        self.renderer = PowerupRenderer(powerup_type, self.width, self.height)

        # Propiedades para compatibilidad
        self.config = self.config_manager.get_config(powerup_type)
        self.sprite = self.renderer.get_sprite()

        # Efecto de flotación (delegado a renderer)
        self.float_offset = 0
        self.float_speed = 2.0

        # Debug flag para renderizado de información adicional
        self.debug = False

    def update(self, delta_time: float):
        """Actualiza el powerup."""
        super().update(delta_time)

        # Actualizar animación de flotación
        self.renderer.update_animation(delta_time)

        # Sincronizar para compatibilidad
        self.float_offset = self.renderer.float_offset

    def _update_logic(self, delta_time: float):
        """Actualiza la lógica específica del powerup."""
        # Actualizar animación mediante el renderer
        self.renderer.update_animation(delta_time)

    def render(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Renderiza el powerup con efecto de flotación."""
        if not self.is_alive:
            return

        # Delegar renderizado al renderer
        self.renderer.render(screen, self.x, self.y, camera_offset)

        # Debug si está habilitado
        if hasattr(self, "debug") and self.debug:
            self.renderer.render_debug(screen, self.x, self.y, camera_offset)

    def get_effect(self) -> PowerupEffect:
        """Obtiene el efecto del powerup."""
        return self.effects_manager.create_effect(self.powerup_type)

    def get_current_frame(self):
        """
        Obtiene el frame actual del sprite del powerup.

        Returns:
            pygame.Surface: Surface del sprite actual del powerup
        """
        # Actualizar sprite a través del renderer
        self.sprite = self.renderer.get_sprite()
        return self.sprite

    # Métodos de compatibilidad con API original
    def _setup_sprite(self):
        """Delegado al renderer para compatibilidad."""
        # El renderer ya maneja esto
        self.sprite = self.renderer.get_sprite()

    def _get_symbol(self) -> str:
        """Delegado a la configuración para compatibilidad."""
        return self.config_manager.get_symbol(self.powerup_type)

    @classmethod
    def create_random(cls, x: float, y: float) -> "Powerup":
        """
        Crea un powerup aleatorio.

        Args:
            x: Posición X
            y: Posición Y

        Returns:
            Powerup aleatorio
        """
        powerup_type = random.choice(list(PowerupType))
        return cls(x, y, powerup_type)

    @classmethod
    def get_all_types(cls) -> list:
        """Obtiene todos los tipos de powerups disponibles."""
        return PowerupConfiguration.get_all_types()

    # Propiedades para mantener compatibilidad
    @property
    def color(self) -> tuple:
        """Color del powerup para compatibilidad."""
        return self.renderer.get_color()

    @property
    def symbol(self) -> str:
        """Símbolo del powerup para compatibilidad."""
        return self.config_manager.get_symbol(self.powerup_type)

    @property
    def name(self) -> str:
        """Nombre del powerup para compatibilidad."""
        return self.config.get("name", "Desconocido")

    @property
    def duration(self) -> float:
        """Duración del powerup para compatibilidad."""
        return self.config.get("duration", 0.0)

    @property
    def value(self) -> float:
        """Valor del powerup para compatibilidad."""
        return self.config.get("value", 1.0)

    @property
    def description(self) -> str:
        """Descripción del powerup para compatibilidad."""
        return self.config.get("description", "")
