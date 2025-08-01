"""
Player Combat - Sistema de Combate del Jugador
=============================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que maneja el sistema de combate del jugador (disparos, daño, etc.).
"""

import logging
import math
from typing import Any

import pygame

from ..entities.powerup import PowerupType
from .player_effects import PlayerEffects
from .player_stats import PlayerStats
from .projectile import Projectile


class AttackConfig:
    """
    Configuración de un ataque (melee, ranged, area, etc.)
    """

    def __init__(self, data: dict[str, Any]):
        self.nombre = data.get("nombre", "")
        self.tipo = data.get("tipo", "melee")
        self.daño = data.get("daño", 0)
        self.alcance = data.get("alcance", 0)
        self.cooldown = data.get("cooldown", 1.0)
        self.animacion = data.get("animacion", "Attack")
        self.sonido = data.get("sonido", None)
        self.efectos = data.get("efectos", [])
        self.hitbox = data.get("hitbox", None)
        self.proyectil = data.get("proyectil", None)
        self.area = data.get("area", None)


class Attack:
    """
    Instancia de un ataque en ejecución.
    """

    def __init__(self, config: AttackConfig, owner, target_pos: tuple[int, int]):
        self.config = config
        self.owner = owner
        self.target_pos = target_pos
        self.cooldown_timer = 0.0
        self.active = True


class PlayerCombat:
    """
    Gestiona el sistema de combate del jugador.
    """

    def __init__(
        self,
        player_stats: PlayerStats,
        player_effects: PlayerEffects,
        attack_configs: list[AttackConfig],
    ):
        """
        Inicializa el sistema de combate.

        Args:
            player_stats: Estadísticas del jugador
            player_effects: Efectos activos del jugador
        """
        self.stats = player_stats
        self.effects = player_effects
        self.logger = logging.getLogger(__name__)

        # Timers de combate
        self.shoot_timer = 0.0
        self.last_shoot_time = 0.0
        self.attack_configs = attack_configs
        self.current_attack_index = 0
        self.last_attack_time = 0.0

    def can_shoot(self, current_time: float) -> bool:
        """
        Verifica si el jugador puede disparar.

        Args:
            current_time: Tiempo actual del juego

        Returns:
            True si puede disparar
        """
        # Obtener velocidad de disparo modificada por efectos
        base_shoot_speed = self.stats.shoot_speed
        fire_rate_boost = self.effects.get_effect_value(PowerupType.RAPID_FIRE)
        modified_shoot_speed = max(0.05, base_shoot_speed - fire_rate_boost)

        return current_time - self.last_shoot_time >= modified_shoot_speed

    def shoot(
        self,
        player_pos: tuple[float, float],
        target_pos: tuple[int, int],
        current_time: float,
    ) -> list[Projectile]:
        """
        Crea proyectiles según el tipo de disparo activo.

        Args:
            player_pos: Posición del jugador (x, y)
            target_pos: Posición objetivo del ratón (x, y)
            current_time: Tiempo actual del juego

        Returns:
            Lista de proyectiles creados
        """
        if not self.can_shoot(current_time):
            return []

        projectiles = []
        player_x, player_y = player_pos
        target_x, target_y = target_pos

        # Calcular dirección del disparo
        dx = target_x - player_x
        dy = target_y - player_y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return []

        # Normalizar dirección
        dx /= distance
        dy /= distance

        # Obtener estadísticas modificadas por efectos
        bullet_speed = self.stats.bullet_speed
        bullet_damage = self.stats.bullet_damage

        # Aplicar modificadores de efectos
        damage_boost = self.effects.get_effect_value(PowerupType.DAMAGE)
        bullet_damage += damage_boost

        # Verificar tipo de disparo
        if self.effects.has_effect(PowerupType.DOUBLE_SHOT):
            # Disparo doble
            projectiles.extend(
                self._create_double_shot(
                    player_x, player_y, dx, dy, bullet_speed, bullet_damage
                )
            )
        elif self.effects.has_effect(PowerupType.SPREAD):
            # Disparo disperso
            projectiles.extend(
                self._create_spread_shot(
                    player_x, player_y, dx, dy, bullet_speed, bullet_damage
                )
            )
        else:
            # Disparo normal
            projectile = Projectile(
                x=player_x,
                y=player_y,
                dx=dx * bullet_speed,
                dy=dy * bullet_speed,
                damage=bullet_damage,
                speed=bullet_speed,
            )
            projectiles.append(projectile)

        # Actualizar timer
        self.last_shoot_time = current_time

        return projectiles

    def _create_double_shot(
        self, x: float, y: float, dx: float, dy: float, speed: float, damage: float
    ) -> list[Projectile]:
        """Crea un disparo doble."""
        projectiles = []

        # Disparo principal
        projectile1 = Projectile(
            x=x + dx * 10,  # Ligeramente separado
            y=y + dy * 10,
            dx=dx * speed,
            dy=dy * speed,
            damage=damage,
            speed=speed,
        )

        # Disparo secundario
        projectile2 = Projectile(
            x=x - dx * 10,  # Ligeramente separado
            y=y - dy * 10,
            dx=dx * speed,
            dy=dy * speed,
            damage=damage,
            speed=speed,
        )

        projectiles.extend([projectile1, projectile2])
        return projectiles

    def _create_spread_shot(
        self, x: float, y: float, dx: float, dy: float, speed: float, damage: float
    ) -> list[Projectile]:
        """Crea un disparo disperso."""
        projectiles = []
        spread_angle = 0.3  # Ángulo de dispersión en radianes

        # Disparo central
        projectile_center = Projectile(
            x=x, y=y, dx=dx * speed, dy=dy * speed, damage=damage, speed=speed
        )
        projectiles.append(projectile_center)

        # Disparos laterales
        for i in range(2):
            angle_offset = (i + 1) * spread_angle * (1 if i == 0 else -1)

            # Rotar dirección
            cos_offset = math.cos(angle_offset)
            sin_offset = math.sin(angle_offset)

            new_dx = dx * cos_offset - dy * sin_offset
            new_dy = dx * sin_offset + dy * cos_offset

            projectile = Projectile(
                x=x,
                y=y,
                dx=new_dx * speed,
                dy=new_dy * speed,
                damage=damage * 0.7,
                speed=speed,  # Menos daño en disparos laterales
            )
            projectiles.append(projectile)

        return projectiles

    def can_attack(self, current_time: float) -> bool:
        attack = self.attack_configs[self.current_attack_index]
        return current_time - self.last_attack_time >= attack.cooldown

    def attack(
        self,
        owner,
        target_pos: tuple[int, int],
        current_time: float,
        enemies: list[Any],
    ) -> list[Any]:
        """
        Ejecuta el ataque actual según el tipo (melee, ranged, area).
        Devuelve lista de entidades afectadas o proyectiles creados.
        """
        attack_cfg = self.attack_configs[self.current_attack_index]
        results = []
        if not self.can_attack(current_time):
            return results
        if attack_cfg.tipo == "melee":
            # Crear hitbox delante del jugador
            hitbox = self._get_melee_hitbox(owner, attack_cfg)
            for enemy in enemies:
                if self._collides(hitbox, enemy):
                    enemy.take_damage(attack_cfg.daño)
                    results.append(enemy)
            self.last_attack_time = current_time
        elif attack_cfg.tipo == "ranged":
            # Crear proyectil
            from .projectile import Projectile

            proj_cfg = attack_cfg.proyectil or {}
            projectile = Projectile(
                x=owner.x,
                y=owner.y,
                target_x=target_pos[0],
                target_y=target_pos[1],
                damage=attack_cfg.daño,
                speed=proj_cfg.get("velocidad", self.stats.bullet_speed),
                config=owner.config,
            )
            results.append(projectile)
            self.last_attack_time = current_time
        elif attack_cfg.tipo == "area":
            # Ataque de área (por radio)
            area_cfg = attack_cfg.area or {"radio": attack_cfg.alcance}
            for enemy in enemies:
                if self._in_area(owner, enemy, area_cfg["radio"]):
                    enemy.take_damage(attack_cfg.daño)
                    results.append(enemy)
            self.last_attack_time = current_time
        # ... otros tipos futuros ...
        return results

    def _get_melee_hitbox(self, owner, attack_cfg: AttackConfig):
        # Calcula la hitbox del ataque melee según orientación
        offset_x = attack_cfg.hitbox.get("offset_x", 0) if attack_cfg.hitbox else 0
        offset_y = attack_cfg.hitbox.get("offset_y", 0) if attack_cfg.hitbox else 0
        ancho = attack_cfg.hitbox.get("ancho", 40) if attack_cfg.hitbox else 40
        alto = attack_cfg.hitbox.get("alto", 40) if attack_cfg.hitbox else 40
        x = owner.x + (offset_x if owner.facing_right else -offset_x - ancho)
        y = owner.y + offset_y
        return pygame.Rect(x, y, ancho, alto)

    def _collides(self, rect: pygame.Rect, entity) -> bool:
        # Comprueba colisión entre la hitbox y la entidad
        if hasattr(entity, "rect"):
            return rect.colliderect(entity.rect)
        return False

    def _in_area(self, owner, entity, radio: float) -> bool:
        # Comprueba si la entidad está dentro del radio de área
        dx = entity.x - owner.x
        dy = entity.y - owner.y
        return (dx * dx + dy * dy) <= radio * radio

    def take_damage(self, damage: float, source=None) -> bool:
        """
        Aplica daño al jugador.

        Args:
            damage: Cantidad de daño
            source: Fuente del daño (opcional)

        Returns:
            True si el jugador murió
        """
        # Aplicar daño al escudo primero
        remaining_damage = self.stats.take_shield_damage(damage)

        # Aplicar daño restante a la vida
        if remaining_damage > 0:
            self.stats.health -= remaining_damage

        # Reiniciar combo al recibir daño
        self.stats.reset_combo()

        # Verificar si murió
        if self.stats.health <= 0:
            self.stats.health = 0
            self.logger.info(f"Jugador murió por daño de {damage} de {source}")
            return True

        self.logger.debug(
            f"Jugador recibió {damage} de daño, vida restante: {self.stats.health}"
        )
        return False

    def heal(self, amount: float):
        """Cura al jugador."""
        self.stats.heal(amount)
        self.logger.debug(f"Jugador curado {amount}, vida actual: {self.stats.health}")

    def add_shield(self, amount: float):
        """Añade escudo al jugador."""
        self.stats.add_shield(amount)
        self.logger.debug(
            f"Escudo añadido {amount}, escudo actual: {self.stats.shield}"
        )

    def add_combo(self, amount: int = 1):
        """Añade puntos de combo."""
        self.stats.add_combo(amount)
        self.logger.debug(f"Combo añadido {amount}, combo actual: {self.stats.combo}")

    def get_combat_stats(self) -> dict:
        """
        Obtiene estadísticas de combate actuales.

        Returns:
            Diccionario con estadísticas de combate
        """
        return {
            "health": self.stats.health,
            "max_health": self.stats.max_health,
            "shield": self.stats.shield,
            "max_shield": self.stats.max_shield,
            "combo": self.stats.combo,
            "max_combo": self.stats.max_combo,
            "bullet_damage": self.stats.bullet_damage,
            "bullet_speed": self.stats.bullet_speed,
            "shoot_speed": self.stats.shoot_speed,
        }
