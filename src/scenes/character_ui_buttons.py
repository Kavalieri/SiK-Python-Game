"""
Character UI Buttons - Gestión de Botones Principales
===================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado para la gestión de botones principales
             (Atrás, Iniciar) en la selección de personajes.
"""

import logging

import pygame


class CharacterUIButtons:
    """
    Gestiona los botones principales de la interfaz de selección de personajes.

    Responsabilidades:
    - Inicialización de botones principales (Atrás, Iniciar)
    - Renderizado de botones con efectos hover
    - Detección de clics en botones principales

    Ejemplo de uso:
        >>> buttons = CharacterUIButtons(screen_width, screen_height, ui_config)
        >>> buttons.render_main_buttons(screen, mouse_pos)
        >>> clicked = buttons.get_main_button_clicked(mouse_pos)
    """

    def __init__(self, screen_width: int, screen_height: int, ui_config):
        """
        Inicializa el sistema de botones principales.

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

        # Inicializar botones principales
        self.main_buttons = {}
        self._init_main_buttons()

        self.logger.info(
            "CharacterUIButtons inicializado con %d botones", len(self.main_buttons)
        )

    def _init_main_buttons(self):
        """Inicializa las posiciones y rectángulos de los botones principales."""
        button_width = self.dimensions["button_width"]
        button_height = self.dimensions["button_height"]
        margin = self.dimensions["margin"]

        # Botón Atrás (esquina inferior izquierda)
        back_x = margin
        back_y = self.screen_height - button_height - margin
        self.main_buttons["back"] = pygame.Rect(
            back_x, back_y, button_width, button_height
        )

        # Botón Iniciar (esquina inferior derecha)
        start_x = self.screen_width - button_width - margin
        start_y = self.screen_height - button_height - margin
        self.main_buttons["start"] = pygame.Rect(
            start_x, start_y, button_width, button_height
        )

        self.logger.debug(
            "Botones principales inicializados: %s", list(self.main_buttons.keys())
        )

    def render_main_buttons(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        """
        Renderiza los botones principales con efectos hover.

        Args:
            screen: Superficie donde renderizar
            mouse_pos: Posición actual del mouse para efectos hover
        """
        button_texts = {"back": "Atrás", "start": "Iniciar"}

        for button_name, button_rect in self.main_buttons.items():
            self._render_main_button(
                screen, button_rect, button_texts[button_name], mouse_pos
            )

    def _render_main_button(
        self,
        screen: pygame.Surface,
        button_rect: pygame.Rect,
        button_text: str,
        mouse_pos: tuple[int, int],
    ):
        """
        Renderiza un botón principal individual.

        Args:
            screen: Superficie donde renderizar
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

    def get_main_button_clicked(self, mouse_pos: tuple[int, int]) -> str | None:
        """
        Detecta qué botón principal fue clickeado.

        Args:
            mouse_pos: Posición donde se hizo clic

        Returns:
            str: Nombre del botón clickeado ('back'/'start') o None
        """
        for button_name, button_rect in self.main_buttons.items():
            if button_rect.collidepoint(mouse_pos):
                self.logger.debug("Botón principal clickeado: %s", button_name)
                return button_name
        return None

    def get_main_button_rect(self, button_name: str) -> pygame.Rect | None:
        """
        Obtiene el rectángulo de un botón principal específico.

        Args:
            button_name: Nombre del botón ('back'/'start')

        Returns:
            pygame.Rect: Rectángulo del botón o None si no existe
        """
        return self.main_buttons.get(button_name)

    def is_main_button_hovered(
        self, button_name: str, mouse_pos: tuple[int, int]
    ) -> bool:
        """
        Verifica si un botón principal específico está siendo hover.

        Args:
            button_name: Nombre del botón ('back'/'start')
            mouse_pos: Posición actual del mouse

        Returns:
            bool: True si el mouse está sobre el botón
        """
        button_rect = self.main_buttons.get(button_name)
        if button_rect is None:
            return False
        return button_rect.collidepoint(mouse_pos)
