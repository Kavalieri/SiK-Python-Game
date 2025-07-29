"""
Main Menu Scene - Escena del Menú Principal
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Escena del menú principal del juego.
"""

import pygame
import logging
from typing import Optional

from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..ui.menu_manager import MenuManager


class MainMenuScene(Scene):
	"""
	Escena del menú principal del juego.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager):
		"""
		Inicializa la escena del menú principal.
		
		Args:
			screen: Superficie de Pygame donde renderizar
			config: Configuración del juego
			game_state: Estado del juego
			save_manager: Gestor de guardado
		"""
		super().__init__(screen, config)
		self.game_state = game_state
		self.save_manager = save_manager
		self.logger = logging.getLogger(__name__)
		
		# Inicializar menú
		self.menu_manager = MenuManager(screen, config, game_state, save_manager)
		self.menu_manager.show_menu('main')
		
		# Configurar callbacks
		self.menu_manager.add_callback('new_game', self._on_new_game)
		self.menu_manager.add_callback('continue_game', self._on_continue_game)
		self.menu_manager.add_callback('load_game', self._on_load_game)
		self.menu_manager.add_callback('options', self._on_options)
		self.menu_manager.add_callback('exit', self._on_exit)
		
		self.logger.info("Escena del menú principal inicializada")
	
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
		self.logger.debug(f"[MainMenuScene] Evento recibido: {event.type} - {event}")
		# Procesar eventos de menú aquí
		if event.type == pygame.KEYDOWN:
			self.logger.info(f"[MainMenuScene] Tecla pulsada: {event.key}")
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.logger.info(f"[MainMenuScene] Click ratón: {event.button} en {event.pos}")
		self.menu_manager.update([event])
	
	def update(self):
		"""Actualiza la lógica de la escena."""
		pass
	
	def render(self):
		"""Renderiza la escena."""
		# Fondo negro
		self.screen.fill((0, 0, 0))
		
		# Renderizar menú
		self.menu_manager.render()
	
	def _on_new_game(self):
		"""Callback para nuevo juego."""
		self.logger.info("[MainMenuScene] Acción: Nuevo Juego - mostrando menú de guardado para nueva partida")
		self.menu_manager.show_menu('save')
	
	def _on_continue_game(self):
		"""Callback para continuar juego."""
		self.logger.info("[MainMenuScene] Acción: Continuar Juego - mostrando menú de guardado para continuar")
		self.menu_manager.show_menu('save')
	
	def _on_load_game(self):
		"""Callback para cargar partida."""
		self.logger.warning("[MainMenuScene] Acción: Cargar Juego - NO IMPLEMENTADO")
		# El menú sigue operativo
	
	def _on_options(self):
		"""Callback para opciones."""
		self.logger.warning("[MainMenuScene] Acción: Opciones - NO IMPLEMENTADO")
		# El menú sigue operativo
	
	def _on_exit(self):
		"""Callback para salir."""
		self.logger.info("[MainMenuScene] Acción: Salir - cerrando juego")
		self.menu_manager.hide_current_menu()
		import pygame, sys
		pygame.quit()
		sys.exit() 