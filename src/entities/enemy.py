"""
Enemy - Enemigos del Juego
=========================

Autor: SiK Team
Fecha: 2024
Descripción: Clase base para todos los enemigos del juego.
"""

import pygame
import logging
from typing import Optional, Tuple
import random
import math

from .entity import Entity, EntityType, EntityStats
from .enemy_types import EnemyConfig, EnemyBehavior, EnemyRarity, EnemyTypes
from ..utils.asset_manager import AssetManager
from ..utils.animation_manager import AnimationManager
from ..utils.config_manager import ConfigManager


class Enemy(Entity):
	"""
	Clase base para todos los enemigos del juego.
	"""
	
	def __init__(self, x: float, y: float, asset_manager: AssetManager, 
				 animation_manager: AnimationManager, config: ConfigManager, player=None, enemy_config: EnemyConfig = None):
		"""
		Inicializa un enemigo.
		
		Args:
			x: Posición X inicial
			y: Posición Y inicial
			asset_manager: Gestor de assets
			animation_manager: Gestor de animaciones
			config: Configuración del juego
			player: Referencia al jugador para perseguir
			enemy_config: Configuración específica del enemigo
		"""
		# Usar configuración específica o crear una por defecto
		if enemy_config is None:
			enemy_config = EnemyTypes.ZOMBIE_NORMAL
		
		# Crear estadísticas del enemigo
		stats = EntityStats(
			health=enemy_config.health,
			max_health=enemy_config.health,
			speed=enemy_config.speed,
			damage=enemy_config.damage,
			armor=enemy_config.armor,
			attack_speed=1.0,
			attack_range=50.0
		)
		
		super().__init__(
			entity_type=EntityType.ENEMY,
			x=x,
			y=y,
			width=enemy_config.size[0],
			height=enemy_config.size[1],
			stats=stats
		)
		
		self.logger = logging.getLogger(__name__)
		self.config = config
		self.asset_manager = asset_manager
		self.animation_manager = animation_manager
		self.player = player
		self.enemy_config = enemy_config
		self.score_value = enemy_config.score_value
		
		# Comportamiento específico
		self.behavior = enemy_config.behavior
		self.rarity = enemy_config.rarity
		
		# Variables de comportamiento
		self.wander_timer = 0
		self.wander_direction = pygame.math.Vector2(0, 0)
		self.ambush_timer = 0
		self.ambush_cooldown = 3.0  # 3 segundos
		self.swarm_target = None
		
		# Configurar sprite
		self._setup_sprite()
		
		self.logger.debug(f"Enemigo {enemy_config.name} creado en ({x}, {y})")
	
	def _setup_sprite(self):
		"""Configura el sprite del enemigo."""
		try:
			# Crear sprite con el color del enemigo
			self.sprite = pygame.Surface((self.width, self.height))
			self.sprite.fill(self.enemy_config.color)
			
			# Añadir borde según rareza
			border_color = self._get_rarity_border_color()
			pygame.draw.rect(self.sprite, border_color, 
						   (0, 0, self.width, self.height), 3)
			
			# Añadir símbolo
			self._add_symbol()
			
		except Exception as e:
			self.logger.error(f"Error al crear sprite de enemigo: {e}")
			# Sprite por defecto
			self.sprite = pygame.Surface((self.width, self.height))
			self.sprite.fill((255, 0, 0))
	
	def _get_rarity_border_color(self) -> Tuple[int, int, int]:
		"""Obtiene el color del borde según la rareza."""
		border_colors = {
			EnemyRarity.NORMAL: (128, 128, 128),    # Gris
			EnemyRarity.RARE: (0, 255, 0),          # Verde
			EnemyRarity.ELITE: (0, 0, 255),         # Azul
			EnemyRarity.LEGENDARY: (255, 215, 0)    # Dorado
		}
		return border_colors.get(self.rarity, (128, 128, 128))
	
	def _add_symbol(self):
		"""Añade un símbolo al sprite según el tipo de enemigo."""
		try:
			font = pygame.font.Font(None, min(self.width, self.height) // 2)
			symbol = self.enemy_config.symbol
			text = font.render(symbol, True, (255, 255, 255))
			
			# Centrar el símbolo
			text_rect = text.get_rect(center=(self.width//2, self.height//2))
			self.sprite.blit(text, text_rect)
		except Exception as e:
			self.logger.warning(f"No se pudo añadir símbolo al enemigo: {e}")
	
	def _update_logic(self, delta_time: float):
		"""Actualiza la lógica específica del enemigo según su comportamiento."""
		if not self.player or not self.player.is_alive:
			return
		
		# Actualizar timers
		self.wander_timer += delta_time
		self.ambush_timer += delta_time
		
		# Aplicar comportamiento específico
		if self.behavior == EnemyBehavior.CHASE:
			self._chase_behavior(delta_time)
		elif self.behavior == EnemyBehavior.WANDER:
			self._wander_behavior(delta_time)
		elif self.behavior == EnemyBehavior.AMBUSH:
			self._ambush_behavior(delta_time)
		elif self.behavior == EnemyBehavior.SWARM:
			self._swarm_behavior(delta_time)
		elif self.behavior == EnemyBehavior.BOSS:
			self._boss_behavior(delta_time)
		
		# Mantener enemigo dentro de los límites del mundo
		world_width = 5000
		world_height = 5000
		
		if self.x < 0:
			self.x = 0
		elif self.x + self.width > world_width:
			self.x = world_width - self.width
		
		if self.y < 0:
			self.y = 0
		elif self.y + self.height > world_height:
			self.y = world_height - self.height
	
	def _chase_behavior(self, delta_time: float):
		"""Comportamiento de persecución directa."""
		# Calcular dirección hacia el jugador
		dx = self.player.x - self.x
		dy = self.player.y - self.y
		distance = (dx*dx + dy*dy)**0.5
		
		if distance > 0:
			# Normalizar dirección
			dx /= distance
			dy /= distance
			
			# Mover hacia el jugador
			self.x += dx * self.stats.speed * delta_time * 60
			self.y += dy * self.stats.speed * delta_time * 60
	
	def _wander_behavior(self, delta_time: float):
		"""Comportamiento de vagabundeo aleatorio."""
		# Cambiar dirección cada 2 segundos
		if self.wander_timer > 2.0:
			self.wander_timer = 0
			angle = random.uniform(0, 2 * 3.14159)
			self.wander_direction = pygame.math.Vector2(
				math.cos(angle),
				math.sin(angle)
			)
		
		# Mover en dirección aleatoria
		self.x += self.wander_direction.x * self.stats.speed * delta_time * 60
		self.y += self.wander_direction.y * self.stats.speed * delta_time * 60
		
		# Si está cerca del jugador, cambiar a persecución
		dx = self.player.x - self.x
		dy = self.player.y - self.y
		distance = (dx*dx + dy*dy)**0.5
		
		if distance < 200:  # Detectar jugador a 200 píxeles
			self._chase_behavior(delta_time)
	
	def _ambush_behavior(self, delta_time: float):
		"""Comportamiento de emboscada."""
		dx = self.player.x - self.x
		dy = self.player.y - self.y
		distance = (dx*dx + dy*dy)**0.5
		
		if distance < 150:  # Cerca del jugador
			if self.ambush_timer > self.ambush_cooldown:
				# Ataque rápido
				self._chase_behavior(delta_time)
				self.stats.speed *= 2.0  # Velocidad temporal
				self.ambush_timer = 0
			else:
				# Esperar
				pass
		else:
			# Acercarse sigilosamente
			if distance > 0:
				dx /= distance
				dy /= distance
				self.x += dx * self.stats.speed * 0.5 * delta_time * 60
				self.y += dy * self.stats.speed * 0.5 * delta_time * 60
	
	def _swarm_behavior(self, delta_time: float):
		"""Comportamiento de enjambre."""
		# Buscar otros enemigos cercanos
		if not self.swarm_target:
			# Por ahora, simplemente perseguir al jugador
			self._chase_behavior(delta_time)
		else:
			# Moverse hacia el objetivo del enjambre
			dx = self.swarm_target.x - self.x
			dy = self.swarm_target.y - self.y
			distance = (dx*dx + dy*dy)**0.5
			
			if distance > 0:
				dx /= distance
				dy /= distance
				self.x += dx * self.stats.speed * delta_time * 60
				self.y += dy * self.stats.speed * delta_time * 60
	
	def _boss_behavior(self, delta_time: float):
		"""Comportamiento de jefe."""
		# Comportamiento más complejo para jefes
		dx = self.player.x - self.x
		dy = self.player.y - self.y
		distance = (dx*dx + dy*dy)**0.5
		
		if distance < 300:
			# Ataque directo
			self._chase_behavior(delta_time)
		else:
			# Movimiento estratégico
			angle = math.atan2(dy, dx)
			# Moverse en círculo alrededor del jugador
			circle_radius = 250
			target_x = self.player.x + circle_radius * math.cos(angle + 0.1)
			target_y = self.player.y + circle_radius * math.sin(angle + 0.1)
			
			dx = target_x - self.x
			dy = target_y - self.y
			distance = (dx*dx + dy*dy)**0.5
			
			if distance > 0:
				dx /= distance
				dy /= distance
				self.x += dx * self.stats.speed * delta_time * 60
				self.y += dy * self.stats.speed * delta_time * 60
	
	def get_enemy_info(self) -> dict:
		"""
		Obtiene información del enemigo.
		
		Returns:
			Dict con información del enemigo
		"""
		return {
			"name": self.enemy_config.name,
			"rarity": self.rarity.value,
			"behavior": self.behavior.value,
			"health": self.stats.health,
			"max_health": self.stats.max_health,
			"damage": self.stats.damage,
			"position": (self.x, self.y),
			"score_value": self.score_value
		} 