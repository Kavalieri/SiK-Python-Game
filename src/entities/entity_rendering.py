"""
Entity Rendering - Sistema de Renderizado y Animaciones
======================================================

Autor: SiK Team
Fecha: 2024
Descripción: Gestión de renderizado, animaciones y sprites para entidades.
"""

from typing import Any, Dict, Optional, Tuple

import pygame


class EntityRenderingSystem:
    """Sistema de renderizado y animaciones para entidades."""

    def __init__(self, entity_instance):
        """
        Inicializa el sistema de renderizado.

        Args:
            entity_instance: Instancia de la entidad propietaria
        """
        self.entity = entity_instance
        self.sprite = None
        self.animation_frames = {}
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0.0

    def update_animation(self, delta_time: float):
        """Actualiza la animación de la entidad."""
        if not self.animation_frames:
            return

        self.animation_timer += delta_time * self.animation_speed

        if self.animation_timer >= 1.0:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(
                self.animation_frames.get(self.entity.state.value, [])
            )

    def get_current_sprite(self) -> Optional[pygame.Surface]:
        """Obtiene el sprite actual para renderizar."""
        if not self.animation_frames:
            return self.sprite

        frames = self.animation_frames.get(self.entity.state.value, [])
        if frames and self.current_frame < len(frames):
            return frames[self.current_frame]

        return self.sprite

    def render(
        self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)
    ):
        """
        Renderiza la entidad en pantalla.

        Args:
            screen: Superficie donde renderizar
            camera_offset: Offset de la cámara (x, y) para coordenadas de pantalla
        """
        if not self.entity.is_alive:
            return

        # Obtener el sprite actual
        current_sprite = self.get_current_sprite()
        if not current_sprite:
            return

        # Usar coordenadas de pantalla si se proporcionan, sino usar posición del mundo
        if camera_offset != (0, 0):
            render_x = camera_offset[0]
            render_y = camera_offset[1]
        else:
            render_x = self.entity.x
            render_y = self.entity.y

        # Centrar el sprite en las coordenadas proporcionadas
        sprite_width = current_sprite.get_width()
        sprite_height = current_sprite.get_height()
        centered_x = render_x - sprite_width // 2
        centered_y = render_y - sprite_height // 2

        # Renderizar sprite centrado
        screen.blit(current_sprite, (centered_x, centered_y))

        # Renderizar efectos visuales
        if hasattr(self.entity, "effects_system"):
            self.entity.effects_system.render_visual_effects(
                screen, centered_x, centered_y, sprite_width, sprite_height
            )

        # Debug: mostrar rectángulo de colisión
        self._render_debug_info(
            screen, centered_x, centered_y, sprite_width, sprite_height
        )

    def _render_debug_info(
        self, screen: pygame.Surface, x: float, y: float, width: int, height: int
    ):
        """Renderiza información de debug si está habilitada."""
        if hasattr(self.entity, "config") and hasattr(self.entity.config, "get"):
            try:
                debug_enabled = self.entity.config.get("game", "debug", False)
                if debug_enabled:
                    debug_rect = pygame.Rect(x, y, width, height)
                    pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)
            except (AttributeError, KeyError, TypeError):
                pass  # Ignorar errores de debug

    def set_sprite(self, sprite: pygame.Surface):
        """Establece el sprite principal."""
        self.sprite = sprite

    def set_animation_frames(self, animation_frames: Dict[str, list]):
        """Establece los frames de animación."""
        self.animation_frames = animation_frames

    def set_animation_speed(self, speed: float):
        """Establece la velocidad de animación."""
        self.animation_speed = speed

    def get_rendering_data(self) -> Dict[str, Any]:
        """Obtiene datos de renderizado para guardado."""
        return {
            "current_frame": self.current_frame,
            "animation_timer": self.animation_timer,
            "animation_speed": self.animation_speed,
        }

    def load_rendering_data(self, data: Dict[str, Any]):
        """Carga datos de renderizado."""
        self.current_frame = data.get("current_frame", 0)
        self.animation_timer = data.get("animation_timer", 0.0)
        self.animation_speed = data.get("animation_speed", 0.1)
