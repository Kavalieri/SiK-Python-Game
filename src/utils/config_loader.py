"""
Config Loader - Carga de configuraciones desde archivos
=======================================================

Autor: SiK Team
Fecha: 2025
Descripción: Módulo especializado en carga de configuraciones desde archivos JSON.
Parte del sistema modular ConfigManager dividido para cumplir límite de 150 líneas.
"""

import json
import logging
from pathlib import Path
from typing import Any


class ConfigLoader:
    """
    Gestor especializado en carga de configuraciones desde archivos JSON.
    """

    def __init__(self):
        """Inicializa el cargador de configuraciones."""
        self.logger = logging.getLogger(__name__)

    def load_default_config(self) -> dict[str, Any]:
        """
        Carga la configuración por defecto.

        Returns:
            Configuración por defecto completa
        """
        return {
            "game": {"title": "SiK Python Game", "version": "0.1.0", "debug": False},
            "display": {
                "width": 1280,
                "height": 720,
                "fps": 60,
                "fullscreen": False,
                "vsync": False,
                "resizable": True,
            },
            "audio": {
                "enabled": True,
                "master_volume": 1.0,
                "music_volume": 0.7,
                "sfx_volume": 0.8,
            },
            "input": {
                "move_up": "w",
                "move_down": "s",
                "move_left": "a",
                "move_right": "d",
                "attack": "space",
                "pause": "escape",
            },
        }

    def load_main_config(self, config_file: Path) -> dict[str, Any]:
        """
        Carga configuración principal desde archivo.

        Args:
            config_file: Ruta al archivo de configuración principal

        Returns:
            Configuración cargada desde archivo o dict vacío si falla
        """
        if not config_file.exists():
            self.logger.info(
                "Archivo %s no existe, usando configuración por defecto", config_file
            )
            return {}

        try:
            with open(config_file, encoding="utf-8") as f:
                config_data = json.load(f)
            self.logger.info("Configuración cargada desde %s", config_file)
            return config_data
        except (json.JSONDecodeError, OSError) as e:
            self.logger.error("Error cargando %s: %s", config_file, e)
            return {}

    def load_specific_configs(self) -> dict[str, dict[str, Any]]:
        """
        Carga configuraciones específicas desde directorio config/.

        Returns:
            Diccionario con configuraciones específicas por categoría
        """
        config_dir = Path("config")
        specific_configs = {}

        config_files = [
            "audio.json",
            "characters.json",
            "display.json",
            "enemies.json",
            "gameplay.json",
            "input.json",
            "loading_screen.json",
            "powerups.json",
            "ui.json",
            "animations.json",
            "save_system.json",
        ]

        for config_file in config_files:
            file_path = config_dir / config_file
            if file_path.exists():
                try:
                    with open(file_path, encoding="utf-8") as f:
                        config_data = json.load(f)

                    # Usar nombre del archivo sin extensión como clave
                    config_key = config_file.replace(".json", "")
                    specific_configs[config_key] = config_data

                    self.logger.debug(
                        "Configuración %s cargada desde %s", config_key, file_path
                    )

                except (json.JSONDecodeError, OSError) as e:
                    self.logger.error("Error cargando %s: %s", file_path, e)
            else:
                self.logger.warning(
                    "Archivo de configuración %s no encontrado", file_path
                )

        self.logger.info(
            "Cargadas %d configuraciones específicas", len(specific_configs)
        )
        return specific_configs

    def save_config_to_file(self, config: dict[str, Any], config_file: Path) -> bool:
        """
        Guarda configuración en archivo JSON.

        Args:
            config: Configuración a guardar
            config_file: Ruta del archivo donde guardar

        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            # Crear directorio si no existe
            config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            self.logger.info("Configuración guardada en %s", config_file)
            return True

        except (OSError, TypeError) as e:
            self.logger.error("Error guardando configuración en %s: %s", config_file, e)
            return False

    def merge_configs(
        self, base_config: dict[str, Any], file_config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Combina configuración base con configuración de archivo.

        Args:
            base_config: Configuración base (por defecto)
            file_config: Configuración desde archivo

        Returns:
            Configuración combinada
        """
        merged = base_config.copy()

        for section, values in file_config.items():
            if (
                section in merged
                and isinstance(merged[section], dict)
                and isinstance(values, dict)
            ):
                # Merge profundo para secciones existentes
                merged[section].update(values)
            else:
                # Sobrescribir sección completa
                merged[section] = values

        return merged
