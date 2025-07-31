"""
Sand Particles - Sistema de Partículas de Arena
==============================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Sistema de partículas de arena para efectos atmosféricos del desierto.
"""

import logging
import math
import random
from typing import List, Tuple

import pygame


class SandParticle:
    """Partícula de arena para efectos atmosféricos."""

    def __init__(self, x: float, y: float, screen_width: int, screen_height: int):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Propiedades de la partícula
        self.size = random.uniform(1, 3)
        self.speed = random.uniform(20, 50)
        self.angle = random.uniform(0, 2 * math.pi)
        self.opacity = random.uniform(50, 150)
        self.life = random.uniform(2, 5)
        self.max_life = self.life

        # Color de arena
        self.color = (
            random.randint(200, 255),  # R
            random.randint(180, 220),  # G
            random.randint(120, 160),  # B
        )

    def update(self, delta_time: float):
        """Actualiza la partícula de arena."""
        # Mover partícula
        self.x += math.cos(self.angle) * self.speed * delta_time
        self.y += math.sin(self.angle) * self.speed * delta_time

        # Reducir vida
        self.life -= delta_time
        self.opacity = (self.life / self.max_life) * 150

        # Reiniciar si sale de pantalla o muere
        if (
            self.x < -10
            or self.x > self.screen_width + 10
            or self.y < -10
            or self.y > self.screen_height + 10
            or self.life <= 0
        ):
            self._reset()

    def _reset(self):
        """Reinicia la partícula en una nueva posición."""
        # Aparecer desde los bordes
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.x = random.uniform(-10, self.screen_width + 10)
            self.y = -10
        elif side == "bottom":
            self.x = random.uniform(-10, self.screen_width + 10)
            self.y = self.screen_height + 10
        elif side == "left":
            self.x = -10
            self.y = random.uniform(-10, self.screen_height + 10)
        else:  # right
            self.x = self.screen_width + 10
            self.y = random.uniform(-10, self.screen_height + 10)

        # Reiniciar propiedades
        self.life = random.uniform(2, 5)
        self.max_life = self.life
        self.opacity = random.uniform(50, 150)
        self.angle = random.uniform(0, 2 * math.pi)

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza la partícula de arena."""
        if self.life <= 0:
            return

        # Posición con offset de cámara
        render_x = int(self.x - camera_offset[0])
        render_y = int(self.y - camera_offset[1])

        # Crear superficie con alpha
        particle_surface = pygame.Surface(
            (int(self.size * 2), int(self.size * 2)),
            pygame.SRCALPHA,  # pylint: disable=no-member
        )

        # Color con alpha
        color_with_alpha = (*self.color, int(self.opacity))
        pygame.draw.circle(
            particle_surface,
            color_with_alpha,
            (int(self.size), int(self.size)),
            int(self.size),
        )

        screen.blit(
            particle_surface, (render_x - int(self.size), render_y - int(self.size))
        )


class SandParticleSystem:
    """Sistema gestor de partículas de arena."""

    def __init__(self, screen_width: int, screen_height: int, particle_count: int = 50):
        """
        Inicializa el sistema de partículas.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
            particle_count: Número de partículas a crear
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particle_count = particle_count
        self.particles: List[SandParticle] = []
        self.logger = logging.getLogger(__name__)

        self._create_particles()

    def _create_particles(self):
        """Crea todas las partículas del sistema."""
        self.particles = []
        for _ in range(self.particle_count):
            x = random.uniform(-10, self.screen_width + 10)
            y = random.uniform(-10, self.screen_height + 10)
            particle = SandParticle(x, y, self.screen_width, self.screen_height)
            self.particles.append(particle)

    def update(self, delta_time: float):
        """Actualiza todas las partículas del sistema."""
        for particle in self.particles:
            particle.update(delta_time)

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza todas las partículas del sistema."""
        for particle in self.particles:
            particle.render(screen, camera_offset)

    def set_wind_effect(self, wind_strength: float, wind_angle: float):
        """
        Aplica efecto de viento a las partículas.

        Args:
            wind_strength: Fuerza del viento (0.0 - 1.0)
            wind_angle: Ángulo del viento en radianes
        """
        for particle in self.particles:
            # Aplicar viento modificando el ángulo y velocidad
            wind_factor = wind_strength * 0.5
            particle.angle += wind_angle * wind_factor * 0.1
            particle.speed += wind_strength * 10

    def set_particle_count(self, count: int):
        """
        Cambia el número de partículas del sistema.

        Args:
            count: Nuevo número de partículas
        """
        self.particle_count = count
        if count > len(self.particles):
            # Añadir partículas
            for _ in range(count - len(self.particles)):
                x = random.uniform(-10, self.screen_width + 10)
                y = random.uniform(-10, self.screen_height + 10)
                particle = SandParticle(x, y, self.screen_width, self.screen_height)
                self.particles.append(particle)
        elif count < len(self.particles):
            # Remover partículas
            self.particles = self.particles[:count]
