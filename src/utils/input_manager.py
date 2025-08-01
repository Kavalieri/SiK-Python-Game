"""
Input Manager - Gestor de entrada
================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestiona las entradas del usuario (teclado, ratón, gamepad).
"""

import logging
from collections.abc import Callable
from enum import Enum

import pygame


class InputType(Enum):
    """Tipos de entrada disponibles."""

    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    GAMEPAD = "gamepad"


class InputAction(Enum):
    """Acciones de entrada predefinidas."""

    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    JUMP = "jump"
    ATTACK = "attack"
    INTERACT = "interact"
    PAUSE = "pause"
    MENU = "menu"


class InputManager:
    """
    Gestiona las entradas del usuario.
    """

    def __init__(self):
        """Inicializa el gestor de entrada."""
        self.logger = logging.getLogger(__name__)

        # Estados de entrada
        self.key_states: dict[int, bool] = {}
        self.mouse_buttons: dict[int, bool] = {}
        self.gamepad_buttons: dict[int, bool] = {}
        self.gamepad_axes: dict[int, float] = {}

        # Mapeo de acciones
        self.action_mappings: dict[InputAction, set[int]] = {
            InputAction.MOVE_UP: {pygame.K_w, pygame.K_UP},
            InputAction.MOVE_DOWN: {pygame.K_s, pygame.K_DOWN},
            InputAction.MOVE_LEFT: {pygame.K_a, pygame.K_LEFT},
            InputAction.MOVE_RIGHT: {pygame.K_d, pygame.K_RIGHT},
            InputAction.JUMP: {pygame.K_SPACE},
            InputAction.ATTACK: {pygame.K_j, pygame.K_RETURN},
            InputAction.INTERACT: {pygame.K_e},
            InputAction.PAUSE: {pygame.K_ESCAPE},
            InputAction.MENU: {pygame.K_ESCAPE},
        }

        # Callbacks de eventos
        self.key_callbacks: dict[int, Callable] = {}
        self.action_callbacks: dict[InputAction, Callable] = {}

        # Configuración
        self.enabled = True
        self.gamepad_enabled = True

        self.logger.info("Gestor de entrada inicializado")

    def handle_event(self, event: pygame.event.Event):
        """
        Procesa un evento de Pygame.

        Args:
                event: Evento de Pygame a procesar
        """
        if not self.enabled:
            return

        if event.type == pygame.KEYDOWN:
            self._handle_key_down(event.key)
        elif event.type == pygame.KEYUP:
            self._handle_key_up(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up(event.button)
        elif event.type == pygame.JOYBUTTONDOWN:
            self._handle_gamepad_down(event.button)
        elif event.type == pygame.JOYBUTTONUP:
            self._handle_gamepad_up(event.button)
        elif event.type == pygame.JOYAXISMOTION:
            self._handle_gamepad_axis(event.axis, event.value)

    def _handle_key_down(self, key: int):
        """Procesa una tecla presionada."""
        self.key_states[key] = True

        # Ejecutar callback específico de la tecla
        if key in self.key_callbacks:
            self.key_callbacks[key]()

        # Verificar acciones
        self._check_actions()

    def _handle_key_up(self, key: int):
        """Procesa una tecla liberada."""
        self.key_states[key] = False

    def _handle_mouse_down(self, button: int):
        """Procesa un botón del ratón presionado."""
        self.mouse_buttons[button] = True

    def _handle_mouse_up(self, button: int):
        """Procesa un botón del ratón liberado."""
        self.mouse_buttons[button] = False

    def _handle_gamepad_down(self, button: int):
        """Procesa un botón del gamepad presionado."""
        if self.gamepad_enabled:
            self.gamepad_buttons[button] = True

    def _handle_gamepad_up(self, button: int):
        """Procesa un botón del gamepad liberado."""
        if self.gamepad_enabled:
            self.gamepad_buttons[button] = False

    def _handle_gamepad_axis(self, axis: int, value: float):
        """Procesa movimiento de eje del gamepad."""
        if self.gamepad_enabled:
            self.gamepad_axes[axis] = value

    def _check_actions(self):
        """Verifica si se han activado acciones."""
        for action, keys in self.action_mappings.items():
            if any(self.key_states.get(key, False) for key in keys):
                if action in self.action_callbacks:
                    self.action_callbacks[action]()

    def is_key_pressed(self, key: int) -> bool:
        """
        Verifica si una tecla está presionada.

        Args:
                key: Código de la tecla

        Returns:
                True si la tecla está presionada
        """
        return self.key_states.get(key, False)

    def is_action_pressed(self, action: InputAction) -> bool:
        """
        Verifica si una acción está activa.

        Args:
                action: Acción a verificar

        Returns:
                True si la acción está activa
        """
        if action not in self.action_mappings:
            return False

        return any(
            self.key_states.get(key, False) for key in self.action_mappings[action]
        )

    def get_mouse_position(self) -> tuple:
        """
        Obtiene la posición actual del ratón.

        Returns:
                Tupla (x, y) con la posición del ratón
        """
        return pygame.mouse.get_pos()

    def is_mouse_button_pressed(self, button: int) -> bool:
        """
        Verifica si un botón del ratón está presionado.

        Args:
                button: Número del botón

        Returns:
                True si el botón está presionado
        """
        return self.mouse_buttons.get(button, False)

    def get_gamepad_axis(self, axis: int) -> float:
        """
        Obtiene el valor de un eje del gamepad.

        Args:
                axis: Número del eje

        Returns:
                Valor del eje (-1.0 a 1.0)
        """
        return self.gamepad_axes.get(axis, 0.0)

    def add_key_callback(self, key: int, callback: Callable):
        """
        Añade un callback para una tecla específica.

        Args:
                key: Código de la tecla
                callback: Función a ejecutar
        """
        self.key_callbacks[key] = callback

    def add_action_callback(self, action: InputAction, callback: Callable):
        """
        Añade un callback para una acción específica.

        Args:
                action: Acción
                callback: Función a ejecutar
        """
        self.action_callbacks[action] = callback

    def set_action_mapping(self, action: InputAction, keys: set[int]):
        """
        Establece el mapeo de teclas para una acción.

        Args:
                action: Acción a mapear
                keys: Conjunto de teclas
        """
        self.action_mappings[action] = keys
        self.logger.debug(f"Mapeo actualizado para {action}: {keys}")

    def reset_states(self):
        """Reinicia todos los estados de entrada."""
        self.key_states.clear()
        self.mouse_buttons.clear()
        self.gamepad_buttons.clear()
        self.gamepad_axes.clear()
