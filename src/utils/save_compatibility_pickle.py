"""
Save Compatibility Pickle - Gestión de archivos pickle
======================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Gestión específica de archivos pickle.
"""

import json
import logging
import pickle
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .save_compatibility_core import SaveCompatibilityCore


class SaveCompatibilityPickle:
    """
    Gestión específica de archivos pickle.
    """

    def __init__(self, core: SaveCompatibilityCore):
        """
        Inicializa el gestor de archivos pickle.

        Args:
            core: Núcleo del sistema de compatibilidad
        """
        self.core = core
        self.logger = logging.getLogger(__name__)

    def save_game_pickle(
        self, slot: int, game_state, additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Guarda el juego usando el sistema pickle tradicional.

        Args:
            slot: Número de slot
            game_state: Estado del juego
            additional_data: Datos adicionales

        Returns:
            True si se guardó correctamente
        """
        try:
            if not self.core.is_encryption_available():
                self.logger.error("Sistema de encriptación no disponible")
                return False

            # Preparar datos para guardar
            save_data = {
                "game_state": game_state.get_state_dict(),
                "additional_data": additional_data,
                "save_timestamp": datetime.now().isoformat(),
                "game_version": self.core.config.get("game", "version", "0.1.0"),
            }

            # Serializar y comprimir datos
            serialized_data = pickle.dumps(save_data)
            compressed_data = zlib.compress(serialized_data)

            # Cifrar datos
            if self.core.encryption_handler is not None:
                encrypted_data = self.core.encryption_handler.encrypt_data(
                    compressed_data
                )
            else:
                self.logger.warning(
                    "No hay handler de encriptación, guardando sin cifrar"
                )
                encrypted_data = compressed_data

            # Guardar archivo cifrado
            saves_path = Path(self.core.config.get("paths", "saves", "saves"))
            saves_path.mkdir(parents=True, exist_ok=True)
            save_file = saves_path / f"save_{slot}.dat"

            with open(save_file, "wb") as f:
                f.write(encrypted_data)

            # Actualizar archivo de información
            self.update_pickle_save_info(slot, game_state)

            self.logger.info("Juego guardado con pickle en slot %d", slot)
            return True

        except (OSError, IOError) as e:
            self.logger.error(
                "Error de archivo guardando con pickle slot %d: %s", slot, e
            )
            return False
        except (MemoryError, pickle.PicklingError) as e:
            self.logger.error(
                "Error de serialización guardando con pickle slot %d: %s", slot, e
            )
            return False

    def update_pickle_save_info(self, slot: int, game_state) -> None:
        """Actualiza el archivo de información pickle."""
        try:
            saves_path = Path(self.core.config.get("paths", "saves", "saves"))
            saves_path.mkdir(parents=True, exist_ok=True)
            info_file = saves_path / f"save_{slot}_info.json"

            save_info = {
                "file_number": slot,
                "exists": True,
                "last_used": datetime.now().isoformat(),
                "player_name": getattr(game_state, "player_name", f"Jugador {slot}"),
                "level": getattr(game_state, "level", 1),
                "score": getattr(game_state, "score", 0),
                "play_time": getattr(game_state, "play_time", 0),
            }

            with open(info_file, "w", encoding="utf-8") as f:
                json.dump(save_info, f, indent=4, ensure_ascii=False)

        except (OSError, IOError) as e:
            self.logger.error("Error actualizando info pickle slot %d: %s", slot, e)
        except (TypeError, ValueError) as e:
            self.logger.error(
                "Error de datos actualizando info pickle slot %d: %s", slot, e
            )

    def delete_pickle_files(self, slot: int) -> bool:
        """
        Elimina archivos pickle de un slot específico.

        Args:
            slot: Número de slot

        Returns:
            True si se eliminaron los archivos
        """
        try:
            saves_path = Path(self.core.config.get("paths", "saves", "saves"))
            save_file = saves_path / f"save_{slot}.dat"
            info_file = saves_path / f"save_{slot}_info.json"

            deleted_count = 0

            if save_file.exists():
                save_file.unlink()
                deleted_count += 1
                self.logger.info("Eliminado archivo de guardado slot %d", slot)

            if info_file.exists():
                info_file.unlink()
                deleted_count += 1
                self.logger.info("Eliminado archivo de info slot %d", slot)

            return deleted_count > 0

        except (OSError, IOError) as e:
            self.logger.error("Error eliminando archivos pickle slot %d: %s", slot, e)
            return False

    def cleanup_old_pickle_files(self, confirm_migration: bool = False) -> bool:
        """
        Limpia archivos pickle antiguos después de migración exitosa.

        Args:
            confirm_migration: Si True, confirma que la migración fue exitosa

        Returns:
            True si se limpiaron los archivos
        """
        if not confirm_migration:
            self.logger.warning("Limpieza de archivos pickle no confirmada")
            return False

        try:
            cleaned_files = 0

            for i in range(1, 4):  # Slots 1-3
                if self.delete_pickle_files(i):
                    cleaned_files += 1

            self.logger.info("Limpiados archivos pickle de %d slots", cleaned_files)
            return cleaned_files > 0

        except (OSError, IOError) as e:
            self.logger.error("Error limpiando archivos pickle: %s", e)
            return False

    def get_pickle_files_info(self) -> Dict[str, Any]:
        """Obtiene información de archivos pickle existentes."""
        info = {"total_files": 0, "active_slots": [], "total_size_bytes": 0}

        try:
            saves_path = Path(self.core.config.get("paths", "saves", "saves"))

            for i in range(1, 4):  # Slots 1-3
                save_file = saves_path / f"save_{i}.dat"
                info_file = saves_path / f"save_{i}_info.json"

                if save_file.exists() and info_file.exists():
                    info["active_slots"].append(i)
                    info["total_files"] += 2
                    info["total_size_bytes"] += (
                        save_file.stat().st_size + info_file.stat().st_size
                    )

        except (OSError, IOError) as e:
            self.logger.error("Error obteniendo información pickle: %s", e)

        return info
