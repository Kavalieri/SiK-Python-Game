"""
Game Engine - Motor principal del juego
======================================

Autor: SiK Team
Fecha: 2024
Descripción: Motor principal que gestiona el bucle del juego, renderizado y eventos.
"""

import pygame
import logging
from typing import Optional
from pathlib import Path

from .game_state import GameState
from .scene_manager import SceneManager
from ..utils.config_manager import ConfigManager
from ..utils.save_manager import SaveManager
from ..ui.menu_manager import MenuManager
from ..scenes.character_select_scene import CharacterSelectScene


class GameEngine:
	"""
	Motor principal del juego que gestiona el bucle principal, renderizado y eventos.
	"""
	
	def __init__(self, config: ConfigManager):
		"""
		Inicializa el motor del juego.
		
		Args:
			config: Gestor de configuración del juego
		"""
		self.logger = logging.getLogger(__name__)
		self.config = config
		self.running = False
		self.clock = None
		self.screen = None
		self.game_state = None
		self.scene_manager = None
		self.save_manager = None
		self.menu_manager = None
		
		self.logger.info("Inicializando motor del juego...")
		self._initialize_pygame()
		self._initialize_components()
		self.logger.info("Motor del juego inicializado correctamente")
	
	def _initialize_pygame(self):
		"""Inicializa Pygame y configura la pantalla."""
		try:
			pygame.init()
			pygame.mixer.init()
			
			# Configurar pantalla
			screen_width = self.config.get('display', 'width', 1280)
			screen_height = self.config.get('display', 'height', 720)
			title = self.config.get('game', 'title', 'SiK Python Game')
			
			self.screen = pygame.display.set_mode((screen_width, screen_height))
			pygame.display.set_caption(title)
			
			# Configurar reloj
			fps = self.config.get('display', 'fps', 60)
			self.clock = pygame.time.Clock()
			
			self.logger.info(f"Pygame inicializado - Resolución: {screen_width}x{screen_height}, FPS: {fps}")
			
		except Exception as e:
			self.logger.error(f"Error al inicializar Pygame: {e}")
			raise
	
	def _initialize_components(self):
		"""Inicializa los componentes principales del juego."""
		try:
			# Inicializar estado del juego
			self.game_state = GameState()
			
			# Inicializar gestor de guardado
			self.save_manager = SaveManager(self.config)
			
			# Inicializar gestor de menús
			self.menu_manager = MenuManager(self.screen, self.config, self.game_state, self.save_manager)
			
			# Inicializar gestor de escenas
			self.scene_manager = SceneManager(self.screen, self.config)
			
			# Configurar escenas iniciales
			self._setup_scenes()
			
			self.logger.info("Componentes del juego inicializados")
			
		except Exception as e:
			self.logger.error(f"Error al inicializar componentes: {e}")
			raise
	
	def _setup_scenes(self):
		"""Configura las escenas iniciales del juego."""
		try:
			from ..scenes.welcome_scene import WelcomeScene
			from ..scenes.main_menu_scene import MainMenuScene
			from ..scenes.game_scene import GameScene
			from ..scenes.pause_scene import PauseScene
			from ..scenes.character_select_scene import CharacterSelectScene
			from ..scenes.loading_scene import LoadingScene
			
			# Crear todas las escenas
			loading_scene = LoadingScene(self.screen, self.config, self.game_state, self.save_manager, 
									   self._on_loading_complete)
			welcome_scene = WelcomeScene(self.screen, self.config, self.game_state, self.save_manager)
			main_menu_scene = MainMenuScene(self.screen, self.config, self.game_state, self.save_manager)
			game_scene = GameScene(self.screen, self.config, self.game_state, self.save_manager)
			pause_scene = PauseScene(self.screen, self.config, self.game_state, self.save_manager)
			character_select_scene = CharacterSelectScene(self.screen, self.config, self.game_state, self.save_manager)
			
			# Añadir escenas al gestor
			self.scene_manager.add_scene('loading', loading_scene)
			self.scene_manager.add_scene('welcome', welcome_scene)
			self.scene_manager.add_scene('main_menu', main_menu_scene)
			self.scene_manager.add_scene('game', game_scene)
			self.scene_manager.add_scene('pause', pause_scene)
			self.scene_manager.add_scene('character_select', character_select_scene)
			
			# Configurar callbacks para transiciones entre escenas
			self._setup_scene_transitions()
			
			# Establecer escena de carga como inicial
			self.scene_manager.change_scene('loading')
			
			self.logger.info("Escenas configuradas correctamente")
			
		except Exception as e:
			self.logger.error(f"Error al configurar escenas: {e}")
			raise
	
	def _setup_scene_transitions(self):
		"""Configura las transiciones entre escenas."""
		# Callbacks para la escena de bienvenida
		welcome_scene = self.scene_manager.scenes['welcome']
		welcome_scene.menu_manager.add_callback('main', lambda: self.scene_manager.change_scene('main_menu'))
		
		# Callbacks para la escena del menú principal
		main_menu_scene = self.scene_manager.scenes['main_menu']
		main_menu_scene.menu_manager.add_callback('new_game', lambda: self.scene_manager.change_scene('character_select'))
		main_menu_scene.menu_manager.add_callback('continue_game', lambda: self.scene_manager.change_scene('game'))
		main_menu_scene.menu_manager.add_callback('back_to_previous', lambda: self.scene_manager.change_scene('welcome'))
		
		# Callbacks para la escena del juego
		game_scene = self.scene_manager.scenes['game']
		# Conectar scene_manager al game_scene para permitir pausa
		game_scene.scene_manager = self.scene_manager
		
		# Callbacks para la escena de pausa
		pause_scene = self.scene_manager.scenes['pause']
		pause_scene.menu_manager.add_callback('resume_game', lambda: self.scene_manager.change_scene('game'))
		pause_scene.menu_manager.add_callback('main_menu', lambda: self.scene_manager.change_scene('main_menu'))
		
		# Callbacks para la escena de selección de personaje
		character_select_scene = self.scene_manager.scenes['character_select']
		character_select_scene.scene_manager = self.scene_manager
		
		self.logger.info("Transiciones entre escenas configuradas")
	
	def _on_loading_complete(self):
		"""Callback cuando termina la carga."""
		self.logger.info("Carga completada, cambiando a escena de bienvenida")
		self.scene_manager.change_scene('welcome')
	
	def run(self):
		"""Ejecuta el bucle principal del juego."""
		self.running = True
		self.logger.info("Iniciando bucle principal del juego...")
		
		try:
			while self.running:
				self._handle_events()
				self._update()
				self._render()
				self.clock.tick(self.config.get('display', 'fps', 60))
				
		except Exception as e:
			self.logger.error(f"Error en el bucle principal: {e}")
			raise
		finally:
			self._cleanup()
	
	def _handle_events(self):
		"""Procesa todos los eventos de Pygame."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			else:
				self.scene_manager.handle_event(event)
	
	def _update(self):
		"""Actualiza la lógica del juego."""
		self.scene_manager.update()
	
	def _render(self):
		"""Renderiza el juego en pantalla."""
		self.scene_manager.render()
		pygame.display.flip()
	
	def _cleanup(self):
		"""Limpia recursos y cierra Pygame."""
		self.logger.info("Limpiando recursos del juego...")
		pygame.quit()
		self.logger.info("Juego cerrado correctamente") 