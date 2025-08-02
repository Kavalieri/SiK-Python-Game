#!/usr/bin/env python3
"""
Test Config System - Prueba del Sistema de Configuración
======================================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Script para probar el sistema de configuración V2.
"""

import sys
from pathlib import Path

from utils.config_manager_v2 import ConfigManagerV2

# Añadir el directorio src al path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


def test_config_system():
    """Prueba el sistema de configuración."""
    print("=== PRUEBA DEL SISTEMA DE CONFIGURACIÓN V2 ===")

    try:
        # Crear instancia del gestor de configuración
        config_manager = ConfigManagerV2()

        print("✅ Gestor de configuración creado correctamente")

        # Validar configuraciones
        if config_manager.validate_configs():
            print("✅ Todas las configuraciones son válidas")
        else:
            print("❌ Error en la validación de configuraciones")
            return False

        # Probar obtención de datos de personajes
        print("\n--- PRUEBA DE PERSONAJES ---")
        characters = config_manager.get_all_characters()
        print(f"Personajes disponibles: {characters}")

        for char_key in characters:
            char_data = config_manager.get_character_data(char_key)
            stats = config_manager.get_character_stats(char_key)
            print(
                f"  {char_key}: {char_data.get('nombre', 'N/A')} - Vida: {stats.get('vida', 0)}"
            )

        # Probar obtención de datos de enemigos
        print("\n--- PRUEBA DE ENEMIGOS ---")
        enemies = config_manager.get_all_enemy_types()
        print(f"Tipos de enemigos: {enemies}")

        for enemy_type in enemies:
            enemy_data = config_manager.get_enemy_data(enemy_type)
            print(
                f"  {enemy_type}: {enemy_data.get('nombre', 'N/A')} - Vida: {enemy_data.get('stats', {}).get('vida', 0)}"
            )

        # Probar obtención de datos de powerups
        print("\n--- PRUEBA DE POWERUPS ---")
        powerups = config_manager.get_all_powerup_types()
        print(f"Tipos de powerups: {powerups}")

        for powerup_type in powerups:
            powerup_data = config_manager.get_powerup_data(powerup_type)
            print(
                f"  {powerup_type}: {powerup_data.get('nombre', 'N/A')} - Duración: {powerup_data.get('duración', 0)}s"
            )

        # Probar configuración de UI
        print("\n--- PRUEBA DE UI ---")
        ui_colors = ["fondo", "texto", "texto_destacado", "botón"]
        for color_name in ui_colors:
            color = config_manager.get_ui_color(color_name)
            print(f"  Color {color_name}: {color}")

        ui_fonts = ["título", "subtítulo", "normal", "pequeña"]
        for font_name in ui_fonts:
            font_size = config_manager.get_ui_font_size(font_name)
            print(f"  Fuente {font_name}: {font_size}px")

        # Probar configuración de gameplay
        print("\n--- PRUEBA DE GAMEPLAY ---")
        gameplay_values = [
            ("niveles", "duración_ronda"),
            ("combate", "daño_colisión_enemigo"),
            ("powerups", "duración_estándar"),
            ("puntuación", "multiplicador_combo"),
        ]

        for category, key in gameplay_values:
            value = config_manager.get_gameplay_value(category, key)
            print(f"  {category}.{key}: {value}")

        # Probar configuración de audio
        print("\n--- PRUEBA DE AUDIO ---")
        audio_volumes = ["música_fondo", "efectos_sonido", "voces", "interfaz"]
        for volume_type in audio_volumes:
            volume = config_manager.get_audio_volume(volume_type)
            print(f"  Volumen {volume_type}: {volume}")

        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        return True

    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_character_data_module():
    """Prueba el módulo de datos de personajes."""
    print("\n=== PRUEBA DEL MÓDULO CHARACTER_DATA ===")

    try:
        from scenes.character_data import CharacterData

        # Probar obtención de personajes
        characters = CharacterData.get_all_characters()
        print(f"Personajes desde CharacterData: {characters}")

        # Probar obtención de datos de personaje
        if characters:
            char_key = characters[0]
            char_data = CharacterData.get_character_data(char_key)
            print(f"Datos de {char_key}: {char_data.get('nombre', 'N/A')}")

        print("✅ Módulo CharacterData funciona correctamente")
        return True

    except Exception as e:
        print(f"❌ Error en CharacterData: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Función principal."""
    print("Iniciando pruebas del sistema de configuración...")

    # Probar sistema de configuración
    config_success = test_config_system()

    # Probar módulo de datos de personajes
    character_success = test_character_data_module()

    # Resumen
    print("\n=== RESUMEN ===")
    print(
        f"Sistema de configuración: {'✅ EXITOSO' if config_success else '❌ FALLIDO'}"
    )
    print(
        f"Módulo CharacterData: {'✅ EXITOSO' if character_success else '❌ FALLIDO'}"
    )

    if config_success and character_success:
        print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        return 0
    else:
        print("\n💥 ALGUNAS PRUEBAS FALLARON")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
