"""
Config Database - Operaciones SQLite para configuraciones
=========================================================

Autor: SiK Team
Fecha: 2025
Descripción: Módulo especializado en operaciones SQLite para configuraciones.
Parte del sistema modular ConfigManager dividido para cumplir límite de 150 líneas.
Maneja migración desde JSON a SQLite.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict

from .database_manager import DatabaseManager


class ConfigDatabase:
    """
    Gestor de configuraciones en base de datos SQLite.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa el gestor de configuraciones en BD.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.logger = logging.getLogger(__name__)
        self.db_manager = database_manager

    def save_config_to_db(
        self, section: str, key: str, value: Any, config_type: str = "object"
    ) -> bool:
        """Guarda una configuración específica en la base de datos."""
        try:
            # Serializar valor si es objeto complejo
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, ensure_ascii=False)
                config_type = "object"
            else:
                serialized_value = str(value)

            query = """
                INSERT INTO configuraciones (categoria, clave, valor, tipo)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(categoria, clave)
                DO UPDATE SET valor = ?, tipo = ?, actualizado_en = CURRENT_TIMESTAMP
            """

            success = self.db_manager.execute_query(
                query,
                (
                    section,
                    key,
                    serialized_value,
                    config_type,
                    serialized_value,
                    config_type,
                ),
            )

            if success is not None:
                self.logger.debug("Configuración %s.%s guardada en BD", section, key)
                return True
            else:
                self.logger.error(
                    "Error guardando configuración %s.%s en BD", section, key
                )
                return False

        except (TypeError, ValueError) as e:
            self.logger.error(
                "Error serializando configuración %s.%s: %s", section, key, e
            )
            return False

    def get_config_from_db(self, section: str, key: str, default: Any = None) -> Any:
        """Obtiene una configuración específica desde la base de datos."""
        try:
            query = "SELECT valor, tipo FROM configuraciones WHERE categoria = ? AND clave = ?"
            result = self.db_manager.execute_query(
                query, (section, key), fetch_results=True
            )

            if not result:
                return default

            value_str, config_type = result[0]
            return self._deserialize_value(value_str, config_type, default)

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            self.logger.error(
                "Error obteniendo configuración %s.%s desde BD: %s", section, key, e
            )
            return default

    def _deserialize_value(
        self, value_str: str, config_type: str, default: Any = None
    ) -> Any:
        """Deserializa valor según su tipo."""
        try:
            if config_type == "object":
                return json.loads(value_str)
            elif config_type == "boolean":
                return value_str.lower() in ("true", "1", "yes")
            elif config_type == "number":
                return int(value_str) if value_str.isdigit() else float(value_str)
            else:
                return value_str
        except (json.JSONDecodeError, ValueError):
            return default

    def get_section_from_db(self, section: str) -> Dict[str, Any]:
        """Obtiene una sección completa de configuración desde BD."""
        try:
            query = "SELECT clave, valor, tipo FROM configuraciones WHERE categoria = ?"
            results = self.db_manager.execute_query(
                query, (section,), fetch_results=True
            )

            if not results:
                return {}

            section_config = {}
            for clave, valor_str, config_type in results:
                section_config[clave] = self._deserialize_value(valor_str, config_type)

            return section_config

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            self.logger.error("Error obteniendo sección %s desde BD: %s", section, e)
            return {}

    def migrate_json_to_db(self, json_configs: Dict[str, Dict[str, Any]]) -> bool:
        """Migra configuraciones desde formato JSON a base de datos SQLite."""
        try:
            migrated_count = 0
            for section, section_config in json_configs.items():
                for key, value in section_config.items():
                    if self.save_config_to_db(section, key, value):
                        migrated_count += 1

            self.logger.info(
                "Migración JSON→SQLite completada: %d configuraciones", migrated_count
            )
            return True

        except (TypeError, ValueError) as e:
            self.logger.error("Error durante migración JSON→SQLite: %s", e)
            return False

    def backup_db_to_json(self, backup_path: Path) -> bool:
        """Crea backup de configuraciones BD a archivo JSON."""
        try:
            query = "SELECT categoria, clave, valor, tipo FROM configuraciones ORDER BY categoria, clave"
            results = self.db_manager.execute_query(query, fetch_results=True)

            if not results:
                self.logger.warning("No hay configuraciones en BD para hacer backup")
                return False

            backup_data = {}
            for categoria, clave, valor_str, config_type in results:
                if categoria not in backup_data:
                    backup_data[categoria] = {}
                backup_data[categoria][clave] = self._deserialize_value(
                    valor_str, config_type
                )

            # Guardar backup
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False)

            self.logger.info("Backup de configuraciones guardado en %s", backup_path)
            return True

        except (OSError, json.JSONDecodeError, ValueError) as e:
            self.logger.error("Error creando backup de configuraciones: %s", e)
            return False
