"""
Enemy System - Sistema de Enemigos
=================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de enemigos con animaciones y volteo.
"""

import math
import random

import pygame

from ..utils.animation_manager import AnimationPlayer


class Enemy:
    """Clase base para enemigos con animaciones y volteo."""

    def __init__(self, x: float, y: float, enemy_type: str, animation_manager):
        """
        Inicializa un enemigo.

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            enemy_type: Tipo de enemigo ('zombiemale' o 'zombieguirl')
            animation_manager: Gestor de animaciones
        """
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.animation_manager = animation_manager

        # Propiedades físicas
        self.width = 32  # Tamaño reducido como el jugador
        self.height = 32
        self.speed = 80.0  # Velocidad aumentada para mejor persecución
        self.health = 100
        self.max_health = 100
        self.damage = 20
        self.attack_range = 60
        self.attack_cooldown = 1000  # milisegundos
        self.last_attack_time = 0

        # Estado del enemigo
        self.facing_right = True  # Dirección a la que mira
        self.is_attacking = False
        self.is_dead = False
        self.target = None  # Objetivo a perseguir

        # Animación
        self.animation_player = AnimationPlayer(animation_manager, enemy_type, "Idle")
        self.current_animation = "Idle"

        # IA básica
        self.patrol_points = []
        self.current_patrol_index = 0
        self.patrol_timer = 0
        self.patrol_delay = 2000  # milisegundos

        # Configuración específica por tipo
        self._setup_enemy_type()

    def _setup_enemy_type(self):
        """Configura propiedades específicas según el tipo de enemigo."""
        if self.enemy_type == "zombiemale":
            self.health = 120
            self.max_health = 120
            self.damage = 25
            self.speed = 70.0  # Velocidad ajustada
            self.attack_range = 50
        elif self.enemy_type == "zombieguirl":
            self.health = 100
            self.max_health = 100
            self.damage = 20
            self.speed = 90.0  # Velocidad ajustada
            self.attack_range = 45

    def update(self, dt: float, player_pos: tuple[float, float] | None = None):
        """
        Actualiza el estado del enemigo.

        Args:
            dt: Delta time en segundos
            player_pos: Posición del jugador (x, y) si está cerca
        """
        if self.is_dead:
            self._update_dead_animation()
            return

        # Actualizar animación
        self.animation_player.set_animation(self.current_animation)

        # IA básica
        if player_pos and self._is_player_in_range(player_pos):
            self._chase_player(player_pos, dt)
        else:
            self._patrol(dt)

        # Actualizar volteo basado en la dirección del movimiento
        self._update_facing_direction()

    def _is_player_in_range(self, player_pos: tuple[float, float]) -> bool:
        """Verifica si el jugador está en rango de detección."""
        distance = math.sqrt(
            (player_pos[0] - self.x) ** 2 + (player_pos[1] - self.y) ** 2
        )
        return distance < 300  # Rango de detección aumentado

    def _chase_player(self, player_pos: tuple[float, float], dt: float):
        """Persigue al jugador."""
        # Calcular dirección hacia el jugador
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Normalizar y aplicar velocidad
            dx = (dx / distance) * self.speed * dt
            dy = (dy / distance) * self.speed * dt

            # Mover hacia el jugador
            self.x += dx
            self.y += dy

            # Verificar si está en rango de ataque
            if distance <= self.attack_range:
                self._attack_player()
                self.current_animation = "Attack"
            else:
                self.current_animation = "Walk"

            # Debug: mostrar distancia al jugador
            if distance < 100:
                print(f"Enemigo {self.enemy_type} a {distance:.1f} píxeles del jugador")
        else:
            self.current_animation = "Idle"

    def _patrol(self, dt: float):
        """Patrulla en un área definida."""
        if not self.patrol_points:
            # Crear puntos de patrulla aleatorios si no existen
            self._generate_patrol_points()

        if self.patrol_points:
            target_point = self.patrol_points[self.current_patrol_index]
            dx = target_point[0] - self.x
            dy = target_point[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 10:  # Llegó al punto de patrulla
                self.current_patrol_index = (self.current_patrol_index + 1) % len(
                    self.patrol_points
                )
                self.current_animation = "Idle"
            else:
                # Mover hacia el punto de patrulla
                if distance > 0:
                    dx = (dx / distance) * self.speed * dt
                    dy = (dy / distance) * self.speed * dt
                    self.x += dx
                    self.y += dy
                    self.current_animation = "Walk"

    def _generate_patrol_points(self):
        """Genera puntos de patrulla aleatorios alrededor de la posición inicial."""
        base_x, base_y = self.x, self.y
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
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.current_animation = "Attack"
            self.last_attack_time = current_time

            # Resetear el estado de ataque después de un tiempo
            pygame.time.set_timer(
                pygame.USEREVENT + 1, 500
            )  # 500ms para resetear ataque

    def _update_facing_direction(self):
        """Actualiza la dirección a la que mira el enemigo."""
        # Determinar la dirección basada en el movimiento o la posición del jugador
        if hasattr(self, "_last_x"):
            if self.x > self._last_x:
                self.facing_right = True
            elif self.x < self._last_x:
                self.facing_right = False
        self._last_x = self.x

    def _update_dead_animation(self):
        """Actualiza la animación de muerte."""
        if self.current_animation != "Dead":
            self.current_animation = "Dead"
            self.animation_player.set_animation("Dead")

    def take_damage(self, damage: int):
        """Recibe daño."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.current_animation = "Dead"

    def get_current_frame(self) -> pygame.Surface | None:
        """Obtiene el frame actual de la animación."""
        frame = self.animation_player.get_current_frame()
        if frame:
            # Escalar al tamaño correcto (32x32)
            frame = pygame.transform.scale(frame, (self.width, self.height))
            if not self.facing_right:
                # Voltear horizontalmente si mira hacia la izquierda
                frame = pygame.transform.flip(frame, True, False)
        return frame

    def get_rect(self) -> pygame.Rect:
        """Obtiene el rectángulo de colisión."""
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )

    def is_attack_ready(self) -> bool:
        """Verifica si puede atacar."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time >= self.attack_cooldown

    def reset_attack_state(self):
        """Resetea el estado de ataque."""
        self.is_attacking = False
        if self.current_animation == "Attack":
            self.current_animation = "Idle"


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
        self.spawn_delay = 1500  # milisegundos (más rápido)
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
            if enemy.is_dead and enemy.animation_player.is_animation_completed():
                self.enemies.remove(enemy)

        # Generar nuevos enemigos
        self._spawn_enemies(dt)

    def _spawn_enemies(self, dt: float):
        """Genera nuevos enemigos."""
        if len(self.enemies) >= self.max_enemies:
            return

        self.spawn_timer += dt * 1000  # Convertir a milisegundos

        if self.spawn_timer >= self.spawn_delay:
            self._spawn_enemy()
            self.spawn_timer = 0

    def _spawn_enemy(self):
        """
        Genera un enemigo en una posición aleatoria en los bordes del mundo.

        Ejemplo:
            >>> gestor_enemigos._spawn_enemy()
        """
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

        enemy = Enemy(x, y, enemy_type, self.animation_manager)
        self.enemies.append(enemy)

    def render(
        self, screen: pygame.Surface, camera_offset: tuple[float, float] = (0, 0)
    ):
        """
        Renderiza todos los enemigos.

        Args:
            screen: Superficie donde renderizar
            camera_offset: Offset de la cámara
        """
        for enemy in self.enemies:
            frame = enemy.get_current_frame()
            if frame:
                # Aplicar offset de cámara
                render_x = enemy.x - camera_offset[0] - frame.get_width() // 2
                render_y = enemy.y - camera_offset[1] - frame.get_height() // 2

                screen.blit(frame, (render_x, render_y))

    def get_enemies_in_range(
        self, pos: tuple[float, float], range: float
    ) -> list[Enemy]:
        """
        Obtiene enemigos en un rango específico.

        Args:
            pos: Posición central del rango (x, y).
            range: Distancia máxima para incluir enemigos.

        Returns:
            List[Enemy]: Lista de enemigos dentro del rango especificado.

        Ejemplo:
            >>> enemigos_cercanos = gestor_enemigos.get_enemies_in_range((100, 200), 50)
            >>> print(len(enemigos_cercanos))
        """
        enemies_in_range = []
        for enemy in self.enemies:
            distance = math.sqrt((pos[0] - enemy.x) ** 2 + (pos[1] - enemy.y) ** 2)
            if distance <= range:
                enemies_in_range.append(enemy)
        return enemies_in_range

    def clear_all_enemies(self):
        """Elimina todos los enemigos."""
        self.enemies.clear()

    def get_enemy_count(self) -> int:
        """Obtiene el número de enemigos activos."""
        return len(self.enemies)
