"""
Config Manager - Gestor de configuración
=======================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona la configuración del juego desde archivos y valores por defecto.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """
    Gestiona la configuración del juego.
    """

    def __init__(self, config_file: str = "config.json"):
        """
        Inicializa el gestor de configuración.

        Args:
                config_file: Ruta al archivo de configuración principal
        """
        self.logger = logging.getLogger(__name__)
        self.config_file = Path(config_file)
        self.config = self._load_default_config()

        self.logger.info("Cargando configuración...")
        self._load_config()
        self._load_specific_configs()
        self.logger.info("Configuración cargada correctamente")

    def _load_default_config(self) -> Dict[str, Any]:
        """
        Carga la configuración por defecto.

        Returns:
                Configuración por defecto
        """
        return {
            "game": {"title": "SiK Python Game", "version": "0.1.0", "debug": False},
            "display": {
                "width": 1280,
                "height": 720,
                "fps": 60,
                "fullscreen": False,
                "vsync": True,
            },
            "audio": {
                "master_volume": 1.0,
                "music_volume": 0.7,
                "sfx_volume": 0.8,
                "enabled": True,
            },
            "input": {
                "keyboard_enabled": True,
                "gamepad_enabled": True,
                "mouse_enabled": True,
            },
            "paths": {"assets": "assets", "saves": "saves", "logs": "logs"},
        }

    def _load_config(self):
        """Carga la configuración principal desde archivo."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    self._merge_config(file_config)
                    self.logger.info(
                        f"Configuración principal cargada desde: {self.config_file}"
                    )
            else:
                self.logger.warning(
                    f"Archivo de configuración no encontrado: {self.config_file}"
                )
                self.save_config()

        except Exception as e:
            self.logger.error(f"Error al cargar configuración principal: {e}")

    def _load_specific_configs(self):
        """Carga las configuraciones específicas desde el directorio config/."""
        try:
            config_dir = Path("config")
            if not config_dir.exists():
                self.logger.warning(
                    f"Directorio de configuración no encontrado: {config_dir}"
                )
                return

            # Archivos de configuración específicos
            config_files = {
                "audio": "audio.json",
                "characters": "characters.json",
                "enemies": "enemies.json",
                "gameplay": "gameplay.json",
                "powerups": "powerups.json",
                "ui": "ui.json",
                "display": "display.json",
                "input": "input.json",
            }

            for section, filename in config_files.items():
                file_path = config_dir / filename
                if file_path.exists():
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_config = json.load(f)
                            self.config[section] = file_config
                            self.logger.info(
                                f"Configuración {section} cargada desde: {file_path}"
                            )
                    except Exception as e:
                        self.logger.error(
                            f"Error al cargar configuración {section}: {e}"
                        )
                else:
                    self.logger.warning(
                        f"Archivo de configuración no encontrado: {file_path}"
                    )

        except Exception as e:
            self.logger.error(f"Error al cargar configuraciones específicas: {e}")

    def _merge_config(self, file_config: Dict[str, Any]):
        """
        Combina la configuración del archivo con la por defecto.

        Args:
                file_config: Configuración del archivo
        """
        for section, values in file_config.items():
            if section in self.config:
                if isinstance(values, dict):
                    self.config[section].update(values)
                else:
                    self.config[section] = values
            else:
                self.config[section] = values

    def save_config(self):
        """Guarda la configuración actual en archivo."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Configuración guardada en: {self.config_file}")

        except Exception as e:
            self.logger.error(f"Error al guardar configuración: {e}")

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.

        Args:
                section: Sección de configuración
                key: Clave del valor
                default: Valor por defecto si no existe

        Returns:
                Valor de configuración
        """
        try:
            return self.config[section][key]
        except KeyError:
            self.logger.warning(f"Configuración no encontrada: {section}.{key}")
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
        self.logger.debug(f"Configuración actualizada: {section}.{key} = {value}")

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Obtiene una sección completa de configuración.

        Args:
                section: Nombre de la sección

        Returns:
                Sección de configuración
        """
        return self.config.get(section, {})

    def reload(self):
        """Recarga la configuración desde archivo."""
        self.logger.info("Recargando configuración...")
        self._load_config()

    def get_music_volume(self) -> float:
        """Obtiene el volumen de música."""
        return self.get("audio", "music_volume", 0.7)

    def get_sfx_volume(self) -> float:
        """Obtiene el volumen de efectos de sonido."""
        return self.get("audio", "sfx_volume", 0.8)

    def get_master_volume(self) -> float:
        """Obtiene el volumen maestro."""
        return self.get("audio", "master_volume", 1.0)

    def get_audio_enabled(self) -> bool:
        """Obtiene si el audio está habilitado."""
        return self.get("audio", "enabled", True)

    # Métodos para configuraciones específicas
    def get_audio_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de audio."""
        return self.config.get("audio", {})

    def get_characters_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de personajes."""
        return self.config.get("characters", {})

    def get_enemies_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de enemigos."""
        return self.config.get("enemies", {})

    def get_gameplay_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de gameplay."""
        return self.config.get("gameplay", {})

    def get_powerups_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de powerups."""
        return self.config.get("powerups", {})

    def get_ui_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de UI."""
        return self.config.get("ui", {})

    # Métodos específicos para valores comunes
    def get_character_data(self, character_name: str) -> Dict[str, Any]:
        """
        Devuelve la configuración completa de un personaje, incluyendo ataques.
        """
        characters = self.get_characters_config().get("characters", {})
        return characters.get(character_name, {})

    def get_enemy_data(self, enemy_type: str) -> Dict[str, Any]:
        """Obtiene los datos de un enemigo específico."""
        enemies = self.get_enemies_config()
        return enemies.get("tipos_enemigos", {}).get(enemy_type, {})

    def get_powerup_data(self, powerup_type: str) -> Dict[str, Any]:
        """Obtiene los datos de un powerup específico."""
        powerups = self.get_powerups_config()
        return powerups.get("tipos_powerups", {}).get(powerup_type, {})

    def get_ui_dimension(self, key: str, default: int = 0) -> int:
        try:
            return int(self.config["ui"]["dimensiones"][key])
        except Exception:
            self.logger.warning(f"Dimensión UI no encontrada: {key}")
            return default

    def get_ui_color(self, key: str, default=(255, 255, 255)) -> tuple:
        try:
            return tuple(self.config["ui"]["colores"][key])
        except Exception:
            self.logger.warning(f"Color UI no encontrado: {key}")
            return default

    def get_ui_font_size(self, key: str, default: int = 24) -> int:
        try:
            return int(self.config["ui"]["fuentes"][key])
        except Exception:
            self.logger.warning(f"Tamaño de fuente UI no encontrado: {key}")
            return default

    def get_display_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de display."""
        return self.config.get("display", {})

    def get_input_config(self) -> Dict[str, Any]:
        """Obtiene la configuración completa de input."""
        return self.config.get("input", {})

    def get_resolution(self) -> tuple:
        """Obtiene la resolución actual."""
        display_config = self.get_display_config()
        resolution = display_config.get("resolución", {})
        return (resolution.get("ancho", 1280), resolution.get("alto", 720))

    def get_fps(self) -> int:
        """Obtiene el FPS configurado."""
        display_config = self.get_display_config()
        return display_config.get("resolución", {}).get("fps", 60)

    def get_key_binding(self, action: str) -> str:
        """Obtiene la tecla asignada a una acción."""
        input_config = self.get_input_config()
        keyboard = input_config.get("teclado", {})

        # Buscar en diferentes secciones
        for section in ["movimiento", "acciones", "ataques"]:
            if action in keyboard.get(section, {}):
                return keyboard[section][action]

        return ""
