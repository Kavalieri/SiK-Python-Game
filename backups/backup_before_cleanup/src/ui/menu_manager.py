"""
Menu Manager - Gestor de Menús
=============================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona todos los menús del juego usando pygame-menu.
"""

import pygame
import pygame_menu
import logging
from typing import Dict, Any, Optional, Callable
from pathlib import Path

from ..utils.config_manager import ConfigManager
from ..core.game_state import GameState
from ..utils.save_manager import SaveManager


class MenuManager:
	"""
	Gestiona todos los menús del juego.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager, game_state: GameState, save_manager: SaveManager):
		"""
		Inicializa el gestor de menús.
		
		Args:
			screen: Superficie de Pygame donde renderizar
			config: Configuración del juego
			game_state: Estado del juego
			save_manager: Gestor de guardado
		"""
		self.screen = screen
		self.config = config
		self.game_state = game_state
		self.save_manager = save_manager
		self.logger = logging.getLogger(__name__)
		
		# Configuración de menús
		self.screen_width = screen.get_width()
		self.screen_height = screen.get_height()
		self.theme = self._create_theme()
		
		# Menús disponibles
		self.menus: Dict[str, pygame_menu.Menu] = {}
		self.current_menu: Optional[pygame_menu.Menu] = None
		self.menu_callbacks: Dict[str, Callable] = {}
		
		self._initialize_menus()
		
		self.logger.info("Gestor de menús inicializado")
	
	def _create_theme(self) -> pygame_menu.themes.Theme:
		"""Crea el tema visual para los menús."""
		# Usar tema por defecto para evitar problemas de compatibilidad
		theme = pygame_menu.themes.THEME_DEFAULT.copy()
		theme.background_color = (0, 0, 0, 180)
		theme.title_font_color = (255, 255, 255)
		theme.widget_font_color = (255, 255, 255)
		theme.selection_color = (255, 165, 0)
		
		return theme
	
	def _initialize_menus(self):
		"""Inicializa todos los menús del juego."""
		self._create_welcome_menu()
		self._create_main_menu()
		self._create_pause_menu()
		self._create_upgrade_menu()
		self._create_character_select_menu()
		self._create_options_menu()
		self._create_inventory_menu()
		self._create_save_menu()
		
		self.logger.debug(f"Menús inicializados: {len(self.menus)} menús")
	
	def _create_welcome_menu(self):
		"""Crea el menú de bienvenida."""
		menu = pygame_menu.Menu(
			title="SiK Python Game",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Título del juego
		menu.add.label("¡Bienvenido al juego!", font_size=30)
		menu.add.vertical_margin(50)
		
		# Botón para empezar
		menu.add.button("Pulsa para empezar", self._on_welcome_start, font_size=25)
		menu.add.vertical_margin(20)
		
		# Información adicional
		menu.add.label("Desarrollado por SiK Team", font_size=15)
		menu.add.label("Versión 0.1.0", font_size=15)
		
		self.menus['welcome'] = menu
	
	def _create_main_menu(self):
		"""Crea el menú principal."""
		menu = pygame_menu.Menu(
			title="Menú Principal",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Botones principales
		menu.add.button("Nuevo Juego", self._on_new_game, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Continuar", self._on_continue_game, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Cargar Partida", self._on_load_game, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Opciones", self._on_options, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Salir", self._on_exit, font_size=25)
		
		self.menus['main'] = menu
	
	def _create_pause_menu(self):
		"""Crea el menú de pausa."""
		menu = pygame_menu.Menu(
			title="Juego Pausado",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Botones de pausa
		menu.add.button("Reanudar", self._on_resume_game, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Opciones", self._on_options, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Guardar", self._on_save_game, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Menú Principal", self._on_main_menu, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Salir", self._on_exit, font_size=25)
		
		self.menus['pause'] = menu
	
	def _create_upgrade_menu(self):
		"""Crea el menú de mejoras."""
		menu = pygame_menu.Menu(
			title="Menú de Mejoras",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Información del jugador
		menu.add.label("Puntos de Mejora Disponibles:", font_size=20)
		upgrade_points_label = menu.add.label("0", font_size=25, font_color=(255, 255, 0))
		menu.add.vertical_margin(20)
		
		# Mejoras disponibles
		menu.add.button("Mejorar Velocidad (10 pts)", self._on_upgrade_speed, font_size=20)
		menu.add.vertical_margin(5)
		
		menu.add.button("Mejorar Daño (15 pts)", self._on_upgrade_damage, font_size=20)
		menu.add.vertical_margin(5)
		
		menu.add.button("Mejorar Vida (20 pts)", self._on_upgrade_health, font_size=20)
		menu.add.vertical_margin(5)
		
		menu.add.button("Mejorar Escudo (25 pts)", self._on_upgrade_shield, font_size=20)
		menu.add.vertical_margin(20)
		
		# Botones de navegación
		menu.add.button("Continuar Juego", self._on_continue_after_upgrade, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Menú Principal", self._on_main_menu, font_size=25)
		
		# Guardar referencia al label de puntos
		menu.upgrade_points_label = upgrade_points_label
		self.menus['upgrade'] = menu
	
	def _create_character_select_menu(self):
		"""Crea el menú de selección de personaje."""
		menu = pygame_menu.Menu(
			title="Selección de Personaje",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Información
		menu.add.label("Elige tu personaje:", font_size=25)
		menu.add.vertical_margin(20)
		
		# Personajes disponibles
		menu.add.button("Guerrero - Equilibrado", lambda: self._on_select_character("guerrero"), font_size=20)
		menu.add.vertical_margin(10)
		
		menu.add.button("Arquero - Rápido", lambda: self._on_select_character("arquero"), font_size=20)
		menu.add.vertical_margin(10)
		
		menu.add.button("Mago - Poderoso", lambda: self._on_select_character("mago"), font_size=20)
		menu.add.vertical_margin(20)
		
		# Botón de volver
		menu.add.button("Volver", self._on_back_to_main, font_size=25)
		
		self.menus['character_select'] = menu
	
	def _create_options_menu(self):
		"""Crea el menú de opciones."""
		menu = pygame_menu.Menu(
			title="Opciones",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Configuración de gráficos
		menu.add.label("Gráficos:", font_size=25)
		resolution_selector = menu.add.selector(
			"Resolución: ",
			[("1280x720", "1280x720"), ("1920x1080", "1920x1080"), ("2560x1440", "2560x1440")],
			default=0,
			onchange=self._on_resolution_change
		)
		menu.add.vertical_margin(10)
		
		fullscreen_toggle = menu.add.toggle_switch(
			"Pantalla Completa: ",
			default=False,
			onchange=self._on_fullscreen_change
		)
		menu.add.vertical_margin(20)
		
		# Configuración de audio
		menu.add.label("Audio:", font_size=25)
		music_volume = menu.add.range_slider(
			"Volumen Música: ",
			default=70,
			range_values=(0, 100),
			increment=5,
			onchange=self._on_music_volume_change
		)
		menu.add.vertical_margin(10)
		
		sfx_volume = menu.add.range_slider(
			"Volumen Efectos: ",
			default=80,
			range_values=(0, 100),
			increment=5,
			onchange=self._on_sfx_volume_change
		)
		menu.add.vertical_margin(20)
		
		# Configuración de controles
		menu.add.label("Controles:", font_size=25)
		menu.add.button("Configurar Controles", self._on_configure_controls, font_size=20)
		menu.add.vertical_margin(20)
		
		# Botones
		menu.add.button("Guardar", self._on_save_options, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Volver", self._on_back_to_previous, font_size=25)
		
		# Guardar referencias
		menu.resolution_selector = resolution_selector
		menu.fullscreen_toggle = fullscreen_toggle
		menu.music_volume = music_volume
		menu.sfx_volume = sfx_volume
		
		self.menus['options'] = menu
	
	def _create_inventory_menu(self):
		"""Crea el menú de inventario."""
		menu = pygame_menu.Menu(
			title="Inventario",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Información del inventario
		menu.add.label("Equipación Actual:", font_size=25)
		menu.add.vertical_margin(10)
		
		# Slots de equipación
		menu.add.button("Arma Principal: Ninguna", self._on_equip_weapon, font_size=20)
		menu.add.vertical_margin(5)
		
		menu.add.button("Armadura: Ninguna", self._on_equip_armor, font_size=20)
		menu.add.vertical_margin(5)
		
		menu.add.button("Accesorio: Ninguno", self._on_equip_accessory, font_size=20)
		menu.add.vertical_margin(20)
		
		# Inventario de items
		menu.add.label("Items en Inventario:", font_size=25)
		menu.add.vertical_margin(10)
		
		# Lista de items (placeholder)
		menu.add.label("No hay items en el inventario", font_size=20, font_color=(128, 128, 128))
		menu.add.vertical_margin(20)
		
		# Botón de volver
		menu.add.button("Volver", self._on_back_to_previous, font_size=25)
		
		self.menus['inventory'] = menu
	
	def _create_save_menu(self):
		"""Crea el menú de gestión de guardados."""
		menu = pygame_menu.Menu(
			title="Gestión de Guardados",
			width=self.screen_width,
			height=self.screen_height,
			theme=self.theme,
			enabled=False
		)
		
		# Información de archivos de guardado
		menu.add.label("Archivos de Guardado:", font_size=25)
		menu.add.vertical_margin(10)
		
		# Crear botones para cada archivo de guardado
		for i in range(3):
			save_info = self.save_manager.get_save_files_info()[i]
			if save_info['exists']:
				text = f"Archivo {i+1}: {save_info['player_name']} - Nivel {save_info['level']}"
			else:
				text = f"Archivo {i+1}: Vacío"
			
			menu.add.button(text, lambda x=i+1: self._on_select_save_file(x), font_size=20)
			menu.add.vertical_margin(5)
		
		menu.add.vertical_margin(20)
		
		# Botones de gestión
		menu.add.button("Nuevo Guardado", self._on_new_save, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Eliminar Guardado", self._on_delete_save, font_size=25)
		menu.add.vertical_margin(10)
		
		menu.add.button("Volver", self._on_back_to_previous, font_size=25)
		
		self.menus['save'] = menu
	
	# Callbacks de menús
	def _on_welcome_start(self):
		"""Callback para el botón de empezar en la pantalla de bienvenida."""
		self.logger.info("Iniciando juego desde pantalla de bienvenida")
		self.hide_current_menu()
		if 'main' in self.menu_callbacks:
			self.menu_callbacks['main']()
	
	def _on_new_game(self):
		"""Callback para nuevo juego."""
		self.logger.info("Nuevo juego seleccionado")
		self.hide_current_menu()
		if 'new_game' in self.menu_callbacks:
			self.menu_callbacks['new_game']()
	
	def _on_continue_game(self):
		"""Callback para continuar juego."""
		self.logger.info("Continuar juego seleccionado")
		self.hide_current_menu()
		if 'continue_game' in self.menu_callbacks:
			self.menu_callbacks['continue_game']()
	
	def _on_load_game(self):
		"""Callback para cargar partida."""
		self.logger.info("Cargar partida seleccionado")
		self.show_menu('save')
	
	def _on_options(self):
		"""Callback para opciones."""
		self.logger.info("Opciones seleccionado")
		self.show_menu('options')
	
	def _on_exit(self):
		"""Callback para salir."""
		self.logger.info("Salir seleccionado")
		if 'exit' in self.menu_callbacks:
			self.menu_callbacks['exit']()
	
	def _on_resume_game(self):
		"""Callback para reanudar juego."""
		self.logger.info("Reanudar juego seleccionado")
		self.hide_current_menu()
		if 'resume_game' in self.menu_callbacks:
			self.menu_callbacks['resume_game']()
	
	def _on_save_game(self):
		"""Callback para guardar juego."""
		self.logger.info("Guardar juego seleccionado")
		if 'save_game' in self.menu_callbacks:
			self.menu_callbacks['save_game']()
	
	def _on_main_menu(self):
		"""Callback para volver al menú principal."""
		self.logger.info("Volver al menú principal seleccionado")
		self.show_menu('main')
	
	def _on_upgrade_speed(self):
		"""Callback para mejorar velocidad."""
		self.logger.info("Mejorar velocidad seleccionado")
		if 'upgrade_speed' in self.menu_callbacks:
			self.menu_callbacks['upgrade_speed']()
	
	def _on_upgrade_damage(self):
		"""Callback para mejorar daño."""
		self.logger.info("Mejorar daño seleccionado")
		if 'upgrade_damage' in self.menu_callbacks:
			self.menu_callbacks['upgrade_damage']()
	
	def _on_upgrade_health(self):
		"""Callback para mejorar vida."""
		self.logger.info("Mejorar vida seleccionado")
		if 'upgrade_health' in self.menu_callbacks:
			self.menu_callbacks['upgrade_health']()
	
	def _on_upgrade_shield(self):
		"""Callback para mejorar escudo."""
		self.logger.info("Mejorar escudo seleccionado")
		if 'upgrade_shield' in self.menu_callbacks:
			self.menu_callbacks['upgrade_shield']()
	
	def _on_continue_after_upgrade(self):
		"""Callback para continuar después de mejoras."""
		self.logger.info("Continuar después de mejoras seleccionado")
		self.hide_current_menu()
		if 'continue_after_upgrade' in self.menu_callbacks:
			self.menu_callbacks['continue_after_upgrade']()
	
	def _on_select_character(self, character: str):
		"""Callback para seleccionar personaje."""
		self.logger.info(f"Personaje seleccionado: {character}")
		if 'select_character' in self.menu_callbacks:
			self.menu_callbacks['select_character'](character)
	
	def _on_back_to_main(self):
		"""Callback para volver al menú principal."""
		self.show_menu('main')
	
	def _on_back_to_previous(self):
		"""Callback para volver al menú anterior."""
		self.hide_current_menu()
		if 'back_to_previous' in self.menu_callbacks:
			self.menu_callbacks['back_to_previous']()
	
	def _on_resolution_change(self, value, resolution):
		"""Callback para cambiar resolución."""
		self.logger.info(f"Resolución cambiada a: {resolution}")
		if 'resolution_change' in self.menu_callbacks:
			self.menu_callbacks['resolution_change'](resolution)
	
	def _on_fullscreen_change(self, value):
		"""Callback para cambiar pantalla completa."""
		self.logger.info(f"Pantalla completa: {value}")
		if 'fullscreen_change' in self.menu_callbacks:
			self.menu_callbacks['fullscreen_change'](value)
	
	def _on_music_volume_change(self, value):
		"""Callback para cambiar volumen de música."""
		self.logger.info(f"Volumen de música: {value}")
		if 'music_volume_change' in self.menu_callbacks:
			self.menu_callbacks['music_volume_change'](value)
	
	def _on_sfx_volume_change(self, value):
		"""Callback para cambiar volumen de efectos."""
		self.logger.info(f"Volumen de efectos: {value}")
		if 'sfx_volume_change' in self.menu_callbacks:
			self.menu_callbacks['sfx_volume_change'](value)
	
	def _on_configure_controls(self):
		"""Callback para configurar controles."""
		self.logger.info("Configurar controles seleccionado")
		if 'configure_controls' in self.menu_callbacks:
			self.menu_callbacks['configure_controls']()
	
	def _on_save_options(self):
		"""Callback para guardar opciones."""
		self.logger.info("Guardar opciones seleccionado")
		if 'save_options' in self.menu_callbacks:
			self.menu_callbacks['save_options']()
	
	def _on_equip_weapon(self):
		"""Callback para equipar arma."""
		self.logger.info("Equipar arma seleccionado")
		if 'equip_weapon' in self.menu_callbacks:
			self.menu_callbacks['equip_weapon']()
	
	def _on_equip_armor(self):
		"""Callback para equipar armadura."""
		self.logger.info("Equipar armadura seleccionado")
		if 'equip_armor' in self.menu_callbacks:
			self.menu_callbacks['equip_armor']()
	
	def _on_equip_accessory(self):
		"""Callback para equipar accesorio."""
		self.logger.info("Equipar accesorio seleccionado")
		if 'equip_accessory' in self.menu_callbacks:
			self.menu_callbacks['equip_accessory']()
	
	def _on_select_save_file(self, file_number: int):
		"""Callback para seleccionar archivo de guardado."""
		self.logger.info(f"Archivo de guardado seleccionado: {file_number}")
		if 'select_save_file' in self.menu_callbacks:
			self.menu_callbacks['select_save_file'](file_number)
	
	def _on_new_save(self):
		"""Callback para nuevo guardado."""
		self.logger.info("Nuevo guardado seleccionado")
		if 'new_save' in self.menu_callbacks:
			self.menu_callbacks['new_save']()
	
	def _on_delete_save(self):
		"""Callback para eliminar guardado."""
		self.logger.info("Eliminar guardado seleccionado")
		if 'delete_save' in self.menu_callbacks:
			self.menu_callbacks['delete_save']()
	
	# Métodos públicos
	def show_menu(self, menu_name: str):
		"""
		Muestra un menú específico.
		
		Args:
			menu_name: Nombre del menú a mostrar
		"""
		if menu_name in self.menus:
			self.current_menu = self.menus[menu_name]
			self.current_menu.enable()
			self.logger.debug(f"Menú mostrado: {menu_name}")
		else:
			self.logger.error(f"Menú no encontrado: {menu_name}")
	
	def hide_current_menu(self):
		"""Oculta el menú actual."""
		if self.current_menu:
			self.current_menu.disable()
			self.current_menu = None
			self.logger.debug("Menú actual oculto")
	
	def update(self, events: list):
		"""
		Actualiza el menú actual.
		
		Args:
			events: Lista de eventos de Pygame
		"""
		if self.current_menu and self.current_menu.is_enabled():
			self.current_menu.update(events)
	
	def render(self):
		"""Renderiza el menú actual."""
		if self.current_menu and self.current_menu.is_enabled():
			self.current_menu.draw(self.screen)
	
	def add_callback(self, callback_name: str, callback: Callable):
		"""
		Añade un callback para un evento específico.
		
		Args:
			callback_name: Nombre del callback
			callback: Función callback
		"""
		self.menu_callbacks[callback_name] = callback
		self.logger.debug(f"Callback añadido: {callback_name}")
	
	def update_save_menu(self):
		"""Actualiza la información del menú de guardados."""
		if 'save' in self.menus:
			# Recrear el menú de guardados con información actualizada
			self._create_save_menu()
	
	def update_upgrade_menu(self, upgrade_points: int):
		"""
		Actualiza el menú de mejoras con los puntos disponibles.
		
		Args:
			upgrade_points: Puntos de mejora disponibles
		"""
		if 'upgrade' in self.menus and hasattr(self.menus['upgrade'], 'upgrade_points_label'):
			self.menus['upgrade'].upgrade_points_label.set_title(str(upgrade_points)) 