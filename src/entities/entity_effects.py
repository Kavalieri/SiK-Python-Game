"""
Entity Effects - Sistema de Efectos y Estados Especiales
=======================================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestión de efectos, invulnerabilidad y estados especiales para entidades.
"""

import logging
import time
from typing import Any

import pygame

from .entity_types import EntityState


class EntityEffectsSystem:
    """Sistema de gestión de efectos para entidades."""

    def __init__(self, entity_instance):
        """
        Inicializa el sistema de efectos.

        Args:
            entity_instance: Instancia de la entidad propietaria
        """
        self.entity = entity_instance
        self.effects = {}
        self.invulnerable_timer = 0.0
        self.logger = logging.getLogger(f"{entity_instance.__class__.__name__}Effects")

    @property
    def is_invulnerable(self) -> bool:
        """Verifica si la entidad es invulnerable."""
        return (
            self.invulnerable_timer > 0.0
            or self.entity.state == EntityState.INVULNERABLE
        )

    def update_effects(self, delta_time: float):
        """Actualiza todos los efectos aplicados."""
        self._update_effect_durations(delta_time)
        self._update_invulnerability(delta_time)

    def _update_effect_durations(self, delta_time: float):
        """Actualiza las duraciones de efectos activos."""
        if isinstance(self.effects, dict):
            effects_to_remove = []

            for effect_name, effect_data in self.effects.items():
                effect_data["duration"] -= delta_time

                if effect_data["duration"] <= 0:
                    effects_to_remove.append(effect_name)
                    self._remove_effect(effect_name)

            for effect_name in effects_to_remove:
                del self.effects[effect_name]
        elif hasattr(self.effects, "update_effects"):
            current_time = time.time()
            self.effects.update_effects(current_time)

    def _update_invulnerability(self, delta_time: float):
        """Actualiza el estado de invulnerabilidad."""
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= delta_time

            if self.invulnerable_timer <= 0:
                self.entity.state = EntityState.IDLE
                self.invulnerable_timer = 0.0

    def add_effect(self, effect_name: str, effect_data: dict[str, Any]):
        """
        Añade un efecto a la entidad.

        Args:
            effect_name: Nombre del efecto
            effect_data: Datos del efecto (duration, value, etc.)
        """
        self.effects[effect_name] = effect_data
        self.logger.debug("Efecto %s añadido", effect_name)

    def _remove_effect(self, effect_name: str):
        """
        Remueve un efecto de la entidad.

        Args:
            effect_name: Nombre del efecto a remover
        """
        self.logger.debug("Efecto %s removido", effect_name)

    def apply_invulnerability(self, duration: float = 0.5):
        """
        Aplica invulnerabilidad temporal.

        Args:
            duration: Duración en segundos
        """
        self.invulnerable_timer = duration

    def take_damage(self, damage: float, source=None) -> bool:
        """
        Procesa el daño recibido.

        Args:
            damage: Cantidad de daño
            source: Fuente del daño (opcional)

        Returns:
            True si el daño fue aplicado
        """
        if self.is_invulnerable:
            return False

        # Aplicar armadura
        actual_damage = max(0, damage - self.entity.stats.armor)
        self.entity.stats.health -= actual_damage

        self.logger.debug(
            "Daño aplicado: %s. Vida restante: %s",
            actual_damage,
            self.entity.stats.health,
        )

        # Cambiar estado y aplicar invulnerabilidad
        if self.entity.stats.health <= 0:
            self.entity.die()
        else:
            self.entity.state = EntityState.HURT
            self.apply_invulnerability()

        if source:
            self.logger.debug("Daño recibido de %s", source)

        return True

    def render_visual_effects(
        self, screen: pygame.Surface, x: float, y: float, width: int, height: int
    ):
        """
        Renderiza efectos visuales.

        Args:
            screen: Superficie de renderizado
            x, y: Posición
            width, height: Dimensiones
        """
        # Efecto de invulnerabilidad (parpadeo)
        if self.is_invulnerable and int(pygame.time.get_ticks() / 100) % 2:
            overlay = pygame.Surface((width, height))
            overlay.set_alpha(128)
            overlay.fill((255, 255, 255))
            screen.blit(overlay, (x, y))

    def get_effects_data(self) -> dict[str, Any]:
        """Obtiene datos de efectos para guardado."""
        return {
            "effects": self.effects.copy(),
            "invulnerable_timer": self.invulnerable_timer,
        }

    def load_effects_data(self, data: dict[str, Any]):
        """Carga datos de efectos."""
        self.effects = data.get("effects", {}).copy()
        self.invulnerable_timer = data.get("invulnerable_timer", 0.0)
