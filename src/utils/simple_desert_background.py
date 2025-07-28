"""
Simple Desert Background - Fondo Simple de Desierto
=================================================

Autor: SiK Team
Fecha: 2024
Descripción: Fondo simple de desierto con colores planos.
"""

import pygame
import logging
from typing import Tuple


class SimpleDesertBackground:
	"""
	Fondo simple de desierto con colores planos.
	"""
	
	def __init__(self, screen_width: int, screen_height: int):
		"""
		Inicializa el fondo simple de desierto.
		
		Args:
			screen_width: Ancho de la pantalla
			screen_height: Alto de la pantalla
		"""
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.logger = logging.getLogger(__name__)
		
		# Colores del desierto
		self.sky_color = (135, 206, 235)  # Azul cielo
		self.sand_color = (238, 203, 173)  # Color arena
		self.horizon_color = (210, 180, 140)  # Color horizonte
		
		# Posición del horizonte (línea que separa cielo y arena)
		self.horizon_y = screen_height * 0.6
		
		self.logger.info("Fondo simple de desierto inicializado")
	
	def update(self, delta_time: float):
		"""
		Actualiza el fondo (no hace nada en esta versión simple).
		
		Args:
			delta_time: Tiempo transcurrido desde el último frame
		"""
		pass
	
	def render(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0):
		"""
		Renderiza el fondo simple de desierto.
		
		Args:
			screen: Superficie donde renderizar
			camera_x: Posición X de la cámara (no usado en esta versión)
			camera_y: Posición Y de la cámara (no usado en esta versión)
		"""
		# Rellenar todo el fondo con el color del cielo
		screen.fill(self.sky_color)
		
		# Dibujar la arena (parte inferior)
		sand_rect = pygame.Rect(0, self.horizon_y, self.screen_width, self.screen_height - self.horizon_y)
		pygame.draw.rect(screen, self.sand_color, sand_rect)
		
		# Dibujar línea del horizonte
		pygame.draw.line(screen, self.horizon_color, 
						(0, self.horizon_y), 
						(self.screen_width, self.horizon_y), 3)
		
		# Añadir algunas líneas de arena para dar textura
		for i in range(0, self.screen_width, 100):
			y_offset = (i % 200) * 0.1
			start_y = self.horizon_y + 20 + y_offset
			end_y = self.screen_height - 20
			
			if start_y < end_y:
				pygame.draw.line(screen, self.horizon_color, 
								(i, start_y), 
								(i, end_y), 1) 