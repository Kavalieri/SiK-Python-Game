"""
Entity Core - Clase Base de Entidades Refactorizada
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Clase base Entity usando arquitectura modular.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple

import pygame

from .entity_effects import EntityEffectsSystem
from .entity_rendering import EntityRenderingSystem
from .entity_types import EntityState, EntityStats, EntityType


class Entity(ABC):
    """Clase base abstracta para todas las entidades del juego."""

    def __init__(
        self,
        entity_type: EntityType,
        x: float,
        y: float,
        width: int,
        height: int,
        stats: Optional[EntityStats] = None,
    ):
        """
        Inicializa una entidad base.

        Args:
            entity_type: Tipo de entidad
            x: Posición X inicial
            y: Posición Y inicial
            width: Ancho de la entidad
            height: Alto de la entidad
            stats: Estadísticas de la entidad
        """
        self.entity_type = entity_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stats = stats or EntityStats()

        # Estado y movimiento
        self.state = EntityState.IDLE
        self.direction = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

        # Colisiones
        self.collision_rect = pygame.Rect(x, y, width, height)
        self.collision_enabled = True

        # Sistemas modulares
        self.effects_system = EntityEffectsSystem(self)
        self.rendering_system = EntityRenderingSystem(self)

        # Logging
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.logger.debug("Entidad %s creada en (%s, %s)", entity_type.value, x, y)

        # Configuración
        self.config = {"game": {"debug": False}}

    @property
    def position(self) -> Tuple[float, float]:
        """Obtiene la posición actual de la entidad."""
        return (self.x, self.y)

    @property
    def center(self) -> Tuple[float, float]:
        """Obtiene el centro de la entidad."""
        return (self.x + self.width // 2, self.y + self.height // 2)

    @property
    def rect(self) -> pygame.Rect:
        """Obtiene el rectángulo de colisión actualizado."""
        self.collision_rect.x = int(self.x)
        self.collision_rect.y = int(self.y)
        return self.collision_rect

    @property
    def is_alive(self) -> bool:
        """Verifica si la entidad está viva."""
        return self.stats.health > 0 and self.state != EntityState.DEAD

    @property
    def is_invulnerable(self) -> bool:
        """Verifica si la entidad es invulnerable."""
        return self.effects_system.is_invulnerable

    def update(self, delta_time: float):
        """
        Actualiza la entidad.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        self._update_position(delta_time)
        self.rendering_system.update_animation(delta_time)
        self.effects_system.update_effects(delta_time)

        # Método abstracto para lógica específica
        self._update_logic(delta_time)

    def _update_position(self, delta_time: float):
        """Actualiza la posición de la entidad."""
        # Aplicar velocidad
        self.x += self.velocity.x * delta_time
        self.y += self.velocity.y * delta_time

        # Mantener dentro de los límites de la pantalla
        self._clamp_position()

    def _clamp_position(self):
        """Mantiene la entidad dentro de los límites de la pantalla."""
        # Esto se puede sobrescribir en clases hijas para límites específicos
        pass

    @abstractmethod
    def _update_logic(self, delta_time: float):
        """
        Actualiza la lógica específica de la entidad.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        pass

    def move(self, direction: pygame.math.Vector2, speed: Optional[float] = None):
        """
        Mueve la entidad en una dirección específica.

        Args:
            direction: Vector de dirección normalizado
            speed: Velocidad de movimiento (opcional)
        """
        if speed is None:
            speed = self.stats.speed

        self.direction = (
            direction.normalize()
            if direction.length() > 0
            else pygame.math.Vector2(0, 0)
        )
        self.velocity = self.direction * speed

        if self.velocity.length() > 0:
            self.state = EntityState.MOVING
        else:
            self.state = EntityState.IDLE

    def take_damage(self, damage: float, source: Optional["Entity"] = None) -> bool:
        """
        La entidad recibe daño (delegado al sistema de efectos).

        Args:
            damage: Cantidad de daño a recibir
            source: Entidad que causa el daño

        Returns:
            True si el daño fue aplicado, False si la entidad es invulnerable
        """
        return self.effects_system.take_damage(damage, source)

    def heal(self, amount: float):
        """
        Cura la entidad.

        Args:
            amount: Cantidad de vida a recuperar
        """
        old_health = self.stats.health
        self.stats.health = min(self.stats.max_health, self.stats.health + amount)

        healed_amount = self.stats.health - old_health
        if healed_amount > 0:
            self.logger.debug(
                "Entidad curada %s puntos. Vida actual: %s",
                healed_amount,
                self.stats.health,
            )

    def die(self):
        """Mata la entidad."""
        self.stats.health = 0
        self.state = EntityState.DEAD
        self.velocity = pygame.math.Vector2(0, 0)

        self.logger.info("Entidad %s ha muerto", self.entity_type.value)
        self._on_death()

    def _on_death(self):
        """Método llamado cuando la entidad muere. Se puede sobrescribir."""
        pass

    def add_effect(self, effect_name: str, effect_data: Dict[str, Any]):
        """Añade un efecto a la entidad (delegado al sistema de efectos)."""
        self.effects_system.add_effect(effect_name, effect_data)

    def collides_with(self, other: "Entity") -> bool:
        """
        Verifica si esta entidad colisiona con otra.

        Args:
            other: Otra entidad

        Returns:
            True si hay colisión
        """
        if not self.collision_enabled or not other.collision_enabled:
            return False

        return self.rect.colliderect(other.rect)

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """Renderiza la entidad (delegado al sistema de renderizado)."""
        self.rendering_system.render(screen, camera_offset)

    def get_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos de la entidad para guardado.

        Returns:
            Diccionario con los datos de la entidad
        """
        data = {
            "entity_type": self.entity_type.value,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "stats": {
                "health": self.stats.health,
                "max_health": self.stats.max_health,
                "speed": self.stats.speed,
                "damage": self.stats.damage,
                "armor": self.stats.armor,
                "attack_speed": self.stats.attack_speed,
                "attack_range": self.stats.attack_range,
            },
            "state": self.state.value,
        }

        # Añadir datos de sistemas modulares
        data.update(self.effects_system.get_effects_data())
        data.update(self.rendering_system.get_rendering_data())

        return data

    def load_data(self, data: Dict[str, Any]):
        """
        Carga datos en la entidad.

        Args:
            data: Datos a cargar
        """
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.width = data.get("width", self.width)
        self.height = data.get("height", self.height)

        # Cargar estadísticas
        stats_data = data.get("stats", {})
        self.stats.health = stats_data.get("health", self.stats.health)
        self.stats.max_health = stats_data.get("max_health", self.stats.max_health)
        self.stats.speed = stats_data.get("speed", self.stats.speed)
        self.stats.damage = stats_data.get("damage", self.stats.damage)
        self.stats.armor = stats_data.get("armor", self.stats.armor)
        self.stats.attack_speed = stats_data.get(
            "attack_speed", self.stats.attack_speed
        )
        self.stats.attack_range = stats_data.get(
            "attack_range", self.stats.attack_range
        )

        # Cargar estado
        state_value = data.get("state", self.state.value)
        self.state = EntityState(state_value)

        # Cargar datos de sistemas modulares
        self.effects_system.load_effects_data(data)
        self.rendering_system.load_rendering_data(data)
