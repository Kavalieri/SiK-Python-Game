"""
Powerup Effects - Efectos y lógica de powerups
==============================================

Autor: SiK Team
Fecha: 2024
Descripción: Efectos y lógica de aplicación de powerups.
"""

import logging
import random

from .powerup_types import PowerupConfiguration, PowerupEffect, PowerupType


class PowerupEffects:
    """Manejador de efectos de powerups."""

    def __init__(self):
        """Inicializa el manejador de efectos."""
        self.logger = logging.getLogger(__name__)
        self.config = PowerupConfiguration()

    def create_effect(self, powerup_type: PowerupType) -> PowerupEffect:
        """
        Crea un efecto de powerup.

        Args:
            powerup_type: Tipo de powerup

        Returns:
            Efecto del powerup
        """
        config = self.config.get_config(powerup_type)
        return PowerupEffect(
            type=powerup_type,
            duration=config.get("duration", 0.0),
            value=config.get("value", 1.0),
            description=config.get("description", ""),
        )

    def apply_effect(self, player, effect: PowerupEffect):
        """
        Aplica un efecto de powerup al jugador.

        Args:
            player: Instancia del jugador
            effect: Efecto a aplicar
        """
        try:
            if effect.type == PowerupType.SPEED:
                self._apply_speed_effect(player, effect)
            elif effect.type == PowerupType.DAMAGE:
                self._apply_damage_effect(player, effect)
            elif effect.type == PowerupType.SHIELD:
                self._apply_shield_effect(player, effect)
            elif effect.type == PowerupType.RAPID_FIRE:
                self._apply_rapid_fire_effect(player, effect)
            elif effect.type == PowerupType.DOUBLE_SHOT:
                self._apply_double_shot_effect(player, effect)
            elif effect.type == PowerupType.HEALTH:
                self._apply_health_effect(player, effect)
            elif effect.type == PowerupType.SPREAD:
                self._apply_spread_effect(player, effect)
            elif effect.type == PowerupType.EXPLOSIVE:
                self._apply_explosive_effect(player, effect)
            elif effect.type == PowerupType.SHRAPNEL:
                self._apply_shrapnel_effect(player, effect)

            self.logger.info("Efecto %s aplicado al jugador", effect.type.value)

        except (AttributeError, ValueError) as e:
            self.logger.error("Error aplicando efecto %s: %s", effect.type.value, e)

    def _apply_speed_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de velocidad."""
        if hasattr(player, "speed_multiplier"):
            player.speed_multiplier = effect.value
        elif hasattr(player, "stats") and hasattr(player.stats, "speed"):
            player.stats.speed *= effect.value

    def _apply_damage_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de daño."""
        if hasattr(player, "damage_multiplier"):
            player.damage_multiplier = effect.value
        elif hasattr(player, "stats") and hasattr(player.stats, "damage"):
            player.stats.damage *= effect.value

    def _apply_shield_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de escudo."""
        if hasattr(player, "shield_active"):
            player.shield_active = True
            player.shield_duration = effect.duration

    def _apply_rapid_fire_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de fuego rápido."""
        if hasattr(player, "attack_speed_multiplier"):
            player.attack_speed_multiplier = effect.value
        elif hasattr(player, "stats") and hasattr(player.stats, "attack_speed"):
            player.stats.attack_speed *= effect.value

    def _apply_double_shot_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de disparo doble."""
        if hasattr(player, "projectile_count"):
            player.projectile_count = int(effect.value)

    def _apply_health_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de salud (instantáneo)."""
        if hasattr(player, "stats") and hasattr(player.stats, "health"):
            player.stats.health = min(
                player.stats.max_health, player.stats.health + effect.value
            )

    def _apply_spread_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de dispersión."""
        if hasattr(player, "spread_shot"):
            player.spread_shot = True
            player.spread_count = int(effect.value)

    def _apply_explosive_effect(self, player, effect: PowerupEffect):
        """Aplica efecto explosivo."""
        if hasattr(player, "explosive_projectiles"):
            player.explosive_projectiles = True
            player.explosion_radius = effect.value

    def _apply_shrapnel_effect(self, player, effect: PowerupEffect):
        """Aplica efecto de metralla."""
        if hasattr(player, "shrapnel_projectiles"):
            player.shrapnel_projectiles = True
            player.shrapnel_count = int(effect.value)

    def create_random_effect(self) -> PowerupEffect:
        """
        Crea un efecto aleatorio.

        Returns:
            Efecto de powerup aleatorio
        """
        powerup_type = random.choice(list(PowerupType))
        return self.create_effect(powerup_type)

    def is_instant_effect(self, effect: PowerupEffect) -> bool:
        """
        Verifica si un efecto es instantáneo.

        Args:
            effect: Efecto a verificar

        Returns:
            True si es instantáneo
        """
        return effect.duration <= 0.0
