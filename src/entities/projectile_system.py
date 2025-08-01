"""
ProjectileSystem - Sistema de Proyectiles del Jugador
===================================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema especializado para la creación y gestión de proyectiles.
"""

import math
import time

from ..entities.powerup import PowerupType
from ..entities.projectile import Projectile
from ..utils.config_manager import ConfigManager


class ProjectileSystem:
    """Sistema especializado para la creación y gestión de proyectiles del jugador."""

    def __init__(self, config: ConfigManager, effects):
        self.config = config
        self.effects = effects
        self.last_shoot_time = 0
        self.shoot_cooldown = 0.2

    def can_shoot(self) -> bool:
        """Verifica si el jugador puede disparar."""
        current_time = time.time()
        return current_time - self.last_shoot_time >= self.shoot_cooldown

    def create_projectiles(
        self,
        player_x: float,
        player_y: float,
        target_x: float,
        target_y: float,
        bullet_damage: int,
        bullet_speed: float,
    ) -> list[Projectile]:
        """Crea proyectiles según las configuraciones y powerups activos."""
        if not self.can_shoot():
            return []

        current_time = time.time()
        projectiles = []

        # Crear proyectil base
        projectile = Projectile(
            x=player_x,
            y=player_y,
            target_x=target_x,
            target_y=target_y,
            damage=bullet_damage,
            speed=bullet_speed,
            config=self.config,
        )
        projectiles.append(projectile)

        # Aplicar efectos especiales si están activos
        if self.effects.has_effect(PowerupType.DOUBLE_SHOT):
            projectiles.extend(
                self._create_double_shot(
                    player_x, player_y, target_x, target_y, bullet_speed, bullet_damage
                )
            )
        elif self.effects.has_effect(PowerupType.SPREAD):
            projectiles.extend(
                self._create_spread_shot(
                    player_x, player_y, target_x, target_y, bullet_speed, bullet_damage
                )
            )

        self.last_shoot_time = current_time
        return projectiles

    def _create_double_shot(
        self,
        x: float,
        y: float,
        target_x: float,
        target_y: float,
        speed: float,
        damage: float,
    ) -> list[Projectile]:
        """Crea un disparo doble."""
        projectiles = []
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            dx /= distance
            dy /= distance
            offset = 15
            perp_x = -dy * offset
            perp_y = dx * offset

            # Proyectiles con offset
            for offset_mult in [1, -1]:
                projectile = Projectile(
                    x=x + perp_x * offset_mult,
                    y=y + perp_y * offset_mult,
                    target_x=target_x,
                    target_y=target_y,
                    damage=damage,
                    speed=speed,
                    config=self.config,
                )
                projectiles.append(projectile)

        return projectiles

    def _create_spread_shot(
        self,
        x: float,
        y: float,
        target_x: float,
        target_y: float,
        speed: float,
        damage: float,
    ) -> list[Projectile]:
        """Crea un disparo en abanico."""
        projectiles = []
        base_angle = math.atan2(target_y - y, target_x - x)
        angles = [base_angle - 0.3, base_angle, base_angle + 0.3]  # ±17 grados

        for angle in angles:
            distance = 500
            proj_target_x = x + math.cos(angle) * distance
            proj_target_y = y + math.sin(angle) * distance

            projectile = Projectile(
                x=x,
                y=y,
                target_x=proj_target_x,
                target_y=proj_target_y,
                damage=damage * 0.7,
                speed=speed,
                config=self.config,
            )
            projectiles.append(projectile)

        return projectiles
