"""
DatabaseManager - Gestor de conexiones y operaciones SQLite

Gestiona conexiones SQLite con pooling, transacciones y logging.
Fase 1 de migración SQLite - Referencia: docs/PLAN_MIGRACION_SQLITE.md
"""

import logging
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any


class DatabaseManager:
    """Gestor centralizado de conexiones SQLite con pooling y transacciones."""

    def __init__(self, db_path: str = "saves/game_database.db", pool_size: int = 5):
        self.db_path = Path(db_path)
        self.pool_size = pool_size
        self._pool: list[sqlite3.Connection] = []
        self._pool_lock = threading.Lock()
        self._logger = logging.getLogger("DatabaseManager")

        # Crear directorio y pool
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_pool()
        self._logger.info("DatabaseManager inicializado: %s", self.db_path)

    def _initialize_pool(self) -> None:
        """Inicializa el pool de conexiones SQLite."""
        try:
            for _ in range(self.pool_size):
                self._pool.append(self._create_connection())
            self._logger.info("Pool creado: %d conexiones", self.pool_size)
        except sqlite3.Error as e:
            self._logger.error("Error inicializando pool: %s", e)
            raise RuntimeError(f"Error inicializando pool: {e}") from e

    def _create_connection(self) -> sqlite3.Connection:
        """Crea una nueva conexión SQLite optimizada."""
        try:
            conn = sqlite3.connect(
                str(self.db_path), timeout=30.0, check_same_thread=False
            )
            conn.row_factory = sqlite3.Row

            # Configuraciones optimizadas
            for pragma in [
                "PRAGMA journal_mode=WAL",
                "PRAGMA foreign_keys=ON",
                "PRAGMA synchronous=NORMAL",
                "PRAGMA cache_size=10000",
                "PRAGMA temp_store=MEMORY",
            ]:
                conn.execute(pragma)

            return conn
        except sqlite3.Error as e:
            self._logger.error("Error creando conexión: %s", e)
            raise RuntimeError(f"Error creando conexión: {e}") from e

    @contextmanager
    def get_connection(self):
        """Context manager para obtener conexión del pool."""
        conn = None
        try:
            with self._pool_lock:
                if self._pool:
                    conn = self._pool.pop()
                else:
                    conn = self._create_connection()

            yield conn

        except sqlite3.Error as e:
            self._logger.error("Error de conexión: %s", e)
            if conn:
                conn.rollback()
            raise RuntimeError(f"Error de base de datos: {e}") from e
        finally:
            if conn:
                with self._pool_lock:
                    if len(self._pool) < self.pool_size:
                        self._pool.append(conn)
                    else:
                        conn.close()

    def execute_query(
        self, query: str, params: tuple | None = None, fetch_all: bool = False
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Ejecuta query SQL y retorna resultados."""
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params or ())

                if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                    conn.commit()
                    return {
                        "rows_affected": cursor.rowcount,
                        "last_row_id": cursor.lastrowid,
                    }

                if fetch_all:
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows] if rows else []
                else:
                    row = cursor.fetchone()
                    return dict(row) if row else None

            except sqlite3.Error as e:
                self._logger.error("Error ejecutando query: %s", e)
                conn.rollback()
                raise RuntimeError(f"Error ejecutando query: {e}") from e

    @contextmanager
    def transaction(self):
        """Context manager para transacciones."""
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
                self._logger.debug("Transacción completada")
            except Exception as e:
                conn.rollback()
                self._logger.error("Transacción fallida: %s", e)
                raise

    def close_all_connections(self) -> None:
        """Cierra todas las conexiones del pool."""
        with self._pool_lock:
            while self._pool:
                try:
                    self._pool.pop().close()
                except sqlite3.Error:
                    pass
        self._logger.info("Todas las conexiones cerradas")

    def get_connection_info(self) -> dict[str, Any]:
        """Obtiene información del estado de conexiones."""
        with self._pool_lock:
            return {
                "db_path": str(self.db_path),
                "pool_size": self.pool_size,
                "available_connections": len(self._pool),
                "db_exists": self.db_path.exists(),
            }

    def backup_database(self, backup_path: str) -> bool:
        """Crea backup de la base de datos."""
        try:
            backup_file = Path(backup_path)
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            with self.get_connection() as source_conn:
                backup_conn = sqlite3.connect(str(backup_file))
                source_conn.backup(backup_conn)
                backup_conn.close()
            self._logger.info("Backup creado: %s", backup_path)
            return True
        except (sqlite3.Error, OSError) as e:
            self._logger.error("Error creando backup: %s", e)
            return False

    def vacuum_database(self) -> bool:
        """Optimiza la base de datos (VACUUM)."""
        try:
            with self.get_connection() as conn:
                conn.execute("VACUUM")
            self._logger.info("VACUUM completado")
            return True
        except sqlite3.Error as e:
            self._logger.error("Error en VACUUM: %s", e)
            return False
