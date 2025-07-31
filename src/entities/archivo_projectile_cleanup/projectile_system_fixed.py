"""
ProjectileSystem - Sistema de Proyectiles del Jugador
===================================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema especializado para la creación y gestión de proyectiles.
"""

import math
import time
from typing import List

from ..entities.projectile import Projectile
from ..entities.powerup import PowerupType
from ..utils.config_manager import ConfigManager


class ProjectileSystem:
    """Sistema especializado para la creación y gestión de proyectiles del jugador."""

    def __init__(self, config: ConfigManager, effects):
        """
        Inicializa el sistema de proyectiles.

        Args:
            config: Gestor de configuración
            effects: Sistema de efectos/powerups
        """
        self.config = config
        self.effects = effects
        self.last_shoot_time = 0
        self.shoot_cooldown = 0.2  # 200ms entre disparos

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
    ) -> List[Projectile]:
        """
        Crea proyectiles según las configuraciones y powerups activos.

        Args:
            player_x: Posición X del jugador
            player_y: Posición Y del jugador
            target_x: Posición X del objetivo
            target_y: Posición Y del objetivo
            bullet_damage: Daño base del proyectil
            bullet_speed: Velocidad base del proyectil

        Returns:
            Lista de proyectiles creados
        """
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

        # Actualizar timer
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
    ) -> List[Projectile]:
        """Crea un disparo doble."""
        projectiles = []

        # Calcular vector dirección
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            # Normalizar
            dx /= distance
            dy /= distance

            # Crear offset perpendicular
            offset = 15
            perp_x = -dy * offset
            perp_y = dx * offset

            # Proyectil 1 (offset izquierdo)
            projectile1 = Projectile(
                x=x + perp_x,
                y=y + perp_y,
                target_x=target_x,
                target_y=target_y,
                damage=damage,
                speed=speed,
                config=self.config,
            )
            projectiles.append(projectile1)

            # Proyectil 2 (offset derecho)
            projectile2 = Projectile(
                x=x - perp_x,
                y=y - perp_y,
                target_x=target_x,
                target_y=target_y,
                damage=damage,
                speed=speed,
                config=self.config,
            )
            projectiles.append(projectile2)

        return projectiles

    def _create_spread_shot(
        self,
        x: float,
        y: float,
        target_x: float,
        target_y: float,
        speed: float,
        damage: float,
    ) -> List[Projectile]:
        """Crea un disparo en abanico."""
        projectiles = []

        # Calcular ángulo base hacia el target
        base_angle = math.atan2(target_y - y, target_x - x)

        # Crear 3 proyectiles en abanico
        angles = [base_angle - 0.3, base_angle, base_angle + 0.3]  # ±17 grados

        for angle in angles:
            # Calcular target para este ángulo
            distance = 500  # Distancia de proyección
            proj_target_x = x + math.cos(angle) * distance
            proj_target_y = y + math.sin(angle) * distance

            projectile = Projectile(
                x=x,
                y=y,
                target_x=proj_target_x,
                target_y=proj_target_y,
                damage=damage * 0.7,  # Menos daño por dispersión
                speed=speed,
                config=self.config,
            )
            projectiles.append(projectile)

        return projectiles
