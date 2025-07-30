"""
Enemy Core - Núcleo del Sistema de Enemigos
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Núcleo base para enemigos con configuración y estado.
"""

from typing import Optional

import pygame

from ..utils.animation_manager import AnimationPlayer


class EnemyCore:
    """Núcleo base para enemigos con configuración y estado básico."""

    def __init__(self, x: float, y: float, enemy_type: str, animation_manager):
        """
        Inicializa el núcleo del enemigo.

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            enemy_type: Tipo de enemigo ('zombiemale' o 'zombieguirl')
            animation_manager: Gestor de animaciones
        """
        # Posición y tipo
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.animation_manager = animation_manager

        # Propiedades físicas base
        self.width = 32
        self.height = 32
        self.speed = 80.0
        self.health = 100
        self.max_health = 100
        self.damage = 20
        self.attack_range = 60
        self.attack_cooldown = 1000
        self.last_attack_time = 0

        # Estado del enemigo
        self.facing_right = True
        self.is_attacking = False
        self.is_dead = False
        self.target = None

        # Sistema de animación
        self.animation_player = AnimationPlayer(animation_manager, enemy_type, "Idle")
        self.current_animation = "Idle"

        # Tracking de movimiento para dirección
        self._last_x = self.x

        # Configuración específica por tipo
        self._setup_enemy_type()

    def _setup_enemy_type(self):
        """Configura propiedades específicas según el tipo de enemigo."""
        if self.enemy_type == "zombiemale":
            self.health = 120
            self.max_health = 120
            self.damage = 25
            self.speed = 70.0
            self.attack_range = 50
        elif self.enemy_type == "zombieguirl":
            self.health = 100
            self.max_health = 100
            self.damage = 20
            self.speed = 90.0
            self.attack_range = 45

    def take_damage(self, damage: int):
        """Recibe daño y actualiza estado."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.current_animation = "Dead"

    def _update_facing_direction(self):
        """Actualiza la dirección a la que mira el enemigo."""
        if hasattr(self, "_last_x"):
            if self.x > self._last_x:
                self.facing_right = True
            elif self.x < self._last_x:
                self.facing_right = False
        self._last_x = self.x

    def update_facing_direction(self):
        """Método público para actualizar dirección."""
        self._update_facing_direction()

    def _update_dead_animation(self):
        """Actualiza la animación de muerte."""
        if self.current_animation != "Dead":
            self.current_animation = "Dead"
            self.animation_player.set_animation("Dead")

    def update_dead_animation(self):
        """Método público para actualizar animación de muerte."""
        self._update_dead_animation()

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """Obtiene el frame actual de la animación con escala y volteo."""
        frame = self.animation_player.get_current_frame()
        if frame:
            frame = pygame.transform.scale(frame, (self.width, self.height))
            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
        return frame

    def get_rect(self) -> pygame.Rect:
        """Obtiene el rectángulo de colisión."""
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )

    def is_attack_ready(self) -> bool:
        """Verifica si puede atacar según cooldown."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time >= self.attack_cooldown

    def reset_attack_state(self):
        """Resetea el estado de ataque."""
        self.is_attacking = False
        if self.current_animation == "Attack":
            self.current_animation = "Idle"

    def update_animation(self):
        """Actualiza el sistema de animación."""
        self.animation_player.set_animation(self.current_animation)
