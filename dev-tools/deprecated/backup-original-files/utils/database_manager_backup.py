"""
DatabaseManager - Gestor de conexiones y operaciones SQLite
===========================================================

Módulo para gestionar conexiones SQLite con pooling, transacciones y logging.
Parte de la migración del sistema de persistencia de pickle a SQLite.

Fase 1 de migración SQLite - Infraestructura base
Referencia: docs/PLAN_MIGRACION_SQLITE.md - Fase 1
"""

import logging
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any


class DatabaseManager:
    """
    Gestor centralizado de conexiones SQLite con pooling y transacciones.

    Características:
    - Connection pooling para evitar bloqueos
    - Manejo de transacciones automático
    - Logging detallado de operaciones
    - Validación de integridad de datos
    - Soporte para backup automático
    """

    def __init__(self, db_path: str = "saves/game_database.db", pool_size: int = 5):
        """
        Inicializa el gestor de base de datos.

        Args:
            db_path: Ruta al archivo de base de datos SQLite
            pool_size: Número máximo de conexiones en el pool
        """
        self.db_path = Path(db_path)
        self.pool_size = pool_size
        self._pool: list[sqlite3.Connection] = []
        self._pool_lock = threading.Lock()
        self._logger = logging.getLogger("DatabaseManager")

        # Crear directorio si no existe
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Inicializar pool de conexiones
        self._initialize_pool()

        self._logger.info(f"DatabaseManager inicializado: {self.db_path}")

    def _initialize_pool(self) -> None:
        """Inicializa el pool de conexiones SQLite."""
        try:
            for _ in range(self.pool_size):
                conn = self._create_connection()
                self._pool.append(conn)
            self._logger.info(f"Pool de conexiones creado: {self.pool_size} conexiones")
        except Exception as e:
            self._logger.error(f"Error inicializando pool: {e}")
            raise

    def _create_connection(self) -> sqlite3.Connection:
        """
        Crea una nueva conexión SQLite optimizada.

        Returns:
            Conexión SQLite configurada
        """
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False, timeout=10.0)

        # Configuraciones de rendimiento
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA cache_size = 10000")
        conn.execute("PRAGMA busy_timeout = 30000")  # 30 segundos timeout

        # Row factory para retornar diccionarios
        conn.row_factory = sqlite3.Row

        return conn

    @contextmanager
    def get_connection(self):
        """
        Context manager para obtener conexión del pool.

        Yields:
            Conexión SQLite del pool
        """
        conn = None
        try:
            with self._pool_lock:
                if self._pool:
                    conn = self._pool.pop()
                else:
                    conn = self._create_connection()

            yield conn

        except Exception as e:
            if conn:
                conn.rollback()
            self._logger.error(f"Error en conexión: {e}")
            raise
        finally:
            if conn:
                with self._pool_lock:
                    if len(self._pool) < self.pool_size:
                        self._pool.append(conn)
                    else:
                        conn.close()

    def execute_query(
        self,
        query: str,
        params: tuple | None = None,
        fetch_one: bool = False,
        fetch_all: bool = True,
    ) -> dict | list[dict] | None:
        """
        Ejecuta una consulta SQL con logging y manejo de errores.

        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta
            fetch_one: Si retornar solo un resultado
            fetch_all: Si retornar todos los resultados

        Returns:
            Resultados de la consulta o None
        """
        start_time = datetime.now()

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Procesar resultados según el tipo de query
                if query.strip().upper().startswith("SELECT"):
                    if fetch_one:
                        result = cursor.fetchone()
                        return dict(result) if result else None
                    elif fetch_all:
                        results = cursor.fetchall()
                        return [dict(row) for row in results]
                else:
                    conn.commit()
                    return {
                        "rows_affected": cursor.rowcount,
                        "last_row_id": cursor.lastrowid,
                    }

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self._logger.error(
                f"Error ejecutando query: {e} (tiempo: {execution_time:.3f}s)"
            )
            self._logger.error(f"Query: {query}")
            self._logger.error(f"Params: {params}")
            raise

        execution_time = (datetime.now() - start_time).total_seconds()
        self._logger.debug(f"Query ejecutada en {execution_time:.3f}s")
        return None

    @contextmanager
    def transaction(self):
        """
        Context manager para transacciones manuales.

        Yields:
            Conexión en transacción
        """
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
                self._logger.debug("Transacción completada exitosamente")
            except Exception as e:
                conn.rollback()
                self._logger.error(f"Transacción fallida, rollback realizado: {e}")
                raise

    def close_all_connections(self) -> None:
        """Cierra todas las conexiones del pool."""
        with self._pool_lock:
            for conn in self._pool:
                conn.close()
            self._pool.clear()
        self._logger.info("Todas las conexiones cerradas")

    def get_database_info(self) -> dict[str, Any]:
        """
        Obtiene información de la base de datos.

        Returns:
            Diccionario con información de la BD
        """
        try:
            info = {
                "db_path": str(self.db_path),
                "exists": self.db_path.exists(),
                "size_bytes": self.db_path.stat().st_size
                if self.db_path.exists()
                else 0,
                "pool_size": len(self._pool),
                "created_at": datetime.now().isoformat(),
            }

            # Información adicional si la BD existe
            if self.db_path.exists():
                tables = self.execute_query(
                    "SELECT name FROM sqlite_master WHERE type='table'", fetch_all=True
                )
                info["tables"] = [table["name"] for table in tables] if tables else []

            return info

        except Exception as e:
            self._logger.error(f"Error obteniendo info de BD: {e}")
            return {"error": str(e)}
