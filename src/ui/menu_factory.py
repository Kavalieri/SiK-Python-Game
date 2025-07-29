"""
Menu Factory - Fábrica de Menús
==============================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que crea y configura todos los menús del juego.
"""

import pygame
import pygame_menu
from typing import Dict
from ..utils.config_manager import ConfigManager
from ..utils.save_manager import SaveManager
from .menu_callbacks import MenuCallbacks
from ..utils.logger import get_logger


class MenuFactory:
    """
    Fábrica para crear y configurar menús del juego.
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
        self.theme = self._create_theme()

    def _create_theme(self) -> pygame_menu.themes.Theme:
        """Crea el tema visual para los menús."""
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.background_color = (0, 0, 0, 180)
        theme.title_font_color = (255, 255, 255)
        theme.widget_font_color = (255, 255, 255)
        theme.selection_color = (255, 165, 0)
        return theme

    def create_main_menu(self) -> pygame_menu.Menu:
        """Crea el menú principal con flujo avanzado y callbacks diferenciados."""
        menu = pygame_menu.Menu(
            title="Menú Principal",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )
        self._main_menu_feedback_label = menu.add.label("", font_size=20)
        menu.add.button("Inicio", self.callbacks.on_new_game, font_size=25)
        menu.add.vertical_margin(10)
        menu.add.button("Continuar", self.callbacks.on_continue_game, font_size=25)
        menu.add.vertical_margin(10)
        menu.add.button("Cargar Juego", self.callbacks.on_load_game, font_size=25)
        menu.add.vertical_margin(10)
        menu.add.button("Opciones", self.callbacks.on_options, font_size=25)
        menu.add.vertical_margin(10)
        menu.add.button("Salir", self.callbacks.on_exit, font_size=25)
        return menu

    def create_pause_menu(self) -> pygame_menu.Menu:
        """Crea el menú de pausa."""
        menu = pygame_menu.Menu(
            title="Juego Pausado",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.button("Reanudar", self.callbacks.on_resume_game, font_size=25)
        menu.add.vertical_margin(10)
        menu.add.button("Guardar", self.callbacks.on_save_game, font_size=25)
        menu.add.vertical_margin(10)
        menu.add.button("Menú Principal", self.callbacks.on_main_menu, font_size=25)

        return menu

    def create_upgrade_menu(self) -> pygame_menu.Menu:
        """Crea el menú de mejoras."""
        menu = pygame_menu.Menu(
            title="Mejoras",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.label("Puntos de Mejora Disponibles:", font_size=20)
        menu.add.vertical_margin(20)

        menu.add.button(
            "Mejorar Velocidad (1 punto)", self.callbacks.on_upgrade_speed, font_size=20
        )
        menu.add.vertical_margin(5)
        menu.add.button(
            "Mejorar Daño (1 punto)", self.callbacks.on_upgrade_damage, font_size=20
        )
        menu.add.vertical_margin(5)
        menu.add.button(
            "Mejorar Vida (1 punto)", self.callbacks.on_upgrade_health, font_size=20
        )
        menu.add.vertical_margin(5)
        menu.add.button(
            "Mejorar Escudo (1 punto)", self.callbacks.on_upgrade_shield, font_size=20
        )
        menu.add.vertical_margin(20)

        menu.add.button(
            "Continuar", self.callbacks.on_continue_after_upgrade, font_size=25
        )

        return menu

    def create_character_select_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de personaje."""
        menu = pygame_menu.Menu(
            title="Selección de Personaje",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.label("Elige tu personaje:", font_size=25)
        menu.add.vertical_margin(20)

        menu.add.button(
            "Guerrero",
            lambda: self.callbacks.on_select_character("guerrero"),
            font_size=20,
        )
        menu.add.vertical_margin(5)
        menu.add.button(
            "Arquera",
            lambda: self.callbacks.on_select_character("adventureguirl"),
            font_size=20,
        )
        menu.add.vertical_margin(5)
        menu.add.button(
            "Robot", lambda: self.callbacks.on_select_character("robot"), font_size=20
        )
        menu.add.vertical_margin(20)

        menu.add.button("Volver", self.callbacks.on_back_to_main, font_size=20)

        return menu

    def create_options_menu(self) -> pygame_menu.Menu:
        """Crea el menú de opciones."""
        menu = pygame_menu.Menu(
            title="Opciones",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        # Resolución
        menu.add.label("Resolución:", font_size=20)
        resolutions = ["800x600", "1024x768", "1280x720", "1920x1080"]
        menu.add.selector(
            "Resolución",
            resolutions,
            onchange=self.callbacks.on_resolution_change,
            font_size=18,
        )
        menu.add.vertical_margin(10)

        # Pantalla completa
        menu.add.toggle_switch(
            "Pantalla Completa",
            self.config.get_fullscreen(),
            onchange=self.callbacks.on_fullscreen_change,
            font_size=18,
        )
        menu.add.vertical_margin(10)

        # Volumen de música
        menu.add.label("Volumen de Música:", font_size=20)
        audio_config = self.config.get_audio_config()
        music_volume = audio_config.get("volúmenes", {}).get("música_fondo", 0.7)
        menu.add.range_slider(
            "Música",
            range_values=(0, 100),
            default=int(music_volume * 100),
            increment=1,
            onchange=lambda value: self.callbacks.on_music_volume_change(value / 100),
            font_size=18,
        )
        menu.add.vertical_margin(10)

        # Volumen de SFX
        menu.add.label("Volumen de Efectos:", font_size=20)
        sfx_volume = audio_config.get("volúmenes", {}).get("efectos_sonido", 0.8)
        menu.add.range_slider(
            "SFX",
            range_values=(0, 100),
            default=int(sfx_volume * 100),
            increment=1,
            onchange=lambda value: self.callbacks.on_sfx_volume_change(value / 100),
            font_size=18,
        )
        menu.add.vertical_margin(20)

        menu.add.button(
            "Configurar Controles", self.callbacks.on_configure_controls, font_size=18
        )
        menu.add.vertical_margin(10)
        menu.add.button(
            "Guardar Opciones", self.callbacks.on_save_options, font_size=18
        )
        menu.add.vertical_margin(10)
        menu.add.button("Volver", self.callbacks.on_back_to_previous, font_size=20)

        return menu

    def create_inventory_menu(self) -> pygame_menu.Menu:
        """Crea el menú de inventario."""
        menu = pygame_menu.Menu(
            title="Inventario",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )

        menu.add.label("Equipación:", font_size=25)
        menu.add.vertical_margin(20)

        menu.add.button("Equipar Arma", self.callbacks.on_equip_weapon, font_size=20)
        menu.add.vertical_margin(5)
        menu.add.button("Equipar Armadura", self.callbacks.on_equip_armor, font_size=20)
        menu.add.vertical_margin(5)
        menu.add.button(
            "Equipar Accesorio", self.callbacks.on_equip_accessory, font_size=20
        )
        menu.add.vertical_margin(20)

        menu.add.button("Volver", self.callbacks.on_back_to_previous, font_size=20)

        return menu

    def create_save_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de slots de guardado avanzado."""
        menu = pygame_menu.Menu(
            title="Gestión de Guardado",
            width=self.screen_width,
            height=self.screen_height,
            theme=self.theme,
            enabled=False,
        )
        menu._feedback_label = menu.add.label("", font_size=20)
        menu.add.label("Archivos de Guardado:", font_size=25)
        menu.add.vertical_margin(20)
        # Mostrar detalles de cada slot
        save_infos = self.save_manager.get_save_files_info()
        for i, info in enumerate(save_infos, 1):
            if info["exists"]:
                label = f"Slot {i} | {info.get('player_name', 'Sin nombre')} | Nivel: {info.get('level', 1)} | Puntos: {info.get('score', 0)} | Última vez: {info.get('last_used', 'N/A')}"
            else:
                label = f"Slot {i} | VACÍO"
            menu.add.button(
                label, lambda slot=i: self.callbacks.on_select_slot(slot), font_size=20
            )
            menu.add.vertical_margin(5)
        menu.add.vertical_margin(10)
        menu.add.button(
            "Vaciar Slot", lambda: self.callbacks.on_clear_slot(1), font_size=20
        )  # Ejemplo para slot 1
        menu.add.vertical_margin(5)
        menu.add.button(
            "Volver", self.callbacks.on_back_to_main_from_slots, font_size=20
        )
        return menu

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
            menus["inventory"] = self.create_inventory_menu()
            menus["save"] = self.create_save_menu()
            self.logger.info(
                f"Todos los menús creados exitosamente: {len(menus)} menús"
            )

        except Exception as e:
            self.logger.error(f"Error creando menús: {e}")

        return menus

    def _show_main_menu_feedback(self, msg: str):
        if hasattr(self, "_main_menu_feedback_label"):
            self._main_menu_feedback_label.set_title(msg)
