#!/usr/bin/env python3
"""
Verificación Sistema Mixto - Estado actual
"""

import sys
from pathlib import Path


def check_system():
    print("VERIFICANDO SISTEMA MIXTO...")

    # Añadir path
    sys.path.insert(0, str(Path.cwd()))

    try:
        # 1. Verificar tablas
        from src.utils.database_manager import DatabaseManager

        db_manager = DatabaseManager()

        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"Tablas SQLite: {len(tables)}")
            for table in tables:
                print(f"  - {table}")

        # 2. Verificar ConfigDatabase
        from src.utils.config_database import ConfigDatabase

        config_db = ConfigDatabase(db_manager)

        print("\nProbando ConfigDatabase:")

        # Personajes
        chars = config_db.get_all_characters()
        print(f"Personajes en DB: {len(chars)}")

        # Enemigos
        enemies = config_db.get_all_enemies()
        print(f"Enemigos en DB: {len(enemies)}")

        print("\n✓ SISTEMA MIXTO FUNCIONAL")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False


if __name__ == "__main__":
    check_system()
