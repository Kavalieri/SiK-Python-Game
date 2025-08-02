"""
Player Core - Núcleo del sistema de jugador
===========================================

Autor: SiK Team
Fecha: 30 de Julio, 2025
Descripción: Núcleo del sistema de jugador con configuración y estado base.
"""

import logging
from enum import Enum
from typing import Any

import pygame

from ..entities.character_data import CharacterDataManager
from ..utils.animation_manager import IntelligentAnimationManager
from ..utils.config_manager import ConfigManager
from .entity import EntityState
from .player_stats import PlayerStats


class AnimationState(Enum):
    """Estados de animación del jugador."""

    IDLE = "Idle"
    RUN = "Run"
    WALK = "Walk"
    ATTACK = "Attack"
    DEAD = "Dead"
    SHOOT = "Shoot"


class PlayerCore:
    """
    Núcleo del sistema de jugador con configuración y estado base.
    Maneja la inicialización, configuración y estado fundamental.
    """

    def __init__(
        self,
        x: float,
        y: float,
        character_name: str,
        config: ConfigManager,
        animation_manager: IntelligentAnimationManager,
    ):
        """
        Inicializa el núcleo del jugador.

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            character_name: Nombre del personaje seleccionado
            config: Configuración del juego
            animation_manager: Gestor de animaciones
        """
        self.x = x
        self.y = y
        self.character_name = character_name
        self.config = config
        self.animation_manager = animation_manager
        self.logger = logging.getLogger(__name__)

        # Configuración del mundo (más grande que la pantalla)
        self.world_width = 5000  # Mundo 5 veces más ancho que la pantalla
        self.world_height = 5000  # Mundo 5 veces más alto que la pantalla

        # Estado del jugador
        self.current_animation_state = AnimationState.IDLE
        self.facing_right = True
        self.state = EntityState.IDLE

        # Inicializar estadísticas
        self.stats = self._get_character_stats(character_name)

        # Cargar animaciones del personaje
        self.animations = self.animation_manager.load_character_animations(
            character_name
        )

        # Configurar sprite inicial
        self.sprite = None
        self._create_fallback_sprite()

        self.logger.info("PlayerCore %s inicializado en (%s, %s)", character_name, x, y)

    def _get_character_stats(self, character_name: str) -> PlayerStats:
        """Obtiene las estadísticas base del personaje."""
        char_manager = CharacterDataManager()
        char_data = char_manager.get_character_data(character_name)

        if char_data is not None and isinstance(char_data, dict):
            # Datos de ConfigDatabase tienen estructura diferente
            stats = char_data.get("stats", {})
            if isinstance(stats, str):
                import json

                stats = json.loads(stats)

            return PlayerStats(
                health=stats.get("vida", 100),
                max_health=stats.get("vida", 100),
                speed=stats.get("velocidad", 200),
                damage=stats.get("daño", 25),
                shoot_speed=stats.get("velocidad_disparo", 0.2),
                bullet_speed=stats.get("bullet_speed", 500),
                bullet_damage=stats.get("bullet_damage", 25),
                shield=stats.get("escudo", 0),
                max_shield=stats.get("max_shield", 100),
            )
        else:
            self.logger.warning(
                "Personaje '%s' no encontrado en base de datos, usando estadísticas por defecto",
                character_name,
            )

        # Estadísticas por defecto si el personaje no existe o los datos son None
        return PlayerStats()

    def _create_fallback_sprite(self):
        """Crea un sprite de fallback si no se pueden cargar las animaciones."""
        try:
            # Crear sprite de fallback
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((0, 255, 0))  # Verde para el jugador

            # Añadir un borde
            pygame.draw.rect(self.sprite, (0, 200, 0), (0, 0, 32, 32), 2)

            # Añadir un punto central para indicar dirección
            pygame.draw.circle(self.sprite, (255, 255, 255), (16, 16), 4)

        except (OSError, RuntimeError) as e:
            self.logger.error("Error creando sprite de fallback: %s", e)
            # Crear sprite mínimo
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((255, 0, 0))  # Rojo como último recurso

    def get_animation_state(self) -> AnimationState:
        """Determina el estado de animación actual."""
        if self.state == EntityState.DEAD:
            return AnimationState.DEAD
        elif self.state == EntityState.ATTACKING:
            return AnimationState.ATTACK
        else:
            return AnimationState.IDLE

    def update_sprite(self):
        """Actualiza el sprite del jugador."""
        if self.animations and self.current_animation_state.value in self.animations:
            animation_data = self.animations[self.current_animation_state.value]
            if (
                animation_data
                and "frames" in animation_data
                and animation_data["frames"]
            ):
                # Obtener el frame actual de la animación
                frames = animation_data["frames"]
                if frames:
                    # Por ahora, usar el primer frame. En el futuro se puede implementar animación
                    self.sprite = frames[0]
                else:
                    self._create_fallback_sprite()
            else:
                self._create_fallback_sprite()
        else:
            self._create_fallback_sprite()

    def clamp_position(self):
        """Mantiene al jugador dentro de los límites del mundo."""
        self.x = max(0, min(self.x, self.world_width - 32))  # 32 = width
        self.y = max(0, min(self.y, self.world_height - 32))  # 32 = height

    def get_data(self) -> dict[str, Any]:
        """Obtiene datos básicos del núcleo para guardado."""
        return {
            "x": self.x,
            "y": self.y,
            "character_name": self.character_name,
            "facing_right": self.facing_right,
            "current_animation_state": self.current_animation_state.value,
        }

    def load_data(self, data: dict[str, Any]):
        """Carga datos básicos del núcleo desde guardado."""
        self.x = data.get("x", self.x)
        self.y = data.get("y", self.y)
        self.character_name = data.get("character_name", self.character_name)
        self.facing_right = data.get("facing_right", self.facing_right)

        anim_state = data.get("current_animation_state", "Idle")
        try:
            self.current_animation_state = AnimationState(anim_state)
        except ValueError:
            self.current_animation_state = AnimationState.IDLE
