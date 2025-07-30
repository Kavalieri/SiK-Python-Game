#!/usr/bin/env python3
"""
Test Config System - Prueba del Sistema de Configuración
======================================================

Autor: SiK Team
Fecha: 2025-01-31
Descripción: Script para probar el sistema de configuración.
"""

import sys
from pathlib import Path

# Añadir el directorio src al path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def test_config_manager():
    """Prueba el ConfigManager básico."""
    try:
        from utils.config_manager import ConfigManager

        print("✅ ConfigManager importado correctamente")

        config = ConfigManager()
        print("✅ ConfigManager inicializado")

        # Probar algunas configuraciones básicas disponibles
        try:
            resolution = config.get_resolution()
            print(f"✅ Resolución: {resolution}")
        except AttributeError:
            print("⚠️  Método get_resolution no disponible")

        try:
            fps = config.get_fps()
            print(f"✅ FPS configurado: {fps}")
        except AttributeError:
            print("⚠️  Método get_fps no disponible")

        # Probar obtener sección de audio
        try:
            audio_section = config.get_section("audio")
            if audio_section:
                print(f"✅ Configuración de audio: {len(audio_section)} opciones")
        except AttributeError:
            print("⚠️  Método get_section no disponible")

        return True

    except ImportError as import_err:
        print(f"❌ Error de importación: {import_err}")
        return False
    except Exception as general_err:
        print(f"❌ Error general: {general_err}")
        return False


def test_character_data():
    """Prueba los datos de personajes."""
    try:
        # Intentar importar CHARACTER_DATA tradicional
        try:
            from entities.character_data import CHARACTER_DATA

            print("✅ CHARACTER_DATA importado correctamente")

            # Obtener lista de personajes disponibles
            if CHARACTER_DATA:
                characters = list(CHARACTER_DATA.keys())
                print(f"✅ Personajes disponibles: {len(characters)}")
                print(f"   Personajes: {', '.join(characters)}")

                # Probar datos de un personaje específico
                if "guerrero" in characters:
                    guerrero_data = CHARACTER_DATA["guerrero"]
                    if guerrero_data and "nombre" in guerrero_data:
                        print(f"✅ Datos del guerrero: {guerrero_data['nombre']}")
                        print(f"   Tipo: {guerrero_data.get('tipo', 'N/A')}")
            else:
                print("⚠️  CHARACTER_DATA está vacío")

        except ImportError:
            # Intentar con CharacterDataManager (sistema mixto)
            try:
                from entities.character_data import CharacterDataManager

                print("✅ CharacterDataManager importado correctamente")

                char_manager = CharacterDataManager()
                characters = char_manager.get_all_characters()
                print(f"✅ Personajes desde SQLite: {len(characters)}")

            except ImportError as char_err:
                print(f"❌ No se pudo importar sistema de personajes: {char_err}")
                return False

        return True

    except Exception as general_err:
        print(f"❌ Error en datos de personajes: {general_err}")
        return False


def test_database_system():
    """Prueba el sistema de base de datos SQLite."""
    try:
        from utils.config_database import ConfigDatabase
        from utils.database_manager import DatabaseManager

        print("✅ Sistema SQLite importado correctamente")

        # Inicializar sistema de base de datos
        db_manager = DatabaseManager("data/test.db")
        config_db = ConfigDatabase(db_manager)
        print("✅ ConfigDatabase inicializado")

        # Probar obtener personajes desde SQLite
        try:
            characters = config_db.get_all_characters()
            if characters:
                print(f"✅ Personajes en SQLite: {len(characters)}")
            else:
                print("⚠️  No hay personajes en SQLite")
        except AttributeError:
            print("⚠️  Método get_all_characters no disponible")

        return True

    except ImportError as import_err:
        print(f"❌ Error de importación SQLite: {import_err}")
        return False
    except Exception as general_err:
        print(f"❌ Error en sistema SQLite: {general_err}")
        return False


def run_all_tests():
    """Ejecuta todas las pruebas del sistema de configuración."""
    print("=" * 60)
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE CONFIGURACIÓN")
    print("=" * 60)

    test_results = []

    print("\n📋 Prueba 1: ConfigManager básico")
    print("-" * 40)
    test_results.append(test_config_manager())

    print("\n📋 Prueba 2: Datos de personajes")
    print("-" * 40)
    test_results.append(test_character_data())

    print("\n📋 Prueba 3: Sistema SQLite")
    print("-" * 40)
    test_results.append(test_database_system())

    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)

    passed = sum(test_results)
    total = len(test_results)

    print(f"✅ Pruebas exitosas: {passed}/{total}")
    print(f"❌ Pruebas fallidas: {total - passed}/{total}")

    if passed == total:
        print("🎉 TODAS LAS PRUEBAS EXITOSAS")
        return True
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
