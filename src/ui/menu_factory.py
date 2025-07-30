"""
Menu Factory - Fábrica de Menús Refactorizada (FACHADA)
====================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Fachada unificada para creación y gestión de menús del juego.
Mantiene 100% compatibilidad con API original.
"""

from typing import Dict

import pygame
import pygame_menu

from ..utils.config_manager import ConfigManager
from ..utils.logger import get_logger
from ..utils.save_manager import SaveManager
from .menu_callbacks import MenuCallbacks
from .menu_configuration import MenuConfiguration
from .menu_creators import MenuCreators
from .menu_theme import MenuTheme


class MenuFactory:
    """
    Fábrica para crear y configurar menús del juego.
    Fachada que mantiene compatibilidad con API original.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        config: ConfigManager,
        save_manager: SaveManager,
        callbacks: MenuCallbacks,
    ):
        """
        Inicializa la fábrica de menús.

        Args:
            screen: Superficie de Pygame
            config: Configuración del juego
            save_manager: Gestor de guardado
            callbacks: Callbacks de menú
        """
        self.screen = screen
        self.config = config
        self.save_manager = save_manager
        self.callbacks = callbacks
        self.logger = get_logger("SiK_Game")

        # Configuración de pantalla
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Inicializar módulos especializados
        self.theme_manager = MenuTheme(screen, config)
        self.config_helper = MenuConfiguration(config, save_manager)
        self.menu_creator = MenuCreators(screen, config, save_manager, callbacks)

        # Mantener compatibilidad con API original
        self.theme = self.theme_manager.create_default_theme()

    def _create_theme(self):
        """Crea el tema visual para los menús (método legacy)."""
        return self.theme_manager.create_default_theme()

    def create_main_menu(self) -> pygame_menu.Menu:
        """Crea el menú principal con flujo avanzado y callbacks diferenciados."""
        return self.menu_creator.create_main_menu()

    def create_pause_menu(self) -> pygame_menu.Menu:
        """Crea el menú de pausa."""
        return self.menu_creator.create_pause_menu()

    def create_upgrade_menu(self) -> pygame_menu.Menu:
        """Crea el menú de mejoras."""
        return self.menu_creator.create_upgrade_menu()

    def create_character_select_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de personaje."""
        return self.menu_creator.create_character_select_menu()

    def create_options_menu(self) -> pygame_menu.Menu:
        """Crea el menú de opciones."""
        return self.menu_creator.create_options_menu()

    def create_inventory_menu(self) -> pygame_menu.Menu:
        """Crea el menú de inventario."""
        return self.menu_creator.create_inventory_menu()

    def create_save_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de slots de guardado avanzado."""
        return self.menu_creator.create_save_menu()

    def create_all_menus(self) -> Dict[str, pygame_menu.Menu]:
        """
        Crea todos los menús del juego.

        Returns:
            Diccionario con todos los menús creados
        """
        menus = {}

        try:
            menus["main"] = self.create_main_menu()
            menus["pause"] = self.create_pause_menu()
            menus["upgrade"] = self.create_upgrade_menu()
            menus["character_select"] = self.create_character_select_menu()
            menus["options"] = self.create_options_menu()
            menus["inventory"] = self.create_inventory_menu()
            menus["save"] = self.create_save_menu()
            self.logger.info(
                "Todos los menús creados exitosamente: %s menús", len(menus)
            )

        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error("Error creando menús: %s", str(e))

        return menus

    def _show_main_menu_feedback(self, msg: str):
        """
        Muestra feedback en el menú principal (método legacy).

        Args:
            msg: Mensaje a mostrar
        """
        self.menu_creator.show_main_menu_feedback(msg)
