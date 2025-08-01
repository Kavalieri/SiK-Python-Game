"""
Character UI - Interfaz de Usuario para Personajes (Fachada Refactorizada)
=========================================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada principal que coordina todos los módulos de UI de personajes
             manteniendo 100% compatibilidad con la API original.
"""

import logging

import pygame

from .character_ui_buttons import CharacterUIButtons
from .character_ui_configuration import CharacterUIConfiguration
from .character_ui_navigation import CharacterUINavigation
from .character_ui_renderer import CharacterUIRenderer


class CharacterUI:
    """
    Fachada principal que gestiona la interfaz de usuario para la selección de personajes.

    Esta clase coordina todos los módulos especializados manteniendo la API original:
    - CharacterUIConfiguration: Fuentes, colores, dimensiones
    - CharacterUIButtons: Botones, navegación, eventos de clic
    - CharacterUIRenderer: Renderizado de elementos visuales

    Ejemplo de uso:
        >>> ui = CharacterUI(screen_width, screen_height, config_manager)
        >>> ui.render_title(screen)
        >>> ui.render_character_card(screen, "guerrero", 100, 100, True)
        >>> clicked_button = ui.get_clicked_button(mouse_pos)
    """

    def __init__(self, screen_width: int, screen_height: int, config_manager):
        """
        Inicializa la interfaz de usuario de personajes.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
            config_manager: Gestor de configuración
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)

        # Inicializar módulos especializados
        self.ui_config = CharacterUIConfiguration(
            screen_width, screen_height, config_manager
        )
        self.ui_buttons = CharacterUIButtons(
            screen_width, screen_height, self.ui_config
        )
        self.ui_navigation = CharacterUINavigation(
            screen_width, screen_height, self.ui_config
        )
        self.renderer = CharacterUIRenderer(self.ui_config)

        # Propiedades de compatibilidad con API original
        self.fonts = self.ui_config.get_fonts()
        self.colors = self.ui_config.get_colors()

        # Crear diccionario unificado de botones para compatibilidad
        self.buttons = {}
        self.buttons.update(self.ui_buttons.main_buttons)
        self.buttons.update(self.ui_navigation.nav_buttons)

        self.logger.info(
            "CharacterUI inicializado - Pantalla: %dx%d, Módulos: configuración, botones, renderer",
            screen_width,
            screen_height,
        )

    # ============================================================================
    # MÉTODOS DE RENDERIZADO (Delegados a CharacterUIRenderer)
    # ============================================================================

    def render_title(self, screen: pygame.Surface):
        """Renderiza el título de la pantalla."""
        self.renderer.render_title(screen)

    def render_character_card(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        is_selected: bool = False,
    ):
        """Renderiza una tarjeta de personaje."""
        self.renderer.render_character_card(screen, character_key, x, y, is_selected)

    def render_character_stats(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """Renderiza las estadísticas de un personaje."""
        self.renderer.render_character_stats(screen, character_key, x, y)

    def render_character_skills(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """Renderiza las habilidades de un personaje."""
        self.renderer.render_character_skills(screen, character_key, x, y)

    # ============================================================================
    # MÉTODOS DE BOTONES Y NAVEGACIÓN (Delegados a módulos especializados)
    # ============================================================================

    def render_buttons(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        """Renderiza los botones de la interfaz."""
        self.ui_buttons.render_main_buttons(screen, mouse_pos)
        self.ui_navigation.render_navigation_buttons(screen, mouse_pos)

    def render_navigation_indicator(
        self, screen: pygame.Surface, current_index: int, total_characters: int
    ):
        """Renderiza el indicador de navegación."""
        self.ui_navigation.render_navigation_indicator(
            screen, current_index, total_characters
        )

    def get_clicked_button(self, mouse_pos: tuple[int, int]) -> str | None:
        """Obtiene el botón clickeado."""
        return self.ui_buttons.get_main_button_clicked(
            mouse_pos
        ) or self.ui_navigation.get_navigation_clicked(mouse_pos)

    def get_character_card_clicked(
        self,
        mouse_pos: tuple[int, int],
        character_positions: dict[str, tuple[int, int]],
    ) -> str | None:
        """Obtiene la tarjeta de personaje clickeada."""
        return self.ui_navigation.get_character_card_clicked(
            mouse_pos, character_positions
        )

    # ============================================================================
    # MÉTODOS DE COMPATIBILIDAD Y ACCESO DIRECTO
    # ============================================================================

    def get_ui_info(self) -> dict:
        """Obtiene información del estado actual de la UI."""
        return {
            "screen_size": (self.screen_width, self.screen_height),
            "modules": {
                "configuration": "CharacterUIConfiguration",
                "buttons": "CharacterUIButtons",
                "renderer": "CharacterUIRenderer",
            },
            "button_count": len(self.buttons),
        }

    def is_button_hovered(self, button_name: str, mouse_pos: tuple[int, int]) -> bool:
        """Verifica si un botón específico está siendo hover."""
        return self.ui_buttons.is_main_button_hovered(
            button_name, mouse_pos
        ) or self.ui_navigation.is_navigation_hovered(button_name, mouse_pos)

    def get_button_rect(self, button_name: str) -> pygame.Rect | None:
        """Obtiene el rectángulo de un botón específico."""
        return self.ui_buttons.get_main_button_rect(
            button_name
        ) or self.ui_navigation.nav_buttons.get(button_name)
