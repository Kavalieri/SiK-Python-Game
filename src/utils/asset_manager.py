"""
Asset Manager - Gestor de recursos
=================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona la carga y almacenamiento de recursos del juego (imágenes, sonidos, etc.).
"""

import pygame
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import json


class AssetManager:
	"""
	Gestiona los recursos del juego (imágenes, sonidos, fuentes, etc.).
	"""
	
	def __init__(self, assets_path: str = "assets"):
		"""
		Inicializa el gestor de assets.
		
		Args:
			assets_path: Ruta al directorio de assets
		"""
		self.logger = logging.getLogger(__name__)
		self.assets_path = Path(assets_path)
		self.images: Dict[str, pygame.Surface] = {}
		self.sounds: Dict[str, pygame.mixer.Sound] = {}
		self.music: Dict[str, str] = {}
		self.fonts: Dict[str, pygame.font.Font] = {}
		self.image_cache: Dict[str, pygame.Surface] = {}
		
		self.logger.info(f"Gestor de assets inicializado en: {self.assets_path}")
	
	def load_image(self, name: str, file_path: str, scale: float = 1.0) -> Optional[pygame.Surface]:
		"""
		Carga una imagen y la almacena en caché.
		
		Args:
			name: Nombre identificativo de la imagen
			file_path: Ruta relativa al archivo de imagen
			scale: Factor de escala (1.0 = tamaño original)
			
		Returns:
			Superficie de Pygame con la imagen cargada
		"""
		try:
			full_path = self.assets_path / file_path
			
			if not full_path.exists():
				self.logger.error(f"Archivo de imagen no encontrado: {full_path}")
				return None
			
			image = pygame.image.load(str(full_path)).convert_alpha()
			
			if scale != 1.0:
				new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
				image = pygame.transform.scale(image, new_size)
			
			self.images[name] = image
			self.logger.debug(f"Imagen cargada: {name} desde {file_path}")
			return image
			
		except Exception as e:
			self.logger.error(f"Error al cargar imagen {name}: {e}")
			return None
	
	def get_image(self, image_name: str) -> Optional[pygame.Surface]:
		"""
		Obtiene una imagen por nombre.
		
		Args:
			image_name: Nombre de la imagen
			
		Returns:
			Superficie de pygame o None si no se encuentra
		"""
		# Buscar en caché primero
		if image_name in self.image_cache:
			return self.image_cache[image_name]
		
		# Intentar diferentes rutas y variaciones
		possible_paths = [
			# Fondos
			f"fondos/{image_name}/{image_name}.png",
			f"fondos/{image_name}/{image_name}_parallax.png",
			f"fondos/{image_name}/{image_name}.1.png",
			f"fondos/{image_name}/{image_name}.2.png",
			f"fondos/{image_name}/{image_name}.3.png",
			f"fondos/{image_name}/{image_name}.4.png",
			f"fondos/{image_name}/game_background_1.png",
			f"fondos/{image_name}/game_background_2.png",
			f"fondos/{image_name}/game_background_3.png",
			f"fondos/{image_name}/game_background_4.png",
			f"fondos/{image_name}/platformer_background_1.png",
			f"fondos/{image_name}/platformer_background_2.png",
			f"fondos/{image_name}/platformer_background_3.png",
			f"fondos/{image_name}/platformer_background_4.png",
			# UI
			f"ui/{image_name}.png",
			# Objetos varios
			f"objects/varios/{image_name}.png",
			f"objects/proyectiles/{image_name}.png",
			# Elementos del mundo (nuevo)
			f"objects/elementos/{image_name}.png",
			f"objects/elementos/{image_name}_1.png",
			f"objects/elementos/{image_name}_2.png",
			f"objects/elementos/{image_name}_3.png",
			# Personajes
			f"characters/{image_name}/Idle_1_.png",
			f"characters/{image_name}/Run_1_.png",
			f"characters/{image_name}/Attack_1_.png",
			f"characters/{image_name}/Walk_1_.png",
			f"characters/{image_name}/Jump_1_.png",
			f"characters/{image_name}/Dead_1_.png",
		]
		
		for path in possible_paths:
			image = self.load_image_direct(path)
			if image:
				self.image_cache[image_name] = image
				return image
		
		# Si no se encuentra, crear un placeholder
		self.logger.warning(f"Imagen no encontrada: {image_name}, creando placeholder")
		placeholder = self._create_placeholder_image(image_name)
		self.image_cache[image_name] = placeholder
		return placeholder
	
	def _create_placeholder_image(self, name: str) -> pygame.Surface:
		"""
		Crea una imagen placeholder cuando no se encuentra la imagen real.
		
		Args:
			name: Nombre de la imagen
			
		Returns:
			Superficie placeholder
		"""
		# Crear superficie de 800x600 para fondos
		if "background" in name.lower() or "fondo" in name.lower():
			surface = pygame.Surface((800, 600))
			# Gradiente de colores
			for y in range(600):
				color = (
					max(0, min(255, 50 + y // 3)),
					max(0, min(255, 100 + y // 4)),
					max(0, min(255, 150 + y // 5))
				)
				pygame.draw.line(surface, color, (0, y), (800, y))
			
			# Añadir texto
			font = pygame.font.Font(None, 36)
			text = font.render(f"Fondo: {name}", True, (255, 255, 255))
			text_rect = text.get_rect(center=(400, 300))
			surface.blit(text, text_rect)
			
			return surface
		else:
			# Para otros tipos de imágenes, crear un cuadrado de color
			surface = pygame.Surface((100, 100))
			# Color basado en el nombre
			hash_value = hash(name) % 0xFFFFFF
			color = (
				(hash_value >> 16) & 0xFF,
				(hash_value >> 8) & 0xFF,
				hash_value & 0xFF
			)
			surface.fill(color)
			
			# Añadir texto
			font = pygame.font.Font(None, 24)
			text = font.render(name[:8], True, (255, 255, 255))
			text_rect = text.get_rect(center=(50, 50))
			surface.blit(text, text_rect)
			
			return surface
	
	def get_character_sprite(self, character_name: str, animation: str = "idle", frame: int = 1) -> Optional[pygame.Surface]:
		"""
		Obtiene un sprite específico de un personaje.
		
		Args:
			character_name: Nombre del personaje
			animation: Tipo de animación
			frame: Número de frame
			
		Returns:
			Superficie del sprite o None si no se encuentra
		"""
		# Crear clave de caché
		cache_key = f"{character_name}_{animation}_{frame}"
		
		# Buscar en caché
		if cache_key in self.image_cache:
			return self.image_cache[cache_key]
		
		# Intentar cargar el sprite con el formato correcto
		# Los archivos pueden estar en subdirectorios o directamente en el directorio del personaje
		# Formato: Idle_1_.png, Run_1_.png, etc.
		animation_capitalized = animation.capitalize()
		
		# Intentar diferentes rutas posibles (nueva estructura organizada)
		possible_paths = [
			# Nueva estructura organizada
			f"characters/used/{character_name}/{animation}/{animation_capitalized}_{frame}_.png",  # Con subdirectorio
			f"characters/used/{character_name}/{animation_capitalized}_{frame}_.png",  # Sin subdirectorio
			f"characters/used/{character_name}/{animation}/{animation_capitalized}_{frame}.png",  # Sin guión bajo
			f"characters/used/{character_name}/{animation_capitalized}_{frame}.png",  # Sin subdirectorio ni guión bajo
			# Estructura original (fallback)
			f"characters/{character_name}/{animation}/{animation_capitalized}_{frame}_.png",  # Con subdirectorio
			f"characters/{character_name}/{animation_capitalized}_{frame}_.png",  # Sin subdirectorio
			f"characters/{character_name}/{animation}/{animation_capitalized}_{frame}.png",  # Sin guión bajo
			f"characters/{character_name}/{animation_capitalized}_{frame}.png"  # Sin subdirectorio ni guión bajo
		]
		
		# Intentar cargar desde las diferentes rutas
		for path in possible_paths:
			sprite = self.load_image(cache_key, path, 1.0)
			if sprite:
				self.image_cache[cache_key] = sprite
				return sprite
		
		# Si no se encuentra, crear un placeholder de personaje
		self.logger.warning(f"Sprite no encontrado: {character_name}/{animation}/{frame}, creando placeholder")
		placeholder = self._create_character_placeholder(character_name, animation)
		self.image_cache[cache_key] = placeholder
		return placeholder
	
	def get_character_animation_frames(self, character_name: str, animation: str = "idle") -> List[pygame.Surface]:
		"""
		Obtiene todos los frames de una animación de personaje.
		
		Args:
			character_name: Nombre del personaje
			animation: Tipo de animación
			
		Returns:
			Lista de superficies con los frames de la animación
		"""
		frames = []
		frame = 1
		
		# Intentar cargar frames hasta que no se encuentre más
		while True:
			sprite = self.get_character_sprite(character_name, animation, frame)
			if sprite:
				frames.append(sprite)
				frame += 1
			else:
				break
		
		# Si no se encontraron frames, crear al menos uno
		if not frames:
			placeholder = self._create_character_placeholder(character_name, animation)
			frames.append(placeholder)
		
		return frames
	
	def _create_character_placeholder(self, character_name: str, animation: str) -> pygame.Surface:
		"""
		Crea un placeholder para sprites de personajes.
		
		Args:
			character_name: Nombre del personaje
			animation: Tipo de animación
			
		Returns:
			Superficie placeholder
		"""
		surface = pygame.Surface((64, 64))
		
		# Color basado en el personaje
		character_colors = {
			"guerrero": (139, 69, 19),    # Marrón
			"robot": (128, 128, 128),     # Gris
			"adventureguirl": (255, 182, 193),  # Rosa claro
			"zombiemale": (34, 139, 34),  # Verde
			"zombieguirl": (218, 112, 214)  # Violeta
		}
		
		color = character_colors.get(character_name.lower(), (255, 0, 0))
		surface.fill(color)
		
		# Añadir borde
		pygame.draw.rect(surface, (255, 255, 255), (0, 0, 64, 64), 2)
		
		# Añadir símbolo según el personaje
		symbols = {
			"guerrero": "⚔️",
			"robot": "🤖",
			"adventureguirl": "👧",
			"zombiemale": "🧟",
			"zombieguirl": "🧟‍♀️"
		}
		
		symbol = symbols.get(character_name.lower(), "?")
		try:
			font = pygame.font.Font(None, 32)
			text = font.render(symbol, True, (255, 255, 255))
			text_rect = text.get_rect(center=(32, 32))
			surface.blit(text, text_rect)
		except:
			pass
		
		return surface
	
	def get_ui_button(self, button_name: str, state: str = "n") -> Optional[pygame.Surface]:
		"""
		Obtiene un botón UI del directorio de botones.
		
		Args:
			button_name: Nombre del botón (ej: "bleft", "bright", "arrow_r_l", "arrow_l_l")
			state: Estado del botón ("n"=normal, "h"=hover, "p"=pressed, "l"=locked)
			
		Returns:
			Superficie del botón o None si no se encuentra
		"""
		# Crear clave de caché
		cache_key = f"ui_button_{button_name}_{state}"
		
		# Buscar en caché
		if cache_key in self.image_cache:
			return self.image_cache[cache_key]
		
		# Intentar cargar el botón
		path = f"ui/Buttons/botonescuadrados/slategrey/{button_name}_{state}.png"
		button = self.load_image(cache_key, path, 1.0)
		
		if button:
			self.image_cache[cache_key] = button
			return button
		
		# Si no se encuentra, crear un placeholder
		self.logger.warning(f"Botón UI no encontrado: {path}, creando placeholder")
		placeholder = self._create_button_placeholder(button_name, state)
		self.image_cache[cache_key] = placeholder
		return placeholder
	
	def _create_button_placeholder(self, button_name: str, state: str) -> pygame.Surface:
		"""
		Crea un placeholder para botones UI.
		
		Args:
			button_name: Nombre del botón
			state: Estado del botón
			
		Returns:
			Superficie placeholder
		"""
		surface = pygame.Surface((60, 60))
		
		# Color basado en el estado
		state_colors = {
			"n": (100, 100, 100),  # Normal - Gris
			"h": (150, 150, 150),  # Hover - Gris claro
			"p": (80, 80, 80),     # Pressed - Gris oscuro
			"l": (60, 60, 60)      # Locked - Gris muy oscuro
		}
		
		color = state_colors.get(state, (100, 100, 100))
		surface.fill(color)
		
		# Añadir borde
		pygame.draw.rect(surface, (200, 200, 200), (0, 0, 60, 60), 2)
		
		# Añadir símbolo según el botón
		symbols = {
			"bleft": "←",
			"bright": "→",
			"blank": "□",
			"circle": "○",
			"star": "★",
			"heart": "♥"
		}
		
		symbol = symbols.get(button_name, "?")
		try:
			font = pygame.font.Font(None, 32)
			text = font.render(symbol, True, (255, 255, 255))
			text_rect = text.get_rect(center=(30, 30))
			surface.blit(text, text_rect)
		except:
			pass
		
		return surface
	
	def get_powerup_sprite(self, powerup_name: str) -> Optional[pygame.Surface]:
		"""
		Obtiene un sprite de powerup.
		
		Args:
			powerup_name: Nombre del powerup
			
		Returns:
			Superficie del powerup o None si no se encuentra
		"""
		# Crear clave de caché
		cache_key = f"powerup_{powerup_name}"
		
		# Buscar en caché
		if cache_key in self.image_cache:
			return self.image_cache[cache_key]
		
		# Intentar cargar el powerup
		path = f"objects/varios/{powerup_name}.png"
		powerup = self.load_image(cache_key, path, 1.0)
		
		if powerup:
			self.image_cache[cache_key] = powerup
			return powerup
		
		# Si no se encuentra, crear un placeholder
		self.logger.warning(f"Powerup no encontrado: {path}, creando placeholder")
		placeholder = self._create_powerup_placeholder(powerup_name)
		self.image_cache[cache_key] = placeholder
		return placeholder
	
	def _create_powerup_placeholder(self, powerup_name: str) -> pygame.Surface:
		"""
		Crea un placeholder para powerups.
		
		Args:
			powerup_name: Nombre del powerup
			
		Returns:
			Superficie placeholder
		"""
		surface = pygame.Surface((32, 32))
		
		# Color basado en el tipo de powerup
		powerup_colors = {
			"potion": (255, 0, 255),      # Magenta
			"shield": (0, 255, 255),      # Cyan
			"sword": (255, 255, 0),       # Amarillo
			"coin": (255, 215, 0),        # Dorado
			"heart": (255, 0, 0),         # Rojo
			"star": (255, 255, 255),      # Blanco
			"crystal": (0, 255, 0),       # Verde
			"ring": (255, 165, 0),        # Naranja
			"scroll": (139, 69, 19),      # Marrón
			"key": (255, 255, 255)        # Blanco
		}
		
		color = powerup_colors.get(powerup_name.lower(), (128, 128, 128))
		surface.fill(color)
		
		# Añadir borde
		pygame.draw.rect(surface, (255, 255, 255), (0, 0, 32, 32), 2)
		
		# Añadir símbolo según el powerup
		symbols = {
			"potion": "⚗",
			"shield": "🛡",
			"sword": "⚔",
			"coin": "💰",
			"heart": "♥",
			"star": "★",
			"crystal": "💎",
			"ring": "💍",
			"scroll": "📜",
			"key": "🔑"
		}
		
		symbol = symbols.get(powerup_name.lower(), "?")
		try:
			font = pygame.font.Font(None, 20)
			text = font.render(symbol, True, (255, 255, 255))
			text_rect = text.get_rect(center=(16, 16))
			surface.blit(text, text_rect)
		except:
			pass
		
		return surface
	
	def load_sound(self, name: str, file_path: str) -> Optional[pygame.mixer.Sound]:
		"""
		Carga un sonido y lo almacena en caché.
		
		Args:
			name: Nombre identificativo del sonido
			file_path: Ruta relativa al archivo de sonido
			
		Returns:
			Objeto Sound de Pygame o None si hay error
		"""
		try:
			full_path = self.assets_path / file_path
			
			if not full_path.exists():
				self.logger.error(f"Archivo de sonido no encontrado: {full_path}")
				return None
			
			sound = pygame.mixer.Sound(str(full_path))
			self.sounds[name] = sound
			self.logger.debug(f"Sonido cargado: {name} desde {file_path}")
			return sound
			
		except Exception as e:
			self.logger.error(f"Error al cargar sonido {name}: {e}")
			return None
	
	def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
		"""
		Obtiene un sonido del caché.
		
		Args:
			name: Nombre del sonido
			
		Returns:
			Objeto Sound de Pygame o None si no existe
		"""
		return self.sounds.get(name)
	
	def load_font(self, name: str, file_path: str, size: int = 24) -> Optional[pygame.font.Font]:
		"""
		Carga una fuente y la almacena en caché.
		
		Args:
			name: Nombre identificativo de la fuente
			file_path: Ruta relativa al archivo de fuente
			size: Tamaño de la fuente
			
		Returns:
			Objeto Font de Pygame o None si hay error
		"""
		try:
			full_path = self.assets_path / file_path
			
			if not full_path.exists():
				self.logger.error(f"Archivo de fuente no encontrado: {full_path}")
				return None
			
			font = pygame.font.Font(str(full_path), size)
			self.fonts[name] = font
			self.logger.debug(f"Fuente cargada: {name} desde {file_path}")
			return font
			
		except Exception as e:
			self.logger.error(f"Error al cargar fuente {name}: {e}")
			return None
	
	def get_font(self, name: str) -> Optional[pygame.font.Font]:
		"""
		Obtiene una fuente del caché.
		
		Args:
			name: Nombre de la fuente
			
		Returns:
			Objeto Font de Pygame o None si no existe
		"""
		return self.fonts.get(name)
	
	def load_assets_from_config(self, config_file: str = "assets_config.json"):
		"""
		Carga assets desde un archivo de configuración.
		
		Args:
			config_file: Ruta al archivo de configuración de assets
		"""
		try:
			config_path = self.assets_path / config_file
			
			if not config_path.exists():
				self.logger.warning(f"Archivo de configuración de assets no encontrado: {config_path}")
				return
			
			with open(config_path, 'r', encoding='utf-8') as f:
				config = json.load(f)
			
			# Cargar imágenes
			for image_config in config.get('images', []):
				self.load_image(
					image_config['name'],
					image_config['path'],
					image_config.get('scale', 1.0)
				)
			
			# Cargar sonidos
			for sound_config in config.get('sounds', []):
				self.load_sound(sound_config['name'], sound_config['path'])
			
			# Cargar fuentes
			for font_config in config.get('fonts', []):
				self.load_font(
					font_config['name'],
					font_config['path'],
					font_config.get('size', 24)
				)
			
			self.logger.info("Assets cargados desde configuración")
			
		except Exception as e:
			self.logger.error(f"Error al cargar assets desde configuración: {e}")
	
	def clear_cache(self):
		"""Limpia el caché de assets."""
		self.images.clear()
		self.sounds.clear()
		self.fonts.clear()
		self.logger.info("Caché de assets limpiado")
	
	def get_files_matching_pattern(self, base_path: str, pattern: str) -> List[str]:
		"""
		Busca archivos que coincidan con un patrón en una ruta base.
		
		Args:
			base_path: Ruta base relativa al directorio de assets
			pattern: Patrón de búsqueda (ej: "*.png", "idle*.png")
			
		Returns:
			Lista de rutas de archivos que coinciden con el patrón
		"""
		import glob
		import os
		
		try:
			full_base_path = self.assets_path / base_path
			if not full_base_path.exists():
				self.logger.warning(f"Ruta base no encontrada: {base_path}")
				return []
			
			# Buscar archivos que coincidan con el patrón
			search_pattern = str(full_base_path / pattern)
			matching_files = glob.glob(search_pattern)
			
			# Convertir a rutas relativas
			relative_files = []
			for file_path in matching_files:
				relative_path = os.path.relpath(file_path, self.assets_path)
				relative_files.append(relative_path.replace('\\', '/'))
			
			self.logger.debug(f"Encontrados {len(relative_files)} archivos para patrón {pattern} en {base_path}")
			return relative_files
			
		except Exception as e:
			self.logger.error(f"Error al buscar archivos con patrón {pattern} en {base_path}: {e}")
			return []
	
	def load_image_direct(self, path: str) -> Optional[pygame.Surface]:
		"""
		Carga una imagen directamente desde una ruta.
		
		Args:
			path: Ruta de la imagen relativa al directorio de assets
			
		Returns:
			Superficie de Pygame con la imagen cargada o None si hay error
		"""
		try:
			full_path = self.assets_path / path
			if full_path.exists():
				image = pygame.image.load(str(full_path)).convert_alpha()
				self.logger.debug(f"Imagen cargada directamente: {path}")
				return image
			else:
				self.logger.warning(f"Archivo de imagen no encontrado: {path}")
				return None
		except Exception as e:
			self.logger.error(f"Error al cargar imagen {path}: {e}")
			return None 