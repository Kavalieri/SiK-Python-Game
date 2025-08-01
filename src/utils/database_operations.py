"""
DatabaseOperations - Operaciones SQLite avanzadas

Gestiona queries, transacciones, backup y mantenimiento de BD.
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .database_connection import DatabaseConnection


class DatabaseOperations:
    """Operaciones SQLite avanzadas con transacciones y mantenimiento."""

    def __init__(self, connection_manager: DatabaseConnection):
        self.connection = connection_manager
        self._logger = logging.getLogger("DatabaseOperations")

    def execute_query(
        self,
        query: str,
        params: Optional[Union[tuple, Dict[str, Any]]] = None,
        fetch_results: bool = True,
    ) -> Optional[List[Dict[str, Any]]]:
        """Ejecuta query SQL con parámetros opcionales."""
        try:
            with self.connection.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch_results:
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows] if rows else []
                return None
        except sqlite3.Error as e:
            self._logger.error("Error ejecutando query: %s - Query: %s", e, query)
            raise RuntimeError(f"Error ejecutando query: {e}") from e

    @contextmanager
    def transaction(self):
        """Context manager para transacciones SQLite."""
        try:
            with self.connection.get_connection() as conn:
                conn.execute("BEGIN")
                self._logger.debug("Transacción iniciada")
                yield conn
                conn.commit()
                self._logger.debug("Transacción confirmada")
        except sqlite3.Error as e:
            self._logger.error("Error en transacción: %s", e)
            conn.rollback()
            self._logger.debug("Transacción revertida")
            raise

    def backup_database(self, backup_path: str) -> bool:
        """Crea backup de la base de datos."""
        try:
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            with self.connection.get_connection() as source_conn:
                backup_conn = sqlite3.connect(str(backup_file))
                source_conn.backup(backup_conn)
                backup_conn.close()
            self._logger.info("Backup creado: %s", backup_path)
            return True
        except (sqlite3.Error, OSError) as e:
            self._logger.error("Error creando backup: %s", e)
            return False

    def vacuum_database(self) -> bool:
        """Optimiza la base de datos con VACUUM."""
        try:
            with self.connection.get_connection() as conn:
                conn.execute("VACUUM")
                conn.commit()
            self._logger.info("Base de datos optimizada con VACUUM")
            return True
        except sqlite3.Error as e:
            self._logger.error("Error en VACUUM: %s", e)
            return False
