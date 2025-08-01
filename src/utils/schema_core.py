"""
SchemaCore - Núcleo del sistema de esquemas SQLite
==================================================

Módulo principal que orquesta la creación de tablas y gestión de esquemas.
Mantiene la funcionalidad principal del SchemaManager original en <150 líneas.

Fase 1 de migración SQLite - Núcleo del sistema
"""

import logging
import shutil
from pathlib import Path
from typing import Any

from .database_manager import DatabaseManager
from .schema_migrations import SchemaMigrations
from .schema_tables import get_all_table_schemas, get_table_list


class SchemaCore:
    """
    Núcleo del sistema de gestión de esquemas SQLite.

    Características principales:
    - Creación automática de todas las tablas del sistema
    - Integración con sistema de migraciones
    - Validación de esquemas e integridad
    - Backup automático antes de cambios importantes
    """

    SCHEMA_VERSION = "1.0.0"

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa el núcleo del sistema de esquemas.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self.migrations = SchemaMigrations(database_manager)
        self._logger = logging.getLogger("SchemaCore")

        # Crear tabla de metadatos si no existe
        self._create_metadata_table()
        self._logger.info("SchemaCore inicializado correctamente")

    def _create_metadata_table(self) -> None:
        """Crea la tabla de metadatos del esquema si no existe."""
        create_metadata_sql = """
        CREATE TABLE IF NOT EXISTS schema_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            checksum TEXT
        )
        """

        try:
            self.db_manager.execute_query(create_metadata_sql)
            self._logger.debug("Tabla de metadatos verificada")
        except Exception as e:
            self._logger.error("Error creando tabla de metadatos: %s", e)
            raise

    def create_all_tables(self) -> bool:
        """
        Crea todas las tablas del sistema de migración SQLite.

        Returns:
            True si todas las tablas se crearon exitosamente
        """
        table_schemas = get_all_table_schemas()

        try:
            with self.db_manager.transaction() as conn:
                for table_name, schema_sql in table_schemas.items():
                    self._logger.info("Creando tabla: %s", table_name)
                    conn.execute(schema_sql)

                # Registrar migración
                self.migrations.record_migration(
                    "Initial schema creation", "CREATE_ALL_TABLES", self.SCHEMA_VERSION
                )

            self._logger.info("✅ Todas las tablas creadas exitosamente")
            return True

        except (ValueError, RuntimeError, OSError) as e:
            self._logger.error("Error creando tablas: %s", e)
            return False

    def validate_schema(self) -> dict[str, Any]:
        """
        Valida la integridad del esquema actual contra las tablas requeridas.

        Returns:
            Diccionario con resultado de validación completa
        """
        required_tables = get_table_list()
        return self.migrations.validate_schema(required_tables)

    def get_current_version(self) -> str:
        """
        Obtiene la versión actual del esquema.

        Returns:
            Versión del esquema actual o versión por defecto
        """
        version = self.migrations.get_schema_version()
        return version or self.SCHEMA_VERSION

    def create_backup(self, backup_path: str | None = None) -> bool:
        """
        Crea backup de la base de datos antes de cambios importantes.

        Args:
            backup_path: Ruta del backup (se genera automáticamente si no se proporciona)

        Returns:
            True si el backup se creó exitosamente
        """
        if not backup_path:
            timestamp = (
                Path().cwd().name
            )  # Usar nombre del directorio como timestamp simple
            backup_path = f"saves/backup_db_{timestamp}.db"

        try:
            db_info = self.db_manager.get_connection_info()
            source_path = db_info["db_path"]

            # Crear directorio de backup si no existe
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(parents=True, exist_ok=True)

            # Copiar archivo de base de datos
            shutil.copy2(source_path, backup_path)

            self._logger.info("✅ Backup creado: %s", backup_path)
            return True

        except (OSError, ValueError, RuntimeError) as e:
            self._logger.error("Error creando backup: %s", e)
            return False

    def get_schema_info(self) -> dict[str, Any]:
        """
        Obtiene información completa del esquema actual.

        Returns:
            Diccionario con información del esquema y base de datos
        """
        info = {
            "version": self.get_current_version(),
            "tables_defined": get_table_list(),
            "database_info": self.db_manager.get_connection_info(),
            "validation": self.validate_schema(),
        }

        return info
