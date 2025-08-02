"""
Enemy Manager - Gestor de Múltiples Enemigos
===========================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestión y spawning de múltiples enemigos en el juego.
"""

import math
import random

import pygame

from .enemy_behavior import EnemyBehavior
from .enemy_core import EnemyCore


class Enemy:
    """Enemigo completo que integra Core + Behavior."""

    def __init__(self, x: float, y: float, enemy_type: str, animation_manager):
        """Inicializa un enemigo completo."""
        self.core = EnemyCore(x, y, enemy_type, animation_manager)
        self.behavior = EnemyBehavior(self.core)

    def update(self, dt: float, player_pos: tuple[float, float] | None = None):
        """Actualiza el enemigo usando el sistema de comportamiento."""
        self.behavior.update(dt, player_pos)

    # Propiedades delegadas para compatibilidad
    @property
    def x(self) -> float:
        """Obtiene la posición X del enemigo."""
        return self.core.x

    @property
    def y(self) -> float:
        """Obtiene la posición Y del enemigo."""
        return self.core.y

    @property
    def is_dead(self) -> bool:
        """Verifica si el enemigo está muerto."""
        return self.core.is_dead

    @property
    def width(self) -> float:
        """Obtiene el ancho del enemigo."""
        return self.core.width

    @property
    def height(self) -> float:
        """Obtiene el alto del enemigo."""
        return self.core.height

    @property
    def damage(self) -> int:
        """Obtiene el daño del enemigo."""
        return self.core.damage

    def take_damage(self, damage: int):
        """Delega daño al core."""
        self.core.take_damage(damage)

    def get_current_frame(self):
        """Delega obtención de frame al core."""
        return self.core.get_current_frame()

    def get_rect(self):
        """Delega rectángulo de colisión al core."""
        return self.core.get_rect()

    def is_attack_ready(self) -> bool:
        """Verifica si el enemigo puede atacar."""
        return self.core.is_attack_ready()

    def reset_attack_state(self):
        """Resetea el estado de ataque del enemigo."""
        self.core.reset_attack_state()

    def render(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Renderiza el enemigo."""
        frame = self.get_current_frame()
        if frame:
            screen.blit(frame, (self.x - camera_offset[0], self.y - camera_offset[1]))


class EnemyManager:
    """Gestor de enemigos para el juego."""

    def __init__(self, animation_manager):
        """
        Inicializa el gestor de enemigos.

        Args:
            animation_manager: Gestor de animaciones
        """
        self.animation_manager = animation_manager
        self.enemies: list[Enemy] = []
        self.spawn_timer = 0
        self.spawn_delay = 1500  # milisegundos
        self.max_enemies = 8

    def update(self, dt: float, player_pos: tuple[float, float] | None = None):
        """
        Actualiza todos los enemigos.

        Args:
            dt: Delta time en segundos
            player_pos: Posición del jugador
        """
        # Actualizar enemigos existentes
        for enemy in self.enemies[:]:
            enemy.update(dt, player_pos)

            # Remover enemigos muertos después de un tiempo
            if enemy.is_dead and enemy.core.animation_player.is_animation_completed():
                self.enemies.remove(enemy)

        # Generar nuevos enemigos
        self._spawn_enemies(dt)

    def _spawn_enemies(self, dt: float):
        """Genera nuevos enemigos si no se ha alcanzado el máximo."""
        if len(self.enemies) >= self.max_enemies:
            return

        self.spawn_timer += dt * 1000  # Convertir a milisegundos

        if self.spawn_timer >= self.spawn_delay:
            self._spawn_enemy()
            self.spawn_timer = 0

    def _spawn_enemy(self):
        """Genera un enemigo en una posición aleatoria en los bordes del mundo."""
        world_width = 5000
        world_height = 5000

        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            x = random.randint(0, world_width)
            y = -50
        elif side == "bottom":
            x = random.randint(0, world_width)
            y = world_height + 50
        elif side == "left":
            x = -50
            y = random.randint(0, world_height)
        else:  # right
            x = world_width + 50
            y = random.randint(0, world_height)

        enemy_type = random.choice(["zombiemale", "zombieguirl"])

        try:
            new_enemy = Enemy(x, y, enemy_type, self.animation_manager)
            self.enemies.append(new_enemy)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error("Error creando enemigo %s: %s", enemy_type, e)

    def render(self, screen, camera_offset: tuple[float, float] = (0, 0)):
        """Renderiza todos los enemigos."""
        for enemy in self.enemies:
            frame = enemy.get_current_frame()
            if frame:
                rect = enemy.get_rect()
                screen_x = rect.x - camera_offset[0]
                screen_y = rect.y - camera_offset[1]
                screen.blit(frame, (screen_x, screen_y))

    def get_enemies_in_range(
        self, pos: tuple[float, float], radius: float
    ) -> list[Enemy]:
        """
        Obtiene enemigos en un rango específico desde una posición.

        Args:
            pos: Posición central del rango (x, y)
            radius: Distancia máxima para incluir enemigos

        Returns:
            Lista de enemigos dentro del rango especificado
        """
        enemies_in_range = []
        for enemy in self.enemies:
            distance = math.sqrt((pos[0] - enemy.x) ** 2 + (pos[1] - enemy.y) ** 2)
            if distance <= radius:
                enemies_in_range.append(enemy)
        return enemies_in_range

    def clear_all_enemies(self):
        """Elimina todos los enemigos."""
        self.enemies.clear()

    def get_enemy_count(self) -> int:
        """Obtiene el número de enemigos activos."""
        return len(self.enemies)
