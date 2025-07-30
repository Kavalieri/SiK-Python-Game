"""
Character UI Renderer - Coordinador de Renderizado de Personajes
===============================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo coordinador que combina renderizado básico y avanzado
             manteniendo compatibilidad API con el sistema original.
"""

import logging

import pygame

from .character_ui_renderer_advanced import CharacterUIRendererAdvanced
from .character_ui_renderer_basic import CharacterUIRendererBasic


class CharacterUIRenderer:
    """
    Coordinador de renderizado que combina funcionalidades básicas y avanzadas.

    Mantiene compatibilidad total con la API original mientras delega
    responsabilidades a módulos especializados.

    Ejemplo de uso:
        >>> renderer = CharacterUIRenderer(ui_config)
        >>> renderer.render_title(screen)
        >>> renderer.render_character_card(screen, "guerrero", 100, 100, True)
    """

    def __init__(self, ui_config):
        """
        Inicializa el coordinador de renderizado.

        Args:
            ui_config: Configuración de UI (CharacterUIConfiguration)
        """
        self.ui_config = ui_config
        self.logger = logging.getLogger(__name__)

        # Inicializar renderizadores especializados
        self.basic_renderer = CharacterUIRendererBasic(ui_config)
        self.advanced_renderer = CharacterUIRendererAdvanced(ui_config)

        # Mantener acceso directo para compatibilidad
        self.colors = ui_config.get_colors()
        self.fonts = ui_config.get_fonts()
        self.dimensions = ui_config.get_dimensions()

        self.logger.info("CharacterUIRenderer coordinador inicializado")

    # ============================================================================
    # MÉTODOS BÁSICOS (Delegados a CharacterUIRendererBasic)
    # ============================================================================

    def render_title(self, screen: pygame.Surface):
        """Delega a renderizador básico."""
        self.basic_renderer.render_title(screen)

    def render_character_card(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        is_selected: bool = False,
    ):
        """Delega a renderizador básico."""
        self.basic_renderer.render_character_card(
            screen, character_key, x, y, is_selected
        )

    def create_character_placeholder(
        self, character_key: str, size: int = 120
    ) -> pygame.Surface:
        """Delega a renderizador básico."""
        return self.basic_renderer.create_character_placeholder(character_key, size)

    # ============================================================================
    # MÉTODOS AVANZADOS (Delegados a CharacterUIRendererAdvanced)
    # ============================================================================

    def render_character_stats(
        self, screen: pygame.Surface, character_key: str, x: int, y: int
    ):
        """Delega a renderizador avanzado."""
        self.advanced_renderer.render_character_stats(screen, character_key, x, y)

    def render_character_skills(
        self, screen: pygame.Surface, char_data, x: int, y: int
    ):
        """Delega a renderizador avanzado."""
        self.advanced_renderer.render_character_skills(screen, char_data, x, y)

    def render_character_description(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        max_width: int = 300,
    ):
        """Delega a renderizador avanzado."""
        self.advanced_renderer.render_character_description(
            screen, character_key, x, y, max_width
        )

    def render_character_info_panel(
        self,
        screen: pygame.Surface,
        character_key: str,
        x: int,
        y: int,
        width: int = 300,
        height: int = 400,
    ):
        """Delega a renderizador avanzado."""
        self.advanced_renderer.render_character_info_panel(
            screen, character_key, x, y, width, height
        )

    # ============================================================================
    # MÉTODOS DE COMPATIBILIDAD
    # ============================================================================

    def get_renderer_info(self) -> dict:
        """
        Obtiene información sobre el estado del renderizador.

        Returns:
            dict: Información del renderizador
        """
        return {
            "type": "CharacterUIRenderer",
            "modules": {
                "basic": self.basic_renderer.__class__.__name__,
                "advanced": self.advanced_renderer.__class__.__name__,
            },
            "fonts_loaded": len(self.fonts),
            "colors_loaded": len(self.colors),
            "dimensions_loaded": len(self.dimensions),
        }
