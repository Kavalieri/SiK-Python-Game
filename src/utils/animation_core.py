"""
Animation Core - Núcleo del Sistema de Animaciones
=================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Núcleo de configuración y cálculos de FPS para animaciones.
"""

import logging
from typing import Dict


class AnimationCore:
    """
    Núcleo del sistema de animaciones con configuración y cálculos base.

    Gestiona:
    - Configuración de velocidades por tipo de animación
    - Cálculo de FPS óptimo según número de frames
    - Configuración base de sistema
    """

    def __init__(self):
        """Inicializa el núcleo de animaciones."""
        self.logger = logging.getLogger(__name__)

        # Configuración de FPS base y ajustes por tipo de animación
        self.base_fps = 20
        self.animation_speeds = {
            "idle": 0.8,  # Más lento para idle
            "walk": 1.0,  # Normal para caminar
            "run": 1.2,  # Más rápido para correr
            "attack": 1.5,  # Rápido para ataques
            "shoot": 1.3,  # Rápido para disparos
            "dead": 0.6,  # Lento para muerte
            "jump": 1.1,  # Normal para saltos
            "melee": 1.4,  # Rápido para melee
            "slide": 1.0,  # Normal para deslizar
        }

        self.logger.info(
            "AnimationCore inicializado con %d tipos de animación",
            len(self.animation_speeds),
        )

    def get_optimal_fps(self, animation_type: str, frame_count: int) -> int:
        """
        Calcula el FPS óptimo para una animación basado en el número de fotogramas.

        Args:
            animation_type: Tipo de animación (idle, run, attack, etc.)
            frame_count: Número de fotogramas disponibles

        Returns:
            FPS óptimo para la animación
        """
        # FPS base ajustado por tipo de animación
        base_speed = self.animation_speeds.get(animation_type.lower(), 1.0)
        adjusted_fps = int(self.base_fps * base_speed)

        # Si tenemos muy pocos fotogramas, reducir FPS para que se vea bien
        if frame_count <= 3:
            return max(8, adjusted_fps // 2)  # Mínimo 8 FPS
        elif frame_count <= 5:
            return max(10, int(adjusted_fps // 1.5))
        elif frame_count <= 8:
            return max(12, int(adjusted_fps // 1.2))
        else:
            return adjusted_fps

    def calculate_optimal_fps(self, frame_count: int, anim_type: str) -> int:
        """
        Calcula el FPS óptimo basado en el número de frames y tipo de animación.

        Args:
            frame_count: Número de frames disponibles
            anim_type: Tipo de animación

        Returns:
            FPS óptimo calculado
        """
        # FPS base por tipo de animación
        base_fps = self.animation_speeds.get(anim_type, 1.0) * self.base_fps

        # Ajustar según el número de frames
        if frame_count <= 4:
            # Pocos frames: FPS más bajo para que se vea fluido
            return max(8, int(base_fps * 0.6))
        elif frame_count <= 8:
            # Frames moderados: FPS medio
            return max(12, int(base_fps * 0.8))
        elif frame_count <= 12:
            # Buen número de frames: FPS estándar
            return int(base_fps)
        else:
            # Muchos frames: FPS alto
            return min(30, int(base_fps * 1.2))

    def get_animation_speed(self, animation_type: str) -> float:
        """
        Obtiene la velocidad configurada para un tipo de animación.

        Args:
            animation_type: Tipo de animación

        Returns:
            Factor de velocidad (multiplicador)
        """
        return self.animation_speeds.get(animation_type.lower(), 1.0)

    def set_animation_speed(self, animation_type: str, speed: float):
        """
        Establece la velocidad para un tipo de animación.

        Args:
            animation_type: Tipo de animación
            speed: Factor de velocidad
        """
        self.animation_speeds[animation_type.lower()] = speed
        self.logger.debug("Velocidad de %s establecida a %.2f", animation_type, speed)

    def get_frame_duration(self, fps: int) -> float:
        """
        Calcula la duración por frame en milisegundos.

        Args:
            fps: Frames por segundo

        Returns:
            Duración en milisegundos
        """
        return 1000.0 / fps if fps > 0 else 1000.0

    def get_animation_config_summary(self) -> Dict[str, float]:
        """
        Obtiene un resumen de la configuración de animaciones.

        Returns:
            Diccionario con configuración actual
        """
        return {
            "base_fps": self.base_fps,
            "animation_types": len(self.animation_speeds),
            **self.animation_speeds,
        }
