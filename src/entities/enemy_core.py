"""
Enemy Core - Núcleo del Sistema de Enemigos
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Núcleo base para enemigos con configuración y estado.
"""

import pygame

from utils.config_manager import ConfigManager


class EnemyCore:
    """Núcleo base para enemigos con configuración y estado básico."""

    def __init__(self, x: float, y: float, enemy_type: str, animation_manager):
        """
        Inicializa el núcleo del enemigo.

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            enemy_type: Tipo de enemigo ('zombiemale' o 'zombieguirl')
            animation_manager: Gestor de animaciones
        """
        # Posición y tipo
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.animation_manager = animation_manager

        # Cargar configuración desde archivos
        self.config_manager = ConfigManager()
        self._load_enemy_config()

        # Estado del enemigo
        self.facing_right = True
        self.is_attacking = False
        self.is_dead = False
        self.target = None

        # Sistema de animación
        self.animation_player = animation_manager.create_animation_player(
            enemy_type, "Idle"
        )
        self.current_animation = "Idle"

        # Tracking de movimiento para dirección
        self._last_x = self.x

    def _load_enemy_config(self):
        """Carga configuración del enemigo desde archivos JSON."""
        # Cargar configuración base del tipo de enemigo
        enemy_config = self.config_manager.get_config("enemies")
        dev_config = enemy_config.get("configuracion_desarrollo", {})

        enemy_data = enemy_config.get("tipos_enemigos", {}).get(self.enemy_type, {})
        stats = enemy_data.get("stats", {})

        # Propiedades físicas configurables
        base_scale = stats.get("escala", 1.0)
        dev_scale = dev_config.get("escala_visual", 1.0)
        self.scale = base_scale * dev_scale

        self.width = int(32 * self.scale)
        self.height = int(32 * self.scale)

        # Stats configurables
        self.speed = stats.get("velocidad", 80.0)
        if dev_config.get("velocidad_debug", False):
            self.speed *= dev_config.get("velocidad_debug", 1.0)

        self.health = stats.get("vida", 100)
        self.max_health = self.health
        self.damage = stats.get("daño", 20)
        self.attack_range = stats.get("rango_ataque", 60)
        self.detection_range = stats.get("rango_detección", 200)

        # Configuración de comportamiento
        self.behavior_type = enemy_data.get("comportamiento", "perseguir")
        self.persistent_tracking = dev_config.get("rango_seguimiento_extendido", False)

        # Configuración de sistema
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def take_damage(self, damage: int):
        """Recibe daño y actualiza estado."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.current_animation = "Dead"

    def _update_facing_direction(self):
        """Actualiza la dirección a la que mira el enemigo."""
        if hasattr(self, "_last_x"):
            if self.x > self._last_x:
                self.facing_right = True
            elif self.x < self._last_x:
                self.facing_right = False
        self._last_x = self.x

    def update_facing_direction(self):
        """Método público para actualizar dirección."""
        self._update_facing_direction()

    def _update_dead_animation(self):
        """Actualiza la animación de muerte."""
        if self.current_animation != "Dead":
            self.current_animation = "Dead"
            self.animation_player.set_animation("Dead")

    def update_dead_animation(self):
        """Método público para actualizar animación de muerte."""
        self._update_dead_animation()

    def get_current_frame(self) -> pygame.Surface | None:
        """Obtiene el frame actual de la animación con escala y volteo."""
        frame = self.animation_player.get_current_frame()
        if frame:
            frame = pygame.transform.scale(frame, (self.width, self.height))
            if not self.facing_right:
                frame = pygame.transform.flip(frame, True, False)
        return frame

    def get_rect(self) -> pygame.Rect:
        """Obtiene el rectángulo de colisión."""
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )

    def is_attack_ready(self) -> bool:
        """Verifica si puede atacar según cooldown."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time >= self.attack_cooldown

    def reset_attack_state(self):
        """Resetea el estado de ataque."""
        self.is_attacking = False
        if self.current_animation == "Attack":
            self.current_animation = "Idle"

    def update_animation(self):
        """Actualiza el sistema de animación."""
        self.animation_player.set_animation(self.current_animation)
