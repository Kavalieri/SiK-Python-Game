"""
Character Assets Animation - Gestión de Animaciones y FPS
========================================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Gestión de frames de animación, información y cálculo de FPS.
"""

import logging
from typing import Any, Dict, List, Optional

import pygame

from .character_assets_loader import CharacterAssetsLoader


class CharacterAssetsAnimation:
    """Gestor de animaciones y frames de personajes."""

    def __init__(self, assets_loader: CharacterAssetsLoader):
        """
        Inicializa el gestor de animaciones.

        Args:
            assets_loader: Instancia del cargador de assets
        """
        self.assets_loader = assets_loader
        self.logger = logging.getLogger(__name__)

        self.logger.info("CharacterAssetsAnimation inicializado")

    def get_character_animation_frames(
        self, character_name: str, animation: str, max_frames: Optional[int] = None
    ) -> List[pygame.Surface]:
        """
        Obtiene todos los frames de una animación específica.

        Args:
            character_name: Nombre del personaje
            animation: Tipo de animación
            max_frames: Número máximo de frames a cargar

        Returns:
            Lista de superficies de pygame
        """
        frames = []
        frame = 1

        # Verificar si el personaje existe en la configuración
        if not self.assets_loader.is_character_available(character_name):
            self.logger.warning(
                "Personaje no encontrado en configuración: %s", character_name
            )
            return frames

        # Verificar si la animación existe para este personaje
        available_animations = self.assets_loader.get_available_animations(
            character_name
        )
        if animation not in available_animations:
            self.logger.warning(
                "Animación '%s' no disponible para %s. Disponibles: %s",
                animation,
                character_name,
                available_animations,
            )
            return frames

        # Obtener el número máximo de frames desde la configuración
        if max_frames is None:
            char_config = self.assets_loader.get_character_config(character_name)
            max_frames = char_config.get("total_frames", 10)

        # Cargar frames hasta encontrar uno que no exista o alcanzar el máximo
        if max_frames is not None:
            while frame <= max_frames:
                sprite = self.assets_loader.get_character_sprite(
                    character_name, animation, frame
                )

                if sprite and not self.assets_loader.asset_loader.is_placeholder_sprite(
                    sprite
                ):
                    frames.append(sprite)
                    frame += 1
                else:
                    # Si encontramos un placeholder, asumimos que no hay más frames
                    break

        self.logger.info(
            "Cargados %d frames para %s/%s", len(frames), character_name, animation
        )
        return frames

    def get_character_animation_info(self, character_name: str) -> Dict[str, Any]:
        """
        Obtiene información completa de las animaciones de un personaje.

        Args:
            character_name: Nombre del personaje

        Returns:
            Diccionario con información de animaciones
        """
        if not self.assets_loader.is_character_available(character_name):
            return {}

        available_animations = self.assets_loader.get_available_animations(
            character_name
        )
        animation_info = {}

        for animation in available_animations:
            frames = self.get_character_animation_frames(character_name, animation)
            animation_info[animation] = {
                "frame_count": len(frames),
                "frames": frames,
                "fps": self.calculate_optimal_fps(len(frames), animation),
            }

        return animation_info

    def calculate_optimal_fps(self, frame_count: int, anim_type: str) -> int:
        """
        Calcula el FPS óptimo para una animación.

        Args:
            frame_count: Número de frames
            anim_type: Tipo de animación

        Returns:
            FPS óptimo
        """
        # FPS base por tipo de animación
        base_fps = {
            "Idle": 12,
            "Walk": 15,
            "Run": 18,
            "Attack": 20,
            "Dead": 10,
            "Shoot": 16,
            "Jump": 14,
            "Melee": 18,
            "Slide": 16,
            "JumpMelee": 16,
            "JumpShoot": 16,
            "RunShoot": 18,
            "JumpAttack": 15,
        }

        fps = base_fps.get(anim_type, 15)

        # Ajustar según el número de frames
        if frame_count <= 4:
            return max(8, fps // 2)
        elif frame_count <= 8:
            return max(10, int(fps * 0.8))
        elif frame_count <= 12:
            return fps
        else:
            return min(30, int(fps * 1.2))

    def preload_character_animations(
        self, character_name: str
    ) -> Dict[str, List[pygame.Surface]]:
        """
        Precarga todas las animaciones de un personaje.

        Args:
            character_name: Nombre del personaje

        Returns:
            Diccionario con animaciones precargadas
        """
        if not self.assets_loader.is_character_available(character_name):
            self.logger.warning(
                "Personaje no disponible para precarga: %s", character_name
            )
            return {}

        preloaded_animations = {}
        available_animations = self.assets_loader.get_available_animations(
            character_name
        )

        for animation in available_animations:
            frames = self.get_character_animation_frames(character_name, animation)
            if frames:
                preloaded_animations[animation] = frames
                self.logger.info(
                    "Precargada animación %s para %s (%d frames)",
                    animation,
                    character_name,
                    len(frames),
                )

        return preloaded_animations
