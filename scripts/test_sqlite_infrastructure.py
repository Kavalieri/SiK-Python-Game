"""
Test de Infraestructura SQLite - Fase 1
=======================================

Script de testing para validar DatabaseManager y SchemaManager
como parte de la migración SQLite.

Referencia: docs/PLAN_MIGRACION_SQLITE.md - Fase 1
"""

import sys
from pathlib import Path

# Agregar src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import logging

from utils.database_manager import DatabaseManager
from utils.schema_manager import SchemaManager

# Configurar logging para testing
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("TestInfraestructura")


def test_database_manager():
    """Prueba el DatabaseManager básico."""
    logger.info("🧪 Iniciando pruebas de DatabaseManager...")

    try:
        # Crear instancia con BD de testing
        db_manager = DatabaseManager("saves/test_database.db")

        # Probar conexión básica
        info = db_manager.get_database_info()
        logger.info(f"✅ Conexión establecida: {info}")

        # Probar query simple
        result = db_manager.execute_query("SELECT 1 as test", fetch_one=True)
        assert result and result["test"] == 1, "Query de prueba falló"
        logger.info("✅ Query de prueba exitosa")

        # Probar transacción
        with db_manager.transaction() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY, name TEXT)"
            )
            conn.execute("INSERT INTO test_table (name) VALUES (?)", ("test_name",))

        # Verificar datos insertados
        result = db_manager.execute_query(
            "SELECT name FROM test_table WHERE name = ?", ("test_name",), fetch_one=True
        )
        assert result and result["name"] == "test_name", "Transacción falló"
        logger.info("✅ Transacción exitosa")

        # Limpiar tabla de prueba
        db_manager.execute_query("DROP TABLE IF EXISTS test_table")

        # Cerrar conexiones
        db_manager.close_all_connections()
        logger.info("✅ DatabaseManager: TODAS LAS PRUEBAS PASARON")

        return True

    except Exception as e:
        logger.error(f"❌ Error en DatabaseManager: {e}")
        return False


def test_schema_manager():
    """Prueba el SchemaManager y creación de esquemas."""
    logger.info("🧪 Iniciando pruebas de SchemaManager...")

    try:
        # Crear instancias
        db_manager = DatabaseManager("saves/test_schema.db")
        schema_manager = SchemaManager(db_manager)

        # Crear backup
        backup_success = schema_manager.create_backup()
        logger.info(f"✅ Backup creado: {backup_success}")

        # Crear todas las tablas
        creation_success = schema_manager.create_all_tables()
        assert creation_success, "Creación de tablas falló"
        logger.info("✅ Todas las tablas creadas")

        # Validar esquema
        validation = schema_manager.validate_schema()
        assert validation[
            "valid"
        ], f"Validación de esquema falló: {validation['errors']}"
        logger.info(
            f"✅ Esquema válido: {len(validation['tables_found'])} tablas encontradas"
        )

        # Verificar versión
        version = schema_manager.get_current_version()
        assert version == "1.0.0", f"Versión incorrecta: {version}"
        logger.info(f"✅ Versión correcta: {version}")

        # Verificar tablas específicas
        required_tables = [
            "partidas_guardadas",
            "configuraciones",
            "personajes",
            "enemigos",
            "estadisticas_juego",
            "configuracion_gameplay",
        ]
        for table in required_tables:
            assert table in validation["tables_found"], f"Tabla {table} no encontrada"
        logger.info(f"✅ Todas las tablas requeridas presentes: {required_tables}")

        # Cerrar conexiones
        db_manager.close_all_connections()
        logger.info("✅ SchemaManager: TODAS LAS PRUEBAS PASARON")

        return True

    except Exception as e:
        logger.error(f"❌ Error en SchemaManager: {e}")
        return False


def test_integration():
    """Prueba de integración completa."""
    logger.info("🧪 Iniciando prueba de integración...")

    try:
        # Crear sistema completo
        db_manager = DatabaseManager("saves/test_integration.db")
        schema_manager = SchemaManager(db_manager)

        # Crear esquema
        schema_manager.create_all_tables()

        # Insertar datos de prueba en todas las tablas principales

        # Partida guardada
        db_manager.execute_query(
            "INSERT INTO partidas_guardadas (slot, nombre_jugador, personaje, puntuacion) VALUES (?, ?, ?, ?)",
            (1, "TestPlayer", "guerrero", 1000),
        )

        # Configuración
        db_manager.execute_query(
            "INSERT INTO configuraciones (categoria, clave, valor, tipo) VALUES (?, ?, ?, ?)",
            ("audio", "master_volume", "0.8", "number"),
        )

        # Personaje
        db_manager.execute_query(
            "INSERT INTO personajes (nombre, nombre_mostrar, tipo, stats, ataques) VALUES (?, ?, ?, ?, ?)",
            ("test_char", "Test Character", "Melee", '{"vida": 100}', '["attack1"]'),
        )

        # Verificar datos insertados
        partida = db_manager.execute_query(
            "SELECT * FROM partidas_guardadas WHERE slot = ?", (1,), fetch_one=True
        )
        assert (
            partida and partida["nombre_jugador"] == "TestPlayer"
        ), "Datos de partida no insertados"

        config = db_manager.execute_query(
            "SELECT * FROM configuraciones WHERE categoria = ? AND clave = ?",
            ("audio", "master_volume"),
            fetch_one=True,
        )
        assert (
            config and config["valor"] == "0.8"
        ), "Datos de configuración no insertados"

        logger.info("✅ Integración: TODAS LAS PRUEBAS PASARON")

        # Limpiar
        db_manager.close_all_connections()

        return True

    except Exception as e:
        logger.error(f"❌ Error en integración: {e}")
        return False


def cleanup_test_files():
    """Limpia archivos de prueba."""
    test_files = [
        "saves/test_database.db",
        "saves/test_schema.db",
        "saves/test_integration.db",
    ]

    for file_path in test_files:
        try:
            if Path(file_path).exists():
                Path(file_path).unlink()
                logger.info(f"🧹 Limpiado: {file_path}")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo limpiar {file_path}: {e}")


def main():
    """Ejecuta todas las pruebas de la infraestructura SQLite."""
    logger.info("🚀 INICIANDO PRUEBAS DE INFRAESTRUCTURA SQLITE - FASE 1")
    logger.info("=" * 60)

    # Limpiar archivos previos
    cleanup_test_files()

    tests = [
        ("DatabaseManager", test_database_manager),
        ("SchemaManager", test_schema_manager),
        ("Integración", test_integration),
    ]

    results = []

    for test_name, test_func in tests:
        logger.info(f"\n📋 Ejecutando prueba: {test_name}")
        logger.info("-" * 40)

        success = test_func()
        results.append((test_name, success))

        if success:
            logger.info(f"🎉 {test_name}: ✅ EXITOSO")
        else:
            logger.error(f"💥 {test_name}: ❌ FALLIDO")

    # Resumen final
    logger.info("\n" + "=" * 60)
    logger.info("📊 RESUMEN DE PRUEBAS:")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        logger.info(f"  {test_name}: {status}")

    logger.info(f"\n🎯 RESULTADO FINAL: {passed}/{total} pruebas pasaron")

    if passed == total:
        logger.info("🎉 ¡TODAS LAS PRUEBAS EXITOSAS! Infraestructura SQLite lista.")
        logger.info("📋 Próximo paso: Fase 2 - Migración del ConfigManager")
    else:
        logger.error("💥 Algunas pruebas fallaron. Revisar antes de continuar.")

    # Limpiar archivos de prueba
    cleanup_test_files()

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
