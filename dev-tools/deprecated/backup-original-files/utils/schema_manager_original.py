"""
SchemaManager - Gestor de esquemas y migraciones SQLite
======================================================

Módulo para gestionar la creación automática de tablas, migraciones de esquema,
y validación de integridad de la base de datos.

Fase 1 de migración SQLite - Infraestructura base
Referencia: docs/PLAN_MIGRACION_SQLITE.md - Fase 1
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .database_manager import DatabaseManager


class SchemaManager:
    """
    Gestor de esquemas SQLite para el sistema de migración.

    Características:
    - Creación automática de todas las tablas del sistema
    - Sistema de migraciones versionadas
    - Validación de integridad de esquemas
    - Backup automático antes de cambios
    - Rollback de migraciones si es necesario
    """

    # Versión actual del esquema
    SCHEMA_VERSION = "1.0.0"

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa el gestor de esquemas.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self._logger = logging.getLogger("SchemaManager")

        # Crear tabla de metadatos si no existe
        self._create_metadata_table()

        self._logger.info("SchemaManager inicializado")

    def _create_metadata_table(self) -> None:
        """Crea la tabla de metadatos del esquema."""
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
            self._logger.debug("Tabla de metadatos creada o verificada")
        except Exception as e:
            self._logger.error(f"Error creando tabla de metadatos: {e}")
            raise

    def create_all_tables(self) -> bool:
        """
        Crea todas las tablas del sistema de migración SQLite.

        Returns:
            True si todas las tablas se crearon exitosamente
        """
        schemas = self._get_table_schemas()

        try:
            with self.db_manager.transaction() as conn:
                for table_name, schema_sql in schemas.items():
                    self._logger.info(f"Creando tabla: {table_name}")
                    conn.execute(schema_sql)

                # Registrar migración
                self._record_migration("Initial schema creation", "CREATE_ALL_TABLES")

            self._logger.info("Todas las tablas creadas exitosamente")
            return True

        except Exception as e:
            self._logger.error(f"Error creando tablas: {e}")
            return False

    def _get_table_schemas(self) -> Dict[str, str]:
        """
        Obtiene todos los esquemas de tablas definidos.

        Returns:
            Diccionario con nombre de tabla y su SQL de creación
        """
        return {
            "partidas_guardadas": """
                CREATE TABLE IF NOT EXISTS partidas_guardadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slot INTEGER NOT NULL CHECK(slot IN (1, 2, 3)),
                    nombre_jugador TEXT NOT NULL,
                    descripcion TEXT,
                    nivel_actual INTEGER DEFAULT 1,
                    puntuacion INTEGER DEFAULT 0,
                    vidas INTEGER DEFAULT 3,
                    tiempo_jugado INTEGER DEFAULT 0,
                    personaje TEXT NOT NULL,
                    estado_juego TEXT,
                    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(slot)
                )
            """,
            "configuraciones": """
                CREATE TABLE IF NOT EXISTS configuraciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL,
                    clave TEXT NOT NULL,
                    valor TEXT NOT NULL,
                    tipo TEXT NOT NULL CHECK(tipo IN ('string', 'number', 'boolean', 'object')),
                    descripcion TEXT,
                    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(categoria, clave)
                )
            """,
            "personajes": """
                CREATE TABLE IF NOT EXISTS personajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    nombre_mostrar TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    descripcion TEXT,
                    stats TEXT NOT NULL,
                    ataques TEXT NOT NULL,
                    sprite_config TEXT,
                    activo BOOLEAN DEFAULT 1,
                    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "enemigos": """
                CREATE TABLE IF NOT EXISTS enemigos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT UNIQUE NOT NULL,
                    nombre_mostrar TEXT NOT NULL,
                    stats TEXT NOT NULL,
                    comportamiento TEXT NOT NULL,
                    animaciones TEXT NOT NULL,
                    variantes TEXT,
                    activo BOOLEAN DEFAULT 1,
                    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "estadisticas_juego": """
                CREATE TABLE IF NOT EXISTS estadisticas_juego (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slot_partida INTEGER NOT NULL,
                    tipo_estadistica TEXT NOT NULL,
                    valor INTEGER NOT NULL,
                    sesion_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (slot_partida) REFERENCES partidas_guardadas(slot)
                )
            """,
            "configuracion_gameplay": """
                CREATE TABLE IF NOT EXISTS configuracion_gameplay (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL,
                    configuracion TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    activo BOOLEAN DEFAULT 1,
                    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """,
        }

    def validate_schema(self) -> Dict[str, Any]:
        """
        Valida la integridad del esquema actual.

        Returns:
            Diccionario con el resultado de la validación
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "tables_found": [],
            "missing_tables": [],
            "schema_version": self.get_current_version(),
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
            required_tables = set(self._get_table_schemas().keys())
            found_tables = set(validation_result["tables_found"])

            missing_tables = required_tables - found_tables
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

            self._logger.info(
                f"Validación de esquema: {'✅ VÁLIDO' if validation_result['valid'] else '❌ INVÁLIDO'}"
            )

        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Error durante validación: {e}")
            self._logger.error(f"Error validando esquema: {e}")

        return validation_result

    def _record_migration(self, description: str, operation: str) -> None:
        """
        Registra una migración en la tabla de metadatos.

        Args:
            description: Descripción de la migración
            operation: Tipo de operación realizada
        """
        try:
            self.db_manager.execute_query(
                "INSERT INTO schema_metadata (version, description, checksum) VALUES (?, ?, ?)",
                (
                    self.SCHEMA_VERSION,
                    f"{description} ({operation})",
                    self._calculate_schema_checksum(),
                ),
            )
        except Exception as e:
            self._logger.error(f"Error registrando migración: {e}")

    def _calculate_schema_checksum(self) -> str:
        """
        Calcula un checksum del esquema actual.

        Returns:
            Checksum del esquema como string
        """
        import hashlib

        try:
            # Obtener información de todas las tablas
            tables_info = self.db_manager.execute_query(
                "SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name",
                fetch_all=True,
            )

            if tables_info:
                schema_text = "".join([table["sql"] or "" for table in tables_info])
                return hashlib.md5(schema_text.encode()).hexdigest()[:8]

        except Exception as e:
            self._logger.error(f"Error calculando checksum: {e}")

        return "unknown"

    def get_current_version(self) -> Optional[str]:
        """
        Obtiene la versión actual del esquema.

        Returns:
            Versión del esquema o None si no existe
        """
        try:
            result = self.db_manager.execute_query(
                "SELECT version FROM schema_metadata ORDER BY applied_at DESC LIMIT 1",
                fetch_one=True,
            )
            if result and isinstance(result, dict):
                return result.get("version")
            return None
        except Exception as e:
            self._logger.error(f"Error obteniendo versión: {e}")
            return None

    def create_backup(self, backup_path: Optional[str] = None) -> bool:
        """
        Crea un backup de la base de datos antes de cambios importantes.

        Args:
            backup_path: Ruta del backup (opcional)

        Returns:
            True si el backup se creó exitosamente
        """
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"saves/backup_db_{timestamp}.db"

        try:
            backup_path_obj = Path(backup_path)
            backup_path_obj.parent.mkdir(parents=True, exist_ok=True)

            # Realizar backup usando SQLite backup API
            with self.db_manager.get_connection():
                import shutil

                shutil.copy2(self.db_manager.db_path, backup_path_obj)

            self._logger.info(f"Backup creado: {backup_path_obj}")
            return True

        except Exception as e:
            self._logger.error(f"Error creando backup: {e}")
            return False
