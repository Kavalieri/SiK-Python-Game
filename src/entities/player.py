"""
Player - Fachada de compatibilidad del jugador
==============================================

Autor: SiK Team
Fecha: 30 de Julio, 2025
Descripción: Fachada que mantiene API original delegando a módulos especializados.
"""

from typing import Any

import pygame

from utils.animation_manager import IntelligentAnimationManager
from utils.config_manager import ConfigManager

from .entity import Entity, EntityType
from .player_core import PlayerCore
from .player_integration import PlayerIntegration
from .player_movement import PlayerMovement


class Player(Entity):
    """
    Fachada del jugador que mantiene API original delegando a módulos especializados.
    Preserva 100% compatibilidad con código existente.
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
        Inicializa el jugador mediante delegación a módulos especializados.

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            character_name: Nombre del personaje seleccionado
            config: Configuración del juego
            animation_manager: Gestor de animaciones
        """
        # Inicializar módulos especializados
        self.core = PlayerCore(x, y, character_name, config, animation_manager)
        self.movement = PlayerMovement(self.core)
        self.integration = PlayerIntegration(self.core, config)

        # Inicializar entidad base usando stats del core con tamaño aumentado
        super().__init__(
            entity_type=EntityType.PLAYER,
            x=x,
            y=y,
            width=100,
            height=100,
            stats=self.core.stats,
        )

    # === PROPIEDADES DE COMPATIBILIDAD ===
    @property
    def character_name(self):
        """Nombre del personaje."""
        return self.core.character_name

    @property
    def config(self):
        """Configuración del juego."""
        return self.core.config

    @config.setter
    def config(self, value):
        """Establece la configuración del juego."""
        self.core.config = value

    @property
    def animation_manager(self):
        """Gestor de animaciones."""
        return self.core.animation_manager

    def get_current_frame(self):
        """
        Obtiene el frame actual del sprite del jugador.

        Returns:
            pygame.Surface: Surface del sprite actual del jugador
        """
        # Actualizar sprite antes de devolverlo
        self.core.update_sprite()
        sprite = self.core.sprite

        # **CRÍTICO: Asegurar tamaño correcto del sprite**
        if sprite and sprite.get_size() != (self.width, self.height):
            sprite = pygame.transform.scale(sprite, (self.width, self.height))

        return sprite

    @property
    def current_animation_state(self):
        """Estado actual de animación."""
        return self.core.current_animation_state

    @current_animation_state.setter
    def current_animation_state(self, value):
        """Establece el estado de animación."""
        self.core.current_animation_state = value

    @property
    def facing_right(self):
        """Si el jugador mira a la derecha."""
        return self.core.facing_right

    @facing_right.setter
    def facing_right(self, value):
        """Establece la dirección del jugador."""
        self.core.facing_right = value

    @property
    def animations(self):
        """Animaciones del jugador."""
        return self.core.animations

    @property
    def sprite(self):
        """Sprite actual del jugador."""
        return self.core.sprite

    @sprite.setter
    def sprite(self, value):
        """Establece el sprite del jugador."""
        self.core.sprite = value

    @property
    def stats(self):
        """Estadísticas del jugador."""
        return self.core.stats

    @stats.setter
    def stats(self, value):
        """Establece las estadísticas del jugador."""
        self.core.stats = value

    @property
    def effects(self):
        """Efectos activos del jugador."""
        return self.integration.effects

    @property
    def combat(self):
        """Sistema de combate del jugador."""
        return self.integration.combat

    @property
    def attack_configs(self):
        """Configuraciones de ataque."""
        return self.integration.attack_configs

    @property
    def velocity(self):
        """Vector de velocidad (compatibilidad con Entity)."""
        vel_x, vel_y = self.movement.get_velocity()

        # Crear objeto con atributos x e y para compatibilidad
        class VelocityVector:
            """Vector de velocidad con atributos x e y para compatibilidad."""

            def __init__(self, x, y):
                self.x, self.y = x, y

        return VelocityVector(vel_x, vel_y)

    @velocity.setter
    def velocity(self, value):
        """Establece el vector de velocidad (compatibilidad con Entity)."""
        if hasattr(value, "x") and hasattr(value, "y"):
            self.movement.set_velocity(value.x, value.y)
        elif isinstance(value, (tuple, list)) and len(value) >= 2:
            self.movement.set_velocity(value[0], value[1])
        else:
            raise ValueError(
                "velocity debe tener atributos x, y o ser una tupla/lista de 2 elementos"
            )

    def handle_input(
        self,
        keys: pygame.key.ScancodeWrapper,
        mouse_pos: tuple[int, int],
        mouse_buttons: tuple[bool, bool, bool],
    ):
        """Maneja la entrada del usuario."""
        return self.movement.handle_input(keys, mouse_pos, mouse_buttons, self.effects)

    def attack(self, target_pos: tuple[int, int], enemies: list[Any]):
        """Ejecuta el ataque actual."""
        return self.integration.attack(target_pos, enemies)

    def take_damage(self, damage: float, source=None) -> bool:
        """Aplica daño al jugador."""
        return self.integration.take_damage(damage, source)

    def heal(self, amount: float):
        """Cura al jugador."""
        self.integration.heal(amount)

    def apply_powerup(self, powerup_effect):
        """Aplica un powerup al jugador."""
        self.integration.apply_powerup(powerup_effect)

    def get_data(self) -> dict[str, Any]:
        """Obtiene datos del jugador para guardado."""
        data = self.core.get_data()
        data.update(self.movement.get_data())
        data.update(self.integration.get_integration_data())
        return data

    def load_data(self, data: dict[str, Any]):
        """Carga datos del jugador desde guardado."""
        self.core.load_data(data)
        self.movement.load_data(data)
        self.integration.load_integration_data(data)

    def update(self, delta_time: float):
        """Actualiza el jugador."""
        self.x, self.y, self.state = self.core.x, self.core.y, self.core.state
        # Actualizar sistemas
        self.movement.update_movement(delta_time)
        self.integration.update_effects(delta_time)
        self.movement.update_animation(delta_time)
        # Sincronizar posición después del movimiento
        self.core.x, self.core.y = self.x, self.y
        # Actualizar lógica base
        super().update(delta_time)

    def clamp_position(self):
        """Mantiene al jugador dentro de los límites del mundo."""
        self.core.clamp_position()

    def _update_logic(self, delta_time: float):
        """
        Implementación requerida del método abstracto de Entity.
        La lógica específica se delega a los módulos especializados.
        """
        # La lógica ya se maneja en el método update() a través de los módulos
        # Actualización adicional de entidad base si es necesaria
        self.movement.update_movement(delta_time)
