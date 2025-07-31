"""
Save Compatibility Migration - Sistema de migración
====================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Sistema de migración entre pickle y SQLite.
"""

import logging
from typing import Any, Dict

from .save_compatibility_core import SaveCompatibilityCore


class SaveCompatibilityMigration:
    """
    Sistema de migración entre pickle y SQLite.
    """

    def __init__(self, core: SaveCompatibilityCore):
        """
        Inicializa el sistema de migración.

        Args:
            core: Núcleo del sistema de compatibilidad
        """
        self.core = core
        self.logger = logging.getLogger(__name__)

    def migrate_pickle_to_sqlite(self, slot: int, pickle_data: Dict[str, Any]) -> bool:
        """
        Migra datos pickle específicos a SQLite.

        Args:
            slot: Número de slot
            pickle_data: Datos del archivo pickle

        Returns:
            True si la migración fue exitosa
        """
        if not self.core.is_sqlite_available() or self.core.database is None:
            self.logger.error("SQLite no disponible para migración")
            return False

        try:
            success = self.core.database.migrate_pickle_to_database(pickle_data, slot)
            if success:
                self.core.log_operation_result("migrate", slot, True, "pickle->sqlite")
            else:
                self.core.log_operation_result("migrate", slot, False, "pickle->sqlite")
            return success
        except (ConnectionError, OSError) as e:
            self.logger.error(
                "Error de conexión migrando pickle a SQLite slot %d: %s", slot, e
            )
            return False
        except (ValueError, TypeError) as e:
            self.logger.error(
                "Error de datos migrando pickle a SQLite slot %d: %s", slot, e
            )
            return False

    def migrate_all_pickle_to_sqlite(self) -> Dict[str, bool]:
        """
        Migra todas las partidas pickle a SQLite.

        Returns:
            Diccionario con resultados de migración por slot
        """
        if not self.core.is_sqlite_available():
            self.logger.error("Base de datos no disponible para migración")
            return {}

        results = {}
        save_files = self.core.loader.load_save_files_info()

        for save_info in save_files:
            if save_info["exists"]:
                slot = save_info["file_number"]

                # Cargar datos pickle
                pickle_data = self.core.loader.load_save_file(slot, save_files)
                if pickle_data:
                    # Migrar a SQLite
                    success = self.migrate_pickle_to_sqlite(slot, pickle_data)
                    results[f"slot_{slot}"] = success

                    if success:
                        self.logger.info("Migración exitosa slot %d", slot)
                    else:
                        self.logger.error("Fallo migración slot %d", slot)
                else:
                    results[f"slot_{slot}"] = False
                    self.logger.error("No se pudo cargar pickle slot %d", slot)

        return results

    def validate_migration(self, slot: int) -> bool:
        """
        Valida que una migración se completó correctamente.

        Args:
            slot: Número de slot a validar

        Returns:
            True si la migración es válida
        """
        if not self.core.is_sqlite_available() or self.core.database is None:
            return False

        try:
            # Verificar que existe en SQLite
            sqlite_data = self.core.database.load_game_from_database(slot)
            if not sqlite_data:
                self.logger.error(
                    "Datos no encontrados en SQLite tras migración slot %d", slot
                )
                return False

            # Verificar integridad básica de datos
            required_fields = ["game_state", "save_timestamp"]
            for field in required_fields:
                if field not in sqlite_data:
                    self.logger.error(
                        "Campo requerido %s faltante en migración slot %d", field, slot
                    )
                    return False

            self.logger.info("Migración validada exitosamente slot %d", slot)
            return True

        except (ConnectionError, OSError) as e:
            self.logger.error(
                "Error de conexión validando migración slot %d: %s", slot, e
            )
            return False

    def get_migration_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado de migración del sistema.

        Returns:
            Estado de migración
        """
        status = {
            "sqlite_available": self.core.is_sqlite_available(),
            "auto_migrate_enabled": self.core.auto_migrate,
            "pickle_files_count": 0,
            "sqlite_saves_count": 0,
            "pending_migrations": [],
        }

        # Contar archivos pickle
        try:
            save_files = self.core.loader.load_save_files_info()
            pickle_count = len([s for s in save_files if s["exists"]])
            status["pickle_files_count"] = pickle_count
        except (OSError, IOError) as e:
            self.logger.warning("No se pudo contar archivos pickle: %s", e)

        # Contar saves en SQLite
        if self.core.is_sqlite_available() and self.core.database is not None:
            try:
                sqlite_saves = self.core.database.get_all_saves_info()
                status["sqlite_saves_count"] = len(sqlite_saves)

                # Identificar pendientes de migración
                sqlite_slots = {save["file_number"] for save in sqlite_saves}
                for save_info in save_files:
                    if (
                        save_info["exists"]
                        and save_info["file_number"] not in sqlite_slots
                    ):
                        status["pending_migrations"].append(save_info["file_number"])

            except (ConnectionError, OSError) as e:
                self.logger.warning("No se pudo contar saves en SQLite: %s", e)

        return status
