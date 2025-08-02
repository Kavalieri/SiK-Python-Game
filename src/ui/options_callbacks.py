"""
Callbacks de opciones y configuración.
Módulo especializado extraído de MenuCallbacks para mantener límite de 150 líneas.
"""

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.game_state import GameState
    from utils.save_manager import SaveManager

logger = logging.getLogger(__name__)


class OptionsCallbacks:
    """
    Gestiona los callbacks de opciones y configuración del juego.
    """

    def __init__(self, game_state: "GameState", save_manager: "SaveManager"):
        """
        Inicializa el gestor de callbacks de opciones.

        Args:
            game_state: Estado del juego
            save_manager: Gestor de archivos de guardado
        """
        self.game_state = game_state
        self.save_manager = save_manager
        self.logger = logger

    def on_resolution_change(self, _value: Any, resolution: str):
        """Callback para cambiar resolución."""
        try:
            self.logger.info("Cambiando resolución a: %s", resolution)
            width, height = map(int, resolution.split("x"))

            # Usar config desde save_manager
            if hasattr(self.save_manager, "config"):
                self.save_manager.config.set("display", "width", width)
                self.save_manager.config.set("display", "height", height)
                self.save_manager.config.save_config()
                self.logger.info("Resolución cambiada a %dx%d", width, height)
            else:
                self.logger.warning("ConfigManager no disponible en save_manager")

        except (ValueError, AttributeError, TypeError) as e:
            self.logger.error("Error cambiando resolución: %s", str(e))

    def on_fullscreen_change(self, value: bool):
        """Callback para cambiar modo pantalla completa."""
        try:
            self.logger.info("Cambiando modo pantalla completa: %s", value)

            # Usar config desde save_manager
            if hasattr(self.save_manager, "config"):
                self.save_manager.config.set("display", "fullscreen", value)
                self.save_manager.config.save_config()
                self.logger.info("Modo pantalla completa: %s", value)
            else:
                self.logger.warning("ConfigManager no disponible en save_manager")

        except (AttributeError, TypeError) as e:
            self.logger.error("Error cambiando modo pantalla completa: %s", str(e))

    def on_music_volume_change(self, value: float):
        """Callback para cambiar volumen de música."""
        try:
            self.logger.info("Cambiando volumen de música: %s", value)

            # Usar config desde save_manager
            if hasattr(self.save_manager, "config"):
                self.save_manager.config.set("audio", "music_volume", value)
                self.save_manager.config.save_config()
                self.logger.info("Volumen de música: %s", value)
            else:
                self.logger.warning("ConfigManager no disponible en save_manager")

        except (AttributeError, TypeError, ValueError) as e:
            self.logger.error("Error cambiando volumen de música: %s", str(e))

    def on_sfx_volume_change(self, value: float):
        """Callback para cambiar volumen de efectos de sonido."""
        try:
            self.logger.info("Cambiando volumen de SFX: %s", value)

            # Usar config desde save_manager
            if hasattr(self.save_manager, "config"):
                self.save_manager.config.set("audio", "sfx_volume", value)
                self.save_manager.config.save_config()
                self.logger.info("Volumen de SFX: %s", value)
            else:
                self.logger.warning("ConfigManager no disponible en save_manager")

        except (AttributeError, TypeError, ValueError) as e:
            self.logger.error("Error cambiando volumen de SFX: %s", str(e))

    def on_configure_controls(self):
        """Callback para configurar controles."""
        try:
            self.logger.info("Abriendo configuración de controles")
            # FUTURE: Implementar interfaz de configuración de controles
            # Por ahora se registra la acción sin implementación
            self.logger.warning("Configuración de controles no implementada")
        except (AttributeError, OSError) as e:
            self.logger.error("Error configurando controles: %s", str(e))

    def on_save_options(self):
        """Callback para guardar opciones."""
        try:
            self.logger.info("Guardando opciones")

            # Usar config desde save_manager
            if hasattr(self.save_manager, "config"):
                self.save_manager.config.save_config()
                self.logger.info("Opciones guardadas exitosamente")
            else:
                self.logger.warning("ConfigManager no disponible en save_manager")

        except (AttributeError, OSError) as e:
            self.logger.error("Error guardando opciones: %s", str(e))

    def get_options_callbacks(self) -> dict:
        """
        Obtiene todos los callbacks de opciones disponibles.

        Returns:
            Diccionario con callbacks de opciones
        """
        return {
            "resolution_change": self.on_resolution_change,
            "fullscreen_change": self.on_fullscreen_change,
            "music_volume_change": self.on_music_volume_change,
            "sfx_volume_change": self.on_sfx_volume_change,
            "configure_controls": self.on_configure_controls,
            "save_options": self.on_save_options,
        }
