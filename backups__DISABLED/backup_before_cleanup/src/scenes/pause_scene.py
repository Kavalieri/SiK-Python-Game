"""
Pause Scene - Escena de Pausa
============================

Autor: SiK Team
Fecha: 2024
Descripción: Escena de pausa del juego.
"""

import pygame
import logging
from typing import Optional

from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..ui.menu_manager import MenuManager


class PauseScene(Scene):
	"""
	Escena de pausa del juego.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager):
		"""
		Inicializa la escena de pausa.
		
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
		self.menu_manager.show_menu('pause')
		
		# Configurar callbacks
		self.menu_manager.add_callback('resume_game', self._on_resume_game)
		self.menu_manager.add_callback('save_game', self._on_save_game)
		self.menu_manager.add_callback('main_menu', self._on_main_menu)
		self.menu_manager.add_callback('exit', self._on_exit)
		
		self.logger.info("Escena de pausa inicializada")
	
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			# Reanudar juego con ESC
			self._on_resume_game()
		else:
			self.menu_manager.update([event])
	
	def update(self):
		"""Actualiza la lógica de la escena."""
		pass
	
	def render(self):
		"""Renderiza la escena."""
		# Fondo semi-transparente
		overlay = pygame.Surface(self.screen.get_size())
		overlay.set_alpha(128)
		overlay.fill((0, 0, 0))
		self.screen.blit(overlay, (0, 0))
		
		# Renderizar menú
		self.menu_manager.render()
	
	def _on_resume_game(self):
		"""Callback para reanudar juego."""
		self.logger.info("Reanudando juego")
		# Aquí se volvería a la escena del juego
		self.menu_manager.hide_current_menu()
	
	def _on_save_game(self):
		"""Callback para guardar juego."""
		self.logger.info("Guardando juego")
		# Aquí se guardaría la partida actual
		# Por ahora solo mostramos un mensaje
		self.menu_manager.hide_current_menu()
	
	def _on_main_menu(self):
		"""Callback para volver al menú principal."""
		self.logger.info("Volviendo al menú principal")
		# Aquí se cambiaría a la escena del menú principal
		self.menu_manager.hide_current_menu()
	
	def _on_exit(self):
		"""Callback para salir."""
		self.logger.info("Saliendo del juego")
		# Aquí se cerraría el juego
		pygame.quit()
		import sys
		sys.exit() 