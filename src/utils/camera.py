"""
Camera System - Sistema de Cámara
================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de cámara que sigue al jugador y muestra la porción visible del mundo.
"""

import pygame
import logging
from typing import Tuple, Optional


class Camera:
	"""
	Sistema de cámara que sigue al jugador y gestiona la vista del mundo.
	"""
	
	def __init__(self, screen_width: int, screen_height: int, world_width: int, world_height: int):
		"""
		Inicializa la cámara.
		
		Args:
			screen_width: Ancho de la pantalla
			screen_height: Alto de la pantalla
			world_width: Ancho del mundo
			world_height: Alto del mundo
		"""
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.world_width = world_width
		self.world_height = world_height
		
		# Posición de la cámara en el mundo
		self.x = 0
		self.y = 0
		
		# Suavizado de la cámara
		self.smooth_factor = 0.1
		self.target_x = 0
		self.target_y = 0
		
		# Límites de la cámara
		self.min_x = screen_width // 2
		self.max_x = world_width - screen_width // 2
		self.min_y = screen_height // 2
		self.max_y = world_height - screen_height // 2
		
		self.logger = logging.getLogger(__name__)
		self.logger.info(f"Cámara inicializada - Mundo: {world_width}x{world_height}, Pantalla: {screen_width}x{screen_height}")
	
	def follow_target(self, target_x: float, target_y: float):
		"""
		Hace que la cámara siga a un objetivo.
		
		Args:
			target_x: Posición X del objetivo
			target_y: Posición Y del objetivo
		"""
		# Centrar la cámara en el objetivo
		self.target_x = target_x - self.screen_width // 2
		self.target_y = target_y - self.screen_height // 2
		
		# Aplicar límites
		self.target_x = max(self.min_x, min(self.max_x, self.target_x))
		self.target_y = max(self.min_y, min(self.max_y, self.target_y))
	
	def update(self, delta_time: float):
		"""
		Actualiza la posición de la cámara con suavizado.
		
		Args:
			delta_time: Tiempo transcurrido desde el último frame
		"""
		# Suavizado de movimiento
		self.x += (self.target_x - self.x) * self.smooth_factor
		self.y += (self.target_y - self.y) * self.smooth_factor
	
	def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
		"""
		Convierte coordenadas del mundo a coordenadas de pantalla.
		
		Args:
			world_x: Coordenada X del mundo
			world_y: Coordenada Y del mundo
			
		Returns:
			Tupla con coordenadas de pantalla (x, y)
		"""
		screen_x = world_x - self.x
		screen_y = world_y - self.y
		return screen_x, screen_y
	
	def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
		"""
		Convierte coordenadas de pantalla a coordenadas del mundo.
		
		Args:
			screen_x: Coordenada X de pantalla
			screen_y: Coordenada Y de pantalla
			
		Returns:
			Tupla con coordenadas del mundo (x, y)
		"""
		world_x = screen_x + self.x
		world_y = screen_y + self.y
		return world_x, world_y
	
	def is_visible(self, world_x: float, world_y: float, width: float = 0, height: float = 0) -> bool:
		"""
		Verifica si un objeto está visible en pantalla.
		
		Args:
			world_x: Posición X del mundo
			world_y: Posición Y del mundo
			width: Ancho del objeto
			height: Alto del objeto
			
		Returns:
			True si el objeto está visible
		"""
		screen_x, screen_y = self.world_to_screen(world_x, world_y)
		
		return (screen_x + width >= 0 and screen_x <= self.screen_width and
				screen_y + height >= 0 and screen_y <= self.screen_height)
	
	def get_viewport(self) -> Tuple[float, float, float, float]:
		"""
		Obtiene el área visible del mundo.
		
		Returns:
			Tupla con (x, y, width, height) del área visible
		"""
		return self.x, self.y, self.screen_width, self.screen_height
	
	def get_position(self) -> Tuple[float, float]:
		"""
		Obtiene la posición actual de la cámara.
		
		Returns:
			Tupla con posición (x, y) de la cámara
		"""
		return self.x, self.y 