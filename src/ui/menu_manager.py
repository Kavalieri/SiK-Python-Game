"""
Menu Manager - Gestor de Menús
=============================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Gestor principal de menús que coordina la fábrica y callbacks.
"""

from collections.abc import Callable

import pygame
import pygame_menu

from core.game_state import GameState
from utils.config_manager import ConfigManager
from utils.logger import get_logger
from utils.save_manager import SaveManager

from .menu_callbacks import MenuCallbacks
from .menu_factory import MenuFactory


class MenuManager:
    """
    Gestor principal de menús del juego.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        config: ConfigManager,
        game_state: GameState,
        save_manager: SaveManager,
    ):
        """
        Inicializa el gestor de menús.

        Args:
            screen: Superficie de Pygame donde renderizar
            config: Configuración del juego
            game_state: Estado del juego
            save_manager: Gestor de guardado
        """
        self.screen = screen
        self.config = config
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = get_logger("SiK_Game")

        # Inicializar callbacks y fábrica
        self.callbacks = MenuCallbacks(game_state, save_manager)
        self.factory = MenuFactory(screen, config, save_manager, self.callbacks)

        # Menús disponibles
        self.menus: dict[str, pygame_menu.Menu] = {}
        self.current_menu: pygame_menu.Menu | None = None

        # Crear todos los menús
        self._initialize_menus()

        self.logger.info("Gestor de menús inicializado")

    def _initialize_menus(self):
        """Inicializa todos los menús del juego."""
        try:
            self.menus = self.factory.create_all_menus()
            self.logger.debug(f"Menús inicializados: {len(self.menus)} menús")
        except Exception as e:
            self.logger.error(f"Error inicializando menús: {e}")

    def show_menu(self, menu_name: str):
        """
        Muestra un menú específico, asegurando integración con el flujo avanzado y callbacks diferenciados.

        Args:
            menu_name: Nombre del menú a mostrar
        """
        self.logger.info(
            f"[MenuManager] Acción: Solicitud de mostrar menú '{menu_name}' (flujo avanzado)"
        )
        if menu_name not in self.menus:
            self.logger.warning(f"[MenuManager] Menú no encontrado: {menu_name}")
            return
        if self.current_menu:
            self.logger.info(
                f"[MenuManager] Ocultando menú actual antes de mostrar '{menu_name}'"
            )
            self.current_menu.disable()
        self.current_menu = self.menus[menu_name]
        self.current_menu.enable()
        self.logger.info(f"[MenuManager] Mostrando menú: {menu_name}")

    def hide_current_menu(self):
        """Oculta el menú actual."""
        if self.current_menu:
            self.logger.info(
                f"[MenuManager] Ocultando menú actual: {self.current_menu.get_title()}"
            )
            self.current_menu.disable()
            self.current_menu = None
            self.logger.debug("Menú actual oculto")

    def update(self, events: list):
        """
        Actualiza el menú actual.

        Args:
            events: Lista de eventos de Pygame
        """
        if self.current_menu:
            for event in events:
                # Solo registrar eventos importantes, no movimiento del ratón
                if event.type != pygame.MOUSEMOTION:  # pylint: disable=no-member
                    self.logger.debug(
                        "[MenuManager] Evento procesado en menú: %s", event
                    )
            self.current_menu.update(events)
        else:
            self.logger.warning("MenuManager: No hay menú actual para actualizar")

    def render(self):
        """Renderiza el menú actual."""
        if self.current_menu:
            if (
                not hasattr(self, "_last_rendered_menu")
                or self._last_rendered_menu != self.current_menu.get_title()
            ):
                self.logger.info(
                    f"[MenuManager] Menú renderizado: {self.current_menu.get_title()}"
                )
                self._last_rendered_menu = self.current_menu.get_title()
            self.current_menu.draw(self.screen)
        else:
            self.logger.warning("MenuManager: No hay menú actual para renderizar")

    def add_callback(self, callback_name: str, callback: Callable):
        """
        Añade un callback personalizado.

        Args:
            callback_name: Nombre del callback
            callback: Función callback
        """
        setattr(self.callbacks, callback_name, callback)
        self.logger.info(
            f"[MenuManager] Callback personalizado añadido: {callback_name}"
        )

    def update_save_menu(self):
        """Actualiza el menú de guardado con información actual."""
        if "save" in self.menus:
            # TODO: Actualizar información de archivos de guardado
            self.logger.debug("Menú de guardado actualizado")

    def update_upgrade_menu(self, upgrade_points: int):
        """
        Actualiza el menú de mejoras con puntos disponibles.

        Args:
            upgrade_points: Puntos de mejora disponibles
        """
        if "upgrade" in self.menus:
            # TODO: Actualizar información de puntos de mejora
            self.logger.debug(
                f"Menú de mejoras actualizado con {upgrade_points} puntos"
            )

    def get_current_menu(self) -> pygame_menu.Menu | None:
        """
        Obtiene el menú actual.

        Returns:
            Menú actual o None si no hay ninguno activo
        """
        return self.current_menu

    def is_menu_active(self) -> bool:
        """
        Verifica si hay un menú activo.

        Returns:
            True si hay un menú activo
        """
        return self.current_menu is not None

    def get_menu_names(self) -> list:
        """
        Obtiene la lista de nombres de menús disponibles.

        Returns:
            Lista de nombres de menús
        """
        return list(self.menus.keys())

    def refresh_menus(self):
        """Recrea todos los menús (útil después de cambios de configuración)."""
        self.logger.info("Refrescando todos los menús")
        self._initialize_menus()
