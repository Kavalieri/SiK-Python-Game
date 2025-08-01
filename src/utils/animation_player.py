"""
Animation Player - Reproductor de Animaciones (Optimizado)
==========================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Reproductor de animaciones para personajes individuales - versión compactada.
"""

import logging

import pygame


class AnimationPlayer:
    """Reproductor de animaciones para un personaje específico."""

    def __init__(
        self,
        character_name: str,
        animations: dict[str, dict],
        initial_animation: str = "Idle",
    ):
        """Inicializa el reproductor de animaciones."""
        self.logger = logging.getLogger(__name__)
        self.character_name = character_name
        self.animations = animations
        self.current_animation = initial_animation
        self.animation_start_time = pygame.time.get_ticks()

        # Validar que la animación inicial existe
        if initial_animation not in self.animations:
            available = list(self.animations.keys())
            if available:
                self.current_animation = available[0]
                self.logger.warning(
                    "Animación inicial '%s' no encontrada para %s. Usando '%s'",
                    initial_animation,
                    character_name,
                    self.current_animation,
                )
            else:
                self.logger.error(
                    "No hay animaciones disponibles para %s", character_name
                )

    def set_animation(self, animation_type: str):
        """Cambia la animación actual."""
        if (
            animation_type != self.current_animation
            and animation_type in self.animations
        ):
            self.current_animation = animation_type
            self.animation_start_time = pygame.time.get_ticks()
            self.logger.debug(
                "Cambiando animación de %s a: %s", self.character_name, animation_type
            )

    def get_current_frame(self) -> pygame.Surface | None:
        """Obtiene el frame actual de la animación."""
        if self.current_animation not in self.animations:
            return None
        frame_index = self._calculate_current_frame_index()
        return self.animations[self.current_animation]["frames"][frame_index]

    def _calculate_current_frame_index(self) -> int:
        """Calcula el índice del frame actual."""
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        animation_data = self.animations[self.current_animation]
        frame_duration = animation_data["frame_duration"]
        frame_count = animation_data["frame_count"]
        return int((elapsed_time // frame_duration) % frame_count)

    @property
    def current_frame_index(self) -> int:
        """Obtiene el índice del frame actual."""
        return (
            0
            if self.current_animation not in self.animations
            else self._calculate_current_frame_index()
        )

    def is_animation_completed(self) -> bool:
        """Verifica si la animación actual se completó."""
        if self.current_animation not in self.animations:
            return True
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        animation_data = self.animations[self.current_animation]
        total_duration = (
            animation_data["frame_duration"] * animation_data["frame_count"]
        )
        return elapsed_time >= total_duration

    def restart_animation(self):
        """Reinicia la animación actual."""
        self.animation_start_time = pygame.time.get_ticks()

    def get_animation_progress(self) -> float:
        """Obtiene el progreso de la animación (0.0-1.0)."""
        if self.current_animation not in self.animations:
            return 1.0
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        animation_data = self.animations[self.current_animation]
        total_duration = (
            animation_data["frame_duration"] * animation_data["frame_count"]
        )
        progress = (elapsed_time % total_duration) / total_duration
        return min(1.0, max(0.0, progress))

    def get_animation_info(self) -> dict:
        """Obtiene información de la animación actual."""
        if self.current_animation not in self.animations:
            return {"error": "No hay animación activa"}
        animation_data = self.animations[self.current_animation]
        return {
            "character": self.character_name,
            "animation": self.current_animation,
            "current_frame": self.current_frame_index,
            "total_frames": animation_data["frame_count"],
            "fps": animation_data["fps"],
            "progress": self.get_animation_progress(),
            "completed": self.is_animation_completed(),
        }

    def has_animation(self, animation_type: str) -> bool:
        """Verifica si existe una animación específica."""
        return animation_type in self.animations

    def get_available_animations(self) -> list:
        """Obtiene la lista de animaciones disponibles."""
        return list(self.animations.keys())
