"""
Debug Específico - Update Movement
==================================

Autor: SiK Team
Fecha: 2 de Agosto, 2025
Descripción: Debug específico del método update_movement.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pygame

from entities.player import Player
from utils.animation_manager import IntelligentAnimationManager
from utils.config_manager import ConfigManager


def debug_update_movement():
    """Debug específico del update_movement."""
    print("🐛 DEBUG ESPECÍFICO - UPDATE MOVEMENT")
    print("=" * 40)

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

    print(f"📊 Posición inicial: ({player.x}, {player.y})")
    print(f"📊 player.core.x, player.core.y: ({player.core.x}, {player.core.y})")

    # Establecer velocidad
    player.movement.set_velocity(200, 100)
    vel_x, vel_y = player.movement.get_velocity()
    print(f"📊 Velocidad establecida: ({vel_x}, {vel_y})")

    # Debug paso a paso
    delta_time = 0.016  # 60 FPS

    print(f"\n🔍 EJECUTANDO update_movement(delta_time={delta_time})...")

    # Valores antes
    print(f"  ANTES - player.x: {player.x}, player.y: {player.y}")
    print(f"  ANTES - player.core.x: {player.core.x}, player.core.y: {player.core.y}")
    print(
        f"  ANTES - velocity: ({player.movement.velocity_x}, {player.movement.velocity_y})"
    )

    # Calcular lo que DEBERÍA pasar
    expected_new_x = player.core.x + (player.movement.velocity_x * delta_time)
    expected_new_y = player.core.y + (player.movement.velocity_y * delta_time)
    print(f"  ESPERADO - new_x: {expected_new_x}, new_y: {expected_new_y}")

    # Ejecutar update_movement
    player.movement.update_movement(delta_time)

    # CRUCIAL: Ejecutar player.update() para sincronizar posición
    player.update(delta_time)

    # Valores después
    print(f"  DESPUÉS - player.x: {player.x}, player.y: {player.y}")
    print(f"  DESPUÉS - player.core.x: {player.core.x}, player.core.y: {player.core.y}")

    # Verificar si hay sincronización entre player y player.core
    if player.x == player.core.x and player.y == player.core.y:
        print("✅ player y player.core están sincronizados")
    else:
        print("❌ player y player.core NO están sincronizados")
        print("   Esto podría ser el problema!")

    # Verificar si player.core cambió
    if player.core.x != 100 or player.core.y != 100:
        print("✅ player.core SÍ cambió de posición")
    else:
        print("❌ player.core NO cambió de posición")

    # Verificar si player cambió
    if player.x != 100 or player.y != 100:
        print("✅ player SÍ cambió de posición")
    else:
        print("❌ player NO cambió de posición")

    # Test con múltiples frames
    print("\n🔄 TEST CON 60 FRAMES (1 segundo)...")

    for frame in range(60):
        player.movement.update_movement(delta_time)
        # CRUCIAL: También sincronizar player desde core cada frame
        player.update(delta_time)
        if frame % 15 == 0:  # Cada ~250ms
            print(
                f"  Frame {frame}: player=({player.x:.1f}, {player.y:.1f}), core=({player.core.x:.1f}, {player.core.y:.1f})"
            )

    final_distance = ((player.x - 100) ** 2 + (player.y - 100) ** 2) ** 0.5
    core_distance = ((player.core.x - 100) ** 2 + (player.core.y - 100) ** 2) ** 0.5

    print("\n📏 Distancia final movida:")
    print(f"   Player: {final_distance:.1f} píxeles")
    print(f"   Core: {core_distance:.1f} píxeles")

    # Verificar propiedades del player
    print("\n🔍 INVESTIGANDO PROPIEDADES:")
    print(f"   type(player.x): {type(player.x)}")
    print(f"   type(player.core.x): {type(player.core.x)}")
    print(f"   player tiene __setattr__: {hasattr(player, '__setattr__')}")
    print(f"   player.core tiene __setattr__: {hasattr(player.core, '__setattr__')}")

    # Ver si player.x es una propiedad
    if hasattr(Player, "x") and isinstance(Player.x, property):
        print("   player.x ES una propiedad - podría estar vinculada a player.core.x")
    else:
        print("   player.x NO es una propiedad")

    pygame.quit()


if __name__ == "__main__":
    debug_update_movement()
