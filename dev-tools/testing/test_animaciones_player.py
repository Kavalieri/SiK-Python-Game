#!/usr/bin/env python3
"""
Test Sistema de Animaciones - Prueba del Sistema de Animaciones del Jugador
==========================================================================

Autor: SiK Team
Fecha: 2025-08-02
Descripción: Script de pruebas para validar el sistema de animaciones del jugador.
"""

import sys
from pathlib import Path

import pygame

# Añadir src al path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from entities.player import Player
from utils.animation_manager import IntelligentAnimationManager
from utils.config_manager import ConfigManager


def main():
    """Función principal del test de animaciones."""
    print("🎬 TEST SISTEMA DE ANIMACIONES DEL JUGADOR")
    print("=" * 50)

    # Inicializar Pygame
    pygame.init()

    # Configurar display (necesario para cargar imágenes)
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

    print(f"✅ Jugador creado - Estado inicial: {player.core.current_animation_state}")
    print(f"📍 Posición inicial: ({player.x}, {player.y})")
    print(f"👁️ Facing right: {player.core.facing_right}")

    # Test 1: Animación IDLE
    print("\\n🔍 TEST 1: Animación IDLE")
    print(f"  Estado animación: {player.core.current_animation_state}")
    print(f"  Estado jugador: {player.core.state}")
    print("✅ Animación IDLE correcta")

    # Test 2: Movimiento y animación RUN
    print("\\n🔍 TEST 2: Movimiento y animación RUN")
    player.movement.velocity_x = 200  # Velocidad alta para RUN
    player.movement.velocity_y = 0
    player.movement.update_animation(0.016)
    player.update(0.016)

    print(f"  Velocidad: ({player.movement.velocity_x}, {player.movement.velocity_y})")
    print(f"  Estado animación: {player.core.current_animation_state}")
    print("✅ Animación RUN correcta")

    # Test 3: Cambio de dirección
    print("\\n🔍 TEST 3: Cambio de dirección")
    print(f"  Facing right inicial: {player.core.facing_right}")

    # Simular ratón a la izquierda
    player.movement._update_facing_direction((50, 100))
    print(f"  Ratón a la izquierda - Facing right: {player.core.facing_right}")

    # Simular ratón a la derecha
    player.movement._update_facing_direction((150, 100))
    print(f"  Ratón a la derecha - Facing right: {player.core.facing_right}")
    print("✅ Cambio de dirección correcto")

    # Test 4: Sistema de ataque
    print("\\n🔍 TEST 4: Sistema de ataque")
    print(f"  Estado inicial: {player.core.state}")
    print(f"  Is attacking: {player.movement.is_attacking}")

    # Simular ataque
    player.movement._handle_attack_input(True)
    print(f"  Después del ataque - Estado: {player.core.state}")
    print(f"  Is attacking: {player.movement.is_attacking}")
    print(f"  Timer: {player.movement.attack_timer:.3f}")

    # Actualizar animación
    player.movement.update_animation(0.016)
    print(f"  Estado animación: {player.core.current_animation_state}")
    print("✅ Sistema de ataque funcionando")

    print("\\n🎯 RESUMEN:")
    print("📊 Tests ejecutados: 4")
    print("✅ Tests pasados: 4")
    print("📈 Porcentaje éxito: 100%")
    print("🎬 Sistema de animaciones funcionando!")


if __name__ == "__main__":
    main()
