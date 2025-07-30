"""
Save Manager - Sistema de Guardado Refactorizado
===============================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada del sistema de guardado que mantiene compatibilidad con API original.
"""

import logging
from typing import Any, Dict, List, Optional

from .config_manager import ConfigManager
from .save_compatibility import SaveCompatibility
from .save_database import SaveDatabase
from .save_encryption import SaveEncryption
from .save_loader import SaveLoader


class SaveManager:
    """
    Gestor de guardado refactorizado que mantiene la API original.

    Este módulo actúa como fachada unificada del sistema modular de guardado.
    """

    def __init__(self, config: ConfigManager):
        """
        Inicializa el gestor de guardado.

        Args:
            config: Configuración del juego
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Inicializar componentes modulares
        self._init_components()

    def _init_components(self) -> None:
        """Inicializa los componentes del sistema modular."""
        try:
            # Componente de encriptación
            self.encryption_handler = SaveEncryption(self.config)

            # Componente de carga de archivos
            self.loader = SaveLoader(self.config, self.encryption_handler)

            # Componente de base de datos (opcional)
            self.database = None
            if self.config.get("save_system", "use_sqlite", False):
                try:
                    from .database_manager import DatabaseManager

                    db_manager = DatabaseManager()
                    self.database = SaveDatabase(db_manager, self.encryption_handler)
                    self.logger.info("Sistema SQLite inicializado")
                except ImportError:
                    self.logger.warning(
                        "DatabaseManager no disponible, usando solo pickle"
                    )
                except Exception as e:
                    self.logger.error("Error inicializando SQLite: %s", e)

            # Componente de compatibilidad
            self.compatibility = SaveCompatibility(
                self.config, self.loader, self.database, self.encryption_handler
            )

            self.logger.info("SaveManager inicializado correctamente")

        except Exception as e:
            self.logger.error("Error inicializando SaveManager: %s", e)
            raise

    # === API ORIGINAL MANTENIDA ===

    def get_save_files_info(self) -> List[Dict[str, Any]]:
        """
        Obtiene información de todos los archivos de guardado.

        Returns:
            Lista de información de archivos de guardado
        """
        return self.compatibility.get_saves_info_unified()

    def save_game(
        self, game_state, additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Guarda el estado del juego en el slot activo.

        Args:
            game_state: Estado del juego a guardar
            additional_data: Datos adicionales a guardar

        Returns:
            True si se guardó correctamente
        """
        # Obtener slot activo del game_state
        slot = getattr(game_state, "active_slot", 1)
        return self.compatibility.save_game_unified(slot, game_state, additional_data)

    def load_save(self, save_file_number: int) -> Optional[Dict[str, Any]]:
        """
        Carga un archivo de guardado.

        Args:
            save_file_number: Número del archivo de guardado

        Returns:
            Datos del guardado o None si hay error
        """
        return self.compatibility.load_game_unified(save_file_number)

    def create_new_save(self, save_file_number: int) -> bool:
        """
        Crea un nuevo archivo de guardado.

        Args:
            save_file_number: Número del archivo de guardado (1-3)

        Returns:
            True si se creó correctamente
        """
        try:
            # Crear archivo de información vacío
            save_info = {
                "file_number": save_file_number,
                "exists": True,
                "last_used": None,
                "player_name": f"Nuevo Jugador {save_file_number}",
                "level": 1,
                "score": 0,
                "play_time": 0,
            }

            # Si SQLite está disponible, crear entrada en base de datos
            if self.database:
                return self.database.create_new_save_slot(save_file_number, save_info)
            else:
                # Crear usando sistema pickle tradicional
                import json
                from datetime import datetime
                from pathlib import Path

                saves_path = Path(self.config.get("paths", "saves", "saves"))
                saves_path.mkdir(exist_ok=True)

                info_file = saves_path / f"save_{save_file_number}_info.json"
                save_info["last_used"] = datetime.now().isoformat()

                with open(info_file, "w", encoding="utf-8") as f:
                    json.dump(save_info, f, indent=4, ensure_ascii=False)

                self.logger.info("Nuevo save creado: slot %d", save_file_number)
                return True

        except Exception as e:
            self.logger.error(
                "Error creando nuevo save slot %d: %s", save_file_number, e
            )
            return False

    def delete_save(self, save_file_number: int) -> bool:
        """
        Elimina un archivo de guardado.

        Args:
            save_file_number: Número del archivo de guardado

        Returns:
            True si se eliminó correctamente
        """
        try:
            success = False

            # Eliminar de SQLite si está disponible
            if self.database:
                success = self.database.delete_save_from_database(save_file_number)

            # Eliminar archivos pickle
            from pathlib import Path

            saves_path = Path(self.config.get("paths", "saves", "saves"))

            save_file = saves_path / f"save_{save_file_number}.dat"
            info_file = saves_path / f"save_{save_file_number}_info.json"

            if save_file.exists():
                save_file.unlink()
                success = True

            if info_file.exists():
                info_file.unlink()
                success = True

            if success:
                self.logger.info("Save eliminado: slot %d", save_file_number)

            return success

        except Exception as e:
            self.logger.error("Error eliminando save slot %d: %s", save_file_number, e)
            return False

    def backup_saves(self) -> bool:
        """
        Crea una copia de seguridad de todos los archivos de guardado.

        Returns:
            True si el backup fue exitoso
        """
        try:
            import shutil
            from datetime import datetime
            from pathlib import Path

            saves_path = Path(self.config.get("paths", "saves", "saves"))
            backup_path = (
                saves_path
                / "backups"
                / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            backup_path.mkdir(parents=True, exist_ok=True)

            # Backup archivos pickle
            for save_file in saves_path.glob("save_*.dat"):
                shutil.copy2(save_file, backup_path)

            for info_file in saves_path.glob("save_*_info.json"):
                shutil.copy2(info_file, backup_path)

            # Backup base de datos SQLite si existe
            if self.database:
                self.database.backup_database(str(backup_path / "game_database.db"))

            self.logger.info("Backup creado en: %s", backup_path)
            return True

        except Exception as e:
            self.logger.error("Error creando backup: %s", e)
            return False

    # === NUEVAS FUNCIONALIDADES ===

    def migrate_to_sqlite(self) -> Dict[str, bool]:
        """
        Migra todas las partidas al sistema SQLite.

        Returns:
            Diccionario con resultados de migración
        """
        return self.compatibility.migrate_all_pickle_to_sqlite()

    def get_system_info(self) -> Dict[str, Any]:
        """
        Obtiene información del sistema de guardado.

        Returns:
            Información del sistema actual
        """
        return {
            "sqlite_available": self.database is not None,
            "encryption_enabled": self.encryption_handler is not None,
            "save_format": "sqlite" if self.database else "pickle",
            "auto_migration": self.config.get("save_system", "auto_migrate", True),
            "total_saves": len(self.get_save_files_info()),
        }

    def validate_saves_integrity(self) -> Dict[str, bool]:
        """
        Valida la integridad de todas las partidas guardadas.

        Returns:
            Diccionario con resultados de validación por slot
        """
        results = {}
        save_files = self.get_save_files_info()

        for save_info in save_files:
            if save_info["exists"]:
                slot = save_info["file_number"]

                # Intentar cargar el save para validar integridad
                try:
                    data = self.load_save(slot)
                    results[f"slot_{slot}"] = data is not None
                except Exception:
                    results[f"slot_{slot}"] = False

        return results
