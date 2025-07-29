"""
Schema Migrations - Sistema de migraciones SQLite
=================================================

Módulo para gestionar migraciones de esquema, validación de integridad
y registro de cambios en la base de datos.

Fase 1 de migración SQLite - Sistema de migraciones
Referencia: docs/PLAN_MIGRACION_SQLITE.md - Fase 1
"""

import hashlib
import logging
from typing import Any, Dict, Optional

from .database_manager import DatabaseManager


class SchemaMigrations:
    """
    Gestor de migraciones y validaciones de esquema SQLite.

    Características:
    - Registro de migraciones aplicadas
    - Validación de integridad de esquemas
    - Cálculo de checksums para cambios
    - Rollback de migraciones si es necesario
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa el gestor de migraciones.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self._logger = logging.getLogger("SchemaMigrations")

    def record_migration(
        self, description: str, operation: str, schema_version: str = "1.0.0"
    ) -> None:
        """
        Registra una migración en la tabla de metadatos.

        Args:
            description: Descripción de la migración aplicada
            operation: Tipo de operación (CREATE_TABLE, ALTER_TABLE, etc.)
            schema_version: Versión del esquema aplicada
        """
        checksum = self._calculate_schema_checksum()

        migration_record = """
        INSERT INTO schema_metadata (version, description, checksum)
        VALUES (?, ?, ?)
        """

        try:
            self.db_manager.execute_query(
                migration_record,
                (schema_version, f"{operation}: {description}", checksum),
            )
            self._logger.info("Migración registrada: %s", description)

        except Exception as e:
            self._logger.error("Error registrando migración: %s", e)
            raise

    def validate_schema(self, required_tables: list) -> Dict[str, Any]:
        """
        Valida la integridad del esquema actual.

        Args:
            required_tables: Lista de tablas que deben existir

        Returns:
            Diccionario con resultado de validación, errores y tablas encontradas
        """
        validation_result = {
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
                fetch_all=True,
            )

            if existing_tables:
                validation_result["tables_found"] = [
                    table["name"] for table in existing_tables
                ]

            # Verificar tablas requeridas
            required_tables_set = set(required_tables)
            found_tables = set(validation_result["tables_found"])

            missing_tables = required_tables_set - found_tables
            if missing_tables:
                validation_result["missing_tables"] = list(missing_tables)
                validation_result["valid"] = False
                validation_result["errors"].append(
                    f"Tablas faltantes: {', '.join(missing_tables)}"
                )

            # Validar integridad referencial
            integrity_result = self.db_manager.execute_query(
                "PRAGMA integrity_check", fetch_all=True
            )

            if integrity_result and len(integrity_result) > 0:
                first_result = integrity_result[0]
                if (
                    isinstance(first_result, dict)
                    and first_result.get("integrity_check") != "ok"
                ):
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        "Falla en integridad referencial"
                    )

            # Verificar versión de esquema
            version_check = self._verify_schema_version()
            if not version_check["valid"]:
                validation_result["warnings"].extend(version_check["warnings"])

            self._logger.info(
                "Validación de esquema: %s",
                "✅ VÁLIDO" if validation_result["valid"] else "❌ INVÁLIDO",
            )

        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Error durante validación: {e}")
            self._logger.error(f"Error validando esquema: {e}")

        return validation_result

    def get_current_version(self) -> Optional[str]:
        """
        Obtiene la versión actual del esquema desde metadatos.

        Returns:
            Versión del esquema o None si no existe
        """
        try:
            result = self.db_manager.execute_query(
                "SELECT version FROM schema_metadata ORDER BY applied_at DESC LIMIT 1",
                fetch_one=True,
            )
            return result["version"] if result else None

        except Exception as e:
            self._logger.warning(f"No se pudo obtener versión del esquema: {e}")
            return None

    def _verify_schema_version(self) -> Dict[str, Any]:
        """
        Verifica la consistencia de la versión del esquema.

        Returns:
            Diccionario con resultado de verificación
        """
        version_result = {"valid": True, "warnings": []}

        try:
            current_version = self.get_current_version()
            expected_version = "1.0.0"  # Versión esperada para Fase 1

            if not current_version:
                version_result["warnings"].append(
                    "No se encontró versión de esquema registrada"
                )
            elif current_version != expected_version:
                version_result["warnings"].append(
                    f"Versión de esquema {current_version} difiere de la esperada {expected_version}"
                )

        except Exception as e:
            version_result["warnings"].append(f"Error verificando versión: {e}")

        return version_result

    def _calculate_schema_checksum(self) -> str:
        """
        Calcula un checksum del esquema actual para detectar cambios.

        Returns:
            Checksum MD5 del esquema actual
        """
        try:
            # Obtener definiciones de todas las tablas
            tables_info = self.db_manager.execute_query(
                "SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name",
                fetch_all=True,
            )

            schema_text = ""
            if tables_info:
                schema_text = "|".join(
                    [table["sql"] for table in tables_info if table["sql"]]
                )

            return hashlib.md5(schema_text.encode()).hexdigest()

        except Exception as e:
            self._logger.warning(f"Error calculando checksum: {e}")
            return "unknown"
