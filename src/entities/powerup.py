"""
Powerup System - Sistema de Powerups
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de powerups que mejoran temporalmente al jugador.
"""

import pygame
import logging
import random
import math
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

from .entity import Entity, EntityType, EntityStats


class PowerupType(Enum):
	"""Tipos de powerups disponibles."""
	SPEED = "speed"
	DAMAGE = "damage"
	SHIELD = "shield"
	RAPID_FIRE = "rapid_fire"
	DOUBLE_SHOT = "double_shot"
	HEALTH = "health"
	SPREAD = "spread"
	EXPLOSIVE = "explosive"
	SHRAPNEL = "shrapnel"


@dataclass
class PowerupEffect:
	"""Efecto de un powerup."""
	type: PowerupType
	duration: float  # Duración en segundos
	value: float     # Valor del efecto
	description: str


class Powerup(Entity):
	"""
	Powerup que mejora temporalmente al jugador.
	"""
	
	# Configuración de powerups
	POWERUP_CONFIGS = {
		PowerupType.SPEED: {
			"name": "Velocidad",
			"color": (0, 255, 0),  # Verde
			"duration": 10.0,
			"value": 1.5,  # Multiplicador de velocidad
			"description": "Aumenta la velocidad de movimiento"
		},
		PowerupType.DAMAGE: {
			"name": "Daño",
			"color": (255, 0, 0),  # Rojo
			"duration": 15.0,
			"value": 2.0,  # Multiplicador de daño
			"description": "Aumenta el daño de los proyectiles"
		},
		PowerupType.SHIELD: {
			"name": "Escudo",
			"color": (0, 0, 255),  # Azul
			"duration": 12.0,
			"value": 0.5,  # Reducción de daño recibido
			"description": "Reduce el daño recibido"
		},
		PowerupType.RAPID_FIRE: {
			"name": "Disparo Rápido",
			"color": (255, 255, 0),  # Amarillo
			"duration": 8.0,
			"value": 0.3,  # Reducción del tiempo entre disparos
			"description": "Aumenta la velocidad de disparo"
		},
		PowerupType.DOUBLE_SHOT: {
			"name": "Doble Disparo",
			"color": (255, 0, 255),  # Magenta
			"duration": 20.0,
			"value": 2,  # Número de proyectiles
			"description": "Dispara dos proyectiles a la vez"
		},
		PowerupType.HEALTH: {
			"name": "Vida",
			"color": (255, 165, 0),  # Naranja
			"duration": 0.0,  # Efecto instantáneo
			"value": 50.0,  # Cantidad de vida restaurada
			"description": "Restaura vida"
		},
		PowerupType.SPREAD: {
			"name": "Disparo Disperso",
			"color": (128, 0, 128),  # Púrpura
			"duration": 15.0,
			"value": 3,  # Número de proyectiles en abanico
			"description": "Dispara múltiples proyectiles en abanico"
		},
		PowerupType.EXPLOSIVE: {
			"name": "Explosivo",
			"color": (255, 69, 0),  # Rojo-naranja
			"duration": 12.0,
			"value": 2.0,  # Radio de explosión
			"description": "Los proyectiles explotan al impactar"
		},
		PowerupType.SHRAPNEL: {
			"name": "Metralla",
			"color": (105, 105, 105),  # Gris
			"duration": 10.0,
			"value": 5,  # Número de fragmentos
			"description": "Los proyectiles se dividen en fragmentos"
		}
	}
	
	def __init__(self, x: float, y: float, powerup_type: PowerupType):
		"""
		Inicializa un powerup.
		
		Args:
			x: Posición X
			y: Posición Y
			powerup_type: Tipo de powerup
		"""
		# Crear estadísticas básicas
		stats = EntityStats(
			health=1.0,
			max_health=1.0,
			speed=0.0,
			damage=0.0,
			armor=0.0,
			attack_speed=0.0,
			attack_range=0.0
		)
		
		super().__init__(
			entity_type=EntityType.POWERUP,
			x=x,
			y=y,
			width=30,
			height=30,
			stats=stats
		)
		
		self.powerup_type = powerup_type
		self.config = self.POWERUP_CONFIGS[powerup_type]
		self.logger = logging.getLogger(__name__)
		
		# Configurar sprite
		self._setup_sprite()
		
		# Efecto de flotación
		self.float_offset = 0
		self.float_speed = 2.0
		self.float_amplitude = 5.0
		
		self.logger.debug(f"Powerup {powerup_type.value} creado en ({x}, {y})")
	
	def _setup_sprite(self):
		"""Configura el sprite del powerup."""
		try:
			# Crear sprite con el color del powerup
			self.sprite = pygame.Surface((self.width, self.height))
			self.sprite.fill(self.config["color"])
			
			# Añadir borde blanco
			pygame.draw.rect(self.sprite, (255, 255, 255), 
						   (0, 0, self.width, self.height), 2)
			
			# Añadir símbolo según el tipo
			self._add_symbol()
			
		except Exception as e:
			self.logger.error(f"Error al crear sprite de powerup: {e}")
			# Sprite por defecto
			self.sprite = pygame.Surface((self.width, self.height))
			self.sprite.fill((128, 128, 128))
	
	def _add_symbol(self):
		"""Añade un símbolo al sprite según el tipo de powerup."""
		font = pygame.font.Font(None, 20)
		symbol = self._get_symbol()
		text = font.render(symbol, True, (255, 255, 255))
		
		# Centrar el símbolo
		text_rect = text.get_rect(center=(self.width//2, self.height//2))
		self.sprite.blit(text, text_rect)
	
	def _get_symbol(self) -> str:
		"""Obtiene el símbolo para el tipo de powerup."""
		symbols = {
			PowerupType.SPEED: "⚡",
			PowerupType.DAMAGE: "⚔",
			PowerupType.SHIELD: "🛡",
			PowerupType.RAPID_FIRE: "🔥",
			PowerupType.DOUBLE_SHOT: "⚡⚡",
			PowerupType.HEALTH: "❤",
			PowerupType.SPREAD: "🎯",
			PowerupType.EXPLOSIVE: "💥",
			PowerupType.SHRAPNEL: "🔫"
		}
		return symbols.get(self.powerup_type, "?")
	
	def update(self, delta_time: float):
		"""Actualiza el powerup."""
		super().update(delta_time)
		
		# Efecto de flotación
		self.float_offset += self.float_speed * delta_time
		if self.float_offset > 2 * 3.14159:  # 2π
			self.float_offset = 0
	
	def _update_logic(self, delta_time: float):
		"""Actualiza la lógica específica del powerup."""
		# Los powerups no tienen lógica de movimiento específica
		pass
	
	def render(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)):
		"""Renderiza el powerup con efecto de flotación."""
		if not self.is_alive or not self.sprite:
			return
		
		# Calcular posición con flotación
		if camera_offset != (0, 0):
			render_x = camera_offset[0]
			render_y = camera_offset[1]
		else:
			render_x = self.x
			render_y = self.y
		
		# Aplicar efecto de flotación
		float_y = render_y + self.float_amplitude * math.sin(self.float_offset)
		
		# Renderizar sprite
		screen.blit(self.sprite, (render_x, float_y))
		
		# Debug: mostrar rectángulo de colisión
		if hasattr(self, 'config') and hasattr(self.config, 'get'):
			try:
				debug_enabled = self.config.get('game', {}).get('debug', False)
				if debug_enabled:
					debug_rect = pygame.Rect(render_x, float_y, self.width, self.height)
					pygame.draw.rect(screen, (255, 255, 0), debug_rect, 2)
			except:
				pass  # Ignorar errores de debug
	
	def get_effect(self) -> PowerupEffect:
		"""Obtiene el efecto del powerup."""
		return PowerupEffect(
			type=self.powerup_type,
			duration=self.config["duration"],
			value=self.config["value"],
			description=self.config["description"]
		)
	
	@classmethod
	def create_random(cls, x: float, y: float) -> 'Powerup':
		"""
		Crea un powerup aleatorio.
		
		Args:
			x: Posición X
			y: Posición Y
			
		Returns:
			Powerup aleatorio
		"""
		powerup_type = random.choice(list(PowerupType))
		return cls(x, y, powerup_type)
	
	@classmethod
	def get_all_types(cls) -> list:
		"""Obtiene todos los tipos de powerups disponibles."""
		return list(PowerupType) 