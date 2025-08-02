"""
OptionsDisplayPanel - Panel de Configuración de Pantalla
========================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Panel especializado para opciones de pantalla.

Responsabilidades:
- Botón de pantalla completa
- Selector de resolución
- Configuración de display
"""

import pygame
import pygame_gui

from ..utils.logger import get_logger


class OptionsDisplayPanel:
    """
    Panel especializado para configuración de pantalla en opciones.
    """

    def __init__(self, ui_manager, config_manager, screen_width, screen_height):
        """
        Inicializa el panel de pantalla.

        Args:
            ui_manager: Gestor de UI pygame_gui
            config_manager: Gestor de configuración
            screen_width: Ancho de pantalla
            screen_height: Alto de pantalla
        """
        self.ui_manager = ui_manager
        self.config = config_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = get_logger("SiK_Game")

        self._create_display_elements()

    def _create_display_elements(self):
        """Crea elementos de UI para configuración de pantalla."""
        # Sección de video
        self.video_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width // 2 - 80, 320), (160, 30)),
            text="VIDEO",
            manager=self.ui_manager,
        )

        # Botón de pantalla completa
        fullscreen_text = (
            "Pantalla Completa: ON"
            if self.config.get_fullscreen()
            else "Pantalla Completa: OFF"
        )
        self.fullscreen_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width // 2 - 100, 370), (200, 40)),
            text=fullscreen_text,
            manager=self.ui_manager,
        )

    def handle_event(self, event):
        """
        Maneja eventos del panel de pantalla.

        Args:
            event: Evento de pygame

        Returns:
            str: Acción a realizar ("toggle_fullscreen" o None)
        """
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.fullscreen_button:
                # Toggle pantalla completa
                current_fullscreen = self.config.get_fullscreen()
                new_fullscreen = not current_fullscreen
                self.config.set_fullscreen(new_fullscreen)

                # Actualizar texto del botón
                new_text = (
                    "Pantalla Completa: ON"
                    if new_fullscreen
                    else "Pantalla Completa: OFF"
                )
                self.fullscreen_button.set_text(new_text)

                self.logger.info("Pantalla completa cambiada a: %s", new_fullscreen)
                return "toggle_fullscreen"

        return None

    def get_display_elements(self):
        """
        Obtiene lista de elementos UI del panel de pantalla.

        Returns:
            Lista de elementos UI
        """
        return [
            self.video_label,
            self.fullscreen_button,
        ]
