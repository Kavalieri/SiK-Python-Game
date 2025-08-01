"""
DatabaseManager - Fachada unificada del sistema de base de datos SQLite

Mantiene API completa delegando a DatabaseConnection y DatabaseOperations.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from .database_connection import DatabaseConnection
from .database_operations import DatabaseOperations


class DatabaseManager:
    """Gestor centralizado de BD SQLite - Fachada unificada preservando API completa."""

    def __init__(self, db_path: str = "saves/game_database.db", pool_size: int = 5):
        self._connection = DatabaseConnection(db_path, pool_size)
        self._operations = DatabaseOperations(self._connection)
        self._logger = logging.getLogger("DatabaseManager")
        self._logger.info("DatabaseManager inicializado con módulos especializados")

    # === API DE CONEXIONES (delegada a DatabaseConnection) ===

    def get_connection(self):
        """Context manager para obtener conexión del pool."""
        return self._connection.get_connection()

    def close_all_connections(self) -> None:
        """Cierra todas las conexiones del pool."""
        return self._connection.close_all_connections()

    def get_connection_info(self) -> Dict[str, Any]:
        """Obtiene información del estado de conexiones."""
        return self._connection.get_connection_info()

    # === API DE OPERACIONES (delegada a DatabaseOperations) ===

    def execute_query(
        self,
        query: str,
        params: Optional[Union[tuple, Dict[str, Any]]] = None,
        fetch_results: bool = True,
    ) -> Optional[List[Dict[str, Any]]]:
        """Ejecuta query SQL con parámetros opcionales."""
        return self._operations.execute_query(query, params, fetch_results)

    def transaction(self):
        """Context manager para transacciones SQLite."""
        return self._operations.transaction()

    def backup_database(self, backup_path: str) -> bool:
        """Crea backup de la base de datos."""
        return self._operations.backup_database(backup_path)

    def vacuum_database(self) -> bool:
        """Optimiza la base de datos con VACUUM."""
        return self._operations.vacuum_database()

    # === PROPIEDADES DE COMPATIBILIDAD ===

    @property
    def db_path(self):
        """Acceso a db_path para compatibilidad."""
        return self._connection.db_path

    @property
    def pool_size(self):
        """Acceso a pool_size para compatibilidad."""
        return self._connection.pool_size
