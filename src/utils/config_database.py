"""
ConfigDatabase - Interfaz SQLite para Sistema Mixto Inteligente (Refactorizada)
===============================================================================

Autor: SiK Team
Fecha: 2 Agosto 2025
Descripción: Interfaz principal para datos complejos en sistema mixto.
Sistema mixto inteligente: SQLite para datos complejos, JSON para configuración simple.

REFACTORIZADA: Ahora orquesta clases especializadas para mejor mantenibilidad.

Gestiona:
- Datos de personajes (characters.json → SQLite)
- Configuración de enemigos (enemies.json → SQLite)
- Estadísticas y datos que requieren consultas complejas

NO gestiona:
- Configuración de usuario (audio.json, display.json)
- Variables frecuentemente modificadas (gameplay.json)
- Configuración simple (ui.json, input.json)
"""

import logging
import sqlite3
from typing import Any

from .character_database import CharacterDatabase
from .database_manager import DatabaseManager
from .enemy_database import EnemyDatabase


class ConfigDatabase:
    """
    Interfaz principal SQLite para datos de configuración complejos del sistema mixto.
    Orquesta las clases especializadas CharacterDatabase y EnemyDatabase.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa la interfaz de configuración SQLite.

        Args:
            database_manager: Instancia del gestor de base de datos
        """
        self.db_manager = database_manager
        self.logger = logging.getLogger(__name__)

        # Inicializar clases especializadas
        self.characters = CharacterDatabase(database_manager)
        self.enemies = EnemyDatabase(database_manager)

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

    # === MÉTODOS DELEGADOS PARA COMPATIBILIDAD ===
    # Mantiene la API original para no romper el código existente

    def get_character_data(self, character_name: str) -> dict[str, Any] | None:
        """Delega a CharacterDatabase. Mantiene compatibilidad de API."""
        return self.characters.get_character_data(character_name)

    def get_all_characters(self) -> list[dict[str, Any]]:
        """Delega a CharacterDatabase. Mantiene compatibilidad de API."""
        return self.characters.get_all_characters()

    def save_character_data(self, character_data: dict[str, Any]) -> bool:
        """Delega a CharacterDatabase. Mantiene compatibilidad de API."""
        return self.characters.save_character_data(character_data)

    def get_enemy_data(self, enemy_type: str) -> dict[str, Any] | None:
        """Delega a EnemyDatabase. Mantiene compatibilidad de API."""
        return self.enemies.get_enemy_data(enemy_type)

    def get_all_enemies(self) -> list[dict[str, Any]]:
        """Delega a EnemyDatabase. Mantiene compatibilidad de API."""
        return self.enemies.get_all_enemies()

    def save_enemy_data(self, enemy_data: dict[str, Any]) -> bool:
        """Delega a EnemyDatabase. Mantiene compatibilidad de API."""
        return self.enemies.save_enemy_data(enemy_data)

    def migrate_characters_from_json(self, json_file_path: str) -> bool:
        """Delega a CharacterDatabase. Mantiene compatibilidad de API."""
        return self.characters.migrate_characters_from_json(json_file_path)

    def migrate_enemies_from_json(self, json_file_path: str) -> bool:
        """Delega a EnemyDatabase. Mantiene compatibilidad de API."""
        return self.enemies.migrate_enemies_from_json(json_file_path)
