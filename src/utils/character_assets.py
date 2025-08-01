"""
Character Assets - Fachada Unificada de Gestión de Assets de Personajes
=======================================================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Fachada que integra carga de configuración y gestión de animaciones.
             Mantiene compatibilidad completa con la API original.
"""

import logging
from typing import Any

import pygame

from .asset_loader import AssetLoader
from .character_assets_animation import CharacterAssetsAnimation
from .character_assets_loader import CharacterAssetsLoader


class CharacterAssets:
    """Gestor unificado de assets de personajes (Refactorizado)."""

    def __init__(self, asset_loader: AssetLoader):
        """
        Inicializa el gestor de assets de personajes refactorizado.

        Args:
            asset_loader: Instancia del cargador base de assets
        """
        self.asset_loader = asset_loader
        self.logger = logging.getLogger(__name__)

        # Inicializar módulos especializados
        self.assets_loader = CharacterAssetsLoader(asset_loader)
        self.assets_animation = CharacterAssetsAnimation(self.assets_loader)

        self.logger.info("CharacterAssets refactorizado inicializado")

    # ========================================
    # API PÚBLICA - COMPATIBILIDAD COMPLETA
    # ========================================

    def get_character_sprite(
        self, character_name: str, animation: str, frame: int = 1, scale: float = 1.0
    ) -> pygame.Surface | None:
        """Delegado a CharacterAssetsLoader.get_character_sprite()"""
        return self.assets_loader.get_character_sprite(
            character_name, animation, frame, scale
        )

    def get_character_animation_frames(
        self, character_name: str, animation: str, max_frames: int | None = None
    ) -> list[pygame.Surface]:
        """Delegado a CharacterAssetsAnimation.get_character_animation_frames()"""
        return self.assets_animation.get_character_animation_frames(
            character_name, animation, max_frames
        )

    def get_character_animation_info(self, character_name: str) -> dict[str, Any]:
        """Delegado a CharacterAssetsAnimation.get_character_animation_info()"""
        return self.assets_animation.get_character_animation_info(character_name)

    def _calculate_optimal_fps(self, frame_count: int, anim_type: str) -> int:
        """Delegado a CharacterAssetsAnimation.calculate_optimal_fps() para compatibilidad"""
        return self.assets_animation.calculate_optimal_fps(frame_count, anim_type)

    # ========================================
    # PROPIEDADES DE COMPATIBILIDAD
    # ========================================

    @property
    def animation_config(self) -> dict[str, Any]:
        """Propiedad de compatibilidad para acceso directo a configuración"""
        return self.assets_loader.animation_config

    # ========================================
    # MÉTODOS ADICIONALES EXPUESTOS
    # ========================================

    def is_character_available(self, character_name: str) -> bool:
        """Delegado a CharacterAssetsLoader.is_character_available()"""
        return self.assets_loader.is_character_available(character_name)

    def get_available_animations(self, character_name: str) -> list:
        """Delegado a CharacterAssetsLoader.get_available_animations()"""
        return self.assets_loader.get_available_animations(character_name)

    def get_character_config(self, character_name: str) -> dict[str, Any]:
        """Delegado a CharacterAssetsLoader.get_character_config()"""
        return self.assets_loader.get_character_config(character_name)

    def preload_character_animations(
        self, character_name: str
    ) -> dict[str, list[pygame.Surface]]:
        """Delegado a CharacterAssetsAnimation.preload_character_animations()"""
        return self.assets_animation.preload_character_animations(character_name)
