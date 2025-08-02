"""
Menu Configuration - Configuración de Widgets y Opciones (Refactorizada)
=========================================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Interfaz principal para configuración de menús.
REFACTORIZADA: Ahora orquesta clases especializadas para mejor mantenibilidad.

Responsabilidades:
- Orquestar configuradores especializados
- Mantener compatibilidad de API
- Delegar a módulos especializados
"""

from collections.abc import Callable
from typing import Any

import pygame_menu

from ..utils.logger import get_logger
from .menu_game_config import MenuGameConfig
from .menu_save_slot_manager import MenuSaveSlotManager
from .menu_widget_config import MenuWidgetConfig


class MenuConfiguration:
    """
    Gestor principal de configuración de widgets y opciones para menús.
    Orquesta las clases especializadas para mejor organización.
    """

    def __init__(self, config_manager=None, save_manager=None, game_state=None):
        """
        Inicializa configuración de menús.

        Args:
            config_manager: Gestor de configuración del juego
            save_manager: Gestor de guardado
            game_state: Estado del juego
        """
        self.config = config_manager
        self.save_manager = save_manager
        self.game_state = game_state
        self.logger = get_logger("SiK_Game")

        # Inicializar módulos especializados
        self.widgets = MenuWidgetConfig(config_manager)
        self.game_config = MenuGameConfig()
        self.save_slots = MenuSaveSlotManager(save_manager, game_state)

    # === MÉTODOS DELEGADOS PARA COMPATIBILIDAD ===
    # Mantiene la API original para no romper el código existente

    def get_resolution_options(self) -> list[str]:
        """Delega a MenuWidgetConfig. Mantiene compatibilidad de API."""
        return self.widgets.get_resolution_options()

    def get_character_options(self) -> list[dict[str, str]]:
        """Delega a MenuGameConfig. Mantiene compatibilidad de API."""
        return self.game_config.get_character_options()

    def get_upgrade_options(self) -> list[dict[str, Any]]:
        """Delega a MenuGameConfig. Mantiene compatibilidad de API."""
        return self.game_config.get_upgrade_options()

    def get_inventory_categories(self) -> list[str]:
        """Delega a MenuGameConfig. Mantiene compatibilidad de API."""
        return self.game_config.get_inventory_categories()

    def configure_volume_slider(
        self,
        menu: pygame_menu.Menu,
        label: str,
        default_value: float,
        callback: Callable[[float], None],
    ) -> None:
        """Delega a MenuWidgetConfig. Mantiene compatibilidad de API."""
        self.widgets.configure_volume_slider(menu, label, default_value, callback)

    def configure_resolution_selector(
        self, menu: pygame_menu.Menu, callback: Callable[[str, int], None]
    ) -> None:
        """Delega a MenuWidgetConfig. Mantiene compatibilidad de API."""
        self.widgets.configure_resolution_selector(menu, callback)

    def configure_fullscreen_toggle(
        self,
        menu: pygame_menu.Menu,
        default_value: bool,
        callback: Callable[[bool], None],
    ) -> None:
        """Delega a MenuWidgetConfig. Mantiene compatibilidad de API."""
        self.widgets.configure_fullscreen_toggle(menu, default_value, callback)

    def add_character_buttons(
        self, menu: pygame_menu.Menu, callback: Callable[[str], None]
    ) -> None:
        """Delega a MenuGameConfig. Mantiene compatibilidad de API."""
        self.game_config.add_character_buttons(menu, callback)

    def add_upgrade_buttons(
        self, menu: pygame_menu.Menu, callback: Callable[[str], None]
    ) -> None:
        """Delega a MenuGameConfig. Mantiene compatibilidad de API."""
        self.game_config.add_upgrade_buttons(menu, callback)

    def add_save_slot_buttons(
        self, menu: pygame_menu.Menu, callback: Callable[[int], None]
    ) -> None:
        """Delega a MenuSaveSlotManager. Mantiene compatibilidad de API."""
        self.save_slots.add_save_slot_buttons(menu, callback)

    def get_audio_volume_values(self) -> dict[str, float]:
        """Delega a MenuWidgetConfig. Mantiene compatibilidad de API."""
        return self.widgets.get_audio_volume_values()

    def get_display_settings(self) -> dict[str, Any]:
        """Delega a MenuWidgetConfig. Mantiene compatibilidad de API."""
        return self.widgets.get_display_settings()

    def add_slot_management_buttons(self, menu, callbacks) -> None:
        """Delega a MenuSaveSlotManager. Mantiene compatibilidad de API."""
        self.save_slots.add_slot_management_buttons(menu, callbacks)

    def add_start_game_slot_buttons(self, menu, callbacks) -> None:
        """Delega a MenuSaveSlotManager. Mantiene compatibilidad de API."""
        self.save_slots.add_start_game_slot_buttons(menu, callbacks)
