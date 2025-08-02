"""
EnemyDatabase - Interfaz SQLite para Datos de Enemigos
======================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Gestión especializada de datos de enemigos en SQLite.

Responsabilidades:
- Obtener configuración de tipos de enemigos
- Listar todos los enemigos disponibles
- Guardar y actualizar datos de enemigos
- Migración desde enemies.json
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

from .database_manager import DatabaseManager


class EnemyDatabase:
    """
    Interfaz SQLite especializada para datos de enemigos.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa la interfaz de enemigos SQLite.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self.logger = logging.getLogger(__name__)

    def get_enemy_data(self, enemy_type: str) -> dict[str, Any] | None:
        """
        Obtiene datos completos de un tipo de enemigo desde SQLite.

        Args:
            enemy_type: Tipo de enemigo ('goblin', 'orc', 'skeleton', etc.)

        Returns:
            Diccionario con datos del enemigo o None si no existe
        """
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
                    self.logger.warning(
                        "Tipo de enemigo '%s' no encontrado", enemy_type
                    )
                    return None

                return {
                    "tipo": row[0],
                    "nombre_mostrar": row[1],
                    "stats": json.loads(row[2]) if row[2] else {},
                    "comportamiento": row[3],
                    "animaciones": json.loads(row[4]) if row[4] else {},
                    "variantes": json.loads(row[5]) if row[5] else {},
                }

        except (sqlite3.Error, json.JSONDecodeError, AttributeError) as e:
            self.logger.error(
                "Error obteniendo datos del enemigo '%s': %s", enemy_type, e
            )
            return None

    def get_all_enemies(self) -> list[dict[str, Any]]:
        """
        Obtiene la lista completa de tipos de enemigos disponibles.

        Returns:
            Lista de diccionarios con datos de todos los enemigos activos
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT tipo, nombre_mostrar, stats, comportamiento,
                           animaciones, variantes
                    FROM enemigos
                    WHERE activo = 1
                    ORDER BY nombre_mostrar
                """
                )

                enemies = []
                for row in cursor.fetchall():
                    enemy_data = {
                        "tipo": row[0],
                        "nombre_mostrar": row[1],
                        "stats": json.loads(row[2]) if row[2] else {},
                        "comportamiento": row[3],
                        "animaciones": json.loads(row[4]) if row[4] else {},
                        "variantes": json.loads(row[5]) if row[5] else {},
                    }
                    enemies.append(enemy_data)

                self.logger.debug(
                    "Obtenidos %s tipos de enemigos de la base de datos", len(enemies)
                )
                return enemies

        except (sqlite3.Error, json.JSONDecodeError, AttributeError) as e:
            self.logger.error("Error obteniendo lista de enemigos: %s", e)
            return []

    def save_enemy_data(self, enemy_data: dict[str, Any]) -> bool:
        """
        Guarda o actualiza datos de un tipo de enemigo en SQLite.

        Args:
            enemy_data: Diccionario con datos del enemigo

        Returns:
            True si se guardó exitosamente, False en caso de error
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO enemigos
                    (tipo, nombre_mostrar, stats, comportamiento, animaciones, variantes, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        enemy_data.get("tipo", ""),
                        enemy_data.get("nombre_mostrar", ""),
                        json.dumps(enemy_data.get("stats", {}), ensure_ascii=False),
                        enemy_data.get("comportamiento", "perseguir"),
                        json.dumps(
                            enemy_data.get("animaciones", {}), ensure_ascii=False
                        ),
                        json.dumps(enemy_data.get("variantes", {}), ensure_ascii=False),
                        enemy_data.get("activo", True),
                    ),
                )
                conn.commit()
                self.logger.debug(
                    "Enemigo '%s' guardado exitosamente", enemy_data.get("tipo")
                )
                return True

        except (sqlite3.Error, TypeError, KeyError) as e:
            self.logger.error("Error guardando datos del enemigo: %s", e)
            return False

    def migrate_enemies_from_json(self, json_file_path: str) -> bool:
        """
        Migra enemigos desde enemies.json a SQLite.

        Args:
            json_file_path: Ruta al archivo enemies.json

        Returns:
            True si la migración fue exitosa, False en caso de error
        """
        try:
            json_path = Path(json_file_path)
            if not json_path.exists():
                self.logger.error(
                    "Archivo enemies.json no encontrado: %s", json_file_path
                )
                return False

            with open(json_path, encoding="utf-8") as f:
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
