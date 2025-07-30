"""
Config Manager - Fachada unificada del sistema de configuración modular
=======================================================================

Autor: SiK Team
Fecha: 2025
Descripción: Fachada unificada que preserva 100% compatibilidad API mientras
usa módulos especializados (ConfigLoader + ConfigDatabase) por debajo.
Mantiene límite de 150 líneas usando delegación modular.
"""

import logging
from pathlib import Path
from typing import Any, Dict

from .config_loader import ConfigLoader
from .config_database import ConfigDatabase
from .database_manager import DatabaseManager


class ConfigManager:
    """
    Gestor de configuración unificado con soporte híbrido JSON + SQLite.
    Preserva 100% compatibilidad API usando delegación modular.
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

        # Inicializar BD si está disponible (opcional para compatibilidad)
        try:
            self.db_manager = DatabaseManager("saves/game_database.db")
            self.db_config = ConfigDatabase(self.db_manager)
            self.use_database = True
        except (ImportError, OSError, ValueError) as e:
            self.logger.warning("Base de datos no disponible, usando solo JSON: %s", e)
            self.db_config = None
            self.use_database = False

        # Cargar configuración usando módulos
        self.config = self._load_complete_config()

        self.logger.info("ConfigManager inicializado: BD=%s", self.use_database)

    def _load_complete_config(self) -> Dict[str, Any]:
        """Carga configuración completa usando módulos especializados."""
        # Cargar configuración base
        base_config = self.loader.load_default_config()

        # Cargar configuración principal
        main_config = self.loader.load_main_config(self.config_file)

        # Cargar configuraciones específicas
        specific_configs = self.loader.load_specific_configs()

        # Combinar todas las configuraciones
        complete_config = self.loader.merge_configs(base_config, main_config)
        complete_config.update(specific_configs)

        return complete_config

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración con fallback híbrido.
        Intenta BD primero, luego JSON.
        """
        # Intentar desde BD si está disponible
        if self.use_database and self.db_config:
            db_value = self.db_config.get_config_from_db(section, key)
            if db_value is not None:
                return db_value

        # Fallback a configuración JSON en memoria
        try:
            return self.config[section][key]
        except KeyError:
            self.logger.warning("Configuración no encontrada: %s.%s", section, key)
            return default

    def set(self, section: str, key: str, value: Any):
        """Establece un valor de configuración en ambos sistemas."""
        # Actualizar en memoria
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

        # Actualizar en BD si está disponible
        if self.use_database and self.db_config:
            self.db_config.save_config_to_db(section, key, value)

    def get_section(self, section: str) -> Dict[str, Any]:
        """Obtiene una sección completa con fallback híbrido."""
        # Intentar desde BD si está disponible
        if self.use_database and self.db_config:
            db_section = self.db_config.get_section_from_db(section)
            if db_section:
                return db_section

        # Fallback a configuración JSON
        return self.config.get(section, {})

    def save_config(self):
        """Guarda configuración en archivo JSON."""
        return self.loader.save_config_to_file(self.config, self.config_file)

    def reload(self):
        """Recarga la configuración desde archivos."""
        self.config = self._load_complete_config()

    # === MÉTODOS DE COMPATIBILIDAD API ===

    def get_music_volume(self) -> float:
        return self.get("audio", "music_volume", 0.7)

    def get_sfx_volume(self) -> float:
        return self.get("audio", "sfx_volume", 0.8)

    def get_master_volume(self) -> float:
        return self.get("audio", "master_volume", 1.0)

    def get_audio_enabled(self) -> bool:
        return self.get("audio", "enabled", True)

    def get_audio_config(self) -> Dict[str, Any]:
        return self.get_section("audio")

    def get_characters_config(self) -> Dict[str, Any]:
        return self.get_section("characters")

    def get_enemies_config(self) -> Dict[str, Any]:
        return self.get_section("enemies")

    def get_gameplay_config(self) -> Dict[str, Any]:
        return self.get_section("gameplay")

    def get_powerups_config(self) -> Dict[str, Any]:
        return self.get_section("powerups")

    def get_ui_config(self) -> Dict[str, Any]:
        return self.get_section("ui")

    def get_character_data(self, character_name: str) -> Dict[str, Any]:
        characters = self.get_characters_config().get("characters", {})
        return characters.get(character_name, {})

    def get_enemy_data(self, enemy_type: str) -> Dict[str, Any]:
        enemies = self.get_enemies_config()
        return enemies.get("tipos_enemigos", {}).get(enemy_type, {})

    def get_powerup_data(self, powerup_type: str) -> Dict[str, Any]:
        powerups = self.get_powerups_config()
        return powerups.get("tipos_powerups", {}).get(powerup_type, {})

    def get_resolution(self) -> tuple:
        display_config = self.get_section("display")
        resolution = display_config.get("resolución", {})
        return (resolution.get("ancho", 1280), resolution.get("alto", 720))

    def get_fps(self) -> int:
        display_config = self.get_section("display")
        return display_config.get("resolución", {}).get("fps", 60)

    def get_key_binding(self, action: str) -> str:
        input_config = self.get_section("input")
        keyboard = input_config.get("teclado", {})
        for section in ["movimiento", "acciones", "ataques"]:
            if action in keyboard.get(section, {}):
                return keyboard[section][action]
        return ""
