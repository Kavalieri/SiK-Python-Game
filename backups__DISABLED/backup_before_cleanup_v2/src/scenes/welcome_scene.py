"""
Welcome Scene - Escena de Bienvenida
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Escena de bienvenida del juego.
"""

import pygame
import logging
from typing import Optional

from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..ui.menu_manager import MenuManager


class WelcomeScene(Scene):
	"""
	Escena de bienvenida del juego.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager):
		"""
		Inicializa la escena de bienvenida.
		
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
		self.menu_manager.show_menu('welcome')
		
		# Configurar callbacks
		self.menu_manager.add_callback('main', self._on_main_menu)
		
		self.logger.info("Escena de bienvenida inicializada")
	
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
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
	
	def _on_main_menu(self):
		"""Callback para ir al menú principal."""
		self.logger.info("Transición al menú principal")
		# Aquí se cambiaría a la escena del menú principal
		# Por ahora solo ocultamos el menú
		self.menu_manager.hide_current_menu() 