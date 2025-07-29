"""
Desert Background - Fondo Dinámico de Desierto
============================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de fondos dinámicos de desierto con efectos visuales.
"""

import pygame
import random
import math
from typing import List, Tuple
import logging


class SandParticle:
	"""Partícula de arena para efectos atmosféricos."""
	
	def __init__(self, x: float, y: float, screen_width: int, screen_height: int):
		self.x = x
		self.y = y
		self.screen_width = screen_width
		self.screen_height = screen_height
		
		# Propiedades de la partícula
		self.size = random.uniform(1, 3)
		self.speed = random.uniform(20, 50)
		self.angle = random.uniform(0, 2 * math.pi)
		self.opacity = random.uniform(50, 150)
		self.life = random.uniform(2, 5)
		self.max_life = self.life
		
		# Color de arena
		self.color = (
			random.randint(200, 255),  # R
			random.randint(180, 220),  # G
			random.randint(120, 160)   # B
		)
	
	def update(self, delta_time: float):
		"""Actualiza la partícula de arena."""
		# Mover partícula
		self.x += math.cos(self.angle) * self.speed * delta_time
		self.y += math.sin(self.angle) * self.speed * delta_time
		
		# Reducir vida
		self.life -= delta_time
		self.opacity = (self.life / self.max_life) * 150
		
		# Reiniciar si sale de pantalla o muere
		if (self.x < -10 or self.x > self.screen_width + 10 or 
			self.y < -10 or self.y > self.screen_height + 10 or 
			self.life <= 0):
			self._reset()
	
	def _reset(self):
		"""Reinicia la partícula en una nueva posición."""
		# Aparecer desde los bordes
		side = random.choice(['top', 'bottom', 'left', 'right'])
		if side == 'top':
			self.x = random.uniform(-10, self.screen_width + 10)
			self.y = -10
		elif side == 'bottom':
			self.x = random.uniform(-10, self.screen_width + 10)
			self.y = self.screen_height + 10
		elif side == 'left':
			self.x = -10
			self.y = random.uniform(-10, self.screen_height + 10)
		else:  # right
			self.x = self.screen_width + 10
			self.y = random.uniform(-10, self.screen_height + 10)
		
		# Reiniciar propiedades
		self.life = random.uniform(2, 5)
		self.max_life = self.life
		self.opacity = random.uniform(50, 150)
		self.angle = random.uniform(0, 2 * math.pi)
	
	def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
		"""Renderiza la partícula de arena."""
		if self.life <= 0:
			return
		
		# Posición con offset de cámara
		render_x = int(self.x - camera_offset[0])
		render_y = int(self.y - camera_offset[1])
		
		# Crear superficie con alpha
		particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
		
		# Color con alpha
		color_with_alpha = (*self.color, int(self.opacity))
		pygame.draw.circle(particle_surface, color_with_alpha, 
						  (int(self.size), int(self.size)), int(self.size))
		
		screen.blit(particle_surface, (render_x - int(self.size), render_y - int(self.size)))


class Dune:
	"""Duna de arena para el fondo."""
	
	def __init__(self, x: float, y: float, width: float, height: float, screen_width: int):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.screen_width = screen_width
		
		# Propiedades de la duna
		self.points = self._generate_dune_points()
		self.color = (
			random.randint(180, 220),  # R
			random.randint(160, 200),  # G
			random.randint(100, 140)   # B
		)
		
		# Efecto de sombra
		self.shadow_color = (
			max(0, self.color[0] - 40),  # R más oscuro
			max(0, self.color[1] - 40),  # G más oscuro
			max(0, self.color[2] - 40)   # B más oscuro
		)
	
	def _generate_dune_points(self) -> List[Tuple[float, float]]:
		"""Genera puntos para dibujar la duna."""
		points = []
		num_points = 20
		
		for i in range(num_points + 1):
			x = self.x + (i / num_points) * self.width
			
			# Función sinusoidal para crear la forma de duna
			progress = i / num_points
			wave = math.sin(progress * math.pi) * 0.3
			noise = random.uniform(-0.1, 0.1)
			
			y = self.y + self.height * (1 - wave + noise)
			points.append((x, y))
		
		return points
	
	def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
		"""Renderiza la duna."""
		# Aplicar offset de cámara
		offset_points = []
		for x, y in self.points:
			offset_x = x - camera_offset[0]
			offset_y = y - camera_offset[1]
			offset_points.append((offset_x, offset_y))
		
		# Dibujar duna principal
		if len(offset_points) > 2:
			pygame.draw.polygon(screen, self.color, offset_points)
		
		# Dibujar sombra
		shadow_points = []
		for x, y in offset_points:
			shadow_points.append((x, y + 5))  # Sombra desplazada hacia abajo
		
		if len(shadow_points) > 2:
			pygame.draw.polygon(screen, self.shadow_color, shadow_points)


class DesertBackground:
	"""
	Sistema de fondo dinámico de desierto con efectos visuales.
	"""
	
	def __init__(self, screen_width: int, screen_height: int):
		"""
		Inicializa el fondo de desierto.
		
		Args:
			screen_width: Ancho de la pantalla
			screen_height: Alto de la pantalla
		"""
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.logger = logging.getLogger(__name__)
		
		# Colores del desierto con más profundidad
		self.colors = {
			'sky_top': (100, 150, 255),      # Azul cielo profundo
			'sky_mid': (135, 206, 235),      # Azul cielo medio
			'sky_bottom': (255, 223, 186),   # Naranja atardecer
			'sand_top': (238, 203, 173),     # Arena clara
			'sand_mid': (216, 191, 161),     # Arena media
			'sand_bottom': (194, 178, 128),  # Arena oscura
			'dune': (210, 180, 140),         # Color duna
			'dune_shadow': (160, 140, 100),  # Sombra duna
			'dune_highlight': (230, 200, 160) # Resaltado duna
		}
		
		# Partículas de arena
		self.sand_particles = []
		self._create_sand_particles(100)  # 100 partículas
		
		# Dunas
		self.dunes = []
		self._create_dunes()
		
		# Efectos atmosféricos
		self.time = 0.0
		self.wind_strength = 0.5
		
		self.logger.info("Fondo de desierto inicializado")
	
	def _create_sand_particles(self, count: int):
		"""Crea partículas de arena."""
		for _ in range(count):
			x = random.uniform(-50, self.screen_width + 50)
			y = random.uniform(-50, self.screen_height + 50)
			particle = SandParticle(x, y, self.screen_width, self.screen_height)
			self.sand_particles.append(particle)
	
	def _create_dunes(self):
		"""Crea las dunas del desierto."""
		num_dunes = 5
		dune_width = self.screen_width * 2
		dune_height = random.uniform(50, 150)
		
		for i in range(num_dunes):
			x = i * (dune_width * 0.6) - dune_width * 0.3
			y = self.screen_height - dune_height - random.uniform(0, 50)
			
			dune = Dune(x, y, dune_width, dune_height, self.screen_width)
			self.dunes.append(dune)
	
	def update(self, delta_time: float):
		"""Actualiza el fondo de desierto."""
		self.time += delta_time
		
		# Actualizar partículas de arena
		for particle in self.sand_particles:
			particle.update(delta_time)
		
		# Variar la intensidad del viento
		self.wind_strength = 0.3 + 0.4 * math.sin(self.time * 0.5)
	
	def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
		"""
		Renderiza el fondo de desierto.
		
		Args:
			screen: Superficie donde renderizar
			camera_offset: Offset de la cámara (x, y)
		"""
		# Renderizar gradiente de cielo
		self._render_sky_gradient(screen, camera_offset)
		
		# Renderizar dunas
		self._render_dunes(screen, camera_offset)
		
		# Renderizar partículas de arena
		self._render_sand_particles(screen, camera_offset)
		
		# Renderizar efectos atmosféricos
		self._render_atmospheric_effects(screen, camera_offset)
	
	def _render_sky_gradient(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
		"""Renderiza el gradiente del cielo con más profundidad."""
		sky_height = self.screen_height * 0.7
		
		for y in range(int(sky_height)):
			# Interpolar entre colores del cielo con tres puntos
			ratio = y / sky_height
			if ratio < 0.5:
				# Primera mitad: de sky_top a sky_mid
				local_ratio = ratio * 2
				color = self._interpolate_color(
					self.colors['sky_top'],
					self.colors['sky_mid'],
					local_ratio
				)
			else:
				# Segunda mitad: de sky_mid a sky_bottom
				local_ratio = (ratio - 0.5) * 2
				color = self._interpolate_color(
					self.colors['sky_mid'],
					self.colors['sky_bottom'],
					local_ratio
				)
			
			# Aplicar offset de cámara
			render_y = y - camera_offset[1]
			if 0 <= render_y < self.screen_height:
				pygame.draw.line(screen, color, (0, render_y), (self.screen_width, render_y))
	
	def _render_dunes(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
		"""Renderiza las dunas de arena con efectos de profundidad."""
		# Renderizar dunas en orden de profundidad (más lejanas primero)
		sorted_dunes = sorted(self.dunes, key=lambda d: d.y, reverse=True)
		
		for dune in sorted_dunes:
			dune.render(screen, camera_offset)
			
			# Añadir efectos de profundidad
			self._render_dune_effects(screen, dune, camera_offset)
	
	def _render_dune_effects(self, screen: pygame.Surface, dune, camera_offset: Tuple[float, float]):
		"""Renderiza efectos adicionales en las dunas."""
		# Aplicar offset de cámara
		offset_points = []
		for x, y in dune.points:
			offset_x = x - camera_offset[0]
			offset_y = y - camera_offset[1]
			offset_points.append((offset_x, offset_y))
		
		if len(offset_points) > 2:
			# Añadir resaltado en la parte superior de la duna
			highlight_points = []
			for i, (x, y) in enumerate(offset_points):
				# Crear línea de resaltado en la parte superior
				highlight_y = y - 3
				highlight_points.append((x, highlight_y))
			
			if len(highlight_points) > 2:
				pygame.draw.polygon(screen, self.colors['dune_highlight'], highlight_points)
	
	def _render_sand_particles(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
		"""Renderiza las partículas de arena."""
		for particle in self.sand_particles:
			particle.render(screen, camera_offset)
	
	def _render_atmospheric_effects(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
		"""Renderiza efectos atmosféricos adicionales."""
		# Efecto de calor (ondulación)
		if self.time % 2 < 1:
			# Crear líneas de calor
			for i in range(0, self.screen_width, 50):
				heat_intensity = random.uniform(0, 30)
				if heat_intensity > 10:
					heat_color = (255, 255, 255, int(heat_intensity))
					heat_surface = pygame.Surface((2, self.screen_height), pygame.SRCALPHA)
					pygame.draw.line(heat_surface, heat_color, (0, 0), (0, self.screen_height))
					screen.blit(heat_surface, (i, 0))
		
		# Efecto de viento en la arena
		self._render_wind_effect(screen, camera_offset)
		
		# Efecto de profundidad atmosférica
		self._render_atmospheric_depth(screen, camera_offset)
	
	def _render_wind_effect(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
		"""Renderiza el efecto del viento en la arena."""
		# Crear líneas de viento que se mueven
		wind_lines = []
		for i in range(0, self.screen_width, 100):
			wind_start_x = i + (self.time * 50) % 100
			wind_start_y = self.screen_height * 0.8
			wind_end_x = wind_start_x + 30
			wind_end_y = wind_start_y - 20
			
			wind_lines.append(((wind_start_x, wind_start_y), (wind_end_x, wind_end_y)))
		
		# Dibujar líneas de viento
		for start, end in wind_lines:
			wind_color = (255, 255, 255, 40)  # Blanco semi-transparente
			wind_surface = pygame.Surface((abs(end[0] - start[0]) + 2, abs(end[1] - start[1]) + 2), pygame.SRCALPHA)
			pygame.draw.line(wind_surface, wind_color, (0, 0), (end[0] - start[0], end[1] - start[1]), 2)
			screen.blit(wind_surface, (start[0], start[1]))
	
	def _render_atmospheric_depth(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
		"""Renderiza efectos de profundidad atmosférica."""
		# Crear gradiente de niebla en la distancia
		fog_height = self.screen_height * 0.3
		fog_start_y = self.screen_height - fog_height
		
		for y in range(int(fog_height)):
			# Interpolar transparencia de la niebla
			ratio = y / fog_height
			alpha = int(ratio * 60)  # Máximo 60 de alpha
			
			if alpha > 0:
				fog_color = (200, 200, 220, alpha)
				fog_surface = pygame.Surface((self.screen_width, 1), pygame.SRCALPHA)
				pygame.draw.line(fog_surface, fog_color, (0, 0), (self.screen_width, 0))
				screen.blit(fog_surface, (0, fog_start_y + y))
	
	def _interpolate_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
		"""Interpola entre dos colores."""
		return (
			int(color1[0] + (color2[0] - color1[0]) * ratio),
			int(color1[1] + (color2[1] - color1[1]) * ratio),
			int(color1[2] + (color2[2] - color1[2]) * ratio)
		)
	
	def get_parallax_offset(self, camera_x: float, camera_y: float, layer: str = 'background') -> Tuple[float, float]:
		"""
		Obtiene el offset de parallax para diferentes capas.
		
		Args:
			camera_x: Posición X de la cámara
			camera_y: Posición Y de la cámara
			layer: Capa del parallax ('background', 'midground', 'foreground')
			
		Returns:
			Offset de parallax (x, y)
		"""
		parallax_factors = {
			'background': 0.1,   # Cielo - muy lento
			'midground': 0.3,    # Dunas - medio
			'foreground': 0.6    # Arena - rápido
		}
		
		factor = parallax_factors.get(layer, 0.1)
		return (camera_x * factor, camera_y * factor) 