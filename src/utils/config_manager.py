"""
Config Manager - Gestor de configuración modular (FACHADA)
=========================================================

Autor: SiK Team
Fecha: 2024
Descripción: Fachada del sistema modular de configuración.
Mantiene API original para compatibilidad con delegación a módulos especializados.
"""

import json
import logging
from pathlib import Path
from typing import Any

from .config_database import ConfigDatabase
from .config_loader import ConfigLoader
from .database_manager import DatabaseManager


class ConfigManager:
    """
    Fachada del sistema de configuración - delega a módulos especializados.
    Mantiene 100% compatibilidad con API original.
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Inicializa el gestor de configuración modular.

        Args:
            config_file: Ruta al archivo de configuración principal
        """
        self.logger = logging.getLogger(__name__)
        self.config_file = Path(config_file)

        # Inicializar módulos especializados
        self.loader = ConfigLoader()
        self.db_manager = DatabaseManager("data/game.db")
        self.database = ConfigDatabase(self.db_manager)

        # Cargar configuración
        self.config = self.loader.load_default_config()
        self._load_main_config()
        self._load_specific_configs()

    def _load_main_config(self):
        """Carga configuración principal delegando a ConfigLoader."""
        try:
            file_config = self.loader.load_main_config(self.config_file)
            if file_config:
                self.config = self.loader.merge_configs(self.config, file_config)
            else:
                self.save_config()
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error al cargar configuración principal: %s", e)

    def _load_specific_configs(self):
        """Carga configuraciones específicas delegando a ConfigLoader."""
        try:
            specific_configs = self.loader.load_specific_configs()
            if specific_configs:
                self.config = self.loader.merge_configs(self.config, specific_configs)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error al cargar configuraciones específicas: %s", e)

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.

        Args:
            section: Sección de configuración
            key: Clave del valor
            default: Valor por defecto

        Returns:
            Valor de configuración o default si no existe
        """
        try:
            return self.config[section][key]
        except KeyError:
            self.logger.warning("Configuración no encontrada: %s.%s", section, key)
            return default

    def set(self, section: str, key: str, value: Any):
        """
        Establece un valor de configuración.

        Args:
            section: Sección de configuración
            key: Clave del valor
            value: Valor a establecer
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = value
        self.logger.debug("Configuración actualizada: %s.%s = %s", section, key, value)

        # Guardar también en base de datos (si el método está disponible)
        if hasattr(self.database, "save_config_to_db"):
            self.database.save_config_to_db(section, key, value)  # type: ignore

    def get_section(self, section: str) -> dict[str, Any]:
        """
        Obtiene una sección completa de configuración.

        Args:
            section: Nombre de la sección

        Returns:
            Sección de configuración
        """
        return self.config.get(section, {})

    def save_config(self):
        """Guarda la configuración actual delegando a ConfigLoader."""
        success = self.loader.save_config_to_file(self.config, self.config_file)
        if success:
            self.logger.info("Configuración guardada exitosamente")
        return success

    def reload_config(self):
        """Recarga la configuración completa."""
        self.config = self.loader.load_default_config()
        self._load_main_config()
        self._load_specific_configs()
        self.logger.info("Configuración recargada")

    # MÉTODOS DE COMPATIBILIDAD - Delegados para preservar API original

    def get_audio_volume(self, key: str, default: float = 0.7) -> float:
        """Obtiene volumen de audio."""
        try:
            return float(self.config["audio"][key])
        except (KeyError, ValueError, TypeError):
            return default

    def get_display_resolution(self) -> tuple:
        """Obtiene resolución de pantalla."""
        try:
            display = self.config["display"]["resolución"]
            return (display["ancho"], display["alto"])
        except (KeyError, TypeError):
            return (1280, 720)

    def get_fps(self) -> int:
        """Obtiene FPS configurado."""
        return self.get("display", "fps", 60)

    def get_ui_font_size(self, key: str, default: int = 24) -> int:
        """Obtiene tamaño de fuente UI."""
        try:
            return int(self.config["ui"]["fuentes"][key])
        except (KeyError, ValueError, TypeError):
            return default

    def get_ui_color(self, key: str, default: tuple = (255, 255, 255)) -> tuple:
        """Obtiene color de UI."""
        try:
            color = self.config["ui"]["colores"][key]
            if isinstance(color, list) and len(color) >= 3:
                return tuple(color[:3])
            return default
        except (KeyError, TypeError):
            return default

    def get_fullscreen(self) -> bool:
        """Obtiene configuración de pantalla completa."""
        try:
            return bool(self.config["display"]["pantalla_completa"])
        except (KeyError, TypeError):
            return False

    def get_audio_config(self) -> dict[str, Any]:
        """Obtiene configuración completa de audio."""
        return self.get_section("audio")

    def get_ui_dimension(self, key: str, default: int = 0) -> int:
        """Obtiene dimensión de UI."""
        try:
            return int(self.config["ui"]["dimensiones"][key])
        except (KeyError, ValueError, TypeError):
            return default

    def get_width(self) -> int:
        """Obtiene ancho de pantalla."""
        resolution = self.get_resolution()
        return resolution[0]

    def get_height(self) -> int:
        """Obtiene alto de pantalla."""
        resolution = self.get_resolution()
        return resolution[1]

    def get_display_config(self) -> dict[str, Any]:
        """Obtiene configuración completa de display."""
        return self.get_section("display")

    def get_input_config(self) -> dict[str, Any]:
        """Obtiene configuración completa de input."""
        return self.get_section("input")

    def get_resolution(self) -> tuple:
        """Obtiene resolución actual."""
        display_config = self.get_display_config()
        resolution = display_config.get("resolución", {})
        return (resolution.get("ancho", 1280), resolution.get("alto", 720))

    def get_key_binding(self, action: str) -> str:
        """Obtiene tecla asignada a una acción."""
        input_config = self.get_input_config()
        keyboard = input_config.get("teclado", {})

        # Buscar en diferentes secciones
        for section in ["movimiento", "acciones", "ataques"]:
            if action in keyboard.get(section, {}):
                return keyboard[section][action]

        return ""
