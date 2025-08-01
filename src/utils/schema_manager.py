"""
SchemaManager - Gestor principal de esquemas SQLite (Refactorizado)
==================================================================

Punto de entrada principal para el sistema de gestión de esquemas SQLite.
Refactorizado para mantener límite de 150 líneas delegando funcionalidad
a módulos especializados.

Fase 1 de migración SQLite - Manager principal
"""

import logging
from typing import Any

from .database_manager import DatabaseManager
from .schema_core import SchemaCore


class SchemaManager:
    """
    Gestor principal de esquemas SQLite para el sistema de migración.

    Esta clase actúa como fachada principal que coordina los diferentes
    componentes del sistema de esquemas manteniendo compatibilidad con
    la API original.

    Características:
    - API compatible con versión original
    - Delegación a módulos especializados
    - Mantenimiento de límite de 150 líneas
    - Logging centralizado y consistente
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa el gestor de esquemas principal.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self.schema_core = SchemaCore(database_manager)
        self._logger = logging.getLogger("SchemaManager")

        self._logger.info("SchemaManager refactorizado inicializado")

    def create_all_tables(self) -> bool:
        """
        Crea todas las tablas del sistema de migración SQLite.

        Delegado a SchemaCore para mantener funcionalidad original
        compatible con tests existentes.

        Returns:
            True si todas las tablas se crearon exitosamente
        """
        self._logger.info("Iniciando creación de todas las tablas")
        result = self.schema_core.create_all_tables()

        if result:
            self._logger.info("✅ Creación de tablas completada exitosamente")
        else:
            self._logger.error("❌ Error en creación de tablas")

        return result

    def validate_schema(self) -> dict[str, Any]:
        """
        Valida la integridad del esquema actual.

        Delegado a SchemaCore para procesamiento especializado.

        Returns:
            Diccionario con resultado de validación, errores y tablas encontradas
        """
        self._logger.debug("Iniciando validación de esquema")
        result = self.schema_core.validate_schema()

        status = "✅ VÁLIDO" if result["valid"] else "❌ INVÁLIDO"
        self._logger.info("Validación de esquema completada: %s", status)

        return result

    def create_backup(self, backup_path: str | None = None) -> bool:
        """
        Crea backup de la base de datos antes de cambios importantes.

        Delegado a SchemaCore para manejo de archivos especializado.

        Args:
            backup_path: Ruta del backup (auto-generada si no se proporciona)

        Returns:
            True si el backup se creó exitosamente
        """
        self._logger.info("Iniciando creación de backup")
        result = self.schema_core.create_backup(backup_path)

        if result:
            self._logger.info("✅ Backup creado exitosamente")
        else:
            self._logger.error("❌ Error creando backup")

        return result

    def get_current_version(self) -> str | None:
        """
        Obtiene la versión actual del esquema desde metadatos.

        Delegado a SchemaCore para acceso a migraciones.

        Returns:
            Versión del esquema o None si no existe
        """
        version = self.schema_core.get_current_version()
        self._logger.debug("Versión de esquema actual: %s", version)
        return version

    def get_schema_info(self) -> dict[str, Any]:
        """
        Obtiene información completa del esquema y estado de la base de datos.

        Delegado a SchemaCore para recopilación de información completa.

        Returns:
            Diccionario con información completa del esquema
        """
        self._logger.debug("Recopilando información completa del esquema")
        return self.schema_core.get_schema_info()

    def get_database_info(self) -> dict[str, Any]:
        """
        Obtiene información de la base de datos subyacente.

        Acceso directo al DatabaseManager para información de BD.

        Returns:
            Diccionario con información de la base de datos
        """
        return self.db_manager.get_connection_info()

    def is_schema_initialized(self) -> bool:
        """
        Verifica si el esquema está completamente inicializado.

        Returns:
            True si todas las tablas requeridas existen y son válidas
        """
        validation = self.validate_schema()
        tables_found = len(validation.get("tables_found", []))

        # Verificar que tenemos al menos las 6 tablas principales
        # partidas_guardadas, configuraciones, personajes, enemigos,
        # estadisticas_juego, configuracion_gameplay
        expected_table_count = 6

        is_initialized = (
            validation["valid"]
            and tables_found >= expected_table_count
            and len(validation.get("missing_tables", [])) == 0
        )

        self._logger.debug(
            "Esquema inicializado: %s (tablas: %d/%d)",
            is_initialized,
            tables_found,
            expected_table_count,
        )

        return is_initialized
