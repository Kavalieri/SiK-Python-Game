"""
Animation Loader - Cargador de Animaciones de Personajes
========================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Módulo especializado en cargar y procesar animaciones de personajes.
"""

import logging
from typing import Dict, Optional

import pygame

from .animation_core import AnimationCore
from .asset_manager import AssetManager


class AnimationLoader:
    """
    Cargador especializado de animaciones de personajes.

    Responsabilidades:
    - Cargar frames de animación desde AssetManager
    - Filtrar placeholders y frames inválidos
    - Crear configuraciones de animación optimizadas
    """

    def __init__(self, asset_manager: AssetManager, animation_core: AnimationCore):
        """
        Inicializa el cargador de animaciones.

        Args:
            asset_manager: Gestor de assets
            animation_core: Núcleo de animaciones
        """
        self.logger = logging.getLogger(__name__)
        self.asset_manager = asset_manager
        self.animation_core = animation_core

        # Cache de animaciones cargadas
        self.animation_cache = {}

        self.logger.info("AnimationLoader inicializado con caché")

    def load_character_animations(self, character_name: str) -> Dict[str, Dict]:
        """
        Carga todas las animaciones disponibles para un personaje usando configuración centralizada.

        Args:
            character_name: Nombre del personaje

        Returns:
            Diccionario con todas las animaciones del personaje
        """
        # Verificar cache primero
        cache_key = f"{character_name}_animations"
        if cache_key in self.animation_cache:
            self.logger.debug("Usando animaciones en caché para %s", character_name)
            return self.animation_cache[cache_key]

        animations = {}

        # Obtener tipos de animación desde config
        char_config = self.asset_manager.animation_config.get("characters", {}).get(
            character_name, {}
        )
        animation_types = char_config.get("animations", [])

        for anim_type in animation_types:
            animation_data = self._load_single_animation(character_name, anim_type)
            if animation_data:
                animations[anim_type] = animation_data

        # Guardar en caché
        self.animation_cache[cache_key] = animations
        self.logger.info(
            "Cargadas %d animaciones para %s", len(animations), character_name
        )
        return animations

    def _load_single_animation(
        self, character_name: str, anim_type: str
    ) -> Optional[Dict]:
        """
        Carga una animación específica de un personaje.

        Args:
            character_name: Nombre del personaje
            anim_type: Tipo de animación

        Returns:
            Datos de la animación o None si no se pudo cargar
        """
        try:
            frames = self.asset_manager.get_character_animation_frames(
                character_name, anim_type
            )
            real_frames = [frame for frame in frames if not self._is_placeholder(frame)]

            if not real_frames:
                self.logger.debug(
                    "No se encontraron frames reales para %s/%s",
                    character_name,
                    anim_type,
                )
                return None

            optimal_fps = self.animation_core.calculate_optimal_fps(
                len(real_frames), anim_type
            )
            frame_duration = self.animation_core.get_frame_duration(optimal_fps)

            animation_data = {
                "frames": real_frames,
                "frame_count": len(real_frames),
                "fps": optimal_fps,
                "frame_duration": frame_duration,
            }

            self.logger.info(
                "Animación cargada: %s/%s - %d frames a %d FPS",
                character_name,
                anim_type,
                len(real_frames),
                optimal_fps,
            )
            return animation_data

        except (AttributeError, ValueError, TypeError) as e:
            self.logger.error(
                "Error cargando animación %s/%s: %s", character_name, anim_type, e
            )
            return None

    def _is_placeholder(self, surface: pygame.Surface) -> bool:
        """Verifica si una superficie es un placeholder."""
        if not surface or surface.get_width() != 64 or surface.get_height() != 64:
            return False

        # Verificar si es un color sólido (placeholder) - muestreo cada 8 píxeles
        colors = set()
        for x in range(0, 64, 8):
            for y in range(0, 64, 8):
                try:
                    color = surface.get_at((x, y))
                    colors.add((color.r, color.g, color.b, color.a))
                except IndexError:
                    continue

        # Si hay muy pocos colores, probablemente es un placeholder
        return len(colors) <= 3

    def clear_cache(self):
        """Limpia el caché de animaciones."""
        self.animation_cache.clear()
        self.logger.info("Caché de animaciones limpiado")

    def get_cache_info(self) -> Dict[str, int]:
        """
        Obtiene información del caché de animaciones.

        Returns:
            Información del caché
        """
        return {
            "cached_characters": len(self.animation_cache),
            "total_animations": sum(
                len(anims) for anims in self.animation_cache.values()
            ),
        }

    def preload_character_animations(self, character_names: list):
        """
        Precarga animaciones para múltiples personajes.

        Args:
            character_names: Lista de nombres de personajes
        """
        for character_name in character_names:
            self.load_character_animations(character_name)
        self.logger.info(
            "Precargadas animaciones para %d personajes", len(character_names)
        )
