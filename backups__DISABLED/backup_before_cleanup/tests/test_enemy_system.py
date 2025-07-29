#!/usr/bin/env python3
"""
Script de test para el sistema de enemigos avanzados
================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del sistema de enemigos con tipos y comportamientos avanzados.
"""

import sys
import os
import pygame
import time

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.entities.enemy_types import EnemyTypes
from src.entities.enemy import Enemy
from src.utils.asset_manager import AssetManager
from src.utils.animation_manager import AnimationManager
from src.utils.config_manager import ConfigManager


def test_enemy_system():
    """Test del sistema de enemigos avanzados."""
    print("🧪 Iniciando test del sistema de enemigos avanzados...")

    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Sistema de Enemigos")
    clock = pygame.time.Clock()

    # Inicializar managers
    config = ConfigManager()
    asset_manager = AssetManager()
    animation_manager = AnimationManager(config, asset_manager)

    # Crear jugador simulado (solo para referencia)
    class MockPlayer:
        def __init__(self):
            self.x = 400
            self.y = 300
            self.is_alive = True

    player = MockPlayer()

    # Lista de enemigos para mostrar
    enemies = []

    # Crear enemigos de diferentes tipos
    print("\n👹 Creando enemigos de diferentes tipos...")

    # Enemigos normales
    enemies.append(
        Enemy(
            100,
            100,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_NORMAL,
        )
    )
    enemies.append(
        Enemy(
            200,
            100,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_GIRL_NORMAL,
        )
    )

    # Enemigos raros
    enemies.append(
        Enemy(
            300,
            100,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_RARE,
        )
    )
    enemies.append(
        Enemy(
            400,
            100,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_GIRL_RARE,
        )
    )

    # Enemigos elite
    enemies.append(
        Enemy(
            100,
            200,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_ELITE,
        )
    )
    enemies.append(
        Enemy(
            200,
            200,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_GIRL_ELITE,
        )
    )

    # Enemigos legendarios
    enemies.append(
        Enemy(
            300,
            200,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_LEGENDARY,
        )
    )
    enemies.append(
        Enemy(
            400,
            200,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_GIRL_LEGENDARY,
        )
    )

    print(f"✅ {len(enemies)} enemigos creados")

    # Mostrar información de cada enemigo
    print("\n📊 Información de enemigos:")
    for i, enemy in enumerate(enemies):
        info = enemy.get_enemy_info()
        print(
            f"  {i+1}. {info['name']} - Rareza: {info['rarity']} - Comportamiento: {info['behavior']}"
        )
        print(
            f"     Vida: {info['health']} - Daño: {info['damage']} - Puntos: {info['score_value']}"
        )

    # Test de generación aleatoria
    print("\n🎲 Probando generación aleatoria...")
    random_enemies = []
    for _ in range(10):
        config = EnemyTypes.get_random_enemy()
        random_enemies.append(config)
        print(f"  - {config.name} (Rareza: {config.rarity.value})")

    # Estadísticas de rareza
    rarity_counts = {}
    for enemy in random_enemies:
        rarity = enemy.rarity.value
        rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1

    print("\n📈 Distribución de rareza en enemigos aleatorios:")
    for rarity, count in rarity_counts.items():
        print(f"  - {rarity}: {count} enemigos")

    # Test de comportamientos
    print("\n🤖 Probando comportamientos...")
    behavior_enemies = [
        Enemy(
            100,
            300,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_NORMAL,
        ),  # CHASE
        Enemy(
            200,
            300,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_GIRL_RARE,
        ),  # WANDER
        Enemy(
            300,
            300,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_RARE,
        ),  # AMBUSH
        Enemy(
            400,
            300,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_ELITE,
        ),  # SWARM
        Enemy(
            500,
            300,
            asset_manager,
            animation_manager,
            config,
            player,
            EnemyTypes.ZOMBIE_LEGENDARY,
        ),  # BOSS
    ]

    behavior_names = ["Persecución", "Vagabundeo", "Emboscada", "Enjambre", "Jefe"]

    for i, enemy in enumerate(behavior_enemies):
        print(f"  {i+1}. {behavior_names[i]}: {enemy.enemy_config.name}")

    # Renderizado y simulación
    print("\n🎨 Probando renderizado...")
    screen.fill((50, 100, 150))  # Fondo azul

    # Renderizar enemigos
    for enemy in enemies:
        enemy.render(screen)

    # Renderizar enemigos de comportamiento
    for enemy in behavior_enemies:
        enemy.render(screen)

    pygame.display.flip()
    print("✅ Enemigos renderizados correctamente")

    # Simulación de movimiento
    print("\n🏃 Simulando movimiento de enemigos...")
    running = True
    start_time = time.time()

    while running and (time.time() - start_time) < 5:  # 5 segundos de simulación
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar enemigos
        delta_time = 1.0 / 60.0
        for enemy in enemies + behavior_enemies:
            enemy.update(delta_time)

        # Renderizar
        screen.fill((50, 100, 150))

        # Dibujar jugador (punto blanco)
        pygame.draw.circle(screen, (255, 255, 255), (int(player.x), int(player.y)), 10)

        # Renderizar enemigos
        for enemy in enemies + behavior_enemies:
            enemy.render(screen)

        pygame.display.flip()
        clock.tick(60)

    # Limpiar
    pygame.quit()
    print("✅ Test del sistema de enemigos avanzados completado")


if __name__ == "__main__":
    test_enemy_system()
