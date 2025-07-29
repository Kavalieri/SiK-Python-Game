#!/usr/bin/env python3
"""
Script de test rápido para el sistema de proyectiles
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test rápido del sistema de proyectiles sin ejecutar el juego completo.
"""

import sys
import os
import pygame

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.entities.projectile import Projectile
from src.entities.enemy import Enemy
from src.utils.config_manager import ConfigManager
from src.utils.asset_manager import AssetManager
from src.utils.animation_manager import AnimationManager


def test_projectile_system():
    """Test rápido del sistema de proyectiles."""
    print("🧪 Iniciando test del sistema de proyectiles...")

    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Sistema de Proyectiles")

    # Configuración
    config = ConfigManager()
    asset_manager = AssetManager()
    animation_manager = AnimationManager(config, asset_manager)

    # Crear entidades de prueba
    projectile = Projectile(400, 300, 500, 200, 25.0, 300.0, config)
    enemy = Enemy(450, 250, asset_manager, animation_manager, config)

    print(f"✅ Proyectil creado: {projectile}")
    print(f"✅ Enemigo creado: {enemy}")

    # Test de movimiento
    initial_x, initial_y = projectile.x, projectile.y
    projectile.update(1.0 / 60.0)
    print(
        f"✅ Proyectil se movió de ({initial_x}, {initial_y}) a ({projectile.x}, {projectile.y})"
    )

    # Test de colisión
    if projectile.rect.colliderect(enemy.rect):
        print("✅ Colisión detectada entre proyectil y enemigo")
        enemy.take_damage(projectile.get_damage())
        projectile.on_hit()
        print(f"✅ Enemigo recibió {projectile.get_damage()} de daño")
        print(f"✅ Vida del enemigo: {enemy.stats.health}")
    else:
        print("❌ No se detectó colisión")

    # Test de daño
    damage = projectile.get_damage()
    print(f"✅ Daño del proyectil: {damage}")

    # Limpiar
    pygame.quit()
    print("✅ Test del sistema de proyectiles completado")


if __name__ == "__main__":
    test_projectile_system()
