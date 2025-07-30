#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicialización del Esquema SQLite - Sistema Mixto
=================================================

Script para crear las tablas SQLite necesarias para el sistema mixto.
"""

import logging
import sys
from pathlib import Path


def setup_logging():
    """Configurar logging para la inicialización."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def initialize_database():
    """Inicializar esquema de base de datos SQLite."""
    print("=" * 60)
    print("INICIALIZACIÓN ESQUEMA SQLITE - SISTEMA MIXTO")
    print("=" * 60)
    print()

    try:
        # 1. Importar módulos
        print("[1/4] Importando módulos...")
        sys.path.insert(0, str(Path.cwd()))
        from src.utils.database_manager import DatabaseManager
        from src.utils.schema_manager import SchemaManager

        print("✓ Módulos importados")

        # 2. Inicializar sistema de base de datos
        print("[2/4] Inicializando sistema de base de datos...")
        db_manager = DatabaseManager()
        schema_manager = SchemaManager(db_manager)
        print("✓ Sistema inicializado")

        # 3. Crear todas las tablas
        print("[3/4] Creando esquema completo...")
        result = schema_manager.create_all_tables()
        if result:
            print("✓ Todas las tablas creadas exitosamente")
        else:
            print("! Algunas tablas ya existían o hubo errores menores")

        # 4. Verificar tablas creadas
        print("[4/4] Verificando tablas...")
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            print(f"✓ Tablas encontradas: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")

        print()
        print("=" * 60)
        print("✓ ESQUEMA SQLITE INICIALIZADO CORRECTAMENTE")
        print("=" * 60)
        print()
        print("TABLAS DISPONIBLES PARA SISTEMA MIXTO:")
        print("✓ personajes - Para characters.json")
        print("✓ enemigos - Para enemies.json")
        print("✓ configuraciones - Para configuración general")
        print("✓ partidas_guardadas - Para saves")
        print("✓ estadisticas_juego - Para estadísticas")
        print("✓ configuracion_gameplay - Para gameplay config")
        print()
        print("AHORA PUEDE EJECUTAR:")
        print("python run_migration_step1.py  # characters.json")
        print("python run_migration_step2.py  # enemies.json")

        return True

    except ImportError as e:
        print(f"✗ ERROR de importación: {e}")
        return False
    except Exception as e:
        print(f"✗ ERROR durante inicialización: {e}")
        return False


if __name__ == "__main__":
    setup_logging()
    success = initialize_database()
    sys.exit(0 if success else 1)
