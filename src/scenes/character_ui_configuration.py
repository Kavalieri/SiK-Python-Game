"""
Character UI Configuration - Configuración de Interfaz de Usuario
===============================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado para la configuración de UI (fuentes, colores, dimensiones)
             y inicialización de componentes de la interfaz de selección de personajes.
"""

import logging
from typing import Dict

import pygame


class CharacterUIConfiguration:
    """
    Gestiona la configuración de la interfaz de usuario para personajes.

    Responsabilidades:
    - Configuración de fuentes según configuración del juego
    - Configuración de colores desde config manager
    - Inicialización de dimensiones y márgenes
    - Gestión de configuración UI centralizada

    Ejemplo de uso:
        >>> config = CharacterUIConfiguration(screen_width, screen_height, config_manager)
        >>> fonts = config.get_fonts()
        >>> colors = config.get_colors()
    """

    def __init__(self, screen_width: int, screen_height: int, config_manager):
        """
        Inicializa la configuración de UI.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
            config_manager: Gestor de configuración del juego
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)

        # Inicializar configuración UI
        self.fonts = {}
        self.colors = {}
        self.dimensions = {}

        self._init_fonts()
        self._init_colors()
        self._init_dimensions()

        self.logger.info(
            "CharacterUIConfiguration inicializada - Pantalla: %dx%d",
            screen_width,
            screen_height,
        )

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
            self.logger.debug("Fuentes UI inicializadas correctamente")
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error("Error al inicializar fuentes UI: %s", e)
            # Fallback a fuentes por defecto
            self._init_fallback_fonts()

    def _init_fallback_fonts(self):
        """Inicializa fuentes por defecto en caso de error."""
        self.fonts = {
            "title": pygame.font.Font(None, 48),
            "subtitle": pygame.font.Font(None, 32),
            "normal": pygame.font.Font(None, 24),
            "small": pygame.font.Font(None, 18),
        }
        self.logger.warning(
            "Usando fuentes por defecto debido a error de configuración"
        )

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
            self.logger.debug("Colores UI inicializados correctamente")
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error("Error al inicializar colores UI: %s", e)
            # Fallback a colores por defecto
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
        self.logger.warning(
            "Usando colores por defecto debido a error de configuración"
        )

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
            self.logger.debug("Dimensiones UI inicializadas correctamente")
        except (KeyError, ValueError, TypeError) as e:
            self.logger.error("Error al inicializar dimensiones UI: %s", e)
            # Fallback a dimensiones por defecto
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
        self.logger.warning(
            "Usando dimensiones por defecto debido a error de configuración"
        )

    def get_fonts(self) -> Dict[str, pygame.font.Font]:
        """
        Obtiene el diccionario de fuentes configuradas.

        Returns:
            Dict[str, pygame.font.Font]: Diccionario de fuentes
        """
        return self.fonts

    def get_colors(self) -> Dict[str, tuple]:
        """
        Obtiene el diccionario de colores configurados.

        Returns:
            Dict[str, tuple]: Diccionario de colores RGB
        """
        return self.colors

    def get_dimensions(self) -> Dict[str, int]:
        """
        Obtiene el diccionario de dimensiones configuradas.

        Returns:
            Dict[str, int]: Diccionario de dimensiones en píxeles
        """
        return self.dimensions

    def get_font(self, font_name: str) -> pygame.font.Font:
        """
        Obtiene una fuente específica.

        Args:
            font_name: Nombre de la fuente

        Returns:
            pygame.font.Font: Fuente solicitada o fuente normal por defecto
        """
        font = self.fonts.get(font_name, self.fonts.get("normal"))
        if font is None:
            # Fallback a fuente pygame por defecto
            font = pygame.font.Font(None, 24)
        return font

    def get_color(self, color_name: str) -> tuple:
        """
        Obtiene un color específico.

        Args:
            color_name: Nombre del color

        Returns:
            tuple: Color RGB o blanco por defecto
        """
        return self.colors.get(color_name, (255, 255, 255))

    def get_dimension(self, dimension_name: str, default: int = 0) -> int:
        """
        Obtiene una dimensión específica.

        Args:
            dimension_name: Nombre de la dimensión
            default: Valor por defecto si no existe

        Returns:
            int: Dimensión en píxeles
        """
        return self.dimensions.get(dimension_name, default)
