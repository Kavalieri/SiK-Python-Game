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
	
	def __init__(self, screen, config, game_state, save_manager):
		"""Inicializa la escena de selección de personajes."""
		super().__init__(screen, config)
		
		# Guardar referencias adicionales
		self.game_state = game_state
		self.save_manager = save_manager
		
		# Asset Manager
		from ..utils.asset_manager import AssetManager
		self.asset_manager = AssetManager()
		
		# Configuración de la pantalla
		self.screen_width = screen.get_width()
		self.screen_height = screen.get_height()
		
		# Datos de personajes jugables (solo los 3 principales)
		self.character_data = {
			"guerrero": {
				"nombre": "Kava",
				"tipo": "Melee",
				"descripcion": "Guerrero experto en combate cuerpo a cuerpo con espada y escudo.",
				"stats": {"vida": 200, "velocidad": 180, "daño": 50, "escudo": 20, "rango_ataque": 80},
				"habilidades": ["Ataque de espada", "Escudo protector", "Mayor resistencia", "Combo de ataques"]
			},
			"adventureguirl": {
				"nombre": "Sara", 
				"tipo": "Ranged",
				"descripcion": "Arquera ágil especializada en ataques a distancia con arco y flechas.",
				"stats": {"vida": 120, "velocidad": 220, "daño": 25, "escudo": 5, "rango_ataque": 300},
				"habilidades": ["Flechas mágicas", "Disparo rápido", "Alta movilidad", "Evasión mejorada"]
			},
			"robot": {
				"nombre": "Guiral",
				"tipo": "Tech", 
				"descripcion": "Robot avanzado con armamento tecnológico y proyectiles de energía.",
				"stats": {"vida": 150, "velocidad": 160, "daño": 35, "escudo": 15, "rango_ataque": 250},
				"habilidades": ["Proyectiles de energía", "Misiles explosivos", "Daño en área", "Blindaje mejorado"]
			}
		}
		
		# Lista de personajes disponibles
		self.character_keys = list(self.character_data.keys())
		self.current_character_index = 0
		self.selected_key = self.character_keys[0]
		
		# Animación de sprites
		self.animation_frames = {}
		self.current_frame = 0
		self.frame_timer = 0
		self.frame_delay = 150  # milisegundos entre frames
		
		# Cargar frames de animación para todos los personajes
		self._load_animation_frames()
		
		# Posición del mouse
		self.mouse_pos = (0, 0)
		
		# Fuentes
		self.fonts = {
			'title': pygame.font.Font(None, 48),
			'subtitle': pygame.font.Font(None, 32),
			'normal': pygame.font.Font(None, 24),
			'small': pygame.font.Font(None, 18)
		}
		
		# Colores
		self.colors = {
			'background': (20, 20, 40),
			'panel': (40, 40, 80),
			'panel_border': (80, 80, 120),
			'text': (255, 255, 255),
			'text_secondary': (200, 200, 200),
			'text_highlight': (255, 255, 0),
			'button': (60, 60, 100),
			'button_hover': (80, 80, 120),
			'button_text': (255, 255, 255),
			'card_selected': (100, 100, 150),
			'card_border_selected': (255, 255, 0)
		}
		
		# Inicializar botones
		self._init_buttons()
		
		# Logger
		self.logger = logging.getLogger(__name__)
		
	def _load_animation_frames(self):
		"""Carga los frames de animación para todos los personajes."""
		for char_key in self.character_keys:
			frames = self.asset_manager.get_character_animation_frames(char_key, "Idle")
			self.animation_frames[char_key] = frames
			self.logger.info(f"Cargados {len(frames)} frames de animación para {char_key}")
	
	def update(self):
		"""Actualiza la escena."""
		# Actualizar animación
		current_time = pygame.time.get_ticks()
		if current_time - self.frame_timer > self.frame_delay:
			# Obtener frames del personaje actual
			frames = self.animation_frames.get(self.selected_key, [])
			if frames:
				# Si hay frames, avanzar al siguiente
				self.current_frame = (self.current_frame + 1) % len(frames)
			else:
				# Si no hay frames, mantener en 0
				self.current_frame = 0
			self.frame_timer = current_time
	
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
		title_text = self.fonts['title'].render("Selección de Personaje", True, self.colors['text_highlight'])
		title_rect = title_text.get_rect(center=(self.screen_width // 2, 40))
		self.screen.blit(title_text, title_rect)
		
		subtitle_text = self.fonts['subtitle'].render("Navega con las flechas", True, self.colors['text_secondary'])
		subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 70))
		self.screen.blit(subtitle_text, subtitle_rect)
	
	def _render_characters(self):
		"""Renderiza la tarjeta del personaje actual."""
		char_key = self.selected_key
		
		# Calcular dimensiones de la tarjeta central - Más ancha para aprovechar el espacio
		card_width = 600
		card_height = 600
		x = (self.screen_width - card_width) // 2
		y = 100
		
		# Color de fondo de la tarjeta
		card_color = (40, 40, 80)  # Azul oscuro
		border_color = (80, 80, 120)  # Azul claro
		
		# Dibujar tarjeta
		card_rect = pygame.Rect(x, y, card_width, card_height)
		pygame.draw.rect(self.screen, card_color, card_rect)
		pygame.draw.rect(self.screen, border_color, card_rect, 3)
		
		# Datos del personaje
		char_data = self.character_data[char_key]
		
		# Nombre
		name_text = self.fonts['title'].render(char_data['nombre'], True, self.colors['text_highlight'])
		name_rect = name_text.get_rect(center=(x + card_width//2, y + 30))
		self.screen.blit(name_text, name_rect)
		
		# Tipo
		type_text = self.fonts['subtitle'].render(char_data['tipo'], True, self.colors['text_secondary'])
		type_rect = type_text.get_rect(center=(x + card_width//2, y + 60))
		self.screen.blit(type_text, type_rect)
		
		# Imagen del personaje (más grande y centrada)
		image_size = 250
		image_x = x + (card_width - image_size) // 2
		image_y = y + 90
		self._render_character_image(char_key, image_x, image_y, image_size)
		
		# Contenedor para estadísticas y habilidades (lado a lado)
		stats_x = x + 30
		skills_x = x + card_width // 2 + 30
		content_y = y + 360
		
		# Estadísticas (lado izquierdo)
		self._render_character_stats(char_data, stats_x, content_y)
		
		# Habilidades (lado derecho)
		self._render_character_skills(char_data, skills_x, content_y)
		
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
			# Placeholder mejorado
			placeholder_rect = pygame.Rect(x, y, size, size)
			pygame.draw.rect(self.screen, (60, 60, 80), placeholder_rect)
			pygame.draw.rect(self.screen, (100, 100, 120), placeholder_rect, 3)
			
			# Línea vertical y rectángulo como placeholder
			center_x = x + size // 2
			center_y = y + size // 2
			pygame.draw.line(self.screen, (150, 150, 150), (center_x, y + 20), (center_x, y + size - 20), 3)
			pygame.draw.rect(self.screen, (150, 150, 150), (center_x - 30, center_y - 20, 60, 40), 2)
	
	def _render_character_stats(self, char_data: dict, x: int, y: int):
		"""Renderiza las estadísticas del personaje."""
		stats = char_data['stats']
		
		# Título de estadísticas
		stats_title = self.fonts['subtitle'].render("ESTADÍSTICAS", True, self.colors['text_highlight'])
		self.screen.blit(stats_title, (x, y))
		
		# Lista de estadísticas con mejor espaciado
		stats_list = [
			f"Vida: {stats['vida']}",
			f"Velocidad: {stats['velocidad']}",
			f"Daño: {stats['daño']}",
			f"Escudo: {stats['escudo']}",
			f"Rango: {stats['rango_ataque']}"
		]
		
		for i, stat in enumerate(stats_list):
			stat_text = self.fonts['normal'].render(stat, True, self.colors['text'])
			self.screen.blit(stat_text, (x, y + 40 + i * 25))
	
	def _render_character_skills(self, char_data: dict, x: int, y: int):
		"""Renderiza las habilidades del personaje."""
		# Título de habilidades
		skills_title = self.fonts['subtitle'].render("HABILIDADES", True, self.colors['text_highlight'])
		self.screen.blit(skills_title, (x, y))
		
		# Lista de habilidades (todas las disponibles)
		skills = char_data['habilidades']
		for i, skill in enumerate(skills):
			skill_text = self.fonts['normal'].render(f"• {skill}", True, self.colors['text_secondary'])
			self.screen.blit(skill_text, (x, y + 40 + i * 25))
	
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
				# Botones de flecha con sprites reales
				# Determinar estado del botón
				if button['rect'].collidepoint(self.mouse_pos):
					button_state = "h"  # hover
				else:
					button_state = "n"  # normal
				
				# Obtener sprite del botón (usando nombres correctos)
				if button_id == "arrow_left":
					button_name = "arrow_l_l"  # arrow left left
				else:
					button_name = "arrow_r_l"  # arrow right left
				
				button_sprite = self.asset_manager.get_ui_button(button_name, button_state)
				
				if button_sprite:
					# Escalar el sprite al tamaño del botón
					scaled_sprite = pygame.transform.scale(button_sprite, (button['rect'].width, button['rect'].height))
					self.screen.blit(scaled_sprite, button['rect'])
				else:
					# Fallback: intentar con nombres alternativos
					fallback_names = {
						"arrow_left": ["bleft", "arrow_l", "left", "arrow_l_n"],
						"arrow_right": ["bright", "arrow_r", "right", "arrow_r_n"]
					}
					
					fallback_list = fallback_names.get(button_id, [])
					button_sprite = None
					
					for fallback_name in fallback_list:
						button_sprite = self.asset_manager.get_ui_button(fallback_name, button_state)
						if button_sprite:
							break
					
					if button_sprite:
						# Escalar el sprite al tamaño del botón
						scaled_sprite = pygame.transform.scale(button_sprite, (button['rect'].width, button['rect'].height))
						self.screen.blit(scaled_sprite, button['rect'])
					else:
						# Fallback final: dibujar botón básico
						if button['rect'].collidepoint(self.mouse_pos):
							button_color = self.colors['button_hover']
							border_color = self.colors['text_highlight']
						else:
							button_color = self.colors['button']
							border_color = self.colors['panel_border']
						
						pygame.draw.rect(self.screen, button_color, button['rect'])
						pygame.draw.rect(self.screen, border_color, button['rect'], 3)
						
						# Texto de la flecha
						button_text = self.fonts['title'].render(button['text'], True, self.colors['text_highlight'])
						button_text_rect = button_text.get_rect(center=button['rect'].center)
						self.screen.blit(button_text, button_text_rect)
	
	def _render_selected_info(self):
		"""Renderiza información adicional del personaje seleccionado."""
		if self.selected_key in self.character_data:
			char_data = self.character_data[self.selected_key]
			
			# Panel de información - Posicionar entre las tarjetas y los botones
			info_rect = pygame.Rect(20, self.screen_height - 100, self.screen_width - 40, 40)
			pygame.draw.rect(self.screen, self.colors['panel'], info_rect)
			pygame.draw.rect(self.screen, self.colors['panel_border'], info_rect, 2)
			
			# Descripción
			desc_text = char_data.get('descripcion', 'Sin descripción disponible')
			# Truncar descripción si es muy larga para el ancho disponible
			max_chars = (self.screen_width - 80) // 8  # Aproximadamente 8 píxeles por carácter
			if len(desc_text) > max_chars:
				desc_text = desc_text[:max_chars-3] + "..."
			
			desc_surface = self.fonts['small'].render(desc_text, True, self.colors['text'])
			desc_rect = desc_surface.get_rect(midleft=(info_rect.x + 10, info_rect.centery))
			self.screen.blit(desc_surface, desc_rect)
	
	def _get_character_image(self, character_key: str) -> Optional[pygame.Surface]:
		"""Obtiene la imagen animada de un personaje."""
		try:
			# Intentar obtener frames de animación
			frames = self.animation_frames.get(character_key, [])
			if frames and len(frames) > 0:
				# Obtener el frame actual de la animación
				frame_index = self.current_frame % len(frames)
				return frames[frame_index]
			
			# Fallback: intentar obtener sprite estático
			image = self.asset_manager.get_character_sprite(character_key, "Idle", 1)
			if image:
				return image
			
			# Si no hay sprite específico, intentar con get_image
			image = self.asset_manager.get_image(character_key)
			if image:
				return image
			
			# Crear placeholder
			self.logger.warning(f"No se encontró imagen para {character_key}, usando placeholder")
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
		# Avanzar al juego después de seleccionar
		self._on_start_clicked()
	
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
	
	def handle_event(self, event: pygame.event.Event):
		"""Procesa eventos de Pygame."""
		if event.type == pygame.MOUSEMOTION:
			self.mouse_pos = event.pos
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:  # Clic izquierdo
				self._handle_click(event.pos)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				self._previous_character()
			elif event.key == pygame.K_RIGHT:
				self._next_character()
			elif event.key == pygame.K_RETURN:
				self._on_start_clicked()
			elif event.key == pygame.K_ESCAPE:
				self._on_back_clicked()
	
	def _handle_click(self, pos):
		"""Maneja los clics del mouse."""
		# Verificar clics en botones usando el diccionario self.buttons
		for button_id, button in self.buttons.items():
			if button['rect'].collidepoint(pos):
				if button_id == 'arrow_left':
					self._previous_character()
					return
				elif button_id == 'arrow_right':
					self._next_character()
					return
				elif button_id == 'start':
					self._on_start_clicked()
					return
				elif button_id == 'back':
					self._on_back_clicked()
					return
	
	def _init_buttons(self):
		"""Inicializa los botones de la interfaz."""
		button_width = 60
		button_height = 60
		button_y = self.screen_height - 100
		
		self.buttons = {
			'arrow_left': {
				'rect': pygame.Rect(50, button_y, button_width, button_height),
				'text': '←'
			},
			'arrow_right': {
				'rect': pygame.Rect(self.screen_width - 110, button_y, button_width, button_height),
				'text': '→'
			},
			'start': {
				'rect': pygame.Rect(self.screen_width // 2 - 100, button_y, 200, 60),
				'text': 'COMENZAR JUEGO'
			},
			'back': {
				'rect': pygame.Rect(20, 20, 100, 40),
				'text': 'VOLVER'
			}
		} 