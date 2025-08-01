"""Save Manager - Sistema de Guardado Refactorizado"""

import logging
from typing import Any

from .config_manager import ConfigManager
from .save_compatibility import SaveCompatibility
from .save_database import SaveDatabase
from .save_encryption import SaveEncryption
from .save_loader import SaveLoader


class SaveManager:
    """Gestor de guardado refactorizado que mantiene la API original."""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._init_components()

    def _init_components(self) -> None:
        try:
            self.encryption_handler = SaveEncryption(self.config)
            self.loader = SaveLoader(self.config, self.encryption_handler)
            self.database = None
            if self.config.get("save_system", "use_sqlite", False):
                try:
                    # Import local para evitar dependencia circular
                    # pylint: disable=import-outside-toplevel
                    from .database_manager import DatabaseManager

                    db_manager = DatabaseManager()
                    self.database = SaveDatabase(db_manager, self.encryption_handler)
                    self.logger.info("Sistema SQLite inicializado")
                except ImportError:
                    self.logger.warning(
                        "DatabaseManager no disponible, usando solo pickle"
                    )
                except OSError as e:
                    self.logger.error("Error inicializando SQLite: %s", e)
            self.compatibility = SaveCompatibility(
                self.config, self.loader, self.database, self.encryption_handler
            )
            self.logger.info("SaveManager inicializado correctamente")
        except (ImportError, OSError) as e:
            self.logger.error("Error inicializando SaveManager: %s", e)
            raise

    def get_save_files_info(self) -> list[dict[str, Any]]:
        """Obtiene información de todos los archivos de guardado."""
        return self.compatibility.get_saves_info_unified()

    def save_game(
        self, game_state, additional_data: dict[str, Any] | None = None
    ) -> bool:
        """Guarda el estado del juego actual."""
        slot = getattr(game_state, "active_slot", 1)
        return self.compatibility.save_game_unified(slot, game_state, additional_data)

    def load_save(self, save_file_number: int) -> dict[str, Any] | None:
        """Carga una partida guardada específica."""
        return self.compatibility.load_game_unified(save_file_number)

    def create_new_save(self, save_file_number: int) -> bool:
        """Crea un nuevo slot de guardado."""
        try:
            save_info = {
                "file_number": save_file_number,
                "exists": True,
                "last_used": None,
                "player_name": f"Nuevo Jugador {save_file_number}",
                "level": 1,
                "score": 0,
                "play_time": 0,
            }
            if self.database:
                return getattr(
                    self.database, "create_new_save_slot", lambda x, y: False
                )(save_file_number, save_info)
            else:
                # Imports locales para funcionalidad específica
                import json  # pylint: disable=import-outside-toplevel
                from datetime import datetime  # pylint: disable=import-outside-toplevel
                from pathlib import Path  # pylint: disable=import-outside-toplevel

                saves_path = Path(self.config.get("paths", "saves", "saves"))
                saves_path.mkdir(exist_ok=True)
                info_file = saves_path / f"save_{save_file_number}_info.json"
                save_info["last_used"] = datetime.now().isoformat()
                with open(info_file, "w", encoding="utf-8") as f:
                    json.dump(save_info, f, indent=4, ensure_ascii=False)
                self.logger.info("Nuevo save creado: slot %d", save_file_number)
                return True
        except (OSError, PermissionError, ValueError) as e:
            self.logger.error(
                "Error creando nuevo save slot %d: %s", save_file_number, e
            )
            return False

    def delete_save(self, save_file_number: int) -> bool:
        """Elimina una partida guardada."""
        try:
            success = False
            if self.database:
                success = getattr(
                    self.database, "delete_save_from_database", lambda x: False
                )(save_file_number)
            # Import local para operaciones de archivo
            from pathlib import Path  # pylint: disable=import-outside-toplevel

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
        except (OSError, PermissionError) as e:
            self.logger.error("Error eliminando save slot %d: %s", save_file_number, e)
            return False

    def clear_slot(self, slot: int) -> bool:
        """Limpia un slot de guardado (alias para delete_save)."""
        self.logger.info("Limpiando slot %d", slot)
        return self.delete_save(slot)

    def backup_saves(self) -> bool:
        """Crea backup de todas las partidas guardadas."""
        try:
            # Imports locales para operaciones de backup
            import shutil  # pylint: disable=import-outside-toplevel
            from datetime import datetime  # pylint: disable=import-outside-toplevel
            from pathlib import Path  # pylint: disable=import-outside-toplevel

            saves_path = Path(self.config.get("paths", "saves", "saves"))
            backup_path = (
                saves_path
                / "backups"
                / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            backup_path.mkdir(parents=True, exist_ok=True)
            for save_file in saves_path.glob("save_*.dat"):
                shutil.copy2(save_file, backup_path)
            for info_file in saves_path.glob("save_*_info.json"):
                shutil.copy2(info_file, backup_path)
            if self.database:
                getattr(self.database, "backup_database", lambda x: None)(
                    str(backup_path / "game_database.db")
                )
            self.logger.info("Backup creado en: %s", backup_path)
            return True
        except (OSError, PermissionError, shutil.Error) as e:
            self.logger.error("Error creando backup: %s", e)
            return False

    def migrate_to_sqlite(self) -> dict[str, bool]:
        """Migra partidas desde pickle a SQLite."""
        return self.compatibility.migrate_all_pickle_to_sqlite()

    def get_system_info(self) -> dict[str, Any]:
        """Obtiene información del sistema de guardado."""
        return {
            "sqlite_available": self.database is not None,
            "encryption_enabled": self.encryption_handler is not None,
            "save_format": "sqlite" if self.database else "pickle",
            "auto_migration": self.config.get("save_system", "auto_migrate", True),
            "total_saves": len(self.get_save_files_info()),
        }

    def validate_saves_integrity(self) -> dict[str, bool]:
        """Valida la integridad de todas las partidas guardadas."""
        results = {}
        save_files = self.get_save_files_info()
        for save_info in save_files:
            if save_info["exists"]:
                slot = save_info["file_number"]
                try:
                    data = self.load_save(slot)
                    results[f"slot_{slot}"] = data is not None
                except (OSError, ValueError, KeyError):
                    results[f"slot_{slot}"] = False
        return results
