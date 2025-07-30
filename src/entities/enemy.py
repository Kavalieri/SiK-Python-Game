"""
Enemy System - Fachada de Compatibilidad
=======================================

Autor: SiK Team
Fecha: 2024
Descripción: Fachada que mantiene API original del sistema de enemigos.
"""

# Imports para compatibilidad
from .enemy_core import EnemyCore
from .enemy_behavior import EnemyBehavior
from .enemy_manager import Enemy, EnemyManager

# Re-exportar clases principales para mantener compatibilidad
__all__ = ["Enemy", "EnemyManager", "EnemyCore", "EnemyBehavior"]


# Clase Enemy ya está en enemy_manager.py integrando Core + Behavior
# EnemyManager ya está en enemy_manager.py con funcionalidad completa

# Esta fachada permite que el código existente siga funcionando:
# from src.entities.enemy import Enemy, EnemyManager


# Funciones de utilidad adicionales si se necesitan en el futuro
def create_enemy(x: float, y: float, enemy_type: str, animation_manager):
    """
    Función de utilidad para crear un enemigo.

    Args:
        x: Posición X inicial
        y: Posición Y inicial
        enemy_type: Tipo de enemigo
        animation_manager: Gestor de animaciones

    Returns:
        Nueva instancia de Enemy
    """
    return Enemy(x, y, enemy_type, animation_manager)


def create_enemy_manager(animation_manager):
    """
    Función de utilidad para crear un gestor de enemigos.

    Args:
        animation_manager: Gestor de animaciones

    Returns:
        Nueva instancia de EnemyManager
    """
    return EnemyManager(animation_manager)
