"""
Player Movement - Sistema de movimiento del jugador
===================================================

Autor: SiK Team
Fecha: 30 de Julio, 2025
Descripción: Sistema de movimiento, input handling y animaciones del jugador.
"""

from typing import Tuple

import pygame

from ..entities.powerup import PowerupType
from .entity import EntityState
from .player_core import AnimationState, PlayerCore


class PlayerMovement:
    """
    Sistema de movimiento del jugador con input handling y animaciones.
    Maneja la lógica de movimiento, entrada del usuario y animaciones.
    """

    def __init__(self, player_core: PlayerCore):
        """
        Inicializa el sistema de movimiento.

        Args:
            player_core: Núcleo del jugador
        """
        self.player_core = player_core

        # Vector de velocidad
        self.velocity_x = 0.0
        self.velocity_y = 0.0

    def handle_input(
        self,
        keys: pygame.key.ScancodeWrapper,
        _mouse_pos: Tuple[int, int],
        mouse_buttons: Tuple[bool, bool, bool],
        player_effects,
    ):
        """
        Maneja la entrada del usuario.

        Args:
            keys: Estado de las teclas
            mouse_pos: Posición del ratón
            mouse_buttons: Estado de los botones del ratón
            player_effects: Sistema de efectos del jugador
        """
        # Reiniciar velocidad
        self.velocity_x = 0
        self.velocity_y = 0

        # Movimiento con WASD
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.player_core.stats.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.player_core.stats.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.player_core.stats.speed
            self.player_core.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.player_core.stats.speed
            self.player_core.facing_right = True

        # Aplicar modificadores de velocidad por efectos
        speed_boost = player_effects.get_effect_value(PowerupType.SPEED)
        if speed_boost > 0:
            self.velocity_x *= 1 + speed_boost
            self.velocity_y *= 1 + speed_boost

        # Disparo con clic izquierdo
        if mouse_buttons[0]:  # Clic izquierdo
            self.player_core.state = EntityState.ATTACKING
        else:
            self.player_core.state = EntityState.IDLE

    def update_movement(self, delta_time: float):
        """
        Actualiza la posición del jugador.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        # Actualizar posición usando el vector velocity
        self.player_core.x += self.velocity_x * delta_time
        self.player_core.y += self.velocity_y * delta_time

        # Mantener dentro de límites
        self.player_core.clamp_position()

    def update_animation(self, _delta_time: float):
        """
        Actualiza las animaciones del jugador.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        # Determinar estado de animación
        new_animation_state = self._get_animation_state()

        if new_animation_state != self.player_core.current_animation_state:
            self.player_core.current_animation_state = new_animation_state
            self.player_core.update_sprite()

    def _get_animation_state(self) -> AnimationState:
        """Determina el estado de animación actual."""
        if self.player_core.state == EntityState.DEAD:
            return AnimationState.DEAD
        elif self.player_core.state == EntityState.ATTACKING:
            return AnimationState.ATTACK
        elif abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1:
            if abs(self.velocity_x) > 50 or abs(self.velocity_y) > 50:
                return AnimationState.RUN
            else:
                return AnimationState.WALK
        else:
            return AnimationState.IDLE

    def get_velocity(self) -> Tuple[float, float]:
        """
        Obtiene la velocidad actual del jugador.

        Returns:
            Tupla con velocidad (x, y)
        """
        return (self.velocity_x, self.velocity_y)

    def set_velocity(self, x: float, y: float):
        """
        Establece la velocidad del jugador.

        Args:
            x: Velocidad en X
            y: Velocidad en Y
        """
        self.velocity_x = x
        self.velocity_y = y

    def is_moving(self) -> bool:
        """
        Verifica si el jugador se está moviendo.

        Returns:
            True si el jugador se está moviendo
        """
        return abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1

    def get_data(self) -> dict:
        """Obtiene datos del movimiento para guardado."""
        return {
            "velocity_x": self.velocity_x,
            "velocity_y": self.velocity_y,
        }

    def load_data(self, data: dict):
        """Carga datos del movimiento desde guardado."""
        self.velocity_x = data.get("velocity_x", 0.0)
        self.velocity_y = data.get("velocity_y", 0.0)
