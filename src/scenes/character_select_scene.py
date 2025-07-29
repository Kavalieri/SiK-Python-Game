"""
Character Select Scene - Selección de Personaje (Refactorizada V2)
===============================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Escena de selección de personaje jugable completamente modularizada.
"""

import pygame
import logging
from typing import Optional
from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from .character_data import CharacterData
from .character_animations import CharacterAnimations
from .character_ui import CharacterUI
from ..utils.logger import get_logger


class CharacterSelectScene(Scene):
	"""
	Escena de selección de personaje jugable (Refactorizada V2).
	"""
	
	def __init__(self, screen, config, game_state, save_manager):
		"""Inicializa la escena de selección de personajes."""
		super().__init__(screen, config)
		
		# Guardar referencias adicionales
		self.game_state = game_state
		self.save_manager = save_manager
		
		# Configuración de la pantalla
		self.screen_width = screen.get_width()
		self.screen_height = screen.get_height()
		
		# Inicializar módulos especializados
		self.character_data = CharacterData()
		self.character_animations = CharacterAnimations()
		self.character_ui = CharacterUI(self.screen_width, self.screen_height, config)
		
		# Lista de personajes disponibles
		self.character_keys = CharacterData.get_all_characters()
		self.current_character_index = 0
		self.selected_key = self.character_keys[0] if self.character_keys else None
		
		# Posición del mouse
		self.mouse_pos = (0, 0)
		
		# Logger
		self.logger = get_logger('SiK_Game')
		self.logger.info('[CharacterSelectScene] Escena de selección de personaje inicializada')
	
	def update(self):
		"""Actualiza la escena."""
		# Actualizar animaciones
		self.character_animations.update(0.016)  # Aproximadamente 60 FPS
		
		# Actualizar posición del mouse
		self.mouse_pos = pygame.mouse.get_pos()
	
	def render(self):
		"""Renderiza la escena."""
		# Fondo
		self.screen.fill((20, 20, 40))  # Color de fondo
		
		# Título
		self.character_ui.render_title(self.screen)
		
		# Renderizar personaje seleccionado
		if self.selected_key:
			self._render_selected_character()
		
		# Botones
		self.character_ui.render_buttons(self.screen, self.mouse_pos)
		
		# Indicador de navegación
		self.character_ui.render_navigation_indicator(
			self.screen, self.current_character_index, len(self.character_keys)
		)
	
	def _render_selected_character(self):
		"""Renderiza el personaje seleccionado."""
		if not self.selected_key:
			return
		
		char_key = self.selected_key
		char_data = CharacterData.get_character_data(char_key)
		if not char_data:
			return
		
		# Calcular dimensiones de la tarjeta central
		card_width = 600
		card_height = 600
		x = (self.screen_width - card_width) // 2
		y = 100
		
		# Dibujar tarjeta
		card_rect = pygame.Rect(x, y, card_width, card_height)
		pygame.draw.rect(self.screen, (40, 40, 80), card_rect)  # Azul oscuro
		pygame.draw.rect(self.screen, (80, 80, 120), card_rect, 3)  # Borde azul claro
		
		# Renderizar imagen del personaje
		image_size = 250
		image_x = x + (card_width - image_size) // 2
		image_y = y + 90
		character_image = self.character_animations.get_character_image(char_key)
		if character_image:
			# Determinar si hay que hacer flip horizontal según el cursor
			mouse_x, _ = self.mouse_pos
			sprite_center_x = image_x + image_size // 2
			flip = mouse_x < sprite_center_x
			if flip:
				character_image = pygame.transform.flip(character_image, True, False)
			scaled_image = pygame.transform.scale(character_image, (image_size, image_size))
			image_rect = scaled_image.get_rect(center=(image_x + image_size//2, image_y + image_size//2))
			self.screen.blit(scaled_image, image_rect)
		
		# Renderizar estadísticas y habilidades
		stats_x = x + 30
		skills_x = x + card_width // 2 + 30
		content_y = y + 360
		
		self.character_ui.render_character_stats(self.screen, char_data, stats_x, content_y)
		self.character_ui.render_character_skills(self.screen, char_data, skills_x, content_y)
	
	def _previous_character(self):
		"""Navega al personaje anterior."""
		if len(self.character_keys) > 1:
			self.current_character_index = (self.current_character_index - 1) % len(self.character_keys)
			self.selected_key = self.character_keys[self.current_character_index]
	
	def _next_character(self):
		"""Navega al personaje siguiente."""
		if len(self.character_keys) > 1:
			self.current_character_index = (self.current_character_index + 1) % len(self.character_keys)
			self.selected_key = self.character_keys[self.current_character_index]
	
	def _on_character_selected(self, character_key: str):
		"""Maneja la selección de un personaje."""
		self.selected_key = character_key
		self.logger.info(f"Personaje seleccionado: {character_key}")
	
	def _on_back_clicked(self):
		"""Maneja el click en el botón Atrás."""
		self.game_state.set_scene("main_menu")
		self.logger.info("Volviendo al menú principal")
	
	def _on_start_clicked(self):
		"""Maneja el click en el botón Iniciar."""
		if self.selected_key:
			# Guardar personaje seleccionado
			self.game_state.selected_character = self.selected_key
			self.game_state.set_scene("game")
			self.logger.info(f"Iniciando juego con personaje: {self.selected_key}")
	
	def handle_event(self, event: pygame.event.Event):
		"""Maneja eventos de la escena."""
		self.logger.info(f'[CharacterSelectScene] Evento recibido: {event.type} - {event}')
		if event.type == pygame.KEYDOWN:
			self.logger.info(f"[CharacterSelectScene] Tecla pulsada: {event.key}")
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				self._previous_character()
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				self._next_character()
			elif event.key == pygame.K_RETURN:
				self._on_start_clicked()
			elif event.key == pygame.K_ESCAPE:
				self._on_back_clicked()
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			self.logger.info(f"[CharacterSelectScene] Click ratón: {event.button} en {event.pos}")
			if event.button == 1:  # Click izquierdo
				self._handle_click(event.pos)
	
	def _handle_click(self, pos):
		"""Maneja clicks del mouse."""
		# Verificar clicks en botones
		clicked_button = self.character_ui.get_clicked_button(pos)
		
		if clicked_button == 'back':
			self._on_back_clicked()
		elif clicked_button == 'start':
			self._on_start_clicked()
		elif clicked_button == 'prev':
			self._previous_character()
		elif clicked_button == 'next':
			self._next_character() 