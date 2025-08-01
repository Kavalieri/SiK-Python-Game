"""
Save Compatibility Core - Núcleo de compatibilidad
===================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Configuración y coordinación central del sistema de compatibilidad.
"""

import logging
from typing import Any

from .config_manager import ConfigManager
from .save_database import SaveDatabase
from .save_encryption import SaveEncryption
from .save_loader import SaveLoader


class SaveCompatibilityCore:
    """
    Núcleo del sistema de compatibilidad entre guardado pickle y SQLite.
    """

    def __init__(
        self,
        config: ConfigManager,
        loader: SaveLoader,
        database: SaveDatabase | None = None,
        encryption_handler: SaveEncryption | None = None,
    ):
        """
        Inicializa el núcleo del sistema de compatibilidad.

        Args:
            config: Configuración del juego
            loader: Cargador de archivos pickle
            database: Interfaz de base de datos (opcional)
            encryption_handler: Manejador de encriptación (opcional)
        """
        self.config = config
        self.loader = loader
        self.database = database
        self.encryption_handler = encryption_handler
        self.logger = logging.getLogger(__name__)

        # Configuración de modo de guardado
        self.use_sqlite = self.config.get("save_system", "use_sqlite", False)
        self.auto_migrate = self.config.get("save_system", "auto_migrate", True)

        self.logger.info(
            "SaveCompatibilityCore inicializado: SQLite=%s, auto_migrate=%s",
            self.use_sqlite,
            self.auto_migrate,
        )

    def is_sqlite_available(self) -> bool:
        """
        Verifica si SQLite está disponible y configurado.

        Returns:
            True si SQLite está disponible
        """
        return self.use_sqlite and self.database is not None

    def is_encryption_available(self) -> bool:
        """
        Verifica si el sistema de encriptación está disponible.

        Returns:
            True si la encriptación está disponible
        """
        return self.encryption_handler is not None

    def get_save_system_info(self) -> dict[str, Any]:
        """
        Obtiene información del sistema de guardado actual.

        Returns:
            Información del sistema de guardado
        """
        return {
            "sqlite_enabled": self.use_sqlite,
            "sqlite_available": self.is_sqlite_available(),
            "auto_migrate": self.auto_migrate,
            "encryption_available": self.is_encryption_available(),
            "primary_system": "sqlite" if self.is_sqlite_available() else "pickle",
            "fallback_system": "pickle" if self.is_sqlite_available() else None,
        }

    def validate_configuration(self) -> bool:
        """
        Valida la configuración del sistema de compatibilidad.

        Returns:
            True si la configuración es válida
        """
        if self.use_sqlite and not self.database:
            self.logger.error("SQLite habilitado pero database no disponible")
            return False

        if not self.encryption_handler:
            self.logger.warning("Sistema de encriptación no disponible")

        if not self.loader:
            self.logger.error("SaveLoader no disponible")
            return False

        self.logger.info("Configuración del sistema de compatibilidad válida")
        return True

    def log_operation_result(
        self, operation: str, slot: int, success: bool, system: str = "unknown"
    ) -> None:
        """
        Registra el resultado de una operación.

        Args:
            operation: Tipo de operación (save, load, migrate)
            slot: Número de slot
            success: Si la operación fue exitosa
            system: Sistema utilizado (sqlite, pickle)
        """
        if success:
            self.logger.info(
                "Operación %s exitosa en slot %d usando %s", operation, slot, system
            )
        else:
            self.logger.error(
                "Falló operación %s en slot %d usando %s", operation, slot, system
            )

    def should_auto_migrate(self) -> bool:
        """
        Determina si se debe migrar automáticamente.

        Returns:
            True si se debe migrar automáticamente
        """
        return (
            self.auto_migrate
            and self.is_sqlite_available()
            and self.is_encryption_available()
        )
