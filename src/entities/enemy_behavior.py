"""
Enemy Behavior - Comportamiento e IA de Enemigos
===============================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de comportamiento e inteligencia artificial para enemigos.
"""

import math
import random
from typing import List, Optional, Tuple

import pygame


class EnemyBehavior:
    """Sistema de comportamiento e IA para enemigos."""

    def __init__(self, enemy_core):
        """
        Inicializa el sistema de comportamiento.

        Args:
            enemy_core: Instancia de EnemyCore con estado básico
        """
        self.core = enemy_core

        # IA y patrullaje
        self.patrol_points: List[Tuple[float, float]] = []
        self.current_patrol_index = 0
        self.patrol_timer = 0
        self.patrol_delay = 2000  # milisegundos

    def update(self, dt: float, player_pos: Optional[Tuple[float, float]] = None):
        """
        Actualiza el comportamiento del enemigo.

        Args:
            dt: Delta time en segundos
            player_pos: Posición del jugador (x, y) si está cerca
        """
        if self.core.is_dead:
            self.core.update_dead_animation()
            return

        # Actualizar animación
        self.core.update_animation()

        # IA básica
        if player_pos and self._is_player_in_range(player_pos):
            self._chase_player(player_pos, dt)
        else:
            self._patrol(dt)

        # Actualizar volteo basado en movimiento
        self.core.update_facing_direction()

    def _is_player_in_range(self, player_pos: Tuple[float, float]) -> bool:
        """Verifica si el jugador está en rango de detección."""
        distance = math.sqrt(
            (player_pos[0] - self.core.x) ** 2 + (player_pos[1] - self.core.y) ** 2
        )
        return distance < 300  # Rango de detección

    def _chase_player(self, player_pos: Tuple[float, float], dt: float):
        """Persigue al jugador calculando dirección y movimiento."""
        dx = player_pos[0] - self.core.x
        dy = player_pos[1] - self.core.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Normalizar y aplicar velocidad
            dx = (dx / distance) * self.core.speed * dt
            dy = (dy / distance) * self.core.speed * dt

            # Mover hacia el jugador
            self.core.x += dx
            self.core.y += dy

            # Verificar si está en rango de ataque
            if distance <= self.core.attack_range:
                self._attack_player()
                self.core.current_animation = "Attack"
            else:
                self.core.current_animation = "Walk"

            # Debug opcional
            if distance < 100:
                print(
                    f"Enemigo {self.core.enemy_type} a {distance:.1f} píxeles del jugador"
                )
        else:
            self.core.current_animation = "Idle"

    def _patrol(self, dt: float):
        """Patrulla en un área definida usando puntos de patrulla."""
        if not self.patrol_points:
            self._generate_patrol_points()

        if self.patrol_points:
            target_point = self.patrol_points[self.current_patrol_index]
            dx = target_point[0] - self.core.x
            dy = target_point[1] - self.core.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 10:  # Llegó al punto de patrulla
                self.current_patrol_index = (self.current_patrol_index + 1) % len(
                    self.patrol_points
                )
                self.core.current_animation = "Idle"
            else:
                # Mover hacia el punto de patrulla
                if distance > 0:
                    dx = (dx / distance) * self.core.speed * dt
                    dy = (dy / distance) * self.core.speed * dt
                    self.core.x += dx
                    self.core.y += dy
                    self.core.current_animation = "Walk"

    def _generate_patrol_points(self):
        """Genera puntos de patrulla aleatorios alrededor de la posición inicial."""
        base_x, base_y = self.core.x, self.core.y
        patrol_radius = 100

        self.patrol_points = [
            (
                base_x + random.randint(-patrol_radius, patrol_radius),
                base_y + random.randint(-patrol_radius, patrol_radius),
            )
            for _ in range(3)
        ]

    def _attack_player(self):
        """Ataca al jugador si el cooldown ha terminado."""
        current_time = pygame.time.get_ticks()
        if current_time - self.core.last_attack_time >= self.core.attack_cooldown:
            self.core.is_attacking = True
            self.core.current_animation = "Attack"
            self.core.last_attack_time = current_time

            # Resetear el estado de ataque después de un tiempo
            # Nota: Timer se maneja externamente por simplicidad
