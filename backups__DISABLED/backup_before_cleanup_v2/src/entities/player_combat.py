"""
Player Combat - Sistema de Combate del Jugador
=============================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que maneja el sistema de combate del jugador (disparos, daño, etc.).
"""

import pygame
import logging
import math
from typing import Optional, Tuple, List
from .projectile import Projectile
from .player_stats import PlayerStats
from .player_effects import PlayerEffects
from ..entities.powerup import PowerupType


class PlayerCombat:
    """
    Gestiona el sistema de combate del jugador.
    """
    
    def __init__(self, player_stats: PlayerStats, player_effects: PlayerEffects):
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
        fire_rate_boost = self.effects.get_effect_value(PowerupType.FIRE_RATE)
        modified_shoot_speed = max(0.05, base_shoot_speed - fire_rate_boost)
        
        return current_time - self.last_shoot_time >= modified_shoot_speed
    
    def shoot(self, player_pos: Tuple[float, float], target_pos: Tuple[int, int], current_time: float) -> List[Projectile]:
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
            projectiles.extend(self._create_double_shot(player_x, player_y, dx, dy, bullet_speed, bullet_damage))
        elif self.effects.has_effect(PowerupType.SPREAD):
            # Disparo disperso
            projectiles.extend(self._create_spread_shot(player_x, player_y, dx, dy, bullet_speed, bullet_damage))
        else:
            # Disparo normal
            projectile = Projectile(
                x=player_x,
                y=player_y,
                dx=dx * bullet_speed,
                dy=dy * bullet_speed,
                damage=bullet_damage,
                speed=bullet_speed
            )
            projectiles.append(projectile)
        
        # Actualizar timer
        self.last_shoot_time = current_time
        
        return projectiles
    
    def _create_double_shot(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float) -> List[Projectile]:
        """Crea un disparo doble."""
        projectiles = []
        
        # Disparo principal
        projectile1 = Projectile(
            x=x + dx * 10,  # Ligeramente separado
            y=y + dy * 10,
            dx=dx * speed,
            dy=dy * speed,
            damage=damage,
            speed=speed
        )
        
        # Disparo secundario
        projectile2 = Projectile(
            x=x - dx * 10,  # Ligeramente separado
            y=y - dy * 10,
            dx=dx * speed,
            dy=dy * speed,
            damage=damage,
            speed=speed
        )
        
        projectiles.extend([projectile1, projectile2])
        return projectiles
    
    def _create_spread_shot(self, x: float, y: float, dx: float, dy: float, speed: float, damage: float) -> List[Projectile]:
        """Crea un disparo disperso."""
        projectiles = []
        spread_angle = 0.3  # Ángulo de dispersión en radianes
        
        # Disparo central
        projectile_center = Projectile(
            x=x, y=y,
            dx=dx * speed, dy=dy * speed,
            damage=damage, speed=speed
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
                x=x, y=y,
                dx=new_dx * speed, dy=new_dy * speed,
                damage=damage * 0.7, speed=speed  # Menos daño en disparos laterales
            )
            projectiles.append(projectile)
        
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
            self.logger.info(f"Jugador murió por daño de {damage} de {source}")
            return True
        
        self.logger.debug(f"Jugador recibió {damage} de daño, vida restante: {self.stats.health}")
        return False
    
    def heal(self, amount: float):
        """Cura al jugador."""
        self.stats.heal(amount)
        self.logger.debug(f"Jugador curado {amount}, vida actual: {self.stats.health}")
    
    def add_shield(self, amount: float):
        """Añade escudo al jugador."""
        self.stats.add_shield(amount)
        self.logger.debug(f"Escudo añadido {amount}, escudo actual: {self.stats.shield}")
    
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
            'health': self.stats.health,
            'max_health': self.stats.max_health,
            'shield': self.stats.shield,
            'max_shield': self.stats.max_shield,
            'combo': self.stats.combo,
            'max_combo': self.stats.max_combo,
            'bullet_damage': self.stats.bullet_damage,
            'bullet_speed': self.stats.bullet_speed,
            'shoot_speed': self.stats.shoot_speed
        } 