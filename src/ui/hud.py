"""
HUD - Bridge de Compatibilidad
=============================

Autor: SiK Team
Fecha: 2024
Descripción: Bridge de compatibilidad que mantiene la API original del HUD.
             Redirige todas las llamadas al nuevo sistema modular.
"""

from .hud_core import HUDCore


class HUD:
    """
    Bridge de compatibilidad para mantener la API original del HUD.

    Esta clase actúa como un proxy hacia el nuevo sistema modular HUDCore,
    preservando la compatibilidad con el código existente.
    """

    def __init__(self, screen, config, game_state):
        """Inicializa el HUD usando el nuevo sistema modular."""
        self.core = HUDCore(screen, config, game_state)

    def update(self, delta_time: float):
        """Actualiza el HUD."""
        self.core.update(delta_time)

    def render(self, player=None):
        """Renderiza el HUD."""
        self.core.render(player)

    def toggle_visibility(self):
        """Alterna la visibilidad del HUD."""
        self.core.toggle_visibility()

    def toggle_debug_mode(self):
        """Alterna el modo debug del HUD."""
        self.core.toggle_debug_mode()

    def set_element_visibility(self, element_name: str, visible: bool):
        """Establece la visibilidad de un elemento específico."""
        self.core.set_element_visibility(element_name, visible)

    # Propiedades para compatibilidad
    @property
    def visible(self):
        """Estado de visibilidad del HUD."""
        return self.core.visible

    @visible.setter
    def visible(self, value: bool):
        """Establece la visibilidad del HUD."""
        self.core.visible = value

    @property
    def debug_mode(self):
        """Estado del modo debug."""
        return self.core.debug_mode

    @debug_mode.setter
    def debug_mode(self, value: bool):
        """Establece el modo debug."""
        self.core.debug_mode = value
