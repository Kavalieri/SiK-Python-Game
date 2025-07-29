"""
Projectile - Proyectiles del Jugador
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Clase para los proyectiles disparados por el jugador.
"""

import pygame
import math
import logging

from .entity import Entity, EntityType, EntityStats
from ..utils.config_manager import ConfigManager


class Projectile(Entity):
    """
    Representa un proyectil disparado por el jugador.
    """

    def __init__(
        self,
        x: float,
        y: float,
        target_x: float,
        target_y: float,
        damage: float,
        speed: float,
        config: ConfigManager,
    ):
        """
        Inicializa un proyectil.

        Args:
                x: Posición X inicial
                y: Posición Y inicial
                target_x: Posición X objetivo (cursor)
                target_y: Posición Y objetivo (cursor)
                damage: Daño del proyectil
                speed: Velocidad del proyectil
                config: Configuración del juego
        """
        # Calcular dirección hacia el objetivo
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 0:
            dx /= distance
            dy /= distance
        else:
            dx, dy = 0, -1  # Disparar hacia arriba por defecto

        # Crear stats del proyectil
        stats = EntityStats(health=1.0, max_health=1.0, speed=speed, damage=damage)

        super().__init__(
            entity_type=EntityType.PROJECTILE, x=x, y=y, width=8, height=8, stats=stats
        )

        self.config = config
        self.logger = logging.getLogger(__name__)

        # Velocidad y dirección
        self.velocity_x = dx * speed
        self.velocity_y = dy * speed

        # Estado del proyectil
        self.alive = True

        # Configurar sprite
        self._setup_sprite()

        self.logger.debug(
            f"Proyectil creado en ({x}, {y}) hacia ({target_x}, {target_y})"
        )

    def _setup_sprite(self):
        """Configura el sprite del proyectil."""
        try:
            # Intentar cargar sprite de proyectil
            sprite_path = "assets/objects/proyectiles/Explosion_1.png"
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        except Exception:
            # Crear sprite por defecto
            self.sprite = pygame.Surface((self.width, self.height))
            self.sprite.fill((255, 255, 0))  # Amarillo para proyectiles
            pygame.draw.circle(
                self.sprite,
                (255, 255, 0),
                (self.width // 2, self.height // 2),
                self.width // 2,
            )

    def _update_logic(self, delta_time: float):
        """Actualiza la lógica del proyectil."""
        # Mover proyectil
        self.x += self.velocity_x * delta_time * 60
        self.y += self.velocity_y * delta_time * 60

        # Verificar si sale de pantalla
        screen_width = self.config.get("display", "width", 1280)
        screen_height = self.config.get("display", "height", 720)

        if (
            self.x < -self.width
            or self.x > screen_width + self.width
            or self.y < -self.height
            or self.y > screen_height + self.height
        ):
            self.alive = False
            self.logger.debug("Proyectil eliminado por salir de pantalla")

    def get_damage(self) -> float:
        """Obtiene el daño del proyectil."""
        return self.stats.damage

    def on_hit(self):
        """Se llama cuando el proyectil impacta con algo."""
        self.alive = False
        self.logger.debug("Proyectil impactó con objetivo")
