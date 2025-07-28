"""
Character Select Scene - Selección de Personaje
==============================================

Autor: SiK Team
Fecha: 2024
Descripción: Escena de selección de personaje jugable.
"""

import pygame
import logging
from typing import Optional
from ..core.scene_manager import Scene
from ..utils.config_manager import ConfigManager
from ..entities.character_data import CHARACTER_DATA

class CharacterSelectScene(Scene):
	"""
	Escena de selección de personaje jugable.
	"""
	
	def __init__(self, screen: pygame.Surface, config: ConfigManager, game_state, save_manager):
		super().__init__(screen, config)
		self.game_state = game_state
		self.save_manager = save_manager
		self.logger = logging.getLogger(__name__)
		self.character_keys = list(CHARACTER_DATA.keys())
		self.current_character_index = 0
		self.selected_key = self.character_keys[0]
		
		# Inicializar asset manager
		from ..utils.asset_manager import AssetManager
		self.asset_manager = AssetManager()
		
		# Configuración de la interfaz
		self.screen_width = screen.get_width()
		self.screen_height = screen.get_height()
		
		# Colores
		self.colors = {
			'background': (20, 20, 40),
			'panel': (40, 40, 60),
			'panel_border': (80, 80, 100),
			'text': (255, 255, 255),
			'text_highlight': (255, 255, 0),
			'text_secondary': (200, 200, 200),
			'button': (60, 60, 80),
			'button_hover': (80, 80, 100),
			'button_selected': (100, 150, 100),
			'button_text': (255, 255, 255)
		}
		
		# Fuentes
		self.fonts = {
			'title': pygame.font.Font(None, 48),
			'subtitle': pygame.font.Font(None, 32),
			'normal': pygame.font.Font(None, 24),
			'small': pygame.font.Font(None, 18),
			'stats': pygame.font.Font(None, 20)
		}
		
		# Botones
		self.buttons = {}
		self._create_buttons()
		
		# Estado del mouse
		self.mouse_pos = (0, 0)
		self.mouse_clicked = False
		
		self.logger.info("Escena de selección de personaje inicializada")
	
	def _create_buttons(self):
		"""Crea los botones de la interfaz."""
		# Botón Volver - Asegurar que esté dentro de la pantalla
		self.buttons['back'] = {
			'rect': pygame.Rect(20, self.screen_height - 60, 100, 40),
			'text': 'Volver',
			'action': 'back'
		}
		
		# Botón Comenzar Juego - Asegurar que esté dentro de la pantalla
		self.buttons['start'] = {
			'rect': pygame.Rect(self.screen_width - 140, self.screen_height - 60, 120, 40),
			'text': 'Comenzar Juego',
			'action': 'start'
		}
		
		# Botones de navegación - Flechas izquierda y derecha
		arrow_size = 60
		arrow_y = self.screen_height // 2 - arrow_size // 2
		
		self.buttons['arrow_left'] = {
			'rect': pygame.Rect(50, arrow_y, arrow_size, arrow_size),
			'text': '←',
			'action': 'previous_character'
		}
		
		self.buttons['arrow_right'] = {
			'rect': pygame.Rect(self.screen_width - 110, arrow_y, arrow_size, arrow_size),
			'text': '→',
			'action': 'next_character'
		}
	
	def handle_event(self, event: pygame.event.Event):
		"""Maneja eventos de la escena."""
		if event.type == pygame.MOUSEMOTION:
			self.mouse_pos = event.pos
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # Clic izquierdo
				self.mouse_clicked = True
				self._handle_click(event.pos)
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT or event.key == pygame.K_a:
				self._previous_character()
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				self._next_character()
			elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
				self._on_start_clicked()
			elif event.key == pygame.K_ESCAPE:
				self._on_back_clicked()
	
	def _handle_click(self, pos):
		"""Maneja los clics del mouse."""
		for button_id, button in self.buttons.items():
			if button['rect'].collidepoint(pos):
				if button['action'] == 'back':
					self._on_back_clicked()
				elif button['action'] == 'start':
					self._on_start_clicked()
				elif button['action'] == 'previous_character':
					self._previous_character()
				elif button['action'] == 'next_character':
					self._next_character()
				break
	
	def update(self):
		"""Actualiza la lógica de la escena."""
		# Resetear estado del mouse
		self.mouse_clicked = False
	
	def render(self):
		"""Renderiza la escena."""
		# Fondo
		self.screen.fill(self.colors['background'])
		
		# Título
		self._render_title()
		
		# Personajes
		self._render_characters()
		
		# Botones
		self._render_buttons()
		
		# Información del personaje seleccionado
		self._render_selected_info()
	
	def _render_title(self):
		"""Renderiza el título de la escena."""
		title_text = self.fonts['title'].render("Selecciona tu Personaje", True, self.colors['text_highlight'])
		title_rect = title_text.get_rect(center=(self.screen_width // 2, 60))
		self.screen.blit(title_text, title_rect)
		
		subtitle_text = self.fonts['subtitle'].render("Elige el héroe que te acompañará en esta aventura", True, self.colors['text_secondary'])
		subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 100))
		self.screen.blit(subtitle_text, subtitle_rect)
	
	def _render_characters(self):
		"""Renderiza la tarjeta del personaje actual."""
		char_key = self.selected_key
		
		# Calcular dimensiones de la tarjeta central
		card_width = 400
		card_height = 500
		x = (self.screen_width - card_width) // 2
		y = 120
		
		# Color de fondo de la tarjeta
		card_color = self.colors['card_selected']
		border_color = self.colors['card_border_selected']
		
		# Dibujar tarjeta
		card_rect = pygame.Rect(x, y, card_width, card_height)
		pygame.draw.rect(self.screen, card_color, card_rect)
		pygame.draw.rect(self.screen, border_color, card_rect, 3)
		
		# Datos del personaje
		char_data = CHARACTER_DATA[char_key]
		
		# Nombre
		name_text = self.fonts['title'].render(char_data['nombre'], True, self.colors['text_highlight'])
		name_rect = name_text.get_rect(center=(x + card_width//2, y + 30))
		self.screen.blit(name_text, name_rect)
		
		# Tipo
		type_text = self.fonts['subtitle'].render(char_data['tipo'], True, self.colors['text_secondary'])
		type_rect = type_text.get_rect(center=(x + card_width//2, y + 60))
		self.screen.blit(type_text, type_rect)
		
		# Imagen del personaje (más grande)
		image_size = 200
		self._render_character_image(char_key, x + (card_width - image_size)//2, y + 90, image_size)
		
		# Estadísticas
		self._render_character_stats(char_data, x + 20, y + 320)
		
		# Habilidades
		self._render_character_skills(char_data, x + 20, y + 420)
		
		# Indicador de selección
		select_text = self.fonts['normal'].render("✓ PERSONAJE SELECCIONADO", True, self.colors['text_highlight'])
		select_rect = select_text.get_rect(center=(x + card_width//2, y + card_height - 20))
		self.screen.blit(select_text, select_rect)
		
		# Mostrar indicador de navegación
		self._render_navigation_indicator()
	
	def _render_navigation_indicator(self):
		"""Renderiza el indicador de navegación entre personajes."""
		# Mostrar información de navegación
		nav_text = f"Personaje {self.current_character_index + 1} de {len(self.character_keys)}"
		nav_surface = self.fonts['small'].render(nav_text, True, self.colors['text_secondary'])
		nav_rect = nav_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 80))
		self.screen.blit(nav_surface, nav_rect)
		
		# Instrucciones de navegación
		instructions = "Usa ← → o A D para navegar • ENTER para seleccionar • ESC para volver"
		inst_surface = self.fonts['small'].render(instructions, True, self.colors['text_secondary'])
		inst_rect = inst_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 60))
		self.screen.blit(inst_surface, inst_rect)
	
	def _render_character_image(self, character_key: str, x: int, y: int, size: int = 120):
		"""Renderiza la imagen del personaje."""
		image = self._get_character_image(character_key)
		if image:
			# Escalar imagen
			scaled_image = pygame.transform.scale(image, (size, size))
			image_rect = scaled_image.get_rect(center=(x + size//2, y + size//2))
			self.screen.blit(scaled_image, image_rect)
		else:
			# Placeholder
			placeholder_rect = pygame.Rect(x, y, size, size)
			pygame.draw.rect(self.screen, (100, 100, 100), placeholder_rect)
			pygame.draw.rect(self.screen, (150, 150, 150), placeholder_rect, 2)
			
			placeholder_text = self.fonts['normal'].render("?", True, self.colors['text'])
			placeholder_text_rect = placeholder_text.get_rect(center=(x + size//2, y + size//2))
			self.screen.blit(placeholder_text, placeholder_text_rect)
	
	def _render_character_stats(self, char_data: dict, x: int, y: int):
		"""Renderiza las estadísticas del personaje."""
		stats = char_data['stats']
		
		# Título de estadísticas
		stats_title = self.fonts['small'].render("ESTADÍSTICAS", True, self.colors['text_highlight'])
		self.screen.blit(stats_title, (x, y))
		
		# Lista de estadísticas
		stats_list = [
			f"❤️ Vida: {stats['vida']}",
			f"⚡ Velocidad: {stats['velocidad']}",
			f"⚔️ Daño: {stats['daño']}",
			f"🛡️ Escudo: {stats['escudo']}",
			f"🎯 Rango: {stats['rango_ataque']}"
		]
		
		for i, stat in enumerate(stats_list):
			stat_text = self.fonts['small'].render(stat, True, self.colors['text'])
			self.screen.blit(stat_text, (x, y + 20 + i * 15))
	
	def _render_character_skills(self, char_data: dict, x: int, y: int):
		"""Renderiza las habilidades del personaje."""
		# Título de habilidades
		skills_title = self.fonts['small'].render("HABILIDADES", True, self.colors['text_highlight'])
		self.screen.blit(skills_title, (x, y))
		
		# Lista de habilidades (máximo 2)
		skills = char_data['habilidades'][:2]
		for i, skill in enumerate(skills):
			skill_text = self.fonts['small'].render(f"• {skill}", True, self.colors['text_secondary'])
			self.screen.blit(skill_text, (x, y + 20 + i * 15))
	
	def _render_buttons(self):
		"""Renderiza los botones de navegación."""
		for button_id, button in self.buttons.items():
			# Determinar color del botón
			if button_id in ['back', 'start']:
				if button['rect'].collidepoint(self.mouse_pos):
					button_color = self.colors['button_hover']
				else:
					button_color = self.colors['button']
				
				# Dibujar botón
				pygame.draw.rect(self.screen, button_color, button['rect'])
				pygame.draw.rect(self.screen, self.colors['panel_border'], button['rect'], 2)
				
				# Texto del botón
				button_text = self.fonts['normal'].render(button['text'], True, self.colors['button_text'])
				button_text_rect = button_text.get_rect(center=button['rect'].center)
				self.screen.blit(button_text, button_text_rect)
			
			elif button_id in ['arrow_left', 'arrow_right']:
				# Botones de flecha
				if button['rect'].collidepoint(self.mouse_pos):
					button_color = self.colors['button_hover']
				else:
					button_color = self.colors['button']
				
				# Dibujar botón de flecha
				pygame.draw.rect(self.screen, button_color, button['rect'])
				pygame.draw.rect(self.screen, self.colors['panel_border'], button['rect'], 2)
				
				# Texto de la flecha (más grande)
				button_text = self.fonts['title'].render(button['text'], True, self.colors['text_highlight'])
				button_text_rect = button_text.get_rect(center=button['rect'].center)
				self.screen.blit(button_text, button_text_rect)
	
	def _render_selected_info(self):
		"""Renderiza información adicional del personaje seleccionado."""
		if self.selected_key in CHARACTER_DATA:
			char_data = CHARACTER_DATA[self.selected_key]
			
			# Panel de información - Posicionar entre las tarjetas y los botones
			info_rect = pygame.Rect(20, self.screen_height - 100, self.screen_width - 40, 40)
			pygame.draw.rect(self.screen, self.colors['panel'], info_rect)
			pygame.draw.rect(self.screen, self.colors['panel_border'], info_rect, 2)
			
			# Descripción
			desc_text = char_data['descripcion']
			# Truncar descripción si es muy larga para el ancho disponible
			max_chars = (self.screen_width - 80) // 8  # Aproximadamente 8 píxeles por carácter
			if len(desc_text) > max_chars:
				desc_text = desc_text[:max_chars-3] + "..."
			
			desc_surface = self.fonts['small'].render(desc_text, True, self.colors['text'])
			desc_rect = desc_surface.get_rect(midleft=(info_rect.x + 10, info_rect.centery))
			self.screen.blit(desc_surface, desc_rect)
	
	def _get_character_image(self, character_key: str) -> Optional[pygame.Surface]:
		"""Obtiene la imagen de un personaje."""
		try:
			# Intentar obtener sprite de idle
			image = self.asset_manager.get_character_sprite(character_key, "idle", 1)
			if image:
				return image
			
			# Si no hay sprite específico, intentar con get_image
			image = self.asset_manager.get_image(character_key)
			if image:
				return image
			
			# Crear placeholder
			return self._create_character_placeholder(character_key)
			
		except Exception as e:
			self.logger.warning(f"No se pudo cargar imagen para {character_key}: {e}")
			return self._create_character_placeholder(character_key)
	
	def _create_character_placeholder(self, character_key: str) -> pygame.Surface:
		"""Crea un placeholder para un personaje."""
		surface = pygame.Surface((120, 120))
		
		# Color basado en el personaje
		character_colors = {
			"guerrero": (139, 69, 19),    # Marrón
			"robot": (128, 128, 128),     # Gris
			"adventureguirl": (255, 182, 193),  # Rosa claro
		}
		
		color = character_colors.get(character_key.lower(), (255, 0, 0))
		surface.fill(color)
		
		# Añadir borde
		pygame.draw.rect(surface, (255, 255, 255), (0, 0, 120, 120), 3)
		
		# Añadir símbolo según el personaje
		symbols = {
			"guerrero": "⚔️",
			"robot": "🤖",
			"adventureguirl": "👧",
		}
		
		symbol = symbols.get(character_key.lower(), "?")
		try:
			font = pygame.font.Font(None, 60)
			text = font.render(symbol, True, (255, 255, 255))
			text_rect = text.get_rect(center=(60, 60))
			surface.blit(text, text_rect)
		except:
			pass
		
		return surface
	
	def _previous_character(self):
		"""Navega al personaje anterior."""
		self.current_character_index = (self.current_character_index - 1) % len(self.character_keys)
		self.selected_key = self.character_keys[self.current_character_index]
		self.game_state.selected_character = self.selected_key
		self.logger.info(f"Personaje anterior seleccionado: {self.selected_key}")
	
	def _next_character(self):
		"""Navega al siguiente personaje."""
		self.current_character_index = (self.current_character_index + 1) % len(self.character_keys)
		self.selected_key = self.character_keys[self.current_character_index]
		self.game_state.selected_character = self.selected_key
		self.logger.info(f"Siguiente personaje seleccionado: {self.selected_key}")
	
	def _on_character_selected(self, character_key: str):
		"""Maneja la selección de un personaje."""
		self.selected_key = character_key
		self.game_state.selected_character = character_key
		self.logger.info(f"Personaje seleccionado: {character_key}")
	
	def _on_back_clicked(self):
		"""Maneja el clic en el botón volver."""
		if hasattr(self, 'scene_manager') and self.scene_manager:
			self.scene_manager.change_scene('main_menu')
		else:
			self.logger.warning("Scene manager no disponible para volver")
	
	def _on_start_clicked(self):
		"""Maneja el clic en el botón comenzar juego."""
		if hasattr(self, 'scene_manager') and self.scene_manager:
			self.scene_manager.change_scene('game')
		else:
			self.logger.warning("Scene manager no disponible para comenzar juego") 