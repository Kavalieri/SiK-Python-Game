"""
Save Compatibility Operations - Operaciones unificadas
=======================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Operaciones unificadas de guardado y carga entre sistemas.
"""

import logging
from typing import Any, Dict, List, Optional

from .save_compatibility_core import SaveCompatibilityCore


class SaveCompatibilityOperations:
    """
    Operaciones unificadas de guardado y carga.
    """

    def __init__(self, core: SaveCompatibilityCore):
        """
        Inicializa las operaciones con referencia al núcleo.

        Args:
            core: Núcleo del sistema de compatibilidad
        """
        self.core = core
        self.logger = logging.getLogger(__name__)

    def save_game_unified(
        self, slot: int, game_state, additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Guarda el juego usando el sistema disponible (SQLite prioritario, fallback a pickle).

        Args:
            slot: Número de slot (1-3)
            game_state: Estado del juego
            additional_data: Datos adicionales

        Returns:
            True si se guardó correctamente
        """
        # Intentar SQLite primero si está disponible
        if self.core.is_sqlite_available():
            try:
                if self.core.database.save_game_to_database(
                    slot, game_state, additional_data or {}
                ):
                    self.core.log_operation_result("save", slot, True, "sqlite")
                    return True
                else:
                    self.logger.warning(
                        "Fallo guardado SQLite slot %d, intentando pickle", slot
                    )
            except (ConnectionError, OSError) as e:
                self.logger.error("Error guardando en SQLite slot %d: %s", slot, e)

        # Fallback a sistema pickle tradicional
        from .save_compatibility_pickle import SaveCompatibilityPickle

        pickle_handler = SaveCompatibilityPickle(self.core)
        success = pickle_handler.save_game_pickle(
            slot, game_state, additional_data or {}
        )
        self.core.log_operation_result("save", slot, success, "pickle")
        return success

    def load_game_unified(self, slot: int) -> Optional[Dict[str, Any]]:
        """
        Carga el juego usando el sistema disponible (SQLite prioritario, fallback a pickle).

        Args:
            slot: Número de slot (1-3)

        Returns:
            Datos del juego o None si hay error
        """
        # Intentar SQLite primero si está disponible
        if self.core.is_sqlite_available():
            try:
                sqlite_data = self.core.database.load_game_from_database(slot)
                if sqlite_data:
                    self.core.log_operation_result("load", slot, True, "sqlite")
                    return sqlite_data
                else:
                    self.logger.info(
                        "No se encontró partida SQLite en slot %d, intentando pickle",
                        slot,
                    )
            except (ConnectionError, OSError) as e:
                self.logger.error("Error cargando desde SQLite slot %d: %s", slot, e)

        # Fallback a sistema pickle tradicional
        save_files = self.core.loader.load_save_files_info()
        pickle_data = self.core.loader.load_save_file(slot, save_files)

        if pickle_data:
            self.core.log_operation_result("load", slot, True, "pickle")

            # Migrar automáticamente a SQLite si es posible
            if self.core.should_auto_migrate():
                from .save_compatibility_migration import SaveCompatibilityMigration

                migration_handler = SaveCompatibilityMigration(self.core)
                if migration_handler.migrate_pickle_to_sqlite(slot, pickle_data):
                    self.logger.info(
                        "Partida migrada automáticamente a SQLite slot %d", slot
                    )
        else:
            self.core.log_operation_result("load", slot, False, "pickle")

        return pickle_data

    def get_saves_info_unified(self) -> List[Dict[str, Any]]:
        """
        Obtiene información de partidas de ambos sistemas.

        Returns:
            Lista consolidada de información de partidas
        """
        saves_info = []

        # Obtener información de SQLite si está disponible
        if self.core.is_sqlite_available():
            try:
                sqlite_saves = self.core.database.get_all_saves_info()
                saves_info.extend(sqlite_saves)
                self.logger.debug(
                    "Obtenidas %d partidas desde SQLite", len(sqlite_saves)
                )
            except (ConnectionError, OSError) as e:
                self.logger.error("Error obteniendo información SQLite: %s", e)

        # Obtener información de archivos pickle
        try:
            pickle_saves = self.core.loader.load_save_files_info()
            sqlite_slots = {save["file_number"] for save in saves_info}

            for save in pickle_saves:
                if save["exists"] and save["file_number"] not in sqlite_slots:
                    saves_info.append(save)

            self.logger.debug(
                "Obtenidas %d partidas adicionales desde pickle",
                len([s for s in pickle_saves if s["exists"]]),
            )

        except (OSError, IOError) as e:
            self.logger.error("Error obteniendo información pickle: %s", e)

        # Ordenar por número de slot
        saves_info.sort(key=lambda x: x["file_number"])
        return saves_info

    def delete_save_unified(self, slot: int) -> bool:
        """
        Elimina una partida de ambos sistemas.

        Args:
            slot: Número de slot

        Returns:
            True si se eliminó exitosamente
        """
        success_sqlite = True
        success_pickle = True

        # Eliminar de SQLite si está disponible
        if self.core.is_sqlite_available():
            try:
                success_sqlite = self.core.database.delete_save_from_database(slot)
                if success_sqlite:
                    self.logger.info("Partida eliminada de SQLite slot %d", slot)
                else:
                    self.logger.warning("No se pudo eliminar de SQLite slot %d", slot)
            except (ConnectionError, OSError) as e:
                self.logger.error("Error eliminando de SQLite slot %d: %s", slot, e)
                success_sqlite = False

        # Eliminar archivos pickle
        from .save_compatibility_pickle import SaveCompatibilityPickle

        pickle_handler = SaveCompatibilityPickle(self.core)
        success_pickle = pickle_handler.delete_pickle_files(slot)

        return success_sqlite and success_pickle
