"""
Player - Jugador del juego
=========================

Autor: SiK Team
Fecha: 2024
Descripción: Clase que representa al jugador con animaciones y mecánicas de bullet hell.
"""

import pygame
import logging
from typing import Optional, Tuple, List
from dataclasses import dataclass

from .entity import Entity, EntityType, EntityState, EntityStats
from ..utils.animation_manager import IntelligentAnimationManager
from ..utils.config_manager import ConfigManager
from enum import Enum

class AnimationState(Enum):
    IDLE = "Idle"
    RUN = "Run"
    WALK = "Walk"
    ATTACK = "Attack"
    DEAD = "Dead"
    SHOOT = "Shoot"
from ..entities.character_data import CHARACTER_DATA
from .projectile import Projectile
from ..entities.powerup import PowerupEffect, PowerupType


@dataclass
class PlayerStats(EntityStats):
	"""Estadísticas específicas del jugador."""
	shoot_speed: float = 0.2  # Tiempo entre disparos
	bullet_speed: float = 500.0  # Velocidad de los proyectiles
	bullet_damage: float = 25.0  # Daño de los proyectiles
	shield: float = 0.0  # Escudo actual
	max_shield: float = 100.0  # Escudo máximo
	upgrade_points: int = 0  # Puntos de mejora
	combo: int = 0  # Combo actual
	max_combo: int = 0  # Combo máximo


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
		self.shoot_timer = 0.0
		self.last_shoot_time = 0.0
		
		# Sistema de efectos activos (powerups)
		self.active_effects = {}  # {PowerupType: (end_time, value)}
		self.base_stats = stats  # Estadísticas base sin efectos
		
		# Cargar animaciones del personaje
		self.animations = self.animation_manager.load_character_animations(character_name)
		
		# Configurar sprite inicial
		self._update_sprite()
		
		self.logger.info(f"Jugador {character_name} creado en ({x}, {y})")
	
	def _get_character_stats(self, character_name: str) -> PlayerStats:
		"""
		Obtiene las estadísticas base según el personaje seleccionado.
		"""
		if character_name in CHARACTER_DATA:
			data = CHARACTER_DATA[character_name]["stats"]
			return PlayerStats(
				health=data.get("vida", 100),
				max_health=data.get("vida", 100),
				speed=data.get("velocidad", 200),
				damage=data.get("daño", 20),
				armor=data.get("escudo", 0),
				attack_speed=data.get("disparo", 1.0),
				shoot_speed=data.get("disparo", 1.0),
				bullet_speed=500.0,
				bullet_damage=data.get("daño", 20)
			)
		return PlayerStats()

	def _update_logic(self, delta_time: float):
		"""Actualiza la lógica específica del jugador."""
		# Actualizar animaciones
		self._update_animation(delta_time)
		
		# Actualizar sprite según la dirección
		self._update_sprite()
		
		# Mantener jugador dentro de los límites del mundo
		self._clamp_position()
	
	def _update_animation(self, delta_time: float):
		"""Actualiza las animaciones del jugador."""
		# Determinar el estado de animación actual
		new_animation_state = self._get_animation_state()
		
		# Cambiar animación si es necesario
		if new_animation_state != self.current_animation_state:
			self.current_animation_state = new_animation_state
			self.animation_manager.set_animation_state(self.character_name, new_animation_state)
		
		# Actualizar la animación actual
		self.animation_manager.update_character_animation(self.character_name, delta_time)
	
	def _get_animation_state(self) -> AnimationState:
		"""Determina el estado de animación actual del jugador."""
		# Verificar si está atacando (disparando)
		if self.shoot_timer > 0:
			return AnimationState.ATTACK
		
		# Verificar si está moviéndose
		if abs(self.velocity.x) > 0.1 or abs(self.velocity.y) > 0.1:
			return AnimationState.WALK
		
		# Por defecto, idle
		return AnimationState.IDLE
	
	def _update_sprite(self):
		"""Actualiza el sprite del jugador según la animación y dirección."""
		try:
			# Obtener el sprite actual de la animación
			current_sprite = self.animation_manager.get_current_sprite(self.character_name)
			
			if current_sprite:
				# Escalar el sprite al tamaño correcto (32x32)
				scaled_sprite = pygame.transform.scale(current_sprite, (self.width, self.height))
				
				# Aplicar rotación según la dirección
				if not self.facing_right:
					# Voltear horizontalmente el sprite
					scaled_sprite = pygame.transform.flip(scaled_sprite, True, False)
				
				self.sprite = scaled_sprite
			else:
				# Fallback: crear sprite básico
				self._create_fallback_sprite()
				
		except Exception as e:
			self.logger.error(f"Error al actualizar sprite del jugador: {e}")
			self._create_fallback_sprite()
	
	def _create_fallback_sprite(self):
		"""Crea un sprite de fallback cuando no se pueden cargar las animaciones."""
		self.sprite = pygame.Surface((self.width, self.height))
		
		# Color según el personaje
		character_colors = {
			"guerrero": (139, 69, 19),    # Marrón
			"robot": (128, 128, 128),     # Gris
			"adventureguirl": (255, 182, 193),  # Rosa claro
		}
		
		color = character_colors.get(self.character_name.lower(), (255, 0, 0))
		self.sprite.fill(color)
		
		# Añadir borde
		pygame.draw.rect(self.sprite, (255, 255, 255), (0, 0, self.width, self.height), 2)
		
		# Añadir símbolo
		symbols = {
			"guerrero": "⚔️",
			"robot": "🤖",
			"adventureguirl": "👧",
		}
		
		symbol = symbols.get(self.character_name.lower(), "?")
		try:
			font = pygame.font.Font(None, 32)
			text = font.render(symbol, True, (255, 255, 255))
			text_rect = text.get_rect(center=(self.width//2, self.height//2))
			self.sprite.blit(text, text_rect)
		except:
			pass
		
		# Aplicar rotación si es necesario
		if not self.facing_right:
			self.sprite = pygame.transform.flip(self.sprite, True, False)
	
	def _clamp_position(self):
		"""Mantiene al jugador dentro de los límites del mundo."""
		self.x = max(0, min(self.world_width - self.width, self.x))
		self.y = max(0, min(self.world_height - self.height, self.y))
	
	def handle_input(self, keys: pygame.key.ScancodeWrapper, mouse_pos: Tuple[int, int], mouse_buttons: Tuple[bool, bool, bool]):
		"""
		Maneja la entrada del jugador para movimiento libre.
		
		Args:
			keys: Teclas presionadas
			mouse_pos: Posición del ratón
			mouse_buttons: Botones del ratón
		"""
		if not self.is_alive:
			return
		
		# Movimiento con WASD - solo cuando las teclas están presionadas
		movement_x = 0
		movement_y = 0
		
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			movement_y -= 1
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			movement_y += 1
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			movement_x -= 1
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			movement_x += 1
		
		# Normalizar movimiento diagonal
		if movement_x != 0 and movement_y != 0:
			movement_x *= 0.707  # 1/√2
			movement_y *= 0.707
		
		# Aplicar movimiento solo si hay input
		if movement_x != 0 or movement_y != 0:
			self.move(pygame.math.Vector2(movement_x, movement_y), self.stats.speed)
			self.state = EntityState.MOVING
		else:
			# Detener el movimiento cuando no hay input
			self.velocity.x = 0
			self.velocity.y = 0
			self.state = EntityState.IDLE
		
		# Actualizar dirección de mirada basada en movimiento y posición del mouse
		if movement_x > 0:
			self.facing_right = True
		elif movement_x < 0:
			self.facing_right = False
		elif mouse_pos[0] > self.x + self.width // 2:
			self.facing_right = True
		elif mouse_pos[0] < self.x + self.width // 2:
			self.facing_right = False
		
		# Disparo con clic izquierdo
		if mouse_buttons[0]:
			projectile = self.shoot(mouse_pos)
			if projectile:
				# Activar animación de ataque
				self.shoot_timer = 0.2  # 0.2 segundos de animación de ataque
	
	def shoot(self, target_pos: Tuple[int, int]) -> Optional[Projectile]:
		"""
		Dispara un proyectil hacia la posición objetivo.
		
		Args:
			target_pos: Posición objetivo (x, y)
			
		Returns:
			Proyectil creado o None si no puede disparar
		"""
		current_time = pygame.time.get_ticks() / 1000.0  # Convertir a segundos
		
		# Verificar cooldown de disparo
		if current_time - self.last_shoot_time < self.stats.shoot_speed:
			return None
		
		# Crear proyectil
		projectile = Projectile(
			x=self.x + self.width // 2,
			y=self.y + self.height // 2,
			target_x=target_pos[0],
			target_y=target_pos[1],
			damage=self.stats.bullet_damage,
			speed=self.stats.bullet_speed,
			config=self.config
		)
		
		# Actualizar timer
		self.last_shoot_time = current_time
		
		self.logger.debug(f"Proyectil disparado hacia {target_pos}")
		return projectile
	
	def take_damage(self, damage: float, source=None) -> bool:
		"""
		El jugador recibe daño.
		
		Args:
			damage: Cantidad de daño
			source: Fuente del daño
			
		Returns:
			True si el daño fue aplicado
		"""
		if not self.is_alive or self.is_invulnerable:
			return False
		
		# Aplicar escudo primero
		actual_damage = damage
		if self.stats.shield > 0:
			if self.stats.shield >= damage:
				self.stats.shield -= damage
				actual_damage = 0
			else:
				actual_damage = damage - self.stats.shield
				self.stats.shield = 0
		
		# Aplicar daño restante a la vida
		if actual_damage > 0:
			super().take_damage(actual_damage, source)
			
			# Resetear combo al recibir daño
			self.stats.combo = 0
		
		return True
	
	def heal(self, amount: float):
		"""
		Cura al jugador.
		
		Args:
			amount: Cantidad de vida a recuperar
		"""
		super().heal(amount)
		self.logger.debug(f"Jugador curado {amount} puntos. Vida actual: {self.stats.health}")
	
	def add_shield(self, amount: float):
		"""
		Añade escudo al jugador.
		
		Args:
			amount: Cantidad de escudo a añadir
		"""
		old_shield = self.stats.shield
		self.stats.shield = min(self.stats.max_shield, self.stats.shield + amount)
		
		added_shield = self.stats.shield - old_shield
		if added_shield > 0:
			self.logger.debug(f"Escudo añadido: {added_shield}. Escudo actual: {self.stats.shield}")
	
	def add_combo(self, amount: int = 1):
		"""
		Añade puntos de combo al jugador.
		
		Args:
			amount: Cantidad de combo a añadir
		"""
		self.stats.combo += amount
		if self.stats.combo > self.stats.max_combo:
			self.stats.max_combo = self.stats.combo
		
		self.logger.debug(f"Combo añadido: {amount}. Combo actual: {self.stats.combo}")
	
	def add_upgrade_points(self, amount: int):
		"""
		Añade puntos de mejora al jugador.
		
		Args:
			amount: Cantidad de puntos de mejora
		"""
		self.stats.upgrade_points += amount
		self.logger.debug(f"Puntos de mejora añadidos: {amount}. Total: {self.stats.upgrade_points}")
	
	def upgrade_stat(self, stat_name: str, cost: int) -> bool:
		"""
		Mejora una estadística del jugador.
		
		Args:
			stat_name: Nombre de la estadística a mejorar
			cost: Costo en puntos de mejora
			
		Returns:
			True si la mejora fue exitosa
		"""
		if self.stats.upgrade_points < cost:
			return False
		
		upgrade_amounts = {
			'speed': 20.0,
			'damage': 5.0,
			'health': 25.0,
			'shield': 25.0,
			'bullet_speed': 50.0,
			'bullet_damage': 5.0,
			'shoot_speed': -0.02  # Reducir tiempo entre disparos
		}
		
		if stat_name in upgrade_amounts:
			amount = upgrade_amounts[stat_name]
			
			if stat_name == 'speed':
				self.stats.speed += amount
			elif stat_name == 'damage':
				self.stats.damage += amount
			elif stat_name == 'health':
				self.stats.max_health += amount
				self.stats.health += amount
			elif stat_name == 'shield':
				self.stats.max_shield += amount
				self.stats.shield += amount
			elif stat_name == 'bullet_speed':
				self.stats.bullet_speed += amount
			elif stat_name == 'bullet_damage':
				self.stats.bullet_damage += amount
			elif stat_name == 'shoot_speed':
				self.stats.shoot_speed = max(0.05, self.stats.shoot_speed + amount)
			
			self.stats.upgrade_points -= cost
			self.logger.info(f"Estadística {stat_name} mejorada en {amount}")
			return True
		
		return False
	
	def get_data(self) -> dict:
		"""
		Obtiene los datos del jugador para guardado.
		
		Returns:
			Diccionario con los datos del jugador
		"""
		data = super().get_data()
		data.update({
			'character_name': self.character_name,
			'facing_right': self.facing_right,
			'combo': self.stats.combo,
			'max_combo': self.stats.max_combo,
			'upgrade_points': self.stats.upgrade_points,
			'shield': self.stats.shield,
			'max_shield': self.stats.max_shield,
			'shoot_speed': self.stats.shoot_speed,
			'bullet_speed': self.stats.bullet_speed,
			'bullet_damage': self.stats.bullet_damage
		})
		return data
	
	def load_data(self, data: dict):
		"""
		Carga datos en el jugador.
		
		Args:
			data: Datos a cargar
		"""
		super().load_data(data)
		
		self.character_name = data.get('character_name', self.character_name)
		self.facing_right = data.get('facing_right', True)
		self.stats.combo = data.get('combo', 0)
		self.stats.max_combo = data.get('max_combo', 0)
		self.stats.upgrade_points = data.get('upgrade_points', 0)
		self.stats.shield = data.get('shield', 0)
		self.stats.max_shield = data.get('max_shield', 100)
		self.stats.shoot_speed = data.get('shoot_speed', 0.2)
		self.stats.bullet_speed = data.get('bullet_speed', 500)
		self.stats.bullet_damage = data.get('bullet_damage', 25) 
	
	def update(self, delta_time: float):
		"""Actualiza el jugador."""
		super().update(delta_time)
		
		# Actualizar timer de disparo
		if self.shoot_timer > 0:
			self.shoot_timer -= delta_time
			if self.shoot_timer < 0:
				self.shoot_timer = 0
		
		# Actualizar efectos activos
		self._update_active_effects(delta_time)
		
		# Mantener posición dentro de límites
		self._clamp_position()
	
	def _update_active_effects(self, delta_time: float):
		"""Actualiza los efectos activos del jugador."""
		current_time = pygame.time.get_ticks() / 1000.0
		
		# Eliminar efectos expirados
		expired_effects = []
		for effect_type, (end_time, value) in self.active_effects.items():
			if current_time >= end_time:
				expired_effects.append(effect_type)
		
		for effect_type in expired_effects:
			del self.active_effects[effect_type]
			self.logger.debug(f"Efecto {effect_type.value} expirado")
		
		# Recalcular estadísticas con efectos activos
		self._recalculate_stats()
	
	def _recalculate_stats(self):
		"""Recalcula las estadísticas del jugador con efectos activos."""
		# Copiar estadísticas base
		self.stats = self.base_stats
		
		# Aplicar efectos activos
		for effect_type, (end_time, value) in self.active_effects.items():
			if effect_type == PowerupType.SPEED:
				self.stats.speed *= value
			elif effect_type == PowerupType.DAMAGE:
				self.stats.damage *= value
			elif effect_type == PowerupType.SHIELD:
				self.stats.armor += value
			elif effect_type == PowerupType.RAPID_FIRE:
				self.stats.shoot_speed *= value
	
	def apply_powerup(self, powerup_effect: PowerupEffect):
		"""
		Aplica un powerup al jugador.
		
		Args:
			powerup_effect: Efecto del powerup a aplicar
		"""
		current_time = pygame.time.get_ticks() / 1000.0
		
		if powerup_effect.duration > 0:
			# Efecto temporal
			end_time = current_time + powerup_effect.duration
			self.active_effects[powerup_effect.type] = (end_time, powerup_effect.value)
			self.logger.info(f"Powerup {powerup_effect.type.value} aplicado por {powerup_effect.duration}s")
		else:
			# Efecto instantáneo
			if powerup_effect.type == PowerupType.HEALTH:
				self.stats.health = min(self.stats.max_health, self.stats.health + powerup_effect.value)
				self.logger.info(f"Vida restaurada: +{powerup_effect.value}")
		
		# Recalcular estadísticas
		self._recalculate_stats()
	
	def has_effect(self, effect_type: PowerupType) -> bool:
		"""
		Verifica si el jugador tiene un efecto activo.
		
		Args:
			effect_type: Tipo de efecto a verificar
			
		Returns:
			True si el efecto está activo
		"""
		return effect_type in self.active_effects
	
	def get_effect_remaining_time(self, effect_type: PowerupType) -> float:
		"""
		Obtiene el tiempo restante de un efecto.
		
		Args:
			effect_type: Tipo de efecto
			
		Returns:
			Tiempo restante en segundos, 0 si no está activo
		"""
		if effect_type in self.active_effects:
			current_time = pygame.time.get_ticks() / 1000.0
			end_time = self.active_effects[effect_type][0]
			return max(0, end_time - current_time)
		return 0.0
	
	def get_active_effects(self) -> dict:
		"""
		Obtiene todos los efectos activos.
		
		Returns:
			Dict con efectos activos y tiempo restante
		"""
		effects = {}
		for effect_type in self.active_effects:
			effects[effect_type] = self.get_effect_remaining_time(effect_type)
		return effects 