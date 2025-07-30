"""
Prueba rápida de DatabaseManager y SchemaManager
"""

import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.database_manager import DatabaseManager
from utils.schema_manager import SchemaManager


def test_simple():
    print("Prueba simple de infraestructura SQLite...")

    # Crear BD de prueba
    db_manager = DatabaseManager("saves/test_simple.db")
    print("DatabaseManager creado")

    # Crear esquema
    schema_manager = SchemaManager(db_manager)
    print("SchemaManager creado")

    # Crear tablas
    success = schema_manager.create_all_tables()
    print(f"Tablas creadas: {success}")

    # Validar básicamente
    validation = schema_manager.validate_schema()
    print(f"Validacion: {validation['valid']}")
    print(f"Tablas encontradas: {validation['tables_found']}")

    # Insertar dato simple
    result = db_manager.execute_query(
        "INSERT INTO configuraciones (categoria, clave, valor, tipo) VALUES (?, ?, ?, ?)",
        ("test", "test_key", "test_value", "string"),
    )
    print(f"Insercion: {result}")

    # Leer dato
    data = db_manager.execute_query(
        "SELECT * FROM configuraciones WHERE categoria = ?", ("test",)
    )
    print(f"Lectura: {data}")

    # Cerrar
    db_manager.close_all_connections()
    print("Conexiones cerradas")

    # Limpiar
    Path("saves/test_simple.db").unlink(missing_ok=True)
    print("Archivo limpiado")

    print("¡Prueba simple exitosa!")


if __name__ == "__main__":
    test_simple()
