"""
Schema Migrations - Sistema de migraciones SQLite

Gestiona migraciones de esquema, validación de integridad y registro de cambios.
Fase 1 de migración SQLite - Referencia: docs/PLAN_MIGRACION_SQLITE.md
"""

import hashlib
import logging
from typing import Any, Dict, Optional

from .database_manager import DatabaseManager


class SchemaMigrations:
    """Gestor de migraciones y validaciones de esquema SQLite."""

    def __init__(self, database_manager: DatabaseManager):
        self.db_manager = database_manager
        self._logger = logging.getLogger("SchemaMigrations")

    def record_migration(
        self, description: str, operation: str, schema_version: str = "1.0.0"
    ) -> None:
        """Registra una migración en la tabla de metadatos."""
        checksum = self._calculate_schema_checksum()
        query = "INSERT INTO schema_metadata (version, description, checksum) VALUES (?, ?, ?)"

        try:
            self.db_manager.execute_query(
                query, (schema_version, f"{operation}: {description}", checksum)
            )
            self._logger.info("Migración registrada: %s", description)
        except (ValueError, RuntimeError) as e:
            self._logger.error("Error registrando migración: %s", e)
            raise

    def validate_schema(self, required_tables: list) -> Dict[str, Any]:
        """Valida la integridad del esquema actual."""
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "tables_found": [],
            "missing_tables": [],
        }

        try:
            # Obtener tablas existentes
            existing_tables = self.db_manager.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'",
                fetch_results=True,
            )

            if existing_tables:
                result["tables_found"] = [table["name"] for table in existing_tables]

            # Verificar tablas requeridas
            missing_tables = set(required_tables) - set(result["tables_found"])
            if missing_tables:
                result["missing_tables"] = list(missing_tables)
                result["valid"] = False
                result["errors"].append(
                    f"Tablas faltantes: {', '.join(missing_tables)}"
                )

            # Validar integridad referencial
            integrity_result = self.db_manager.execute_query(
                "PRAGMA integrity_check", fetch_results=True
            )
            if integrity_result and len(integrity_result) > 0:
                first_result = integrity_result[0]
                if (
                    isinstance(first_result, dict)
                    and first_result.get("integrity_check") != "ok"
                ):
                    result["valid"] = False
                    result["errors"].append("Falla en integrity_check de SQLite")

        except (ValueError, RuntimeError) as e:
            result["valid"] = False
            result["errors"].append(f"Error durante validación: {e}")
            self._logger.error("Error validando esquema: %s", e)

        return result

    def get_schema_version(self) -> Optional[str]:
        """Obtiene la versión actual del esquema."""
        try:
            query_result = self.db_manager.execute_query(
                "SELECT version FROM schema_metadata ORDER BY id DESC LIMIT 1"
            )
            if isinstance(query_result, dict):
                return query_result.get("version")
            return None
        except (ValueError, RuntimeError) as e:
            self._logger.warning("No se pudo obtener versión del esquema: %s", e)
            return None

    def get_migration_history(self) -> list:
        """Obtiene el historial de migraciones aplicadas."""
        try:
            result = self.db_manager.execute_query(
                "SELECT * FROM schema_metadata ORDER BY id ASC", fetch_results=True
            )
            return result if isinstance(result, list) else []
        except (ValueError, RuntimeError) as e:
            self._logger.warning("Error obteniendo historial: %s", e)
            return []

    def _calculate_schema_checksum(self) -> str:
        """Calcula un checksum del esquema actual."""
        try:
            # Obtener todas las tablas y sus esquemas
            tables_query = """
            SELECT name, sql FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
            tables = self.db_manager.execute_query(tables_query, fetch_results=True)

            # Crear string único del esquema
            schema_string = ""
            if tables:
                for table in tables:
                    schema_string += f"{table.get('name', '')}:{table.get('sql', '')}\n"

            # Calcular checksum MD5
            return hashlib.md5(schema_string.encode()).hexdigest()

        except (ValueError, RuntimeError) as e:
            self._logger.warning("Error calculando checksum: %s", e)
            return "unknown_checksum"

    def backup_schema(self, backup_path: str) -> bool:
        """Crea un backup del esquema actual."""
        try:
            # Implementación simplificada - obtener DDL de todas las tablas
            ddl_query = """
            SELECT sql FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """
            ddl_statements = self.db_manager.execute_query(
                ddl_query, fetch_results=True
            )

            with open(backup_path, "w", encoding="utf-8") as f:
                f.write("-- Schema backup\n")
                if ddl_statements:
                    for statement in ddl_statements:
                        f.write(f"{statement.get('sql', '')};\n")

            self._logger.info("Backup creado: %s", backup_path)
            return True

        except (ValueError, RuntimeError, IOError) as e:
            self._logger.error("Error creando backup: %s", e)
            return False

    def rollback_migration(self, target_version: str) -> bool:
        """Rollback a una versión específica (implementación básica)."""
        try:
            # Implementación simplificada - solo registro
            self._logger.warning("Rollback solicitado a versión: %s", target_version)
            self._logger.warning(
                "Implementación de rollback pendiente de desarrollo completo"
            )
            return False
        except (ValueError, RuntimeError) as e:
            self._logger.error("Error en rollback: %s", e)
            return False
