"""
CharacterDatabase - Interfaz SQLite para Datos de Personajes
===========================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Gestión especializada de datos de personajes en SQLite.

Responsabilidades:
- Obtener datos completos de personajes
- Listar todos los personajes disponibles
- Guardar y actualizar datos de personajes
- Migración desde characters.json
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

from .database_manager import DatabaseManager


class CharacterDatabase:
    """
    Interfaz SQLite especializada para datos de personajes.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa la interfaz de personajes SQLite.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self.logger = logging.getLogger(__name__)

    def get_character_data(self, character_name: str) -> dict[str, Any] | None:
        """
        Obtiene datos completos de un personaje desde SQLite.

        Args:
            character_name: Nombre del personaje ('guerrero', 'adventureguirl', etc.)

        Returns:
            Diccionario con datos del personaje o None si no existe
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT nombre, nombre_mostrar, tipo, descripcion,
                           stats, ataques, sprite_config
                    FROM personajes
                    WHERE nombre = ? AND activo = 1
                """,
                    (character_name,),
                )

                row = cursor.fetchone()
                if not row:
                    self.logger.warning("Personaje '%s' no encontrado", character_name)
                    return None

                return {
                    "nombre": row[0],
                    "nombre_mostrar": row[1],
                    "tipo": row[2],
                    "descripcion": row[3],
                    "stats": json.loads(row[4]) if row[4] else {},
                    "ataques": json.loads(row[5]) if row[5] else [],
                    "sprite_config": json.loads(row[6]) if row[6] else {},
                }

        except (sqlite3.Error, json.JSONDecodeError, AttributeError) as e:
            self.logger.error(
                "Error obteniendo datos del personaje '%s': %s", character_name, e
            )
            return None

    def get_all_characters(self) -> list[dict[str, Any]]:
        """
        Obtiene la lista completa de personajes disponibles.

        Returns:
            Lista de diccionarios con datos de todos los personajes activos
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT nombre, nombre_mostrar, tipo, descripcion,
                           stats, ataques, sprite_config
                    FROM personajes
                    WHERE activo = 1
                    ORDER BY nombre_mostrar
                """
                )

                characters = []
                for row in cursor.fetchall():
                    character_data = {
                        "nombre": row[0],
                        "nombre_mostrar": row[1],
                        "tipo": row[2],
                        "descripcion": row[3],
                        "stats": json.loads(row[4]) if row[4] else {},
                        "ataques": json.loads(row[5]) if row[5] else [],
                        "sprite_config": json.loads(row[6]) if row[6] else {},
                    }
                    characters.append(character_data)

                self.logger.debug(
                    "Obtenidos %s personajes de la base de datos", len(characters)
                )
                return characters

        except (sqlite3.Error, json.JSONDecodeError, AttributeError) as e:
            self.logger.error("Error obteniendo lista de personajes: %s", e)
            return []

    def save_character_data(self, character_data: dict[str, Any]) -> bool:
        """
        Guarda o actualiza datos de un personaje en SQLite.

        Args:
            character_data: Diccionario con datos del personaje

        Returns:
            True si se guardó exitosamente, False en caso de error
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO personajes
                    (nombre, nombre_mostrar, tipo, descripcion, stats, ataques, sprite_config, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        character_data.get("nombre", ""),
                        character_data.get("nombre_mostrar", ""),
                        character_data.get("tipo", ""),
                        character_data.get("descripcion", ""),
                        json.dumps(character_data.get("stats", {}), ensure_ascii=False),
                        json.dumps(
                            character_data.get("ataques", []), ensure_ascii=False
                        ),
                        json.dumps(
                            character_data.get("sprite_config", {}), ensure_ascii=False
                        ),
                        character_data.get("activo", True),
                    ),
                )
                conn.commit()
                self.logger.debug(
                    "Personaje '%s' guardado exitosamente", character_data.get("nombre")
                )
                return True

        except (sqlite3.Error, TypeError, KeyError) as e:
            self.logger.error("Error guardando datos del personaje: %s", e)
            return False

    def migrate_characters_from_json(self, json_file_path: str) -> bool:
        """
        Migra personajes desde characters.json a SQLite.

        Args:
            json_file_path: Ruta al archivo characters.json

        Returns:
            True si la migración fue exitosa, False en caso de error
        """
        try:
            json_path = Path(json_file_path)
            if not json_path.exists():
                self.logger.error(
                    "Archivo characters.json no encontrado: %s", json_file_path
                )
                return False

            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)

            characters = data.get("characters", {})
            migrated_count = 0

            for char_name, char_data in characters.items():
                character_record = {
                    "nombre": char_name,
                    "nombre_mostrar": char_data.get("nombre", char_name),
                    "tipo": char_data.get("tipo", ""),
                    "descripcion": char_data.get("descripcion", ""),
                    "stats": char_data.get("stats", {}),
                    "ataques": char_data.get("ataques", []),
                    "sprite_config": char_data.get("sprite_config", {}),
                    "activo": True,
                }

                if self.save_character_data(character_record):
                    migrated_count += 1

            self.logger.info(
                "Migrados %s personajes desde characters.json", migrated_count
            )
            return migrated_count > 0

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error migrando personajes desde JSON: %s", e)
            return False
