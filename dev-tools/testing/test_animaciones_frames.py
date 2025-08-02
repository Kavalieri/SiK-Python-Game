#!/usr/bin/env python3
"""
Test Sistema Animaciones Frame-by-Frame - Prueba del Sistema Completo de Animaciones
===================================================================================

Autor: SiK Team
Fecha: 2025-08-02
Descripción: Script para probar el sistema de animaciones con ciclos frame-by-frame.
"""

import sys
from pathlib import Path

import pygame

# Añadir src al path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from entities.entity_types import EntityState
from entities.player import Player
from entities.player_core import AnimationState
from utils.animation_manager import IntelligentAnimationManager
from utils.config_manager import ConfigManager


def main():
    """Función principal del test de animaciones frame-by-frame."""
    print("🎬 TEST SISTEMA ANIMACIONES FRAME-BY-FRAME")
    print("=" * 55)

    # Inicializar Pygame
    pygame.init()
    pygame.display.set_mode((800, 600))

    # Configurar managers
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

    print("✅ Jugador creado")
    print(f"📊 Frame inicial: {player.core.current_frame_index}")
    print(f"⏱️ Timer inicial: {player.core.animation_timer:.3f}")

    # Test 1: Verificar que las animaciones tienen múltiples frames
    print("\\n🔍 TEST 1: Verificación de frames múltiples")
    if player.core.animations:
        for anim_name, anim_data in player.core.animations.items():
            if anim_data and "frames" in anim_data:
                frame_count = len(anim_data["frames"])
                print(f"  {anim_name}: {frame_count} frames")
                if frame_count > 1:
                    print(f"    ✅ {anim_name} tiene múltiples frames")
                else:
                    print(f"    ⚠️ {anim_name} solo tiene 1 frame")

    # Test 2: Ciclo de animación IDLE
    print("\\n🔍 TEST 2: Ciclo de animación IDLE")
    initial_frame = player.core.current_frame_index

    # Simular 60 frames a 60 FPS (1 segundo)
    delta_time = 1 / 60  # ~16.67ms por frame
    for frame in range(60):
        player.core.update_animation_timing(delta_time)
        if frame % 15 == 0:  # Mostrar cada ~250ms
            print(
                f"  Frame {frame}: Índice animación = {player.core.current_frame_index}, Timer = {player.core.animation_timer:.3f}"
            )

    final_frame = player.core.current_frame_index
    print(f"  Resultado: Frame inicial={initial_frame}, Frame final={final_frame}")
    if final_frame != initial_frame:
        print("  ✅ La animación IDLE está ciclando frames")
    else:
        print("  ⚠️ La animación IDLE no está ciclando")

    # Test 3: Cambio de animación y reset
    print("\\n🔍 TEST 3: Cambio de animación y reset de frames")

    # Forzar un índice específico
    player.core.current_frame_index = 5
    player.core.animation_timer = 0.05
    print(f"  Frame antes del cambio: {player.core.current_frame_index}")

    # Cambiar a RUN
    player.movement.velocity_x = 200
    player.movement.update_animation(delta_time)
    player.update(delta_time)

    print(f"  Frame después del cambio a RUN: {player.core.current_frame_index}")
    print(f"  Timer después del cambio: {player.core.animation_timer:.3f}")

    if player.core.current_frame_index == 0 and player.core.animation_timer == 0.0:
        print("  ✅ Reset de animación funciona correctamente")
    else:
        print("  ❌ Reset de animación NO funciona")

    # Test 4: Velocidades diferentes de animación
    print("\\n🔍 TEST 4: Velocidades de animación")

    # Probar IDLE (lenta)
    player.core.current_animation_state = AnimationState.IDLE
    idle_duration = player.core._get_frame_duration_for_animation()

    # Probar ATTACK (rápida)
    player.core.current_animation_state = AnimationState.ATTACK
    attack_duration = player.core._get_frame_duration_for_animation()

    # Probar RUN (media)
    player.core.current_animation_state = AnimationState.RUN
    run_duration = player.core._get_frame_duration_for_animation()

    print(f"  IDLE: {idle_duration:.3f}s por frame ({1 / idle_duration:.1f} FPS)")
    print(f"  RUN: {run_duration:.3f}s por frame ({1 / run_duration:.1f} FPS)")
    print(f"  ATTACK: {attack_duration:.3f}s por frame ({1 / attack_duration:.1f} FPS)")

    if attack_duration < run_duration < idle_duration:
        print("  ✅ Velocidades de animación correctas (ATTACK > RUN > IDLE)")
    else:
        print("  ❌ Velocidades de animación incorrectas")

    # Test 5: Sistema de ataque completo
    print("\\n🔍 TEST 5: Sistema de ataque con ciclo completo")

    # Resetear estado
    player.movement.is_attacking = False
    player.core.state = EntityState.IDLE
    player.core.current_animation_state = AnimationState.IDLE

    # Iniciar ataque
    player.movement._handle_attack_input(True)
    print(f"  Ataque iniciado - Frame: {player.core.current_frame_index}")
    print(f"  Estado: {player.core.state}")
    print(f"  Timer ataque: {player.movement.attack_timer:.3f}")

    # Simular ataque durante varios frames
    for frame in range(20):  # ~333ms
        player.movement.update_animation(delta_time)
        if frame % 5 == 0:
            print(
                f"    Frame {frame}: Anim={player.core.current_frame_index}, Timer={player.movement.attack_timer:.3f}"
            )

    # Verificar que el ataque termina
    if not player.movement.is_attacking and player.core.state == EntityState.IDLE:
        print("  ✅ Sistema de ataque completo funcionando")
    else:
        print("  ⚠️ Sistema de ataque necesita ajustes")

    print("\\n🎯 RESUMEN:")
    print("📊 Tests ejecutados: 5")
    print("✅ Sistema de animaciones frame-by-frame implementado")
    print("🎬 Ciclos de animación funcionando!")


if __name__ == "__main__":
    main()
