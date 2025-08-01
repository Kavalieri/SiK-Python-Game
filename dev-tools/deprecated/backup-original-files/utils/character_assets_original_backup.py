"""
Character Assets - Gestión de Assets de Personajes
=================================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Gestión especializada de sprites y animaciones de personajes.
"""

import json
import logging
from pathlib import Path
from typing import Any

import pygame

from .asset_loader import AssetLoader


class CharacterAssets:
    """Gestor especializado de assets de personajes."""

    def __init__(self, asset_loader: AssetLoader):
        """
        Inicializa el gestor de assets de personajes.

        Args:
            asset_loader: Instancia del cargador base
        """
        self.asset_loader = asset_loader
        self.logger = logging.getLogger(__name__)
        self.animation_config = self._load_animation_config()
        self.logger.info("CharacterAssets inicializado")

    def _load_animation_config(self) -> dict[str, Any]:
        """Carga configuración de animaciones desde config/animations.json."""
        config_path = Path("config/animations.json")
        if config_path.exists():
            try:
                with open(config_path, encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                self.logger.error(
                    "Error de decodificación JSON en config/animations.json: %s", e
                )
            except OSError as e:
                self.logger.error(
                    "Error de E/S al cargar config/animations.json: %s", e
                )

        # Fallback: estructura vacía
        self.logger.warning(
            "No se pudo cargar config/animations.json, usando configuración vacía."
        )
        return {"characters": {}, "sprite_paths": []}

    def get_character_sprite(
        self, character_name: str, animation: str, frame: int = 1, scale: float = 1.0
    ) -> pygame.Surface | None:
        """
        Obtiene un sprite de personaje específico.

        Args:
            character_name: Nombre del personaje
            animation: Tipo de animación
            frame: Número de frame
            scale: Factor de escala

        Returns:
            Superficie del sprite o None si falla
        """
        # Verificar si el personaje existe en la configuración
        if character_name not in self.animation_config["characters"]:
            self.logger.warning(
                "Personaje no encontrado en configuración: %s", character_name
            )
            return self.asset_loader.create_placeholder(64, 64, scale)

        # Leer escala personalizada si no se ha especificado un scale explícito
        if scale == 1.0:
            char_config = self.animation_config["characters"][character_name]
            scale = char_config.get("escala_sprite", 1.0)

        # Verificar si la animación existe para este personaje
        available_animations = self.animation_config["characters"][character_name][
            "animations"
        ]
        if animation not in available_animations:
            self.logger.warning(
                "Animación '%s' no disponible para %s. Disponibles: %s",
                animation,
                character_name,
                available_animations,
            )
            return self.asset_loader.create_placeholder(64, 64, scale)

        # Usar rutas desde config
        sprite_paths = self.animation_config.get(
            "sprite_paths",
            [
                "characters/used/{character}/{animation}_{frame}_.png",
                "characters/used/{character}/{animation}_{frame}.png",
                "characters/{character}/{animation}_{frame}_.png",
                "characters/{character}/{animation}_{frame}.png",
            ],
        )
        animation_capitalized = animation.capitalize()
        possible_paths = [
            path.format(
                character=character_name, animation=animation_capitalized, frame=frame
            )
            for path in sprite_paths
        ]

        for path in possible_paths:
            sprite = self.asset_loader.load_image(path, scale)
            if sprite and not self.asset_loader.is_placeholder_sprite(sprite):
                return sprite

        self.logger.warning(
            "Sprite no encontrado: %s/%s_%d, creando placeholder",
            character_name,
            animation_capitalized,
            frame,
        )
        return self.asset_loader.create_placeholder(64, 64, scale)

    def get_character_animation_frames(
        self, character_name: str, animation: str, max_frames: int | None = None
    ) -> list[pygame.Surface]:
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
        if character_name not in self.animation_config["characters"]:
            self.logger.warning(
                "Personaje no encontrado en configuración: %s", character_name
            )
            return frames

        # Verificar si la animación existe para este personaje
        available_animations = self.animation_config["characters"][character_name][
            "animations"
        ]
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
            max_frames = self.animation_config["characters"][character_name].get(
                "total_frames", 10
            )

        # Cargar frames hasta encontrar uno que no exista o alcanzar el máximo
        if max_frames is not None:
            while frame <= max_frames:
                sprite = self.get_character_sprite(character_name, animation, frame)

                if sprite and not self.asset_loader.is_placeholder_sprite(sprite):
                    frames.append(sprite)
                    frame += 1
                else:
                    # Si encontramos un placeholder, asumimos que no hay más frames
                    break

        self.logger.info(
            "Cargados %d frames para %s/%s", len(frames), character_name, animation
        )
        return frames

    def get_character_animation_info(self, character_name: str) -> dict[str, Any]:
        """
        Obtiene información completa de las animaciones de un personaje.

        Args:
            character_name: Nombre del personaje

        Returns:
            Diccionario con información de animaciones
        """
        if character_name not in self.animation_config["characters"]:
            return {}

        char_config = self.animation_config["characters"][character_name]
        animation_info = {}

        for animation in char_config["animations"]:
            frames = self.get_character_animation_frames(character_name, animation)
            animation_info[animation] = {
                "frame_count": len(frames),
                "frames": frames,
                "fps": self._calculate_optimal_fps(len(frames), animation),
            }

        return animation_info

    def _calculate_optimal_fps(self, frame_count: int, anim_type: str) -> int:
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
