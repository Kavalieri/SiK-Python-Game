"""
Loading Scene Renderer - Renderizado de la pantalla de carga
=============================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Renderizado de elementos visuales de la pantalla de carga.
"""

import time
from typing import TYPE_CHECKING

import pygame

from utils.logger import get_logger

if TYPE_CHECKING:
    from .loading_scene_core import LoadingSceneCore


class LoadingSceneRenderer:
    """
    Renderizador para la escena de carga.
    """

    def __init__(self, core: "LoadingSceneCore"):
        """
        Inicializa el renderizador.

        Args:
            core: Núcleo de la escena de carga
        """
        self.core = core
        self.logger = get_logger("SiK_Game")

    def render_all(self):
        """Renderiza todos los elementos de la pantalla de carga."""
        # Fondo con gradiente
        self._render_background()

        # Título
        self._render_title()

        # Barra de progreso
        self._render_progress_bar()

        # Mensaje actual
        self._render_current_message()

        # Indicador de carga animado
        self._render_loading_indicator()

        # Información adicional
        self._render_additional_info()

    def _render_background(self):
        """Renderiza el fondo con gradiente."""
        height = self.core.screen.get_height()
        for y in range(height):
            # Gradiente de azul oscuro a azul claro
            ratio = y / height
            color = (
                int(20 + ratio * 30),  # R
                int(40 + ratio * 60),  # G
                int(80 + ratio * 100),  # B
            )
            pygame.draw.line(
                self.core.screen, color, (0, y), (self.core.screen.get_width(), y)
            )

    def _render_title(self):
        """Renderiza el título del juego."""
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)

        # Título principal configurable
        title_text = font_large.render(self.core.title, True, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(self.core.screen.get_width() // 2, 150)
        )
        self.core.screen.blit(title_text, title_rect)

        # Subtítulo configurable
        subtitle_text = font_small.render(self.core.subtitle, True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(
            center=(self.core.screen.get_width() // 2, 200)
        )
        self.core.screen.blit(subtitle_text, subtitle_rect)

    def _render_progress_bar(self):
        """Renderiza la barra de progreso."""
        bar_width = 600
        bar_height = 30
        bar_x = (self.core.screen.get_width() - bar_width) // 2
        bar_y = 300

        # Fondo de la barra
        pygame.draw.rect(
            self.core.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height)
        )
        pygame.draw.rect(
            self.core.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), 2
        )

        # Barra de progreso
        progress_width = int(bar_width * self.core.loading_progress)
        if progress_width > 0:
            # Gradiente de color según el progreso
            if self.core.loading_progress < 0.5:
                color = (255, 100, 100)  # Rojo
            elif self.core.loading_progress < 0.8:
                color = (255, 255, 100)  # Amarillo
            else:
                color = (100, 255, 100)  # Verde

            pygame.draw.rect(
                self.core.screen, color, (bar_x, bar_y, progress_width, bar_height)
            )

        # Texto de progreso
        font = pygame.font.Font(None, 24)
        progress_text = font.render(
            f"{self.core.loading_progress:.1%}", True, (255, 255, 255)
        )
        progress_rect = progress_text.get_rect(
            center=(self.core.screen.get_width() // 2, bar_y + bar_height + 20)
        )
        self.core.screen.blit(progress_text, progress_rect)

    def _render_current_message(self):
        """Renderiza el mensaje actual de carga."""
        if self.core.current_message_index < len(self.core.loading_messages):
            font = pygame.font.Font(None, 28)
            message = self.core.loading_messages[self.core.current_message_index]
            message_text = font.render(message, True, (220, 220, 220))
            message_rect = message_text.get_rect(
                center=(self.core.screen.get_width() // 2, 400)
            )
            self.core.screen.blit(message_text, message_rect)

    def _render_loading_indicator(self):
        """Renderiza un indicador de carga animado."""
        dot_count = 3
        dot_spacing = 20
        animation_speed = 0.3
        dot_offset = int((time.time() * animation_speed) % dot_count)

        start_x = self.core.screen.get_width() // 2 - (dot_count * dot_spacing) // 2
        y = 450

        for i in range(dot_count):
            x = start_x + i * dot_spacing
            alpha = 255 if i == dot_offset else 100
            color = (255, 255, 255, alpha)

            # Crear superficie con alpha
            dot_surface = pygame.Surface((8, 8), 32)  # 32 = SRCALPHA
            pygame.draw.circle(dot_surface, color, (4, 4), 4)
            self.core.screen.blit(dot_surface, (x, y))

    def _render_additional_info(self):
        """Renderiza información adicional."""
        font = pygame.font.Font(None, 20)

        # Versión configurable
        version_text = font.render(self.core.version, True, (150, 150, 150))
        version_rect = version_text.get_rect(
            bottomright=(
                self.core.screen.get_width() - 20,
                self.core.screen.get_height() - 20,
            )
        )
        self.core.screen.blit(version_text, version_rect)

        # Consejo aleatorio
        tip_text = font.render(
            f"Consejo: {self.core.current_tip}", True, (180, 220, 255)
        )
        tip_rect = tip_text.get_rect(center=(self.core.screen.get_width() // 2, 500))
        self.core.screen.blit(tip_text, tip_rect)

        # Instrucciones
        if self.core.loading_complete:
            instruction_text = font.render(
                "Presiona cualquier tecla para continuar", True, (200, 200, 200)
            )
            instruction_rect = instruction_text.get_rect(
                center=(self.core.screen.get_width() // 2, 550)
            )
            self.core.screen.blit(instruction_text, instruction_rect)
