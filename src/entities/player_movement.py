"""
Player Movement - Sistema de movimiento del jugador
===================================================

Autor: SiK Team
Fecha: 30 de Julio, 2025
Descripción: Sistema de movimiento, input handling y animaciones del jugador.
"""

import pygame

from entities.powerup import PowerupType

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

        # Sistema de ataque
        self.attack_timer = 0.0
        self.attack_duration = 0.4  # Duración de la animación de ataque (400ms)
        self.is_attacking = False

        # Cache para optimización
        self._last_mouse_pos = (0, 0)
        self._last_animation_state = None

    def handle_input(
        self,
        keys: pygame.key.ScancodeWrapper,
        mouse_pos: tuple[int, int],
        mouse_buttons: tuple[bool, bool, bool],
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

        # Determinar dirección del personaje basada en el ratón
        self._update_facing_direction(mouse_pos)

        # Movimiento con WASD
        if keys[119] or keys[273]:  # W or UP
            self.velocity_y = -self.player_core.stats.speed
        if keys[115] or keys[274]:  # S or DOWN
            self.velocity_y = self.player_core.stats.speed
        if keys[97] or keys[276]:  # A or LEFT
            self.velocity_x = -self.player_core.stats.speed
        if keys[100] or keys[275]:  # D or RIGHT
            self.velocity_x = self.player_core.stats.speed

        # Aplicar modificadores de velocidad por efectos
        speed_boost = (
            player_effects.get_effect_value(PowerupType.SPEED)
            if player_effects
            else 0.0
        )
        if speed_boost > 0:
            self.velocity_x *= 1 + speed_boost
            self.velocity_y *= 1 + speed_boost

        # Manejar ataque con clic izquierdo
        self._handle_attack_input(mouse_buttons[0])

    def _update_facing_direction(self, mouse_pos: tuple[int, int]):
        """
        Actualiza la dirección del personaje basada en la posición del ratón.

        Args:
            mouse_pos: Posición del ratón en la pantalla (coordenadas de pantalla)
        """
        # Solo actualizar si la posición del ratón cambió significativamente (optimización)
        if abs(mouse_pos[0] - getattr(self, "_last_mouse_x", 0)) > 5:
            self._last_mouse_x = mouse_pos[0]

            # Obtener centro de la pantalla para calcular dirección relativa
            # El mouse_pos ya viene en coordenadas de pantalla
            screen_center_x = 640  # Mitad de 1280px (pantalla)

            # Determinar dirección horizontal basada en la mitad de la pantalla
            if mouse_pos[0] > screen_center_x:
                new_facing = True  # Mirando a la derecha
            elif mouse_pos[0] < screen_center_x:
                new_facing = False  # Mirando a la izquierda
            else:
                return  # Mantener dirección actual si está en el centro exacto

            # Solo actualizar si cambió la dirección (evitar updates innecesarios)
            if self.player_core.facing_right != new_facing:
                self.player_core.facing_right = new_facing
                self.player_core.update_sprite()  # Actualizar sprite inmediatamente

    def _handle_attack_input(self, mouse_clicked: bool):
        """
        Maneja la entrada de ataque.

        Args:
            mouse_clicked: Si se hizo clic con el botón izquierdo
        """
        if mouse_clicked and not self.is_attacking:
            # Iniciar ataque
            self.is_attacking = True
            self.attack_timer = self.attack_duration
            self.player_core.state = EntityState.ATTACKING
            # Resetear animación de ataque para que empiece desde el principio
            self.player_core.current_frame_index = 0
            self.player_core.animation_timer = (
                0.0  # No cambiar a IDLE aquí, se maneja en update_animation
            )

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

    def update_animation(self, delta_time: float):
        """
        Actualiza las animaciones del jugador.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        # Actualizar temporizador de ataque
        if self.is_attacking:
            self.attack_timer -= delta_time
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.player_core.state = EntityState.IDLE

        # Determinar estado de animación solo si es necesario (optimización)
        new_animation_state = self._get_animation_state()

        if new_animation_state != self._last_animation_state:
            self._last_animation_state = new_animation_state
            self.player_core.current_animation_state = new_animation_state
            # Resetear animación al cambiar de estado
            self.player_core.current_frame_index = 0
            self.player_core.animation_timer = 0.0
            self.player_core.update_sprite()
            # No llamar update_animation_timing aquí para evitar timing inmediato
        else:
            # Actualizar timing de la animación solo si no cambió de estado
            self.player_core.update_animation_timing(delta_time)

    def _get_animation_state(self) -> AnimationState:
        """Determina el estado de animación actual basado en el estado del jugador."""
        # Prioridad 1: Estado de muerte
        if self.player_core.state == EntityState.DEAD:
            return AnimationState.DEAD

        # Prioridad 2: Estado de ataque (tiene precedencia sobre movimiento)
        if self.player_core.state == EntityState.ATTACKING:
            return AnimationState.ATTACK

        # Prioridad 3: Estados de movimiento
        is_moving = abs(self.velocity_x) > 0.1 or abs(self.velocity_y) > 0.1
        if is_moving:
            # Determinar si es caminata o carrera basado en velocidad
            total_speed = (self.velocity_x**2 + self.velocity_y**2) ** 0.5
            if total_speed > 150:  # Umbral para correr
                return AnimationState.RUN
            else:
                return AnimationState.WALK

        # Por defecto: IDLE
        return AnimationState.IDLE

    def get_velocity(self) -> tuple[float, float]:
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
