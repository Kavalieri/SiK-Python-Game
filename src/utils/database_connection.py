"""
DatabaseConnection - Gestor de conexiones SQLite con pooling

Gestiona el pool de conexiones, configuración y conexiones básicas.
"""

import logging
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, List


class DatabaseConnection:
    """Gestor de conexiones SQLite con pooling optimizado."""

    def __init__(self, db_path: str = "saves/game_database.db", pool_size: int = 5):
        self.db_path = Path(db_path)
        self.pool_size = pool_size
        self._pool: List[sqlite3.Connection] = []
        self._pool_lock = threading.Lock()
        self._logger = logging.getLogger("DatabaseConnection")

        # Crear directorio y pool
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_pool()
        self._logger.info("DatabaseConnection inicializado: %s", self.db_path)

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

            # Configuraciones optimizadas consolidadas
            pragmas = [
                "PRAGMA journal_mode=WAL",
                "PRAGMA synchronous=NORMAL",
                "PRAGMA cache_size=10000",
                "PRAGMA foreign_keys=ON",
                "PRAGMA temp_store=MEMORY",
            ]
            for pragma in pragmas:
                conn.execute(pragma)
            conn.commit()
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
            self._logger.debug("Conexión obtenida del pool")
            yield conn
        except sqlite3.Error as e:
            self._logger.error("Error en conexión: %s", e)
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                try:
                    conn.commit()
                    with self._pool_lock:
                        if len(self._pool) < self.pool_size:
                            self._pool.append(conn)
                        else:
                            conn.close()
                except sqlite3.Error as e:
                    self._logger.error("Error devolviendo conexión: %s", e)
                    conn.close()

    def close_all_connections(self) -> None:
        """Cierra todas las conexiones del pool."""
        try:
            with self._pool_lock:
                for conn in self._pool:
                    conn.close()
                self._pool.clear()
            self._logger.info("Todas las conexiones cerradas")
        except sqlite3.Error as e:
            self._logger.error("Error cerrando conexiones: %s", e)

    def get_connection_info(self) -> Dict[str, Any]:
        """Obtiene información del estado de conexiones."""
        with self._pool_lock:
            return {
                "db_path": str(self.db_path),
                "pool_size": self.pool_size,
                "available_connections": len(self._pool),
                "db_exists": self.db_path.exists(),
            }
