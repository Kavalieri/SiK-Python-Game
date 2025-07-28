"""
Player - Jugador del juego
=========================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Clase principal del jugador que coordina todos los sistemas.
"""

import pygame
import logging
from typing import Optional, Tuple, List
from enum import Enum

from .entity import Entity, EntityType, EntityState
from .player_stats import PlayerStats
from .player_effects import PlayerEffects
from .player_combat import PlayerCombat
from ..utils.animation_manager import IntelligentAnimationManager
from ..utils.config_manager import ConfigManager
from ..entities.character_data import CHARACTER_DATA
from ..entities.powerup import PowerupEffect, PowerupType


class AnimationState(Enum):
    """Estados de animación del jugador."""
    IDLE = "Idle"
    RUN = "Run"
    WALK = "Walk"
    ATTACK = "Attack"
    DEAD = "Dead"
    SHOOT = "Shoot"


class Player(Entity):
    """
    Representa al jugador del juego con animaciones y mecánicas de bullet hell.
    """
    
    def __init__(self, 
                 x: float, 
                 y: float, 
                 character_name: str,
                 config: ConfigManager,
                 animation_manager: IntelligentAnimationManager):
        """
        Inicializa el jugador.
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            character_name: Nombre del personaje seleccionado
            config: Configuración del juego
            animation_manager: Gestor de animaciones
        """
        # Configurar estadísticas según el personaje
        stats = self._get_character_stats(character_name)
        
        super().__init__(
            entity_type=EntityType.PLAYER,
            x=x,
            y=y,
            width=32,  # Tamaño reducido del sprite
            height=32,
            stats=stats
        )
        
        self.character_name = character_name
        self.config = config
        self.animation_manager = animation_manager
        self.logger = logging.getLogger(__name__)
        
        # Configuración del mundo (más grande que la pantalla)
        self.world_width = 5000  # Mundo 5 veces más ancho que la pantalla
        self.world_height = 5000  # Mundo 5 veces más alto que la pantalla
        
        # Estado del jugador
        self.current_animation_state = AnimationState.IDLE
        self.facing_right = True
        
        # Inicializar sistemas modulares
        self.stats = stats
        self.effects = PlayerEffects()
        self.combat = PlayerCombat(stats, self.effects)
        
        # Cargar animaciones del personaje
        self.animations = self.animation_manager.load_character_animations(character_name)
        
        # Configurar sprite inicial
        self._create_fallback_sprite()
        
        self.logger.info(f"Jugador {character_name} inicializado en ({x}, {y})")
    
    def _get_character_stats(self, character_name: str) -> PlayerStats:
        """Obtiene las estadísticas base del personaje."""
        if character_name in CHARACTER_DATA:
            char_data = CHARACTER_DATA[character_name]
            return PlayerStats(
                health=char_data.get('health', 100),
                max_health=char_data.get('health', 100),
                speed=char_data.get('speed', 200),
                damage=char_data.get('damage', 25),
                shoot_speed=char_data.get('shoot_speed', 0.2),
                bullet_speed=char_data.get('bullet_speed', 500),
                bullet_damage=char_data.get('bullet_damage', 25),
                shield=char_data.get('shield', 0),
                max_shield=char_data.get('max_shield', 100)
            )
        else:
            # Estadísticas por defecto
            return PlayerStats()
    
    def _update_logic(self, delta_time: float):
        """Actualiza la lógica del jugador."""
        # La lógica principal se maneja en los sistemas modulares
        pass
    
    def _update_animation(self, delta_time: float):
        """Actualiza las animaciones del jugador."""
        # Determinar estado de animación
        new_animation_state = self._get_animation_state()
        
        if new_animation_state != self.current_animation_state:
            self.current_animation_state = new_animation_state
            self._update_sprite()
    
    def _get_animation_state(self) -> AnimationState:
        """Determina el estado de animación actual."""
        if self.state == EntityState.DEAD:
            return AnimationState.DEAD
        elif self.state == EntityState.ATTACKING:
            return AnimationState.ATTACK
        elif abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1:
            if abs(self.velocity_x) > 50 or abs(self.velocity_y) > 50:
                return AnimationState.RUN
            else:
                return AnimationState.WALK
        else:
            return AnimationState.IDLE
    
    def _update_sprite(self):
        """Actualiza el sprite del jugador."""
        if self.animations and self.current_animation_state.value in self.animations:
            animation = self.animations[self.current_animation_state.value]
            if animation and animation.frames:
                self.sprite = animation.get_current_frame()
            else:
                self._create_fallback_sprite()
        else:
            self._create_fallback_sprite()
    
    def _create_fallback_sprite(self):
        """Crea un sprite de fallback si no se pueden cargar las animaciones."""
        try:
            # Crear sprite de fallback
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((0, 255, 0))  # Verde para el jugador
            
            # Añadir un borde
            pygame.draw.rect(self.sprite, (0, 200, 0), (0, 0, 32, 32), 2)
            
            # Añadir un punto central para indicar dirección
            pygame.draw.circle(self.sprite, (255, 255, 255), (16, 16), 4)
            
        except Exception as e:
            self.logger.error(f"Error creando sprite de fallback: {e}")
            # Crear sprite mínimo
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((255, 0, 0))  # Rojo como último recurso
    
    def _clamp_position(self):
        """Mantiene al jugador dentro de los límites del mundo."""
        self.x = max(0, min(self.x, self.world_width - self.width))
        self.y = max(0, min(self.y, self.world_height - self.height))
    
    def handle_input(self, keys: pygame.key.ScancodeWrapper, mouse_pos: Tuple[int, int], mouse_buttons: Tuple[bool, bool, bool]):
        """
        Maneja la entrada del usuario.
        
        Args:
            keys: Estado de las teclas
            mouse_pos: Posición del ratón
            mouse_buttons: Estado de los botones del ratón
        """
        # Reiniciar velocidad
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Movimiento con WASD
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.stats.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.stats.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.stats.speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.stats.speed
            self.facing_right = True
        
        # Aplicar modificadores de velocidad por efectos
        speed_boost = self.effects.get_effect_value(PowerupType.SPEED)
        if speed_boost > 0:
            self.velocity_x *= (1 + speed_boost)
            self.velocity_y *= (1 + speed_boost)
        
        # Disparo con clic izquierdo
        if mouse_buttons[0]:  # Clic izquierdo
            self.state = EntityState.ATTACKING
        else:
            self.state = EntityState.IDLE
    
    def shoot(self, target_pos: Tuple[int, int]) -> List:
        """
        Dispara hacia la posición objetivo.
        
        Args:
            target_pos: Posición objetivo del ratón
            
        Returns:
            Lista de proyectiles creados
        """
        import time
        current_time = time.time()
        return self.combat.shoot((self.x, self.y), target_pos, current_time)
    
    def take_damage(self, damage: float, source=None) -> bool:
        """
        Aplica daño al jugador.
        
        Args:
            damage: Cantidad de daño
            source: Fuente del daño
            
        Returns:
            True si el jugador murió
        """
        if self.combat.take_damage(damage, source):
            self.state = EntityState.DEAD
            return True
        return False
    
    def heal(self, amount: float):
        """Cura al jugador."""
        self.combat.heal(amount)
    
    def add_shield(self, amount: float):
        """Añade escudo al jugador."""
        self.combat.add_shield(amount)
    
    def add_combo(self, amount: int = 1):
        """Añade puntos de combo."""
        self.combat.add_combo(amount)
    
    def add_upgrade_points(self, amount: int):
        """Añade puntos de mejora."""
        self.stats.add_upgrade_points(amount)
    
    def upgrade_stat(self, stat_name: str, cost: int) -> bool:
        """
        Mejora una estadística.
        
        Args:
            stat_name: Nombre de la estadística
            cost: Costo en puntos de mejora
            
        Returns:
            True si la mejora fue exitosa
        """
        return self.stats.upgrade_stat(stat_name, cost)
    
    def apply_powerup(self, powerup_effect: PowerupEffect):
        """
        Aplica un powerup al jugador.
        
        Args:
            powerup_effect: Efecto del powerup
        """
        import time
        current_time = time.time()
        self.effects.apply_powerup(powerup_effect, current_time)
    
    def has_effect(self, effect_type) -> bool:
        """Verifica si tiene un efecto activo."""
        return self.effects.has_effect(effect_type)
    
    def get_effect_remaining_time(self, effect_type) -> float:
        """Obtiene el tiempo restante de un efecto."""
        import time
        current_time = time.time()
        return self.effects.get_effect_remaining_time(effect_type, current_time)
    
    def get_active_effects(self) -> dict:
        """Obtiene todos los efectos activos."""
        return self.effects.get_active_effects()
    
    def get_data(self) -> dict:
        """Obtiene datos del jugador para guardado."""
        return {
            'x': self.x,
            'y': self.y,
            'character_name': self.character_name,
            'stats': self.stats.to_dict(),
            'effects': self.effects.get_active_effects(),
            'combo': self.stats.combo,
            'max_combo': self.stats.max_combo
        }
    
    def load_data(self, data: dict):
        """Carga datos del jugador desde guardado."""
        self.x = data.get('x', self.x)
        self.y = data.get('y', self.y)
        self.character_name = data.get('character_name', self.character_name)
        
        # Cargar estadísticas
        if 'stats' in data:
            self.stats = PlayerStats.from_dict(data['stats'])
        
        # Cargar efectos
        if 'effects' in data:
            self.effects.active_effects = data['effects']
    
    def update(self, delta_time: float):
        """Actualiza el jugador."""
        # Actualizar posición
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        
        # Mantener dentro de límites
        self._clamp_position()
        
        # Actualizar efectos
        import time
        current_time = time.time()
        self.effects.update_effects(current_time)
        
        # Actualizar animaciones
        self._update_animation(delta_time)
        
        # Actualizar lógica base
        super().update(delta_time) 