"""
Entity - Clase Base de Entidades
==============================

Autor: SiK Team
Fecha: 2024
Descripción: Clase base para todas las entidades del juego.
"""

import pygame
import logging
from typing import Tuple, Optional, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class EntityType(Enum):
	"""Tipos de entidades en el juego."""
	PLAYER = "player"
	ENEMY = "enemy"
	PROJECTILE = "projectile"
	POWERUP = "powerup"
	CHARACTER = "character"
	TILE = "tile"


class EntityState(Enum):
	"""Estados posibles de una entidad."""
	IDLE = "idle"
	MOVING = "moving"
	ATTACKING = "attacking"
	HURT = "hurt"
	DEAD = "dead"
	INVULNERABLE = "invulnerable"


@dataclass
class EntityStats:
	"""Estadísticas base de una entidad."""
	health: float = 100.0
	max_health: float = 100.0
	speed: float = 1.0
	damage: float = 10.0
	armor: float = 0.0
	attack_speed: float = 1.0
	attack_range: float = 50.0


class Entity(ABC):
	"""
	Clase base abstracta para todas las entidades del juego.
	"""
	
	def __init__(self, 
				 entity_type: EntityType,
				 x: float, 
				 y: float, 
				 width: int, 
				 height: int,
				 stats: EntityStats = None):
		"""
		Inicializa una entidad base.
		
		Args:
			entity_type: Tipo de entidad
			x: Posición X inicial
			y: Posición Y inicial
			width: Ancho de la entidad
			height: Alto de la entidad
			stats: Estadísticas de la entidad
		"""
		self.entity_type = entity_type
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.stats = stats or EntityStats()
		
		# Estado y animación
		self.state = EntityState.IDLE
		self.direction = pygame.math.Vector2(0, 0)
		self.velocity = pygame.math.Vector2(0, 0)
		
		# Renderizado
		self.sprite = None
		self.animation_frames = {}
		self.current_frame = 0
		self.animation_speed = 0.1
		self.animation_timer = 0.0
		
		# Colisiones
		self.collision_rect = pygame.Rect(x, y, width, height)
		self.collision_enabled = True
		
		# Efectos
		self.invulnerable_timer = 0.0
		self.effects = {}
		
		# Logging
		self.logger = logging.getLogger(f"{self.__class__.__name__}")
		
		self.logger.debug(f"Entidad {entity_type.value} creada en ({x}, {y})")
	
	@property
	def position(self) -> Tuple[float, float]:
		"""Obtiene la posición actual de la entidad."""
		return (self.x, self.y)
	
	@property
	def center(self) -> Tuple[float, float]:
		"""Obtiene el centro de la entidad."""
		return (self.x + self.width // 2, self.y + self.height // 2)
	
	@property
	def rect(self) -> pygame.Rect:
		"""Obtiene el rectángulo de colisión actualizado."""
		self.collision_rect.x = self.x
		self.collision_rect.y = self.y
		return self.collision_rect
	
	@property
	def is_alive(self) -> bool:
		"""Verifica si la entidad está viva."""
		return self.stats.health > 0 and self.state != EntityState.DEAD
	
	@property
	def is_invulnerable(self) -> bool:
		"""Verifica si la entidad es invulnerable."""
		return self.invulnerable_timer > 0.0 or self.state == EntityState.INVULNERABLE
	
	def update(self, delta_time: float):
		"""
		Actualiza la entidad.
		
		Args:
			delta_time: Tiempo transcurrido desde el último frame
		"""
		self._update_position(delta_time)
		self._update_animation(delta_time)
		self._update_effects(delta_time)
		self._update_invulnerability(delta_time)
		
		# Método abstracto para lógica específica
		self._update_logic(delta_time)
	
	def _update_position(self, delta_time: float):
		"""Actualiza la posición de la entidad."""
		# Aplicar velocidad
		self.x += self.velocity.x * delta_time
		self.y += self.velocity.y * delta_time
		
		# Mantener dentro de los límites de la pantalla
		self._clamp_position()
	
	def _update_animation(self, delta_time: float):
		"""Actualiza la animación de la entidad."""
		if not self.animation_frames:
			return
		
		self.animation_timer += delta_time * self.animation_speed
		
		if self.animation_timer >= 1.0:
			self.animation_timer = 0.0
			self.current_frame = (self.current_frame + 1) % len(self.animation_frames.get(self.state.value, []))
	
	def _update_effects(self, delta_time: float):
		"""Actualiza los efectos aplicados a la entidad."""
		effects_to_remove = []
		
		for effect_name, effect_data in self.effects.items():
			effect_data['duration'] -= delta_time
			
			if effect_data['duration'] <= 0:
				effects_to_remove.append(effect_name)
				self._remove_effect(effect_name)
		
		for effect_name in effects_to_remove:
			del self.effects[effect_name]
	
	def _update_invulnerability(self, delta_time: float):
		"""Actualiza el estado de invulnerabilidad."""
		if self.invulnerable_timer > 0:
			self.invulnerable_timer -= delta_time
			
			if self.invulnerable_timer <= 0:
				self.state = EntityState.IDLE
				self.invulnerable_timer = 0.0
	
	def _clamp_position(self):
		"""Mantiene la entidad dentro de los límites de la pantalla."""
		# Esto se puede sobrescribir en clases hijas para límites específicos
		pass
	
	@abstractmethod
	def _update_logic(self, delta_time: float):
		"""
		Actualiza la lógica específica de la entidad.
		
		Args:
			delta_time: Tiempo transcurrido desde el último frame
		"""
		pass
	
	def move(self, direction: pygame.math.Vector2, speed: float = None):
		"""
		Mueve la entidad en una dirección específica.
		
		Args:
			direction: Vector de dirección normalizado
			speed: Velocidad de movimiento (opcional)
		"""
		if speed is None:
			speed = self.stats.speed
		
		self.direction = direction.normalize() if direction.length() > 0 else pygame.math.Vector2(0, 0)
		self.velocity = self.direction * speed
		
		if self.velocity.length() > 0:
			self.state = EntityState.MOVING
		else:
			self.state = EntityState.IDLE
	
	def take_damage(self, damage: float, source: 'Entity' = None) -> bool:
		"""
		La entidad recibe daño.
		
		Args:
			damage: Cantidad de daño a recibir
			source: Entidad que causa el daño
			
		Returns:
			True si el daño fue aplicado, False si la entidad es invulnerable
		"""
		if self.is_invulnerable:
			return False
		
		# Aplicar armadura
		actual_damage = max(0, damage - self.stats.armor)
		self.stats.health -= actual_damage
		
		self.logger.debug(f"Entidad recibió {actual_damage} de daño. Vida restante: {self.stats.health}")
		
		# Cambiar estado
		if self.stats.health <= 0:
			self.die()
		else:
			self.state = EntityState.HURT
			self.invulnerable_timer = 0.5  # 0.5 segundos de invulnerabilidad
		
		return True
	
	def heal(self, amount: float):
		"""
		Cura la entidad.
		
		Args:
			amount: Cantidad de vida a recuperar
		"""
		old_health = self.stats.health
		self.stats.health = min(self.stats.max_health, self.stats.health + amount)
		
		healed_amount = self.stats.health - old_health
		if healed_amount > 0:
			self.logger.debug(f"Entidad curada {healed_amount} puntos. Vida actual: {self.stats.health}")
	
	def die(self):
		"""Mata la entidad."""
		self.stats.health = 0
		self.state = EntityState.DEAD
		self.velocity = pygame.math.Vector2(0, 0)
		
		self.logger.info(f"Entidad {self.entity_type.value} ha muerto")
		self._on_death()
	
	def _on_death(self):
		"""Método llamado cuando la entidad muere. Se puede sobrescribir."""
		pass
	
	def add_effect(self, effect_name: str, effect_data: Dict[str, Any]):
		"""
		Añade un efecto a la entidad.
		
		Args:
			effect_name: Nombre del efecto
			effect_data: Datos del efecto (duration, value, etc.)
		"""
		self.effects[effect_name] = effect_data
		self.logger.debug(f"Efecto {effect_name} añadido a la entidad")
	
	def _remove_effect(self, effect_name: str):
		"""
		Remueve un efecto de la entidad.
		
		Args:
			effect_name: Nombre del efecto a remover
		"""
		self.logger.debug(f"Efecto {effect_name} removido de la entidad")
	
	def collides_with(self, other: 'Entity') -> bool:
		"""
		Verifica si esta entidad colisiona con otra.
		
		Args:
			other: Otra entidad
			
		Returns:
			True si hay colisión
		"""
		if not self.collision_enabled or not other.collision_enabled:
			return False
		
		return self.rect.colliderect(other.rect)
	
	def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
		"""
		Renderiza la entidad en pantalla.
		
		Args:
			screen: Superficie donde renderizar
			camera_offset: Offset de la cámara (x, y) para coordenadas de pantalla
		"""
		if not self.is_alive:
			return
		
		# Usar coordenadas de pantalla si se proporcionan, sino usar posición del mundo
		if camera_offset != (0, 0):
			render_x = camera_offset[0]
			render_y = camera_offset[1]
		else:
			render_x = self.x
			render_y = self.y
		
		# Renderizar sprite
		screen.blit(self.sprite, (render_x, render_y))
		
		# Renderizar efectos
		self._render_effects(screen, render_x, render_y)
		
		# Debug: mostrar rectángulo de colisión
		if hasattr(self, 'config') and hasattr(self.config, 'get'):
			try:
				debug_enabled = self.config.get('game', 'debug', False)
				if debug_enabled:
					debug_rect = pygame.Rect(render_x, render_y, self.width, self.height)
					pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)
			except:
				pass  # Ignorar errores de debug
	
	def _get_current_sprite(self) -> Optional[pygame.Surface]:
		"""Obtiene el sprite actual para renderizar."""
		if not self.animation_frames:
			return self.sprite
		
		frames = self.animation_frames.get(self.state.value, [])
		if frames and self.current_frame < len(frames):
			return frames[self.current_frame]
		
		return self.sprite
	
	def _render_effects(self, screen: pygame.Surface, x: float, y: float):
		"""Renderiza efectos visuales de la entidad."""
		# Efecto de invulnerabilidad (parpadeo)
		if self.is_invulnerable and int(pygame.time.get_ticks() / 100) % 2:
			overlay = pygame.Surface((self.width, self.height))
			overlay.set_alpha(128)
			overlay.fill((255, 255, 255))
			screen.blit(overlay, (x, y))
	
	def get_data(self) -> Dict[str, Any]:
		"""
		Obtiene los datos de la entidad para guardado.
		
		Returns:
			Diccionario con los datos de la entidad
		"""
		return {
			'entity_type': self.entity_type.value,
			'x': self.x,
			'y': self.y,
			'width': self.width,
			'height': self.height,
			'stats': {
				'health': self.stats.health,
				'max_health': self.stats.max_health,
				'speed': self.stats.speed,
				'damage': self.stats.damage,
				'armor': self.stats.armor,
				'attack_speed': self.stats.attack_speed,
				'attack_range': self.stats.attack_range
			},
			'state': self.state.value,
			'effects': self.effects.copy()
		}
	
	def load_data(self, data: Dict[str, Any]):
		"""
		Carga datos en la entidad.
		
		Args:
			data: Datos a cargar
		"""
		self.x = data.get('x', self.x)
		self.y = data.get('y', self.y)
		self.width = data.get('width', self.width)
		self.height = data.get('height', self.height)
		
		# Cargar estadísticas
		stats_data = data.get('stats', {})
		self.stats.health = stats_data.get('health', self.stats.health)
		self.stats.max_health = stats_data.get('max_health', self.stats.max_health)
		self.stats.speed = stats_data.get('speed', self.stats.speed)
		self.stats.damage = stats_data.get('damage', self.stats.damage)
		self.stats.armor = stats_data.get('armor', self.stats.armor)
		self.stats.attack_speed = stats_data.get('attack_speed', self.stats.attack_speed)
		self.stats.attack_range = stats_data.get('attack_range', self.stats.attack_range)
		
		# Cargar estado
		state_value = data.get('state', self.state.value)
		self.state = EntityState(state_value)
		
		# Cargar efectos
		self.effects = data.get('effects', {}).copy() 