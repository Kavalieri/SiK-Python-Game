"""Save Database - Interfaz SQLite para Guardado"""

import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

from .database_manager import DatabaseManager
from .save_encryption import SaveEncryption


class SaveDatabase:
    """Interfaz SQLite para el sistema de guardado."""

    def __init__(
        self, database_manager: DatabaseManager, encryption_handler: SaveEncryption
    ):
        self.db_manager = database_manager
        self.encryption_handler = encryption_handler
        self.logger = logging.getLogger(__name__)

    def save_game_to_database(
        self, slot: int, game_state, additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Guarda el estado del juego en la base de datos SQLite encriptado.

        Args:
            slot: Número del slot de guardado (1-3)
            game_state: Estado del juego a guardar
            additional_data: Datos adicionales opcionales

        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        """
        try:
            game_data = {
                "game_state": game_state.get_state_dict(),
                "additional_data": additional_data or {},
            }
            json_data = json.dumps(game_data, ensure_ascii=False)
            encrypted_package = self.encryption_handler.create_encrypted_package(
                json_data.encode()
            )
            save_data = {
                "slot": slot,
                "nombre_jugador": getattr(game_state, "player_name", f"Jugador {slot}"),
                "descripcion": (
                    f"Partida guardada - Nivel {getattr(game_state, 'level', 1)}"
                ),
                "nivel_actual": getattr(game_state, "level", 1),
                "puntuacion": getattr(game_state, "score", 0),
                "vidas": getattr(game_state, "lives", 3),
                "tiempo_jugado": getattr(game_state, "play_time", 0),
                "personaje": getattr(game_state, "selected_character", "guerrero"),
                "estado_juego": json.dumps(encrypted_package, ensure_ascii=False),
                "actualizado_en": datetime.now().isoformat(),
            }
            query = "INSERT OR REPLACE INTO partidas_guardadas (slot, nombre_jugador, descripcion, nivel_actual, puntuacion, vidas, tiempo_jugado, personaje, estado_juego, actualizado_en, creado_en) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT creado_en FROM partidas_guardadas WHERE slot = ?), ?))"
            params = (
                save_data["slot"],
                save_data["nombre_jugador"],
                save_data["descripcion"],
                save_data["nivel_actual"],
                save_data["puntuacion"],
                save_data["vidas"],
                save_data["tiempo_jugado"],
                save_data["personaje"],
                save_data["estado_juego"],
                save_data["actualizado_en"],
                save_data["slot"],
                save_data["actualizado_en"],
            )
            result = self.db_manager.execute_query(query, params)
            if result:
                self.logger.info("Partida guardada exitosamente en slot %d", slot)
                return True
            else:
                self.logger.error("Error guardando partida en slot %d", slot)
                return False
        except (sqlite3.Error, json.JSONDecodeError, ValueError) as e:
            self.logger.error("Error guardando en base de datos slot %d: %s", slot, e)
            return False

    def load_game_from_database(self, slot: int) -> Optional[Dict[str, Any]]:
        """Carga el estado del juego desde la base de datos SQLite.

        Args:
            slot: Número del slot de guardado (1-3)

        Returns:
            Optional[Dict[str, Any]]: Datos del juego o None si no existe
        """
        try:
            query = "SELECT * FROM partidas_guardadas WHERE slot = ?"
            results = self.db_manager.execute_query(query, (slot,), fetch_results=True)
            if not results:
                self.logger.info("No se encontró partida en slot %d", slot)
                return None
            save_record = results[0]
            # Acceso por índices usando variables para evitar errores de tipo
            idx_encrypted_data = 9
            idx_slot = 1
            idx_nombre = 2
            idx_descripcion = 3
            idx_nivel = 4
            idx_puntuacion = 5
            idx_vidas = 6
            idx_tiempo = 7
            idx_personaje = 8
            idx_encrypted_data = 9
            idx_creado = 10
            idx_actualizado = 11

            encrypted_package_json = save_record[idx_encrypted_data]  # type: ignore[index]
            encrypted_package = json.loads(encrypted_package_json)
            decrypted_data = self.encryption_handler.extract_encrypted_package(
                encrypted_package
            )
            game_data = json.loads(decrypted_data.decode())
            complete_data = {
                "game_state": game_data["game_state"],
                "additional_data": game_data["additional_data"],
                "save_metadata": {
                    "slot": save_record[idx_slot],  # type: ignore[index]
                    "nombre_jugador": save_record[idx_nombre],  # type: ignore[index]
                    "descripcion": save_record[idx_descripcion],  # type: ignore[index]
                    "nivel_actual": save_record[idx_nivel],  # type: ignore[index]
                    "puntuacion": save_record[idx_puntuacion],  # type: ignore[index]
                    "vidas": save_record[idx_vidas],  # type: ignore[index]
                    "tiempo_jugado": save_record[idx_tiempo],  # type: ignore[index]
                    "personaje": save_record[idx_personaje],  # type: ignore[index]
                    "creado_en": save_record[idx_creado],  # type: ignore[index]
                    "actualizado_en": save_record[idx_actualizado],  # type: ignore[index]
                },
            }
            self.logger.info("Partida cargada exitosamente desde slot %d", slot)
            return complete_data
        except (sqlite3.Error, json.JSONDecodeError, ValueError) as e:
            self.logger.error("Error cargando desde base de datos slot %d: %s", slot, e)
            return None

    def get_all_saves_info(self) -> List[Dict[str, Any]]:
        """Obtiene información de todas las partidas guardadas.

        Returns:
            List[Dict[str, Any]]: Lista con información de partidas guardadas
        """
        try:
            query = (
                "SELECT slot, nombre_jugador, descripcion, nivel_actual, "
                "puntuacion, vidas, tiempo_jugado, personaje, creado_en, "
                "actualizado_en FROM partidas_guardadas ORDER BY slot"
            )
            results = self.db_manager.execute_query(query, fetch_results=True)
            saves_info = []
            if results:
                for row in results:
                    # Índices de columnas usando variables
                    idx_slot = 0
                    idx_nombre = 1
                    idx_descripcion = 2
                    idx_nivel = 3
                    idx_puntuacion = 4
                    idx_vidas = 5
                    idx_tiempo = 6
                    idx_personaje = 7
                    idx_creado = 8
                    idx_actualizado = 9

                    save_info = {
                        "file_number": row[idx_slot],  # type: ignore[index]
                        "exists": True,
                        "player_name": row[idx_nombre],  # type: ignore[index]
                        "description": row[idx_descripcion],  # type: ignore[index]
                        "level": row[idx_nivel],  # type: ignore[index]
                        "score": row[idx_puntuacion],  # type: ignore[index]
                        "lives": row[idx_vidas],  # type: ignore[index]
                        "play_time": row[idx_tiempo],  # type: ignore[index]
                        "character": row[idx_personaje],  # type: ignore[index]
                        "created_at": row[idx_creado],  # type: ignore[index]
                        "last_used": row[idx_actualizado],  # type: ignore[index]
                    }
                    saves_info.append(save_info)
            return saves_info
        except (sqlite3.Error, ValueError) as e:
            self.logger.error("Error obteniendo información de partidas: %s", e)
            return []

    def delete_save_from_database(self, slot: int) -> bool:
        """Elimina una partida guardada de la base de datos.

        Args:
            slot: Número del slot de guardado (1-3)

        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            query = "DELETE FROM partidas_guardadas WHERE slot = ?"
            result = self.db_manager.execute_query(query, (slot,))
            if result:
                self.logger.info("Partida eliminada exitosamente del slot %d", slot)
                return True
            else:
                self.logger.warning(
                    "No se encontró partida para eliminar en slot %d", slot
                )
                return False
        except (sqlite3.Error, ValueError) as e:
            self.logger.error("Error eliminando partida del slot %d: %s", slot, e)
            return False

    def migrate_pickle_to_database(
        self, pickle_data: Dict[str, Any], slot: int
    ) -> bool:
        """Migra datos de pickle a la base de datos SQLite.

        Args:
            pickle_data: Datos deserializados del archivo pickle
            slot: Número del slot de guardado (1-3)

        Returns:
            bool: True si se migró exitosamente, False en caso contrario
        """
        try:
            if "game_state" not in pickle_data:
                self.logger.error("Datos pickle inválidos - falta game_state")
                return False

            class TempGameState:
                """Clase temporal para compatibilidad con datos pickle."""

                def __init__(self, state_dict):
                    """Inicializa el estado temporal desde diccionario."""
                    for key, value in state_dict.items():
                        setattr(self, key, value)

                def get_state_dict(self):
                    """Obtiene el estado como diccionario."""
                    return self.__dict__

            temp_game_state = TempGameState(pickle_data["game_state"])
            additional_data = pickle_data.get("additional_data", {})
            success = self.save_game_to_database(slot, temp_game_state, additional_data)
            if success:
                self.logger.info("Migración pickle → SQLite exitosa para slot %d", slot)
            return success
        except (sqlite3.Error, ValueError, json.JSONDecodeError) as e:
            self.logger.error(
                "Error migrando pickle a SQLite slot %d: %s", slot, str(e)
            )
            return False
