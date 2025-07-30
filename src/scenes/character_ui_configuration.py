"""Character UI Configuration - Configuración de Interfaz de Usuario"""

import logging
from typing import Dict

import pygame


class CharacterUIConfiguration:
    """Gestiona la configuración de la interfaz de usuario para personajes."""

    def __init__(self, screen_width: int, screen_height: int, config_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self.fonts = {}
        self.colors = {}
        self.dimensions = {}
        self._init_fonts()
        self._init_colors()
        self._init_dimensions()

    def _init_fonts(self):
        """Inicializa las fuentes desde la configuración."""
        try:
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
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error("Error al inicializar fuentes UI: %s", e)
            self._init_fallback_fonts()

    def _init_fallback_fonts(self):
        """Inicializa fuentes por defecto en caso de error."""
        self.fonts = {
            "title": pygame.font.Font(None, 48),
            "subtitle": pygame.font.Font(None, 32),
            "normal": pygame.font.Font(None, 24),
            "small": pygame.font.Font(None, 18),
        }

    def _init_colors(self):
        """Inicializa los colores desde la configuración."""
        try:
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
                "card_selected": self.config_manager.get_ui_color(
                    "tarjeta_seleccionada"
                ),
                "card_border_selected": self.config_manager.get_ui_color(
                    "tarjeta_borde_seleccionada"
                ),
            }
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error("Error al inicializar colores UI: %s", e)
            self._init_fallback_colors()

    def _init_fallback_colors(self):
        """Inicializa colores por defecto en caso de error."""
        self.colors = {
            "background": (30, 30, 30),
            "panel": (60, 60, 60),
            "panel_border": (100, 100, 100),
            "text": (255, 255, 255),
            "text_secondary": (180, 180, 180),
            "text_highlight": (255, 215, 0),
            "button": (80, 80, 80),
            "button_hover": (120, 120, 120),
            "button_text": (255, 255, 255),
            "card_selected": (100, 150, 100),
            "card_border_selected": (150, 255, 150),
        }

    def _init_dimensions(self):
        """Inicializa las dimensiones desde la configuración."""
        try:
            self.dimensions = {
                "button_width": self.config_manager.get_ui_dimension(
                    "botón_ancho", 120
                ),
                "button_height": self.config_manager.get_ui_dimension("botón_alto", 40),
                "margin": self.config_manager.get_ui_dimension("margen", 20),
                "card_width": 200,
                "card_height": 280,
                "nav_width": 60,
                "nav_height": 40,
            }
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error("Error al inicializar dimensiones UI: %s", e)
            self._init_fallback_dimensions()

    def _init_fallback_dimensions(self):
        """Inicializa dimensiones por defecto en caso de error."""
        self.dimensions = {
            "button_width": 120,
            "button_height": 40,
            "margin": 20,
            "card_width": 200,
            "card_height": 280,
            "nav_width": 60,
            "nav_height": 40,
        }

    def get_fonts(self) -> Dict[str, pygame.font.Font]:
        """Obtiene el diccionario de fuentes configuradas."""
        return self.fonts

    def get_colors(self) -> Dict[str, tuple]:
        """Obtiene el diccionario de colores configurados."""
        return self.colors

    def get_dimensions(self) -> Dict[str, int]:
        """Obtiene el diccionario de dimensiones configuradas."""
        return self.dimensions

    def get_font(self, font_name: str) -> pygame.font.Font:
        """Obtiene una fuente específica."""
        font = self.fonts.get(font_name, self.fonts.get("normal"))
        if font is None:
            font = pygame.font.Font(None, 24)
        return font

    def get_color(self, color_name: str) -> tuple:
        """Obtiene un color específico."""
        return self.colors.get(color_name, (255, 255, 255))

    def get_dimension(self, dimension_name: str, default: int = 0) -> int:
        """Obtiene una dimensión específica."""
        return self.dimensions.get(dimension_name, default)
