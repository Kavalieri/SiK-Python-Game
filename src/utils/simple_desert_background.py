"""
Simple Desert Background - Fondo Simple de Desierto
=================================================

Autor: SiK Team
Fecha: 2024
Descripción: Fondo simple de desierto completamente plano.
"""

import logging

import pygame


class SimpleDesertBackground:
    """
    Fondo simple de desierto completamente plano.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Inicializa el fondo simple de desierto.

        Args:
                screen_width: Ancho de la pantalla
                screen_height: Alto de la pantalla
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logger = logging.getLogger(__name__)

        # Color principal del desierto (arena)
        self.desert_color = (238, 203, 173)  # Color arena cálido

        # Variaciones de color para dar textura sutil
        self.desert_variations = [
            (238, 203, 173),  # Arena clara
            (216, 191, 161),  # Arena media
            (194, 178, 128),  # Arena oscura
            (210, 180, 140),  # Arena cálida
            (222, 184, 135),  # Arena dorada
        ]

        self.logger.info("Fondo plano de desierto inicializado")

    def update(self, delta_time: float):
        """
        Actualiza el fondo (no hace nada en esta versión simple).

        Args:
                delta_time: Tiempo transcurrido desde el último frame
        """
        pass

    def render(self, screen: pygame.Surface, camera_x: float = 0, camera_y: float = 0):
        """
        Renderiza el fondo plano de desierto.

        Args:
                screen: Superficie donde renderizar
                camera_x: Posición X de la cámara (no usado en esta versión)
                camera_y: Posición Y de la cámara (no usado en esta versión)
        """
        # Rellenar todo el fondo con el color principal del desierto
        screen.fill(self.desert_color)

        # Añadir textura sutil con variaciones de color
        self._add_desert_texture(screen)

    def _add_desert_texture(self, screen: pygame.Surface):
        """
        Añade textura sutil al fondo del desierto.

        Args:
                screen: Superficie donde renderizar
        """
        # Crear líneas horizontales sutiles para simular ondulaciones de arena
        for y in range(0, self.screen_height, 20):
            # Seleccionar color de variación
            variation_color = self.desert_variations[
                y // 20 % len(self.desert_variations)
            ]

            # Dibujar línea horizontal sutil
            pygame.draw.line(screen, variation_color, (0, y), (self.screen_width, y), 1)

        # Añadir algunas líneas verticales muy sutiles para simular textura de arena
        for x in range(0, self.screen_width, 50):
            # Color ligeramente más oscuro para las líneas verticales
            line_color = (
                max(0, self.desert_color[0] - 10),
                max(0, self.desert_color[1] - 10),
                max(0, self.desert_color[2] - 10),
            )

            pygame.draw.line(screen, line_color, (x, 0), (x, self.screen_height), 1)
