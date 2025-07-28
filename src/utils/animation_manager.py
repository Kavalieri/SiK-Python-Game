"""
Animation Manager - Gestor de Animaciones
========================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona las animaciones de sprites para todas las entidades del juego.
"""

import pygame
import logging
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from enum import Enum

from .config_manager import ConfigManager
from .asset_manager import AssetManager


class AnimationState(Enum):
	"""Estados de animación disponibles."""
	IDLE = "idle"
	WALK = "walk"
	RUN = "run"
	JUMP = "jump"
	ATTACK = "attack"
	SHOOT = "shoot"
	MELEE = "melee"
	SLIDE = "slide"
	DEAD = "dead"
	EXPLOSION = "explosion"


class Animation:
	"""
	Representa una animación con sus frames y configuración.
	"""
	
	def __init__(self, frames: List[pygame.Surface], fps: float = 10.0, loop: bool = True):
		"""
		Inicializa una animación.
		
		Args:
			frames: Lista de superficies (frames) de la animación
			fps: Frames por segundo de la animación
			loop: Si la animación debe repetirse
		"""
		self.frames = frames
		self.fps = fps
		self.loop = loop
		self.frame_duration = 1.0 / fps
		self.current_frame = 0
		self.timer = 0.0
		self.finished = False
	
	def update(self, delta_time: float):
		"""
		Actualiza la animación.
		
		Args:
			delta_time: Tiempo transcurrido desde el último frame
		"""
		if self.finished:
			return
		
		self.timer += delta_time
		
		if self.timer >= self.frame_duration:
			self.timer = 0.0
			self.current_frame += 1
			
			if self.current_frame >= len(self.frames):
				if self.loop:
					self.current_frame = 0
				else:
					self.current_frame = len(self.frames) - 1
					self.finished = True
	
	def get_current_frame(self) -> pygame.Surface:
		"""
		Obtiene el frame actual de la animación.
		
		Returns:
			Superficie del frame actual
		"""
		if self.frames and self.current_frame < len(self.frames):
			return self.frames[self.current_frame]
		return None
	
	def reset(self):
		"""Reinicia la animación."""
		self.current_frame = 0
		self.timer = 0.0
		self.finished = False
	
	def is_finished(self) -> bool:
		"""
		Verifica si la animación ha terminado.
		
		Returns:
			True si la animación ha terminado
		"""
		return self.finished


class AnimationManager:
	"""
	Gestiona las animaciones de todas las entidades del juego.
	"""
	
	def __init__(self, config: ConfigManager, asset_manager: AssetManager):
		"""
		Inicializa el gestor de animaciones.
		
		Args:
			config: Configuración del juego
			asset_manager: Gestor de assets
		"""
		self.config = config
		self.asset_manager = asset_manager
		self.logger = logging.getLogger(__name__)
		
		# Configuración de animaciones
		self.animations: Dict[str, Dict[AnimationState, Animation]] = {}
		self.animation_configs = self._load_animation_configs()
		
		self.logger.info("Gestor de animaciones inicializado")
	
	def _load_animation_configs(self) -> Dict[str, Dict[str, Dict]]:
		"""
		Carga las configuraciones de animación.
		
		Returns:
			Configuraciones de animación por entidad
		"""
		return {
			'guerrero': {
				'idle': {'fps': 8, 'loop': True},
				'walk': {'fps': 10, 'loop': True},
				'run': {'fps': 12, 'loop': True},
				'jump': {'fps': 8, 'loop': False},
				'attack': {'fps': 15, 'loop': False},
				'dead': {'fps': 6, 'loop': False}
			},
			'adventureguirl': {
				'idle': {'fps': 8, 'loop': True},
				'run': {'fps': 12, 'loop': True},
				'jump': {'fps': 8, 'loop': False},
				'shoot': {'fps': 15, 'loop': False},
				'melee': {'fps': 12, 'loop': False},
				'slide': {'fps': 10, 'loop': False},
				'dead': {'fps': 6, 'loop': False}
			},
			'robot': {
				'idle': {'fps': 8, 'loop': True},
				'run': {'fps': 12, 'loop': True},
				'jump': {'fps': 8, 'loop': False},
				'shoot': {'fps': 15, 'loop': False},
				'melee': {'fps': 12, 'loop': False},
				'slide': {'fps': 10, 'loop': False},
				'runshoot': {'fps': 12, 'loop': True},
				'jumpshoot': {'fps': 8, 'loop': False},
				'jumpmelee': {'fps': 8, 'loop': False},
				'dead': {'fps': 6, 'loop': False}
			},
			'zombiemale': {
				'idle': {'fps': 6, 'loop': True},
				'walk': {'fps': 8, 'loop': True},
				'attack': {'fps': 10, 'loop': False},
				'dead': {'fps': 6, 'loop': False}
			},
			'zombieguirl': {
				'idle': {'fps': 6, 'loop': True},
				'walk': {'fps': 8, 'loop': True},
				'attack': {'fps': 10, 'loop': False},
				'dead': {'fps': 6, 'loop': False}
			},
			'explosion': {
				'explosion': {'fps': 15, 'loop': False}
			}
		}
	
	def load_character_animations(self, character_name: str) -> Dict[AnimationState, Animation]:
		"""
		Carga las animaciones de un personaje.
		
		Args:
			character_name: Nombre del personaje
			
		Returns:
			Diccionario con las animaciones del personaje
		"""
		if character_name in self.animations:
			return self.animations[character_name]
		
		animations = {}
		character_path = f"characters/{character_name}"
		
		# Obtener configuración del personaje
		config = self.animation_configs.get(character_name, {})
		
		# Cargar cada animación disponible
		for anim_name, anim_config in config.items():
			try:
				anim_state = AnimationState(anim_name)
				frames = self._load_animation_frames(character_path, anim_name)
			except ValueError:
				self.logger.warning(f"Estado de animación no válido: {anim_name}")
				continue
			
			if frames:
				animations[anim_state] = Animation(
					frames=frames,
					fps=anim_config.get('fps', 10),
					loop=anim_config.get('loop', True)
				)
				self.logger.debug(f"Animación {anim_name} cargada para {character_name}: {len(frames)} frames")
		
		self.animations[character_name] = animations
		return animations
	
	def _load_animation_frames(self, base_path: str, animation_name: str) -> List[pygame.Surface]:
		"""
		Carga los frames de una animación específica.
		
		Args:
			base_path: Ruta base del personaje
			animation_name: Nombre de la animación
			
		Returns:
			Lista de frames de la animación
		"""
		frames = []
		animation_path = f"{base_path}/{animation_name}"
		
		try:
			# Buscar archivos de la animación
			pattern = f"{animation_name}*.png"
			files = self.asset_manager.get_files_matching_pattern(animation_path, pattern)
			
			if not files:
				self.logger.warning(f"No se encontraron archivos para la animación {animation_path}")
				return frames
			
			# Ordenar archivos por número
			files.sort(key=lambda x: self._extract_number_from_filename(x))
			
			# Cargar cada frame
			for file_path in files:
				frame = self.asset_manager.load_image(file_path)
				if frame:
					frames.append(frame)
			
			self.logger.debug(f"Cargados {len(frames)} frames para {animation_path}")
			
		except Exception as e:
			self.logger.error(f"Error al cargar animación {animation_path}: {e}")
		
		return frames
	
	def _extract_number_from_filename(self, filename: str) -> int:
		"""
		Extrae el número del nombre del archivo.
		
		Args:
			filename: Nombre del archivo
			
		Returns:
			Número extraído del archivo
		"""
		try:
			# Buscar números en el nombre del archivo
			import re
			numbers = re.findall(r'\d+', filename)
			if numbers:
				return int(numbers[0])
		except:
			pass
		return 0
	
	def load_explosion_animation(self) -> Animation:
		"""
		Carga la animación de explosión.
		
		Returns:
			Animación de explosión
		"""
		frames = []
		explosion_path = "objects/proyectiles"
		
		try:
			# Cargar frames de explosión
			for i in range(1, 11):  # Explosion_1.png a Explosion_10.png
				frame_path = f"{explosion_path}/Explosion_{i}.png"
				frame = self.asset_manager.load_image(frame_path)
				if frame:
					frames.append(frame)
			
			if frames:
				config = self.animation_configs.get('explosion', {}).get('explosion', {})
				animation = Animation(
					frames=frames,
					fps=config.get('fps', 15),
					loop=config.get('loop', False)
				)
				self.logger.debug(f"Animación de explosión cargada: {len(frames)} frames")
				return animation
				
		except Exception as e:
			self.logger.error(f"Error al cargar animación de explosión: {e}")
		
		return None
	
	def get_animation(self, character_name: str, state: AnimationState) -> Optional[Animation]:
		"""
		Obtiene una animación específica.
		
		Args:
			character_name: Nombre del personaje
			state: Estado de la animación
			
		Returns:
			Animación solicitada o None si no existe
		"""
		if character_name not in self.animations:
			self.load_character_animations(character_name)
		
		animations = self.animations.get(character_name, {})
		return animations.get(state)
	
	def update_animation(self, character_name: str, state: AnimationState, delta_time: float):
		"""
		Actualiza una animación específica.
		
		Args:
			character_name: Nombre del personaje
			state: Estado de la animación
			delta_time: Tiempo transcurrido
		"""
		animation = self.get_animation(character_name, state)
		if animation:
			animation.update(delta_time)
	
	def reset_animation(self, character_name: str, state: AnimationState):
		"""
		Reinicia una animación específica.
		
		Args:
			character_name: Nombre del personaje
			state: Estado de la animación
		"""
		animation = self.get_animation(character_name, state)
		if animation:
			animation.reset()
	
	def get_current_frame(self, character_name: str, state: AnimationState) -> Optional[pygame.Surface]:
		"""
		Obtiene el frame actual de una animación.
		
		Args:
			character_name: Nombre del personaje
			state: Estado de la animación
			
		Returns:
			Frame actual o None si no existe
		"""
		animation = self.get_animation(character_name, state)
		if animation:
			return animation.get_current_frame()
		return None
	
	def is_animation_finished(self, character_name: str, state: AnimationState) -> bool:
		"""
		Verifica si una animación ha terminado.
		
		Args:
			character_name: Nombre del personaje
			state: Estado de la animación
			
		Returns:
			True si la animación ha terminado
		"""
		animation = self.get_animation(character_name, state)
		if animation:
			return animation.is_finished()
		return True
	
	def preload_all_animations(self):
		"""Precarga todas las animaciones disponibles."""
		characters = ['guerrero', 'adventureguirl', 'robot', 'zombiemale', 'zombieguirl']
		
		for character in characters:
			self.load_character_animations(character)
		
		self.logger.info(f"Todas las animaciones precargadas: {len(self.animations)} personajes")
	
	def get_available_animations(self, character_name: str) -> List[AnimationState]:
		"""
		Obtiene las animaciones disponibles para un personaje.
		
		Args:
			character_name: Nombre del personaje
			
		Returns:
			Lista de estados de animación disponibles
		"""
		if character_name not in self.animations:
			self.load_character_animations(character_name)
		
		animations = self.animations.get(character_name, {})
		return list(animations.keys())
	
	def set_animation_state(self, character_name: str, state: AnimationState):
		"""
		Establece el estado de animación actual para un personaje.
		
		Args:
			character_name: Nombre del personaje
			state: Estado de animación a establecer
		"""
		if character_name not in self.animations:
			self.load_character_animations(character_name)
		
		animations = self.animations.get(character_name, {})
		if state in animations:
			# Reiniciar la animación del nuevo estado
			animations[state].reset()
	
	def get_current_sprite(self, character_name: str) -> Optional[pygame.Surface]:
		"""
		Obtiene el sprite actual del personaje basado en su estado de animación.
		
		Args:
			character_name: Nombre del personaje
			
		Returns:
			Superficie del sprite actual o None
		"""
		if character_name not in self.animations:
			self.load_character_animations(character_name)
		
		animations = self.animations.get(character_name, {})
		# Buscar la primera animación disponible
		for state, animation in animations.items():
			if animation and animation.frames:
				return animation.get_current_frame()
		return None
	
	def update_character_animation(self, character_name: str, delta_time: float):
		"""
		Actualiza la animación del personaje.
		
		Args:
			character_name: Nombre del personaje
			delta_time: Tiempo transcurrido
		"""
		if character_name not in self.animations:
			self.load_character_animations(character_name)
		
		animations = self.animations.get(character_name, {})
		for animation in animations.values():
			if animation:
				animation.update(delta_time) 