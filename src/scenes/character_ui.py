"""
Character UI - Interfaz de Usuario para Personajes (Fachada Refactorizada)
=========================================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada principal que coordina todos los módulos de UI de personajes
             manteniendo 100% compatibilidad con la API original.
"""

import logging
from typing import Dict, Optional, Tuple

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
        """
        Renderiza el título de la pantalla.

        Args:
            screen: Superficie donde renderizar
        """
        self.renderer.render_title(screen)

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
        self.renderer.render_character_card(screen, character_key, x, y, is_selected)

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
        self.renderer.render_character_stats(screen, char_data, x, y)

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
        self.renderer.render_character_skills(screen, char_data, x, y)

    # ============================================================================
    # MÉTODOS DE BOTONES Y NAVEGACIÓN (Delegados a CharacterUIButtons)
    # ============================================================================

    def render_buttons(self, screen: pygame.Surface, mouse_pos: Tuple[int, int]):
        """
        Renderiza los botones de la interfaz.

        Args:
            screen: Superficie donde renderizar
            mouse_pos: Posición del mouse
        """
        # Renderizar botones principales
        self.ui_buttons.render_main_buttons(screen, mouse_pos)

        # Renderizar botones de navegación
        self.ui_navigation.render_navigation_buttons(screen, mouse_pos)

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
        self.ui_navigation.render_navigation_indicator(
            screen, current_index, total_characters
        )

    def get_clicked_button(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Obtiene el botón clickeado.

        Args:
            mouse_pos: Posición del mouse

        Returns:
            Nombre del botón clickeado o None
        """
        # Verificar botones principales primero
        main_button = self.ui_buttons.get_main_button_clicked(mouse_pos)
        if main_button:
            return main_button

        # Verificar botones de navegación
        nav_button = self.ui_navigation.get_navigation_clicked(mouse_pos)
        if nav_button:
            return nav_button

        return None

    def get_character_card_clicked(
        self,
        mouse_pos: Tuple[int, int],
        character_positions: Dict[str, Tuple[int, int]],
    ) -> Optional[str]:
        """
        Obtiene la tarjeta de personaje clickeada.

        Args:
            mouse_pos: Posición del mouse
            character_positions: Posiciones de las tarjetas de personajes

        Returns:
            Clave del personaje clickeado o None
        """
        return self.ui_navigation.get_character_card_clicked(
            mouse_pos, character_positions
        )

    # ============================================================================
    # MÉTODOS DE COMPATIBILIDAD Y ACCESO DIRECTO
    # ============================================================================

    def _render_character_image(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        size: int = 120,
    ):
        """
        Método de compatibilidad para renderizar imagen de personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Posición X
            y: Posición Y
            size: Tamaño de la imagen
        """
        self.renderer.render_character_image(screen, character_key, x, y, size)

    def _create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """
        Método de compatibilidad para crear placeholder de personaje.

        Args:
            character_key: Clave del personaje
            size: Tamaño del placeholder

        Returns:
            pygame.Surface: Superficie placeholder
        """
        return self.renderer.create_character_placeholder(character_key, size)

    def _init_ui_from_config(self):
        """
        Método de compatibilidad - la inicialización se hace automáticamente.
        """
        # Ya inicializado en __init__ a través de CharacterUIConfiguration
        return

    def _init_buttons(self):
        """
        Método de compatibilidad - los botones se inicializan automáticamente.
        """
        # Ya inicializado en __init__ a través de CharacterUIButtons y CharacterUINavigation
        return

    # ============================================================================
    # MÉTODOS DE INFORMACIÓN Y DEBUG
    # ============================================================================

    def get_ui_info(self) -> dict:
        """
        Obtiene información del estado actual de la UI.

        Returns:
            dict: Información de módulos y configuración
        """
        return {
            "screen_size": (self.screen_width, self.screen_height),
            "modules": {
                "configuration": self.ui_config.__class__.__name__,
                "buttons": self.ui_buttons.__class__.__name__,
                "renderer": self.renderer.__class__.__name__,
            },
            "button_count": len(self.buttons),
            "fonts_loaded": len(self.fonts),
            "colors_loaded": len(self.colors),
        }

    def is_button_hovered(self, button_name: str, mouse_pos: Tuple[int, int]) -> bool:
        """
        Verifica si un botón específico está siendo hover.

        Args:
            button_name: Nombre del botón
            mouse_pos: Posición del mouse

        Returns:
            bool: True si el mouse está sobre el botón
        """
        # Verificar en botones principales
        if self.ui_buttons.is_main_button_hovered(button_name, mouse_pos):
            return True

        # Verificar en botones de navegación
        return self.ui_navigation.is_navigation_hovered(button_name, mouse_pos)

    def get_button_rect(self, button_name: str) -> Optional[pygame.Rect]:
        """
        Obtiene el rectángulo de un botón específico.

        Args:
            button_name: Nombre del botón

        Returns:
            pygame.Rect: Rectángulo del botón o None si no existe
        """
        # Verificar en botones principales
        rect = self.ui_buttons.get_main_button_rect(button_name)
        if rect:
            return rect

        # Verificar en botones de navegación
        return self.ui_navigation.nav_buttons.get(button_name)
