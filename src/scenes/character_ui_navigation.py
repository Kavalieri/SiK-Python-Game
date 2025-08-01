"""
Character UI Navigation - Sistema de Navegación
==============================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado para la navegación entre personajes,
             indicadores visuales y detección de clics en tarjetas.
"""

import logging

import pygame


class CharacterUINavigation:
    """
    Gestiona la navegación y selección de personajes.

    Responsabilidades:
    - Botones de navegación (Anterior/Siguiente)
    - Indicadores visuales de navegación
    - Detección de clics en tarjetas de personajes
    - Gestión de posiciones de tarjetas

    Ejemplo de uso:
        >>> navigation = CharacterUINavigation(screen_width, screen_height, ui_config)
        >>> navigation.render_navigation_buttons(screen, mouse_pos)
        >>> clicked_char = navigation.get_character_card_clicked(mouse_pos, positions)
    """

    def __init__(self, screen_width: int, screen_height: int, ui_config):
        """
        Inicializa el sistema de navegación.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
            ui_config: Configuración de UI (CharacterUIConfiguration)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ui_config = ui_config
        self.logger = logging.getLogger(__name__)

        # Obtener configuración
        self.colors = ui_config.get_colors()
        self.fonts = ui_config.get_fonts()
        self.dimensions = ui_config.get_dimensions()

        # Inicializar botones de navegación
        self.nav_buttons = {}
        self._init_navigation_buttons()

        self.logger.info("CharacterUINavigation inicializado")

    def _init_navigation_buttons(self):
        """Inicializa los botones de navegación (Anterior/Siguiente)."""
        margin = self.dimensions["margin"]
        nav_width = self.dimensions["nav_width"]
        nav_height = self.dimensions["nav_height"]

        # Botón Anterior (centro inferior izquierda)
        prev_x = self.screen_width // 2 - nav_width - margin
        prev_y = self.screen_height - nav_height - margin
        self.nav_buttons["prev"] = pygame.Rect(prev_x, prev_y, nav_width, nav_height)

        # Botón Siguiente (centro inferior derecha)
        next_x = self.screen_width // 2 + margin
        next_y = self.screen_height - nav_height - margin
        self.nav_buttons["next"] = pygame.Rect(next_x, next_y, nav_width, nav_height)

        self.logger.debug(
            "Botones navegación inicializados: %s", list(self.nav_buttons.keys())
        )

    def render_navigation_buttons(
        self, screen: pygame.Surface, mouse_pos: tuple[int, int]
    ):
        """
        Renderiza los botones de navegación con efectos hover.

        Args:
            screen: Superficie donde renderizar
            mouse_pos: Posición actual del mouse para efectos hover
        """
        button_texts = {"prev": "<", "next": ">"}

        for button_name, button_rect in self.nav_buttons.items():
            self._render_navigation_button(
                screen, button_rect, button_texts[button_name], mouse_pos
            )

    def _render_navigation_button(
        self,
        screen: pygame.Surface,
        button_rect: pygame.Rect,
        button_text: str,
        mouse_pos: tuple[int, int],
    ):
        """
        Renderiza un botón de navegación individual.

        Args:
            screen: Superficie donde renderizar
            button_name: Nombre del botón
            button_rect: Rectángulo del botón
            button_text: Texto a mostrar
            mouse_pos: Posición del mouse
        """
        # Detectar hover
        is_hover = button_rect.collidepoint(mouse_pos)

        # Colores según estado
        bg_color = self.colors["button_hover"] if is_hover else self.colors["button"]
        border_color = self.colors["panel_border"]
        text_color = self.colors["button_text"]

        # Dibujar fondo del botón
        pygame.draw.rect(screen, bg_color, button_rect)
        pygame.draw.rect(screen, border_color, button_rect, 2)

        # Renderizar texto centrado
        font = self.fonts["normal"]
        text_surface = font.render(button_text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def render_navigation_indicator(
        self, screen: pygame.Surface, current_index: int, total_characters: int
    ):
        """
        Renderiza el indicador de navegación (puntos que muestran personaje actual).

        Args:
            screen: Superficie donde renderizar
            current_index: Índice del personaje actual
            total_characters: Total de personajes disponibles
        """
        if total_characters <= 1:
            return

        dot_size = 8
        dot_spacing = 20
        total_width = (total_characters - 1) * dot_spacing
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height - 60

        for i in range(total_characters):
            x = start_x + i * dot_spacing

            # Color según si es el personaje actual
            color = (
                self.colors["text_highlight"]
                if i == current_index
                else self.colors["text_secondary"]
            )

            pygame.draw.circle(screen, color, (x, y), dot_size)

        self.logger.debug(
            "Indicador navegación renderizado: %d/%d",
            current_index + 1,
            total_characters,
        )

    def get_navigation_clicked(self, mouse_pos: tuple[int, int]) -> str | None:
        """
        Detecta qué botón de navegación fue clickeado.

        Args:
            mouse_pos: Posición donde se hizo clic

        Returns:
            str: Nombre del botón clickeado ('prev'/'next') o None
        """
        for button_name, button_rect in self.nav_buttons.items():
            if button_rect.collidepoint(mouse_pos):
                self.logger.debug("Botón navegación clickeado: %s", button_name)
                return button_name
        return None

    def get_character_card_clicked(
        self,
        mouse_pos: tuple[int, int],
        character_positions: dict[str, tuple[int, int]],
    ) -> str | None:
        """
        Detecta qué tarjeta de personaje fue clickeada.

        Args:
            mouse_pos: Posición donde se hizo clic
            character_positions: Diccionario con posiciones de tarjetas {character_key: (x, y)}

        Returns:
            str: Clave del personaje clickeado o None si no hubo clic en tarjeta
        """
        card_width = self.dimensions["card_width"]
        card_height = self.dimensions["card_height"]

        for character_key, (x, y) in character_positions.items():
            card_rect = pygame.Rect(x, y, card_width, card_height)
            if card_rect.collidepoint(mouse_pos):
                self.logger.debug("Tarjeta de personaje clickeada: %s", character_key)
                return character_key

        return None

    def is_navigation_hovered(
        self, button_name: str, mouse_pos: tuple[int, int]
    ) -> bool:
        """
        Verifica si un botón de navegación específico está siendo hover.

        Args:
            button_name: Nombre del botón ('prev'/'next')
            mouse_pos: Posición actual del mouse

        Returns:
            bool: True si el mouse está sobre el botón
        """
        button_rect = self.nav_buttons.get(button_name)
        if button_rect is None:
            return False
        return button_rect.collidepoint(mouse_pos)
