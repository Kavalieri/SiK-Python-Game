"""
Scene Manager - Gestor de escenas
================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona las diferentes escenas del juego (menú, juego, pausa, etc.).
"""

import pygame
import logging
from typing import Optional, Dict
from abc import ABC, abstractmethod

from ..utils.config_manager import ConfigManager


class Scene(ABC):
	"""
	Clase base abstracta para todas las escenas del juego.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager):
		"""
		Inicializa la escena.
		
		Args:
			screen: Superficie de Pygame donde renderizar
			config: Configuración del juego
		"""
		self.screen = screen
		self.config = config
		self.logger = logging.getLogger(self.__class__.__name__)
	
	@abstractmethod
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
		pass
	
	@abstractmethod
	def update(self):
		"""Actualiza la lógica de la escena."""
		pass
	
	@abstractmethod
	def render(self):
		"""Renderiza la escena."""
		pass
	
	def enter(self):
		"""Se llama cuando se entra en la escena."""
		self.logger.info(f"Entrando en escena: {self.__class__.__name__}")
	
	def exit(self):
		"""Se llama cuando se sale de la escena."""
		self.logger.info(f"Saliendo de escena: {self.__class__.__name__}")


class SceneManager:
	"""
	Gestiona las diferentes escenas del juego.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager):
		"""
		Inicializa el gestor de escenas.
		
		Args:
			screen: Superficie de Pygame donde renderizar
			config: Configuración del juego
		"""
		self.screen = screen
		self.config = config
		self.logger = logging.getLogger(__name__)
		
		self.scenes: Dict[str, Scene] = {}
		self.current_scene: Optional[Scene] = None
		self.next_scene: Optional[str] = None
		
		self.logger.info("Gestor de escenas inicializado")
	
	def add_scene(self, name: str, scene: Scene):
		"""
		Añade una escena al gestor.
		
		Args:
			name: Nombre identificativo de la escena
			scene: Instancia de la escena
		"""
		self.scenes[name] = scene
		self.logger.info(f"Escena añadida: {name}")
	
	def change_scene(self, scene_name: str):
		"""
		Cambia a una escena específica.
		
		Args:
			scene_name: Nombre de la escena a cambiar
		"""
		if scene_name not in self.scenes:
			self.logger.error(f"Escena no encontrada: {scene_name}")
			return
		
		self.next_scene = scene_name
		self.logger.info(f"Solicitado cambio a escena: {scene_name}")
	
	def _switch_scene(self):
		"""Realiza el cambio de escena."""
		if self.next_scene is None:
			return
		
		# Salir de la escena actual
		if self.current_scene:
			self.current_scene.exit()
		
		# Entrar en la nueva escena
		self.current_scene = self.scenes[self.next_scene]
		self.current_scene.enter()
		
		self.logger.info(f"Cambiado a escena: {self.next_scene}")
		self.next_scene = None
	
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
		if self.current_scene:
			self.current_scene.handle_event(event)
	
	def update(self):
		"""Actualiza la lógica del gestor de escenas."""
		self._switch_scene()
		
		if self.current_scene:
			self.current_scene.update()
	
	def render(self):
		"""Renderiza la escena actual."""
		if self.current_scene:
			self.current_scene.render()
		else:
			# Pantalla de carga o error
			self.screen.fill((0, 0, 0))
			font = pygame.font.Font(None, 36)
			text = font.render("Cargando...", True, (255, 255, 255))
			text_rect = text.get_rect(center=self.screen.get_rect().center)
			self.screen.blit(text, text_rect) 