"""
Save Database - Interfaz SQLite para Guardado
==============================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo para interfaz con base de datos SQLite para el sistema de guardado.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from .database_manager import DatabaseManager
from .save_encryption import SaveEncryption


class SaveDatabase:
    """
    Interfaz SQLite para el sistema de guardado.
    """

    def __init__(
        self, database_manager: DatabaseManager, encryption_handler: SaveEncryption
    ):
        """
        Inicializa la interfaz de base de datos.

        Args:
            database_manager: Gestor de base de datos
            encryption_handler: Manejador de encriptación
        """
        self.db_manager = database_manager
        self.encryption_handler = encryption_handler
        self.logger = logging.getLogger(__name__)

    def save_game_to_database(
        self, slot: int, game_state, additional_data: Dict[str, Any] = None
    ) -> bool:
        """
        Guarda el estado del juego en la base de datos SQLite.

        Args:
            slot: Número de slot (1-3)
            game_state: Estado del juego a guardar
            additional_data: Datos adicionales

        Returns:
            True si se guardó correctamente
        """
        try:
            # Preparar datos para guardado
            game_data = {
                "game_state": game_state.get_state_dict(),
                "additional_data": additional_data or {},
            }

            # Convertir a JSON para encriptar
            json_data = json.dumps(game_data, ensure_ascii=False)

            # Encriptar datos del estado del juego
            encrypted_package = self.encryption_handler.create_encrypted_package(
                json_data.encode()
            )

            # Preparar datos para la base de datos
            save_data = {
                "slot": slot,
                "nombre_jugador": getattr(game_state, "player_name", f"Jugador {slot}"),
                "descripcion": f"Partida guardada - Nivel {getattr(game_state, 'level', 1)}",
                "nivel_actual": getattr(game_state, "level", 1),
                "puntuacion": getattr(game_state, "score", 0),
                "vidas": getattr(game_state, "lives", 3),
                "tiempo_jugado": getattr(game_state, "play_time", 0),
                "personaje": getattr(game_state, "selected_character", "guerrero"),
                "estado_juego": json.dumps(encrypted_package, ensure_ascii=False),
                "actualizado_en": datetime.now().isoformat(),
            }

            # Ejecutar query de inserción/actualización
            query = """
                INSERT OR REPLACE INTO partidas_guardadas
                (slot, nombre_jugador, descripcion, nivel_actual, puntuacion, vidas,
                 tiempo_jugado, personaje, estado_juego, actualizado_en, creado_en)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                 COALESCE((SELECT creado_en FROM partidas_guardadas WHERE slot = ?), ?))
            """

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

        except Exception as e:
            self.logger.error("Error guardando en base de datos slot %d: %s", slot, e)
            return False

    def load_game_from_database(self, slot: int) -> Optional[Dict[str, Any]]:
        """
        Carga el estado del juego desde la base de datos SQLite.

        Args:
            slot: Número de slot (1-3)

        Returns:
            Datos del juego o None si hay error
        """
        try:
            query = "SELECT * FROM partidas_guardadas WHERE slot = ?"
            results = self.db_manager.execute_query(query, (slot,), fetch_results=True)

            if not results:
                self.logger.info("No se encontró partida en slot %d", slot)
                return None

            save_record = results[0]

            # Extraer y desencriptar datos del estado del juego
            encrypted_package_json = save_record[9]  # estado_juego column
            encrypted_package = json.loads(encrypted_package_json)

            # Desencriptar datos
            decrypted_data = self.encryption_handler.extract_encrypted_package(
                encrypted_package
            )
            game_data = json.loads(decrypted_data.decode())

            # Combinar con metadatos de la base de datos
            complete_data = {
                "game_state": game_data["game_state"],
                "additional_data": game_data["additional_data"],
                "save_metadata": {
                    "slot": save_record[1],  # slot
                    "nombre_jugador": save_record[2],  # nombre_jugador
                    "descripcion": save_record[3],  # descripcion
                    "nivel_actual": save_record[4],  # nivel_actual
                    "puntuacion": save_record[5],  # puntuacion
                    "vidas": save_record[6],  # vidas
                    "tiempo_jugado": save_record[7],  # tiempo_jugado
                    "personaje": save_record[8],  # personaje
                    "creado_en": save_record[10],  # creado_en
                    "actualizado_en": save_record[11],  # actualizado_en
                },
            }

            self.logger.info("Partida cargada exitosamente desde slot %d", slot)
            return complete_data

        except Exception as e:
            self.logger.error("Error cargando desde base de datos slot %d: %s", slot, e)
            return None

    def get_all_saves_info(self) -> List[Dict[str, Any]]:
        """
        Obtiene información de todas las partidas guardadas.

        Returns:
            Lista con información de partidas
        """
        try:
            query = """
                SELECT slot, nombre_jugador, descripcion, nivel_actual, puntuacion,
                       vidas, tiempo_jugado, personaje, creado_en, actualizado_en
                FROM partidas_guardadas
                ORDER BY slot
            """

            results = self.db_manager.execute_query(query, fetch_results=True)

            saves_info = []
            for row in results:
                save_info = {
                    "file_number": row[0],  # slot
                    "exists": True,
                    "player_name": row[1],  # nombre_jugador
                    "description": row[2],  # descripcion
                    "level": row[3],  # nivel_actual
                    "score": row[4],  # puntuacion
                    "lives": row[5],  # vidas
                    "play_time": row[6],  # tiempo_jugado
                    "character": row[7],  # personaje
                    "created_at": row[8],  # creado_en
                    "last_used": row[9],  # actualizado_en
                }
                saves_info.append(save_info)

            return saves_info

        except Exception as e:
            self.logger.error("Error obteniendo información de partidas: %s", e)
            return []

    def delete_save_from_database(self, slot: int) -> bool:
        """
        Elimina una partida guardada de la base de datos.

        Args:
            slot: Número de slot (1-3)

        Returns:
            True si se eliminó correctamente
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

        except Exception as e:
            self.logger.error("Error eliminando partida del slot %d: %s", slot, e)
            return False

    def migrate_pickle_to_database(
        self, pickle_data: Dict[str, Any], slot: int
    ) -> bool:
        """
        Migra datos de pickle a la base de datos SQLite.

        Args:
            pickle_data: Datos del archivo pickle
            slot: Número de slot destino

        Returns:
            True si la migración fue exitosa
        """
        try:
            # Extraer game_state de los datos pickle
            if "game_state" not in pickle_data:
                self.logger.error("Datos pickle inválidos - falta game_state")
                return False

            # Crear un objeto temporal para la migración
            class TempGameState:
                def __init__(self, state_dict):
                    for key, value in state_dict.items():
                        setattr(self, key, value)

                def get_state_dict(self):
                    return self.__dict__

            temp_game_state = TempGameState(pickle_data["game_state"])
            additional_data = pickle_data.get("additional_data", {})

            # Guardar usando el método estándar
            success = self.save_game_to_database(slot, temp_game_state, additional_data)

            if success:
                self.logger.info("Migración pickle → SQLite exitosa para slot %d", slot)

            return success

        except Exception as e:
            self.logger.error("Error migrando pickle a SQLite slot %d: %s", slot, e)
            return False
