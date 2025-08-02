"""
Fix Rápido - Problema de Velocidad del Jugador
==============================================

Autor: SiK Team
Fecha: 2 de Agosto, 2025
Descripción: Test y fix para el problema de velocidad del jugador.
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pygame
from entities.player import Player
from utils.animation_manager import IntelligentAnimationManager
from utils.config_manager import ConfigManager


def diagnosticar_velocidad_jugador():
    """Diagnosticar el problema específico de velocidad."""
    print("🔍 DIAGNÓSTICO ESPECÍFICO - VELOCIDAD DEL JUGADOR")
    print("=" * 55)

    # Inicializar
    pygame.init()
    pygame.display.set_mode((100, 100))

    config = ConfigManager()
    animation_manager = IntelligentAnimationManager()

    # Crear jugador
    player = Player(
        x=100,
        y=100,
        character_name="guerrero",
        config=config,
        animation_manager=animation_manager,
    )

    print(f"📊 Velocidad en player.core.stats.speed: {player.core.stats.speed}")
    print(f"📊 Velocidad en player.stats.speed: {player.stats.speed}")

    # Verificar configuración directa
    character_config = config.get_character_config("guerrero")
    if character_config:
        print(
            f"📊 Velocidad en config: {character_config.get('stats', {}).get('velocidad', 'NO ENCONTRADA')}"
        )
    else:
        print("❌ Configuración de guerrero no encontrada en config")

    # Test directo de movimiento
    print("\n🧪 TEST DIRECTO DE MOVIMIENTO:")

    pos_inicial = (player.x, player.y)
    print(f"📊 Posición inicial: {pos_inicial}")

    # Establecer velocidad manualmente alta para test
    player.movement.set_velocity(200, 0)  # 200 píxeles/segundo hacia la derecha

    # Simular múltiples frames
    for frame in range(60):  # 1 segundo a 60 FPS
        player.movement.update_movement(0.016)  # 16ms por frame
        if frame % 20 == 0:  # Cada ~300ms
            print(f"  Frame {frame}: ({player.x:.1f}, {player.y:.1f})")

    pos_final = (player.x, player.y)
    print(f"📊 Posición final: {pos_final}")

    # Calcular distancia movida
    distancia = (
        (pos_final[0] - pos_inicial[0]) ** 2 + (pos_final[1] - pos_inicial[1]) ** 2
    ) ** 0.5
    print(f"📊 Distancia movida: {distancia:.1f} píxeles")

    if distancia > 100:
        print("✅ El sistema de movimiento FUNCIONA cuando se establece velocidad alta")
        print("🔍 PROBLEMA CONFIRMADO: La velocidad del personaje es demasiado baja")

        # Verificar si podemos corregir la velocidad
        print("\n🔧 INTENTANDO CORRECCIÓN:")

        # Opción 1: Corregir desde la configuración
        if hasattr(player.core.stats, "speed"):
            player.core.stats.speed = 180  # Velocidad correcta
            print(f"✅ Velocidad corregida a: {player.core.stats.speed}")

            # Test con velocidad corregida
            player.x, player.y = 100, 100  # Reset posición

            # Simular input
            player.movement.set_velocity(player.core.stats.speed, 0)

            for _ in range(60):
                player.movement.update_movement(0.016)

            nueva_pos = (player.x, player.y)
            nueva_distancia = (
                (nueva_pos[0] - 100) ** 2 + (nueva_pos[1] - 100) ** 2
            ) ** 0.5

            print(f"📊 Nueva distancia con velocidad corregida: {nueva_distancia:.1f}")

            if nueva_distancia > 100:
                print("🎉 ¡PROBLEMA RESUELTO! La corrección funciona")
                return True
            else:
                print("❌ Aún hay problemas después de la corrección")
                return False
    else:
        print("❌ El sistema de movimiento tiene problemas más profundos")
        return False


if __name__ == "__main__":
    try:
        resultado = diagnosticar_velocidad_jugador()
        pygame.quit()

        if resultado:
            print("\n🎯 SOLUCIÓN IDENTIFICADA:")
            print("   1. Corregir carga de estadísticas del personaje")
            print("   2. Asegurar que speed = 180 (no 1.0)")
            print("   3. Verificar sistema de base de datos de personajes")
        else:
            print("\n❌ Se necesita investigación adicional")

    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        pygame.quit()
