"""
Save Compatibility - Sistema de compatibilidad principal
=========================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada principal del sistema de compatibilidad entre pickle y SQLite.
"""

import logging
from typing import Any, Dict, List, Optional

from .config_manager import ConfigManager
from .save_compatibility_core import SaveCompatibilityCore
from .save_compatibility_migration import SaveCompatibilityMigration
from .save_compatibility_operations import SaveCompatibilityOperations
from .save_compatibility_pickle import SaveCompatibilityPickle
from .save_database import SaveDatabase
from .save_encryption import SaveEncryption
from .save_loader import SaveLoader


class SaveCompatibility:
    """
    Sistema de compatibilidad entre guardado pickle y SQLite.
    """

    def __init__(
        self,
        config: ConfigManager,
        loader: SaveLoader,
        database: Optional[SaveDatabase] = None,
        encryption_handler: Optional[SaveEncryption] = None,
    ):
        """
        Inicializa el sistema de compatibilidad.

        Args:
            config: Configuración del juego
            loader: Cargador de archivos pickle
            database: Interfaz de base de datos (opcional)
            encryption_handler: Manejador de encriptación (opcional)
        """
        # Inicializar módulos especializados
        self.core = SaveCompatibilityCore(config, loader, database, encryption_handler)
        self.operations = SaveCompatibilityOperations(self.core)
        self.migration = SaveCompatibilityMigration(self.core)
        self.pickle_handler = SaveCompatibilityPickle(self.core)

        self.logger = logging.getLogger(__name__)
        self.logger.info("SaveCompatibility inicializado correctamente")

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
        return self.operations.save_game_unified(slot, game_state, additional_data)

    def load_game_unified(self, slot: int) -> Optional[Dict[str, Any]]:
        """
        Carga el juego usando el sistema disponible (SQLite prioritario, fallback a pickle).

        Args:
            slot: Número de slot (1-3)

        Returns:
            Datos del juego o None si hay error
        """
        return self.operations.load_game_unified(slot)

    def get_saves_info_unified(self) -> List[Dict[str, Any]]:
        """
        Obtiene información de partidas de ambos sistemas.

        Returns:
            Lista consolidada de información de partidas
        """
        return self.operations.get_saves_info_unified()

    def migrate_all_pickle_to_sqlite(self) -> Dict[str, bool]:
        """
        Migra todas las partidas pickle a SQLite.

        Returns:
            Diccionario con resultados de migración por slot
        """
        return self.migration.migrate_all_pickle_to_sqlite()

    def cleanup_old_pickle_files(self, confirm_migration: bool = False) -> bool:
        """
        Limpia archivos pickle antiguos después de migración exitosa.

        Args:
            confirm_migration: Si True, confirma que la migración fue exitosa

        Returns:
            True si se limpiaron los archivos
        """
        return self.pickle_handler.cleanup_old_pickle_files(confirm_migration)

    def delete_save_unified(self, slot: int) -> bool:
        """
        Elimina una partida de ambos sistemas.

        Args:
            slot: Número de slot

        Returns:
            True si se eliminó exitosamente
        """
        return self.operations.delete_save_unified(slot)

    def get_system_info(self) -> Dict[str, Any]:
        """
        Obtiene información completa del sistema de guardado.

        Returns:
            Información del sistema
        """
        system_info = self.core.get_save_system_info()
        migration_status = self.migration.get_migration_status()
        pickle_info = self.pickle_handler.get_pickle_files_info()

        return {
            "system": system_info,
            "migration": migration_status,
            "pickle_files": pickle_info,
            "modules_loaded": {
                "core": True,
                "operations": True,
                "migration": True,
                "pickle_handler": True,
            },
        }

    def validate_system(self) -> bool:
        """
        Valida que el sistema esté correctamente configurado.

        Returns:
            True si el sistema es válido
        """
        return self.core.validate_configuration()

    def force_migrate_slot(self, slot: int) -> bool:
        """
        Fuerza la migración de un slot específico.

        Args:
            slot: Número de slot

        Returns:
            True si la migración fue exitosa
        """
        save_files = self.core.loader.load_save_files_info()
        pickle_data = self.core.loader.load_save_file(slot, save_files)

        if pickle_data:
            return self.migration.migrate_pickle_to_sqlite(slot, pickle_data)
        else:
            self.logger.error("No se encontraron datos pickle para slot %d", slot)
            return False
