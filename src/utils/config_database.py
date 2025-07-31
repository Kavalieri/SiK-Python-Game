"""
ConfigDatabase - Interfaz SQLite para Sistema Mixto Inteligente
================================================================

Autor: SiK Team
Fecha: 30 Julio 2025
Descripción: Interfaz SQLite para datos complejos en sistema mixto.
Sistema mixto inteligente: SQLite para datos complejos, JSON para configuración simple.

Gestiona:            self.logger.info("Migrados %s enemigos desde enemies.json", migrated_count)
            return migrated_count > 0

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error migrando enemigos desde JSON: %s", e)
            return Falseos de personajes (characters.json → SQLite)
- Configuración de enemigos (enemies.json → SQLite)
- Estadísticas y datos que requieren consultas complejas

NO gestiona:
- Configuración de usuario (audio.json, display.json)
- Variables frecuentemente modificadas (gameplay.json)
- Configuración simple (ui.json, input.json)
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from .database_manager import DatabaseManager


class ConfigDatabase:
    """
    Interfaz SQLite para datos de configuración complejos del sistema mixto.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa la interfaz de configuración SQLite.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self.logger = logging.getLogger(__name__)
        self._ensure_config_tables()

    def _ensure_config_tables(self):
        """Asegura que las tablas de configuración existan."""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND (name='personajes' OR name='enemigos')
                """)
                existing_tables = [row[0] for row in cursor.fetchall()]

                if len(existing_tables) < 2:
                    self.logger.info(
                        "Tablas de configuración incompletas, verificando SchemaManager..."
                    )

        except (sqlite3.Error, AttributeError, ValueError) as e:
            self.logger.error("Error verificando tablas de configuración: %s", e)

    # === MÉTODOS PARA PERSONAJES ===

    def get_character_data(self, character_name: str) -> Optional[Dict[str, Any]]:
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

        except (sqlite3.Error, json.JSONDecodeError, ValueError) as e:
            self.logger.error(
                "Error obteniendo datos del personaje '%s': %s", character_name, e
            )
            return None

    def get_all_characters(self) -> List[Dict[str, Any]]:
        """Obtiene todos los personajes activos."""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nombre, nombre_mostrar, tipo, descripcion,
                           stats, ataques, sprite_config
                    FROM personajes
                    WHERE activo = 1
                    ORDER BY nombre
                """)

                characters = []
                for row in cursor.fetchall():
                    characters.append(
                        {
                            "nombre": row[0],
                            "nombre_mostrar": row[1],
                            "tipo": row[2],
                            "descripcion": row[3],
                            "stats": json.loads(row[4]) if row[4] else {},
                            "ataques": json.loads(row[5]) if row[5] else [],
                            "sprite_config": json.loads(row[6]) if row[6] else {},
                        }
                    )

                return characters

        except (sqlite3.Error, json.JSONDecodeError) as e:
            self.logger.error("Error obteniendo lista de personajes: %s", e)
            return []

    def save_character_data(self, character_data: Dict[str, Any]) -> bool:
        """Guarda o actualiza datos de un personaje."""
        try:
            with self.db_manager.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO personajes
                    (nombre, nombre_mostrar, tipo, descripcion, stats,
                     ataques, sprite_config, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        character_data.get("nombre"),
                        character_data.get("nombre_mostrar", ""),
                        character_data.get("tipo", ""),
                        character_data.get("descripcion", ""),
                        json.dumps(character_data.get("stats", {})),
                        json.dumps(character_data.get("ataques", [])),
                        json.dumps(character_data.get("sprite_config", {})),
                        character_data.get("activo", True),
                    ),
                )

                self.logger.info(
                    "Personaje '%s' guardado exitosamente", character_data.get("nombre")
                )
                return True

        except (sqlite3.Error, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error guardando personaje: %s", e)
            return False

    # === MÉTODOS PARA ENEMIGOS ===

    def get_enemy_data(self, enemy_type: str) -> Optional[Dict[str, Any]]:
        """Obtiene datos de configuración de un enemigo."""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT tipo, nombre_mostrar, stats, comportamiento,
                           animaciones, variantes
                    FROM enemigos
                    WHERE tipo = ? AND activo = 1
                """,
                    (enemy_type,),
                )

                row = cursor.fetchone()
                if not row:
                    self.logger.warning("Enemigo '%s' no encontrado", enemy_type)
                    return None

                return {
                    "tipo": row[0],
                    "nombre_mostrar": row[1],
                    "stats": json.loads(row[2]) if row[2] else {},
                    "comportamiento": row[3],
                    "animaciones": json.loads(row[4]) if row[4] else {},
                    "variantes": json.loads(row[5]) if row[5] else {},
                }

        except (sqlite3.Error, json.JSONDecodeError, ValueError) as e:
            self.logger.error(
                "Error obteniendo datos del enemigo '%s': %s", enemy_type, e
            )
            return None

    def get_all_enemies(self) -> List[Dict[str, Any]]:
        """Obtiene todos los tipos de enemigos activos."""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT tipo, nombre_mostrar, stats, comportamiento,
                           animaciones, variantes
                    FROM enemigos
                    WHERE activo = 1
                    ORDER BY tipo
                """)

                enemies = []
                for row in cursor.fetchall():
                    enemies.append(
                        {
                            "tipo": row[0],
                            "nombre_mostrar": row[1],
                            "stats": json.loads(row[2]) if row[2] else {},
                            "comportamiento": row[3],
                            "animaciones": json.loads(row[4]) if row[4] else {},
                            "variantes": json.loads(row[5]) if row[5] else {},
                        }
                    )

                return enemies

        except (sqlite3.Error, json.JSONDecodeError) as e:
            self.logger.error("Error obteniendo lista de enemigos: %s", e)
            return []

    def save_enemy_data(self, enemy_data: Dict[str, Any]) -> bool:
        """Guarda o actualiza datos de un enemigo."""
        try:
            with self.db_manager.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO enemigos
                    (tipo, nombre_mostrar, stats, comportamiento, animaciones, variantes, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        enemy_data.get("tipo"),
                        enemy_data.get("nombre_mostrar", ""),
                        json.dumps(enemy_data.get("stats", {})),
                        enemy_data.get("comportamiento", "perseguir"),
                        json.dumps(enemy_data.get("animaciones", {})),
                        json.dumps(enemy_data.get("variantes", {})),
                        enemy_data.get("activo", True),
                    ),
                )

                self.logger.info(
                    "Enemigo '%s' guardado exitosamente", enemy_data.get("tipo")
                )
                return True

        except (sqlite3.Error, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error guardando enemigo: %s", e)
            return False

    # === MÉTODOS DE MIGRACIÓN DESDE JSON ===

    def migrate_characters_from_json(self, json_file_path: str) -> bool:
        """Migra personajes desde characters.json a SQLite."""
        try:
            json_path = Path(json_file_path)
            if not json_path.exists():
                self.logger.error(
                    "Archivo characters.json no encontrado: %s", json_file_path
                )
                return False

            with open(json_path, "r", encoding="utf-8") as f:
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

    def migrate_enemies_from_json(self, json_file_path: str) -> bool:
        """Migra enemigos desde enemies.json a SQLite."""
        try:
            json_path = Path(json_file_path)
            if not json_path.exists():
                self.logger.error(
                    "Archivo enemies.json no encontrado: %s", json_file_path
                )
                return False

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            enemies = data.get("tipos_enemigos", {})
            migrated_count = 0

            for enemy_type, enemy_data in enemies.items():
                enemy_record = {
                    "tipo": enemy_type,
                    "nombre_mostrar": enemy_data.get("nombre", enemy_type),
                    "stats": enemy_data.get("stats", {}),
                    "comportamiento": enemy_data.get("comportamiento", "perseguir"),
                    "animaciones": enemy_data.get("animaciones", {}),
                    "variantes": enemy_data.get("variantes", {}),
                    "activo": True,
                }

                if self.save_enemy_data(enemy_record):
                    migrated_count += 1

            self.logger.info("Migrados %s enemigos desde enemies.json", migrated_count)
            return migrated_count > 0

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            self.logger.error("Error migrando enemigos desde JSON: %s", e)
            return False
