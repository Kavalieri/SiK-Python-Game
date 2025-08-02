"""
OptionsAudioPanel - Panel de Configuración de Audio
===================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Panel especializado para opciones de audio.

Responsabilidades:
- Slider de volumen maestro
- Slider de efectos de sonido
- Configuración de audio
"""

import pygame
import pygame_gui

from ..utils.logger import get_logger


class OptionsAudioPanel:
    """
    Panel especializado para configuración de audio en opciones.
    """

    def __init__(self, ui_manager, config_manager, screen_width, screen_height):
        """
        Inicializa el panel de audio.

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

        self._create_audio_elements()

    def _create_audio_elements(self):
        """Crea elementos de UI para configuración de audio."""
        # Sección de audio
        self.audio_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width // 2 - 80, 150), (160, 30)),
            text="AUDIO",
            manager=self.ui_manager,
        )

        # Slider de volumen maestro
        self.volumen_maestro_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width // 2 - 200, 200), (150, 30)),
            text="Volumen Maestro:",
            manager=self.ui_manager,
        )

        self.volumen_maestro_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.screen_width // 2 - 40, 200), (200, 30)),
            start_value=int(self.config.get("audio", "master_volume", 0.8) * 100),
            value_range=(0, 100),
            manager=self.ui_manager,
        )

        # Slider de efectos de sonido
        self.volumen_sfx_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen_width // 2 - 200, 250), (150, 30)),
            text="Efectos de Sonido:",
            manager=self.ui_manager,
        )

        self.volumen_sfx_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.screen_width // 2 - 40, 250), (200, 30)),
            start_value=int(self.config.get("audio", "sfx_volume", 0.7) * 100),
            value_range=(0, 100),
            manager=self.ui_manager,
        )

    def handle_event(self, event):
        """
        Maneja eventos del panel de audio.

        Args:
            event: Evento de pygame
        """
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.volumen_maestro_slider:
                new_value = event.value / 100.0
                self.config.set("audio", "master_volume", new_value)
                self.logger.debug("Volumen maestro cambiado a: %s", new_value)

            elif event.ui_element == self.volumen_sfx_slider:
                new_value = event.value / 100.0
                self.config.set("audio", "sfx_volume", new_value)
                self.logger.debug("Volumen SFX cambiado a: %s", new_value)

    def get_audio_elements(self):
        """
        Obtiene lista de elementos UI del panel de audio.

        Returns:
            Lista de elementos UI
        """
        return [
            self.audio_label,
            self.volumen_maestro_label,
            self.volumen_maestro_slider,
            self.volumen_sfx_label,
            self.volumen_sfx_slider,
        ]
