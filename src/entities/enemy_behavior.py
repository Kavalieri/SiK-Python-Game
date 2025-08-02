"""
Enemy Behavior - Comportamiento e IA de Enemigos
===============================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de comportamiento e inteligencia artificial para enemigos.
"""

import math
import random

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
        self.patrol_points: list[tuple[float, float]] = []
        self.current_patrol_index = 0
        self.patrol_timer = 0
        self.patrol_delay = 2000  # milisegundos

        # Seguimiento persistente del jugador
        self.last_player_position = None
        self.tracking_timer = 0.0
        self.max_tracking_time = 10.0  # Segundos sin contacto visual
        self.is_tracking_player = False

    def update(self, dt: float, player_pos: tuple[float, float] | None = None):
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

        # Sistema de seguimiento mejorado
        self._update_tracking_state(player_pos, dt)

        # IA según estado de seguimiento
        if self.is_tracking_player and (player_pos or self.last_player_position):
            target_pos = player_pos if player_pos else self.last_player_position
            self._chase_player(target_pos, dt)
        else:
            self._patrol(dt)

        # Actualizar volteo basado en movimiento
        self.core.update_facing_direction()

    def _update_tracking_state(self, player_pos: tuple[float, float] | None, dt: float):
        """Actualiza el estado de seguimiento persistente del jugador."""
        if player_pos and self._is_player_in_range(player_pos):
            # Jugador detectado - iniciar o continuar seguimiento
            self.last_player_position = player_pos
            self.tracking_timer = 0.0
            self.is_tracking_player = True
        elif self.is_tracking_player:
            # Continuar siguiendo hasta que expire el timer
            self.tracking_timer += dt
            if self.tracking_timer >= self.max_tracking_time:
                self.is_tracking_player = False
                self.last_player_position = None

    def _is_player_in_range(self, player_pos: tuple[float, float]) -> bool:
        """Verifica si el jugador está en rango de detección."""
        distance = math.sqrt(
            (player_pos[0] - self.core.x) ** 2 + (player_pos[1] - self.core.y) ** 2
        )
        detection_range = getattr(self.core, "detection_range", 300)

        # Aumentar rango si está en modo de seguimiento persistente
        if self.is_tracking_player and self.core.persistent_tracking:
            detection_range *= 2.0

        return distance < detection_range

    def _chase_player(self, player_pos: tuple[float, float], dt: float):
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
