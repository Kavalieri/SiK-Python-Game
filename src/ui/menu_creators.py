"""
Menu Creators - Lógica de Creación de Menús Específicos
======================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo para creación de menús específicos del juego.
"""

import pygame
import pygame_menu

from ..utils.logger import get_logger
from .menu_configuration import MenuConfiguration
from .menu_theme import MenuTheme


class MenuCreators:
    """
    Creador de menús específicos del juego.
    """

    def __init__(self, screen: pygame.Surface, config_manager, save_manager, callbacks):
        """Inicializa el creador de menús."""
        self.screen = screen
        self.config = config_manager
        self.save_manager = save_manager
        self.callbacks = callbacks
        self.logger = get_logger("SiK_Game")

        # Módulos auxiliares
        self.theme_manager = MenuTheme(screen, config_manager)
        self.config_helper = MenuConfiguration(config_manager, save_manager)

        # Configuración base
        self.screen_width, self.screen_height = self.theme_manager.get_menu_dimensions()
        self.theme = self.theme_manager.create_default_theme()
        self.font_sizes = self.theme_manager.get_font_sizes()

        # Referencias a elementos de feedback
        self._main_menu_feedback_label = None
        self._save_menu_feedback_label = None

    def create_main_menu(self) -> pygame_menu.Menu:
        """Crea el menú principal con flujo avanzado y callbacks diferenciados."""
        menu = pygame_menu.Menu(
            "Menú Principal",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        self._main_menu_feedback_label = menu.add.label(
            "", font_size=self.font_sizes["option"]
        )

        # Botones principales con tamaños de fuente configurables
        buttons = [
            ("Inicio", self.callbacks.on_new_game),
            ("Continuar", self.callbacks.on_continue_game),
            ("Cargar Juego", self.callbacks.on_load_game),
            ("Opciones", self.callbacks.on_options),
            ("Salir", self.callbacks.on_exit),
        ]

        for label, callback in buttons:
            menu.add.button(label, callback, font_size=self.font_sizes["button"])
            menu.add.vertical_margin(10)

        return menu

    def create_pause_menu(self) -> pygame_menu.Menu:
        """Crea el menú de pausa."""
        menu = pygame_menu.Menu(
            "Juego Pausado",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        buttons = [
            ("Reanudar", self.callbacks.on_resume_game),
            ("Guardar", self.callbacks.on_save_game),
            ("Menú Principal", self.callbacks.on_main_menu),
        ]

        for label, callback in buttons:
            menu.add.button(label, callback, font_size=self.font_sizes["button"])
            menu.add.vertical_margin(10)

        return menu

    def create_upgrade_menu(self) -> pygame_menu.Menu:
        """Crea el menú de mejoras."""
        menu = pygame_menu.Menu(
            "Mejoras",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.label(
            "Puntos de Mejora Disponibles:", font_size=self.font_sizes["option"]
        )
        menu.add.vertical_margin(20)

        self.config_helper.add_upgrade_buttons(menu, self._create_upgrade_callback())
        menu.add.vertical_margin(20)
        menu.add.button(
            "Continuar",
            self.callbacks.on_continue_after_upgrade,
            font_size=self.font_sizes["button"],
        )
        return menu

    def create_character_select_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de personaje."""
        menu = pygame_menu.Menu(
            "Selección de Personaje",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.label("Elige tu personaje:", font_size=self.font_sizes["button"])
        menu.add.vertical_margin(20)

        self.config_helper.add_character_buttons(
            menu, self.callbacks.on_select_character
        )
        menu.add.vertical_margin(20)
        menu.add.button(
            "Volver",
            self.callbacks.on_back_to_main,
            font_size=self.font_sizes["option"],
        )
        return menu

    def create_options_menu(self) -> pygame_menu.Menu:
        """Crea el menú de opciones."""
        menu = pygame_menu.Menu(
            "Opciones",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        # Configuración usando helpers
        self.config_helper.configure_resolution_selector(
            menu, self.callbacks.on_resolution_change
        )
        display_settings = self.config_helper.get_display_settings()
        self.config_helper.configure_fullscreen_toggle(
            menu, display_settings["fullscreen"], self.callbacks.on_fullscreen_change
        )

        audio_volumes = self.config_helper.get_audio_volume_values()
        self.config_helper.configure_volume_slider(
            menu,
            "Música",
            audio_volumes["music"],
            self.callbacks.on_music_volume_change,
        )
        self.config_helper.configure_volume_slider(
            menu, "Efectos", audio_volumes["sfx"], self.callbacks.on_sfx_volume_change
        )

        # Botones adicionales compactos
        menu.add.vertical_margin(20)
        buttons = [
            ("Configurar Controles", self.callbacks.on_configure_controls),
            ("Guardar Opciones", self.callbacks.on_save_options),
            ("Volver", self.callbacks.on_back_to_previous),
        ]

        for label, callback in buttons:
            menu.add.button(label, callback, font_size=self.font_sizes["label"])
            menu.add.vertical_margin(10)
        return menu

    def create_inventory_menu(self) -> pygame_menu.Menu:
        """Crea el menú de inventario."""
        menu = pygame_menu.Menu(
            "Inventario",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.label("Equipación:", font_size=self.font_sizes["button"])
        menu.add.vertical_margin(20)

        buttons = [
            ("Equipar Arma", self.callbacks.on_equip_weapon),
            ("Equipar Armadura", self.callbacks.on_equip_armor),
            ("Equipar Accesorio", self.callbacks.on_equip_accessory),
        ]

        for label, callback in buttons:
            menu.add.button(label, callback, font_size=self.font_sizes["option"])
            menu.add.vertical_margin(5)

        menu.add.vertical_margin(20)
        menu.add.button(
            "Volver",
            self.callbacks.on_back_to_previous,
            font_size=self.font_sizes["option"],
        )
        return menu

    def create_save_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de slots de guardado avanzado."""
        menu = pygame_menu.Menu(
            "Gestión de Guardado",
            self.screen_width,
            self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        self._save_menu_feedback_label = menu.add.label(
            "", font_size=self.font_sizes["option"]
        )
        menu.add.label("Archivos de Guardado:", font_size=self.font_sizes["button"])
        menu.add.vertical_margin(20)

        self.config_helper.add_save_slot_buttons(menu, self.callbacks.on_select_slot)
        menu.add.vertical_margin(10)

        buttons = [
            ("Vaciar Slot", lambda: self.callbacks.on_clear_slot(1)),
            ("Volver", self.callbacks.on_back_to_main_from_slots),
        ]

        for label, callback in buttons:
            menu.add.button(label, callback, font_size=self.font_sizes["option"])
            menu.add.vertical_margin(5)
        return menu

    def _create_upgrade_callback(self):
        """Crea callback dinámico para mejoras."""

        def upgrade_callback(upgrade_type: str):
            callbacks_map = {
                "velocidad": self.callbacks.on_upgrade_speed,
                "daño": self.callbacks.on_upgrade_damage,
                "vida": self.callbacks.on_upgrade_health,
                "escudo": self.callbacks.on_upgrade_shield,
            }

            if upgrade_type in callbacks_map:
                callbacks_map[upgrade_type]()
            else:
                self.logger.warning("Tipo de mejora desconocido: %s", upgrade_type)

        return upgrade_callback

    def show_main_menu_feedback(self, message: str) -> None:
        """Muestra mensaje de feedback en el menú principal."""
        self.logger.info("Feedback del menú principal: %s", message)
