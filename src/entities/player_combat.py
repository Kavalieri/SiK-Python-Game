"""
PlayerCombat - Sistema de Combate del Jugador (Facade Refactorizado)
================================================================

Autor: SiK Team
Fecha: 2024
Descripción: Facade principal que mantiene la interfaz original del sistema
de combate del jugador, simplificado para compatibilidad inmediata.
"""

import logging
from typing import Any, List, Tuple

from ..entities.powerup import PowerupType
from ..utils.config_manager import ConfigManager
from .player_effects import PlayerEffects
from .player_stats import PlayerStats
from .projectile import Projectile


class PlayerCombat:
    """
    Gestiona el sistema de combate del jugador - Facade refactorizado.

    Mantiene 100% compatibilidad con la interfaz original implementando
    funcionalidad básica directamente.
    """

    def __init__(
        self,
        player_stats: PlayerStats,
        player_effects: PlayerEffects,
        attack_configs: List[Any],
    ):
        """
        Inicializa el sistema de combate.

        Args:
            player_stats: Estadísticas del jugador
            player_effects: Efectos activos del jugador
            attack_configs: Configuraciones de ataques
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

        # Crear config básico para proyectiles
        self.config = ConfigManager()

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
        player_pos: Tuple[float, float],
        target_pos: Tuple[int, int],
        current_time: float,
    ) -> List[Projectile]:
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

        # Crear proyectil básico
        projectile = Projectile(
            x=player_x,
            y=player_y,
            target_x=target_x,
            target_y=target_y,
            damage=int(self.stats.bullet_damage),
            speed=self.stats.bullet_speed,
            config=self.config,
        )
        projectiles.append(projectile)

        self.last_shoot_time = current_time
        return projectiles

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
            self.logger.info("Jugador murió por daño de %s de %s", damage, source)
            return True

        self.logger.debug(
            "Jugador recibió %s de daño, vida restante: %s", damage, self.stats.health
        )
        return False

    def heal(self, amount: float):
        """Cura al jugador."""
        self.stats.heal(amount)
        self.logger.debug(
            "Jugador curado %s, vida actual: %s", amount, self.stats.health
        )

    def add_shield(self, amount: float):
        """Añade escudo al jugador."""
        self.stats.add_shield(amount)
        self.logger.debug(
            "Escudo añadido %s, escudo actual: %s", amount, self.stats.shield
        )

    def add_combo(self, amount: int = 1):
        """Añade puntos de combo."""
        self.stats.add_combo(amount)
        self.logger.debug(
            "Combo añadido %s, combo actual: %s", amount, self.stats.combo
        )

    def attack(
        self,
        player_core,
        target_pos: Tuple[int, int],
        current_time: float,
        enemies: List[Any],
    ) -> List[Any]:
        """
        Ejecuta un ataque del jugador.

        Args:
            player_core: Núcleo del jugador
            target_pos: Posición objetivo del ataque
            current_time: Tiempo actual del juego
            enemies: Lista de enemigos en el área

        Returns:
            Lista de resultados del ataque (proyectiles u otros efectos)
        """
        # Implementar lógica específica según el tipo de ataque y enemigos cercanos
        player_pos = (player_core.x, player_core.y)

        # Si hay múltiples enemigos cercanos, crear ataques adicionales
        if enemies and len(enemies) > 1:
            # Crear proyectil principal hacia el objetivo
            main_projectiles = self.shoot(player_pos, target_pos, current_time)

            # Crear proyectiles adicionales hacia enemigos cercanos (máximo 2 adicionales)
            additional_projectiles = []
            max_additional = min(2, len(enemies) - 1)

            for enemy in enemies[:max_additional]:
                if hasattr(enemy, "x") and hasattr(enemy, "y"):
                    enemy_pos = (enemy.x, enemy.y)
                    # Reducir daño de proyectiles adicionales
                    additional_projectiles.extend(
                        self.shoot(player_pos, enemy_pos, current_time)
                    )

            return main_projectiles + additional_projectiles
        else:
            # Ataque normal hacia la posición objetivo
            return self.shoot(player_pos, target_pos, current_time)

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
