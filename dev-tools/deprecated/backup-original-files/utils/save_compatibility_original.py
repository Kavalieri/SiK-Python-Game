"""
Save Compatibility - Compatibilidad y Migración
================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo para compatibilidad entre sistemas de guardado pickle y SQLite.
"""

import json
import logging
import pickle
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any

from .config_manager import ConfigManager
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
        database: SaveDatabase | None = None,
        encryption_handler: SaveEncryption | None = None,
    ):
        """
        Inicializa el sistema de compatibilidad.

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

    def save_game_unified(
        self, slot: int, game_state, additional_data: dict[str, Any] | None = None
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
        if self.use_sqlite and self.database:
            try:
                if self.database.save_game_to_database(
                    slot, game_state, additional_data or {}
                ):
                    self.logger.info(
                        "Juego guardado exitosamente en SQLite slot %d", slot
                    )
                    return True
                else:
                    self.logger.warning(
                        "Fallo guardado SQLite slot %d, intentando pickle", slot
                    )
            except Exception as e:
                self.logger.error("Error guardando en SQLite slot %d: %s", slot, e)

        # Fallback a sistema pickle tradicional
        return self._save_game_pickle(slot, game_state, additional_data or {})

    def load_game_unified(self, slot: int) -> dict[str, Any] | None:
        """
        Carga el juego usando el sistema disponible (SQLite prioritario, fallback a pickle).

        Args:
            slot: Número de slot (1-3)

        Returns:
            Datos del juego o None si hay error
        """
        # Intentar SQLite primero si está disponible
        if self.use_sqlite and self.database:
            try:
                sqlite_data = self.database.load_game_from_database(slot)
                if sqlite_data:
                    self.logger.info(
                        "Juego cargado exitosamente desde SQLite slot %d", slot
                    )
                    return sqlite_data
                else:
                    self.logger.info(
                        "No se encontró partida SQLite en slot %d, intentando pickle",
                        slot,
                    )
            except Exception as e:
                self.logger.error("Error cargando desde SQLite slot %d: %s", slot, e)

        # Fallback a sistema pickle tradicional
        save_files = self.loader.load_save_files_info()
        pickle_data = self.loader.load_save_file(slot, save_files)

        if pickle_data and self.auto_migrate and self.database:
            # Migrar automáticamente a SQLite si es posible
            if self._migrate_pickle_to_sqlite(slot, pickle_data):
                self.logger.info(
                    "Partida migrada automáticamente a SQLite slot %d", slot
                )

        return pickle_data

    def get_saves_info_unified(self) -> list[dict[str, Any]]:
        """
        Obtiene información de partidas de ambos sistemas.

        Returns:
            Lista consolidada de información de partidas
        """
        saves_info = []

        # Obtener información de SQLite si está disponible
        if self.use_sqlite and self.database:
            try:
                sqlite_saves = self.database.get_all_saves_info()
                saves_info.extend(sqlite_saves)
                self.logger.debug(
                    "Obtenidas %d partidas desde SQLite", len(sqlite_saves)
                )
            except Exception as e:
                self.logger.error("Error obteniendo información SQLite: %s", e)

        # Obtener información de archivos pickle
        try:
            pickle_saves = self.loader.load_save_files_info()

            # Filtrar slots ya presentes en SQLite para evitar duplicados
            sqlite_slots = {save["file_number"] for save in saves_info}

            for save in pickle_saves:
                if save["exists"] and save["file_number"] not in sqlite_slots:
                    saves_info.append(save)

            self.logger.debug(
                "Obtenidas %d partidas adicionales desde pickle",
                len([s for s in pickle_saves if s["exists"]]),
            )

        except Exception as e:
            self.logger.error("Error obteniendo información pickle: %s", e)

        # Ordenar por número de slot
        saves_info.sort(key=lambda x: x["file_number"])
        return saves_info

    def migrate_all_pickle_to_sqlite(self) -> dict[str, bool]:
        """
        Migra todas las partidas pickle a SQLite.

        Returns:
            Diccionario con resultados de migración por slot
        """
        if not self.database:
            self.logger.error("Base de datos no disponible para migración")
            return {}

        results = {}
        save_files = self.loader.load_save_files_info()

        for save_info in save_files:
            if save_info["exists"]:
                slot = save_info["file_number"]

                # Cargar datos pickle
                pickle_data = self.loader.load_save_file(slot, save_files)
                if pickle_data:
                    # Migrar a SQLite
                    success = self._migrate_pickle_to_sqlite(slot, pickle_data)
                    results[f"slot_{slot}"] = success

                    if success:
                        self.logger.info("Migración exitosa slot %d", slot)
                    else:
                        self.logger.error("Fallo migración slot %d", slot)
                else:
                    results[f"slot_{slot}"] = False
                    self.logger.error("No se pudo cargar pickle slot %d", slot)

        return results

    def _save_game_pickle(
        self, slot: int, game_state, additional_data: dict[str, Any] | None = None
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
            if not self.encryption_handler:
                self.logger.error("Sistema de encriptación no disponible")
                return False

            # Preparar datos para guardar
            save_data = {
                "game_state": game_state.get_state_dict(),
                "additional_data": additional_data,
                "save_timestamp": datetime.now().isoformat(),
                "game_version": self.config.get("game", "version", "0.1.0"),
            }

            # Serializar y comprimir datos
            serialized_data = pickle.dumps(save_data)
            compressed_data = zlib.compress(serialized_data)

            # Cifrar datos
            encrypted_data = self.encryption_handler.encrypt_data(compressed_data)

            # Guardar archivo cifrado
            saves_path = Path(self.config.get("paths", "saves", "saves"))
            save_file = saves_path / f"save_{slot}.dat"

            with open(save_file, "wb") as f:
                f.write(encrypted_data)

            # Actualizar archivo de información
            self._update_pickle_save_info(slot, game_state)

            self.logger.info("Juego guardado con pickle en slot %d", slot)
            return True

        except Exception as e:
            self.logger.error("Error guardando con pickle slot %d: %s", slot, e)
            return False

    def _migrate_pickle_to_sqlite(self, slot: int, pickle_data: dict[str, Any]) -> bool:
        """
        Migra datos pickle específicos a SQLite.

        Args:
            slot: Número de slot
            pickle_data: Datos del archivo pickle

        Returns:
            True si la migración fue exitosa
        """
        if not self.database:
            return False

        try:
            return self.database.migrate_pickle_to_database(pickle_data, slot)
        except Exception as e:
            self.logger.error("Error migrando pickle a SQLite slot %d: %s", slot, e)
            return False

    def _update_pickle_save_info(self, slot: int, game_state) -> None:
        """
        Actualiza el archivo de información pickle.

        Args:
            slot: Número de slot
            game_state: Estado del juego
        """
        try:
            saves_path = Path(self.config.get("paths", "saves", "saves"))
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

        except Exception as e:
            self.logger.error("Error actualizando info pickle slot %d: %s", slot, e)

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
            saves_path = Path(self.config.get("paths", "saves", "saves"))
            cleaned_files = 0

            for i in range(1, 4):  # Slots 1-3
                save_file = saves_path / f"save_{i}.dat"
                info_file = saves_path / f"save_{i}_info.json"

                if save_file.exists():
                    save_file.unlink()
                    cleaned_files += 1

                if info_file.exists():
                    info_file.unlink()
                    cleaned_files += 1

            self.logger.info("Limpiados %d archivos pickle antiguos", cleaned_files)
            return True

        except Exception as e:
            self.logger.error("Error limpiando archivos pickle: %s", e)
            return False
