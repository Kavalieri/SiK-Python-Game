"""
Menu Theme - Configuración de Temas y Estilos
===========================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo para configuración de temas visuales de menús.
"""

import pygame
import pygame_menu
from pygame_menu import themes  # Import directo de themes para evitar pylint error

from utils.logger import get_logger


class MenuTheme:
    """
    Gestor de temas visuales para menús del juego.
    """

    def __init__(self, screen: pygame.Surface, config_manager=None):
        """
        Inicializa el gestor de temas.

        Args:
            screen: Superficie de pantalla para dimensiones
            config_manager: Configuración opcional del juego
        """
        self.screen = screen
        self.config = config_manager
        self.logger = get_logger("SiK_Game")

        # Configuración base
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def create_default_theme(self):
        """Crea el tema visual por defecto para los menús."""
        theme = themes.THEME_DEFAULT.copy()
        theme.background_color = (0, 0, 0, 180)
        theme.title_font_color = (255, 255, 255)
        theme.widget_font_color = (255, 255, 255)
        theme.selection_color = (255, 165, 0)
        return theme

    def create_dark_theme(self):
        """Crea tema oscuro alternativo."""
        theme = themes.THEME_DARK.copy()
        theme.background_color = (20, 20, 30, 200)
        theme.title_font_color = (220, 220, 220)
        theme.widget_font_color = (200, 200, 200)
        theme.selection_color = (100, 150, 255)
        return theme

    def create_game_theme(self):
        """Crea tema personalizado del juego."""
        theme = themes.THEME_SOLARIZED.copy()
        theme.background_color = (40, 40, 60, 190)
        theme.title_font_color = (255, 215, 0)  # Dorado
        theme.widget_font_color = (245, 245, 245)
        theme.selection_color = (255, 140, 0)  # Naranja
        return theme

    def get_theme_by_name(self, theme_name: str = "default"):
        """
        Obtiene tema por nombre.

        Args:
            theme_name: Nombre del tema ('default', 'dark', 'game')

        Returns:
            Tema solicitado o default si no existe
        """
        theme_options = {
            "default": self.create_default_theme,
            "dark": self.create_dark_theme,
            "game": self.create_game_theme,
        }

        if theme_name in theme_options:
            return theme_options[theme_name]()
        else:
            self.logger.warning("Tema '%s' no encontrado, usando default", theme_name)
            return self.create_default_theme()

    def get_menu_dimensions(self) -> tuple[int, int]:
        """Obtiene dimensiones para menús."""
        return self.screen_width, self.screen_height

    def get_font_sizes(self) -> dict[str, int]:
        """Obtiene tamaños de fuente estándar."""
        return {"title": 30, "button": 25, "option": 20, "label": 18, "small": 16}

    def get_spacing_config(self) -> dict[str, int]:
        """Obtiene configuración de espaciado."""
        return {
            "vertical_margin_small": 5,
            "vertical_margin_medium": 10,
            "vertical_margin_large": 20,
            "horizontal_margin": 15,
        }

    def apply_theme_to_menu(
        self, menu: pygame_menu.Menu, theme_name: str = "default"
    ) -> None:
        """
        Aplica tema a menú existente.

        Args:
            menu: Menú al que aplicar tema
            theme_name: Nombre del tema a aplicar
        """
        try:
            theme = self.get_theme_by_name(theme_name)
            # Recrear el menú es más seguro que acceder a miembros protegidos
            if hasattr(menu, "get_theme"):
                current_theme = menu.get_theme()
                # Copiar propiedades del nuevo tema al actual
                current_theme.background_color = theme.background_color
                current_theme.title_font_color = theme.title_font_color
                current_theme.widget_font_color = theme.widget_font_color
                current_theme.selection_color = theme.selection_color
            self.logger.debug("Tema '%s' aplicado correctamente", theme_name)
        except (AttributeError, ValueError) as e:
            self.logger.error("Error aplicando tema '%s': %s", theme_name, str(e))

    def get_color_palette(self) -> dict[str, tuple]:
        """Obtiene paleta de colores del juego."""
        return {
            "primary": (255, 165, 0),  # Naranja principal
            "secondary": (255, 215, 0),  # Dorado
            "background": (0, 0, 0, 180),  # Negro transparente
            "text": (255, 255, 255),  # Blanco
            "success": (0, 255, 0),  # Verde
            "error": (255, 0, 0),  # Rojo
            "warning": (255, 255, 0),  # Amarillo
            "info": (0, 100, 255),  # Azul
        }
