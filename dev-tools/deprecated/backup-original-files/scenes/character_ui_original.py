"""
Character UI - Interfaz de Usuario para Personajes
================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que maneja la interfaz de usuario para la selección de personajes.
"""

import logging

import pygame

from .character_data import CharacterData


class CharacterUI:
    """
    Gestiona la interfaz de usuario para la selección de personajes.

    Ejemplo de uso:
        >>> ui = CharacterUI(screen_width, screen_height, config_manager)
        >>> ui.render_title(screen)
    """

    def __init__(self, screen_width: int, screen_height: int, config_manager):
        """
        Inicializa la interfaz de usuario de personajes.

        Args:
            screen_width: Ancho de la pantalla.
            screen_height: Alto de la pantalla.
            config_manager: Gestor de configuración.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)
        self.config_manager = config_manager

        # Inicializar fuentes y colores desde configuración
        self._init_ui_from_config()

        # Botones
        self.buttons = {}
        self._init_buttons()

    def _init_ui_from_config(self):
        """Inicializa la UI desde la configuración."""
        # Fuentes
        self.fonts = {
            "title": pygame.font.Font(
                None, self.config_manager.get_ui_font_size("título")
            ),
            "subtitle": pygame.font.Font(
                None, self.config_manager.get_ui_font_size("subtítulo")
            ),
            "normal": pygame.font.Font(
                None, self.config_manager.get_ui_font_size("normal")
            ),
            "small": pygame.font.Font(
                None, self.config_manager.get_ui_font_size("pequeña")
            ),
        }

        # Colores
        self.colors = {
            "background": self.config_manager.get_ui_color("fondo"),
            "panel": self.config_manager.get_ui_color("panel"),
            "panel_border": self.config_manager.get_ui_color("panel_borde"),
            "text": self.config_manager.get_ui_color("texto"),
            "text_secondary": self.config_manager.get_ui_color("texto_secundario"),
            "text_highlight": self.config_manager.get_ui_color("texto_destacado"),
            "button": self.config_manager.get_ui_color("botón"),
            "button_hover": self.config_manager.get_ui_color("botón_hover"),
            "button_text": self.config_manager.get_ui_color("botón_texto"),
            "card_selected": self.config_manager.get_ui_color("tarjeta_seleccionada"),
            "card_border_selected": self.config_manager.get_ui_color(
                "tarjeta_borde_seleccionada"
            ),
        }

    def _init_buttons(self):
        """Inicializa los botones de la interfaz."""
        button_width = self.config_manager.get_ui_dimension("botón_ancho")
        button_height = self.config_manager.get_ui_dimension("botón_alto")
        margin = self.config_manager.get_ui_dimension("margen")

        # Botón Atrás
        back_x = margin
        back_y = self.screen_height - button_height - margin
        self.buttons["back"] = pygame.Rect(back_x, back_y, button_width, button_height)

        # Botón Iniciar
        start_x = self.screen_width - button_width - margin
        start_y = self.screen_height - button_height - margin
        self.buttons["start"] = pygame.Rect(
            start_x, start_y, button_width, button_height
        )

        # Botones de navegación
        nav_width = 60
        nav_height = 40

        # Botón Anterior
        prev_x = self.screen_width // 2 - nav_width - margin
        prev_y = self.screen_height - nav_height - margin
        self.buttons["prev"] = pygame.Rect(prev_x, prev_y, nav_width, nav_height)

        # Botón Siguiente
        next_x = self.screen_width // 2 + margin
        next_y = self.screen_height - nav_height - margin
        self.buttons["next"] = pygame.Rect(next_x, next_y, nav_width, nav_height)

    def render_title(self, screen: pygame.Surface):
        """
        Renderiza el título de la pantalla.

        Args:
            screen: Superficie donde renderizar
        """
        title_text = "Selecciona tu Personaje"
        title_surface = self.fonts["title"].render(
            title_text, True, self.colors["text_highlight"]
        )
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title_surface, title_rect)

    def render_character_card(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        is_selected: bool = False,
    ):
        """
        Renderiza una tarjeta de personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Posición X
            y: Posición Y
            is_selected: Si está seleccionado
        """
        card_width = 200
        card_height = 280
        card_rect = pygame.Rect(x, y, card_width, card_height)

        # Color de fondo según selección
        bg_color = self.colors["card_selected"] if is_selected else self.colors["panel"]
        border_color = (
            self.colors["card_border_selected"]
            if is_selected
            else self.colors["panel_border"]
        )

        # Dibujar tarjeta
        pygame.draw.rect(screen, bg_color, card_rect)
        pygame.draw.rect(screen, border_color, card_rect, 3)

        # Obtener datos del personaje
        char_data = CharacterData.get_character_data(character_key)
        if not char_data:
            return

        # Renderizar imagen del personaje
        self._render_character_image(screen, character_key, x + 40, y + 20)

        # Renderizar nombre
        name_text = char_data["nombre"]
        name_surface = self.fonts["subtitle"].render(
            name_text, True, self.colors["text"]
        )
        name_rect = name_surface.get_rect(center=(x + card_width // 2, y + 160))
        screen.blit(name_surface, name_rect)

        # Renderizar tipo
        type_text = char_data["tipo"]
        type_surface = self.fonts["small"].render(
            type_text, True, self.colors["text_secondary"]
        )
        type_rect = type_surface.get_rect(center=(x + card_width // 2, y + 185))
        screen.blit(type_surface, type_rect)

    def _render_character_image(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        size: int = 120,
    ):
        """
        Renderiza la imagen de un personaje.

        Args:
            screen: Superficie donde renderizar.
            character_key: Clave del personaje.
            x: Posición X.
            y: Posición Y.
            size: Tamaño de la imagen.

        Ejemplo:
            >>> ui._render_character_image(screen, "guerrero", 100, 100, 120)
        """
        try:
            # Obtener imagen del personaje (placeholder por ahora)
            placeholder = self._create_character_placeholder(character_key, size)

            # Escalar si es necesario
            if placeholder.get_size() != (size, size):
                placeholder = pygame.transform.scale(placeholder, (size, size))

            screen.blit(placeholder, (x, y))

        except pygame.error as e:
            self.logger.error(
                "Error de Pygame al renderizar imagen de %s: %s", character_key, e
            )
        except Exception as e:
            self.logger.error(
                "Error inesperado al renderizar imagen de %s: %s", character_key, e
            )

    def _create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """
        Crea un placeholder para un personaje.

        Args:
            character_key: Clave del personaje.
            size: Tamaño del placeholder.

        Returns:
            pygame.Surface: Superficie placeholder.

        Ejemplo:
            >>> placeholder = ui._create_character_placeholder("guerrero", 120)
        """
        placeholder = pygame.Surface((size, size))

        # Color según el personaje
        character_colors = {
            "guerrero": (139, 69, 19),  # Marrón
            "robot": (128, 128, 128),  # Gris
            "adventureguirl": (255, 182, 193),  # Rosa claro
        }

        color = character_colors.get(character_key.lower(), (255, 0, 0))
        placeholder.fill(color)

        # Añadir borde
        pygame.draw.rect(placeholder, (255, 255, 255), (0, 0, size, size), 3)

        return placeholder

    def render_character_stats(
        self, screen: pygame.Surface, char_data: dict, x: int, y: int
    ):
        """
        Renderiza las estadísticas de un personaje.

        Args:
            screen: Superficie donde renderizar
            char_data: Datos del personaje
            x: Posición X
            y: Posición Y
        """
        stats = char_data.get("stats", {})

        # Título de estadísticas
        stats_title = self.fonts["normal"].render(
            "Estadísticas:", True, self.colors["text_highlight"]
        )
        screen.blit(stats_title, (x, y))

        y_offset = 30
        for stat_name, stat_value in stats.items():
            # Formatear nombre de estadística
            stat_display = stat_name.replace("_", " ").title()

            # Renderizar estadística
            stat_text = f"{stat_display}: {stat_value}"
            stat_surface = self.fonts["small"].render(
                stat_text, True, self.colors["text"]
            )
            screen.blit(stat_surface, (x, y + y_offset))
            y_offset += 20

    def render_character_skills(
        self, screen: pygame.Surface, char_data: dict, x: int, y: int
    ):
        """
        Renderiza las habilidades de un personaje.

        Args:
            screen: Superficie donde renderizar
            char_data: Datos del personaje
            x: Posición X
            y: Posición Y
        """
        skills = char_data.get("habilidades", [])

        # Título de habilidades
        skills_title = self.fonts["normal"].render(
            "Habilidades:", True, self.colors["text_highlight"]
        )
        screen.blit(skills_title, (x, y))

        y_offset = 30
        for skill in skills:
            skill_surface = self.fonts["small"].render(
                f"• {skill}", True, self.colors["text"]
            )
            screen.blit(skill_surface, (x, y + y_offset))
            y_offset += 20

    def render_buttons(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        """
        Renderiza los botones de la interfaz.

        Args:
            screen: Superficie donde renderizar
            mouse_pos: Posición del mouse
        """
        button_texts = {"back": "Atrás", "start": "Iniciar", "prev": "<", "next": ">"}

        for button_name, button_rect in self.buttons.items():
            # Color según hover
            is_hover = button_rect.collidepoint(mouse_pos)
            bg_color = (
                self.colors["button_hover"] if is_hover else self.colors["button"]
            )

            # Dibujar botón
            pygame.draw.rect(screen, bg_color, button_rect)
            pygame.draw.rect(screen, self.colors["panel_border"], button_rect, 2)

            # Texto del botón
            text = button_texts.get(button_name, "")
            if text:
                text_surface = self.fonts["normal"].render(
                    text, True, self.colors["button_text"]
                )
                text_rect = text_surface.get_rect(center=button_rect.center)
                screen.blit(text_surface, text_rect)

    def render_navigation_indicator(
        self, screen: pygame.Surface, current_index: int, total_characters: int
    ):
        """
        Renderiza el indicador de navegación.

        Args:
            screen: Superficie donde renderizar
            current_index: Índice actual
            total_characters: Total de personajes
        """
        if total_characters <= 1:
            return

        # Crear indicador de puntos
        dot_size = 8
        dot_spacing = 20
        total_width = (total_characters - 1) * dot_spacing
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height - 60

        for i in range(total_characters):
            x = start_x + i * dot_spacing
            color = (
                self.colors["text_highlight"]
                if i == current_index
                else self.colors["text_secondary"]
            )
            pygame.draw.circle(screen, color, (x, y), dot_size)

    def get_clicked_button(self, mouse_pos: tuple[int, int]) -> str | None:
        """
        Obtiene el botón clickeado.

        Args:
            mouse_pos: Posición del mouse

        Returns:
            Nombre del botón clickeado o None
        """
        for button_name, button_rect in self.buttons.items():
            if button_rect.collidepoint(mouse_pos):
                return button_name
        return None

    def get_character_card_clicked(
        self,
        mouse_pos: tuple[int, int],
        character_positions: dict[str, tuple[int, int]],
    ) -> str | None:
        """
        Obtiene la tarjeta de personaje clickeada.

        Args:
            mouse_pos: Posición del mouse
            character_positions: Posiciones de las tarjetas de personajes

        Returns:
            Clave del personaje clickeado o None
        """
        card_width = 200
        card_height = 280

        for character_key, (x, y) in character_positions.items():
            card_rect = pygame.Rect(x, y, card_width, card_height)
            if card_rect.collidepoint(mouse_pos):
                return character_key

        return None
