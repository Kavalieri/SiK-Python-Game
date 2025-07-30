"""
CombatActions - Acciones de Combate del Jugador
=============================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de acciones de combate para ataques cuerpo a cuerpo,
a distancia y en área.
"""

import math
from typing import List

import pygame

from ..entities.powerup import PowerupType
from ..entities.projectile import Projectile
from ..utils.config_manager import ConfigManager


class CombatActions:
    """Sistema de acciones de combate del jugador."""

    def __init__(self, config: ConfigManager):
        """
        Inicializa el sistema de acciones de combate.

        Args:
            config: Gestor de configuración
        """
        self.config = config
        self.melee_range = 80
        self.area_attack_range = 120

    def execute_melee_attack(
        self,
        player_rect: pygame.Rect,
        enemies: List,
        damage: int,
        direction: str = "right",
    ) -> List:
        """
        Ejecuta un ataque cuerpo a cuerpo.

        Args:
            player_rect: Rectángulo del jugador
            enemies: Lista de enemigos
            damage: Daño del ataque
            direction: Dirección del ataque

        Returns:
            Lista de enemigos dañados
        """
        damaged_enemies = []

        # Calcular área de ataque según dirección
        attack_rect = self._calculate_melee_area(player_rect, direction)

        for enemy in enemies:
            if hasattr(enemy, "rect") and attack_rect.colliderect(enemy.rect):
                if hasattr(enemy, "take_damage"):
                    enemy.take_damage(damage)
                    damaged_enemies.append(enemy)

        return damaged_enemies

    def execute_area_attack(
        self, player_rect: pygame.Rect, enemies: List, damage: int, powerup_effects=None
    ) -> List:
        """
        Ejecuta un ataque en área.

        Args:
            player_rect: Rectángulo del jugador
            enemies: Lista de enemigos
            damage: Daño base del ataque
            powerup_effects: Efectos de powerups activos

        Returns:
            Lista de enemigos dañados
        """
        damaged_enemies = []

        # Aumentar rango si hay powerup
        attack_range = self.area_attack_range
        if powerup_effects and powerup_effects.has_effect(PowerupType.DAMAGE):
            attack_range *= 1.5
            damage = int(damage * 1.3)

        player_center = player_rect.center

        for enemy in enemies:
            if hasattr(enemy, "rect"):
                enemy_center = enemy.rect.center
                distance = math.sqrt(
                    (player_center[0] - enemy_center[0]) ** 2
                    + (player_center[1] - enemy_center[1]) ** 2
                )

                if distance <= attack_range:
                    if hasattr(enemy, "take_damage"):
                        # Daño decrece con distancia
                        distance_factor = max(0.3, 1.0 - (distance / attack_range))
                        final_damage = int(damage * distance_factor)
                        enemy.take_damage(final_damage)
                        damaged_enemies.append(enemy)

        return damaged_enemies

    def execute_ranged_attack(
        self,
        projectile_system,
        player_x: float,
        player_y: float,
        target_x: float,
        target_y: float,
        damage: int,
        speed: float,
    ) -> List[Projectile]:
        """
        Ejecuta un ataque a distancia creando proyectiles.

        Args:
            projectile_system: Sistema de proyectiles
            player_x: Posición X del jugador
            player_y: Posición Y del jugador
            target_x: Posición X del objetivo
            target_y: Posición Y del objetivo
            damage: Daño del proyectil
            speed: Velocidad del proyectil

        Returns:
            Lista de proyectiles creados
        """
        return projectile_system.create_projectiles(
            player_x, player_y, target_x, target_y, damage, speed
        )

    def _calculate_melee_area(
        self, player_rect: pygame.Rect, direction: str
    ) -> pygame.Rect:
        """
        Calcula el área de ataque cuerpo a cuerpo.

        Args:
            player_rect: Rectángulo del jugador
            direction: Dirección del ataque

        Returns:
            Rectángulo del área de ataque
        """
        if direction == "right":
            return pygame.Rect(
                player_rect.right,
                player_rect.top - 10,
                self.melee_range,
                player_rect.height + 20,
            )
        elif direction == "left":
            return pygame.Rect(
                player_rect.left - self.melee_range,
                player_rect.top - 10,
                self.melee_range,
                player_rect.height + 20,
            )
        elif direction == "up":
            return pygame.Rect(
                player_rect.left - 10,
                player_rect.top - self.melee_range,
                player_rect.width + 20,
                self.melee_range,
            )
        elif direction == "down":
            return pygame.Rect(
                player_rect.left - 10,
                player_rect.bottom,
                player_rect.width + 20,
                self.melee_range,
            )
        else:
            # Por defecto, ataque hacia la derecha
            return pygame.Rect(
                player_rect.right,
                player_rect.top - 10,
                self.melee_range,
                player_rect.height + 20,
            )
