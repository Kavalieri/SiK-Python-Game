"""
Asset Manager - Fachada Unificada de Gestión de Assets
======================================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Gestor centralizado que integra todas las funcionalidades de assets.
              Mantiene compatibilidad completa con la API original.
"""

import logging
from typing import Any, Dict, List, Optional

import pygame

from .asset_loader import AssetLoader
from .character_assets import CharacterAssets
from .ui_assets import UIAssets


class AssetManager:
    """Gestor centralizado de assets del juego (Refactorizado)."""

    def __init__(self, base_path: str = "assets"):
        """
        Inicializa el AssetManager refactorizado.

        Args:
            base_path: Ruta base de los assets
        """
        self.logger = logging.getLogger(__name__)

        # Inicializar módulos especializados
        self.asset_loader = AssetLoader(base_path)
        self.character_assets = CharacterAssets(self.asset_loader)
        self.ui_assets = UIAssets(self.asset_loader)

        self.logger.info("AssetManager refactorizado inicializado")

    # ========================================
    # API PÚBLICA - COMPATIBILIDAD COMPLETA
    # ========================================

    def load_image(self, path: str, scale: float = 1.0) -> Optional[pygame.Surface]:
        """Delegado a AssetLoader.load_image()"""
        return self.asset_loader.load_image(path, scale)

    def load_image_direct(self, path: str) -> Optional[pygame.Surface]:
        """Delegado a AssetLoader.load_image_direct()"""
        return self.asset_loader.load_image_direct(path)

    def get_character_sprite(
        self, character_name: str, animation: str, frame: int = 1, scale: float = 1.0
    ) -> Optional[pygame.Surface]:
        """Delegado a CharacterAssets.get_character_sprite()"""
        return self.character_assets.get_character_sprite(
            character_name, animation, frame, scale
        )

    def get_character_animation_frames(
        self, character_name: str, animation: str, max_frames: Optional[int] = None
    ) -> List[pygame.Surface]:
        """Delegado a CharacterAssets.get_character_animation_frames()"""
        return self.character_assets.get_character_animation_frames(
            character_name, animation, max_frames
        )

    def get_character_animation_info(self, character_name: str) -> Dict[str, Any]:
        """Delegado a CharacterAssets.get_character_animation_info()"""
        return self.character_assets.get_character_animation_info(character_name)

    def get_ui_button(
        self, button_name: str, state: str = "normal"
    ) -> Optional[pygame.Surface]:
        """Delegado a UIAssets.get_ui_button()"""
        return self.ui_assets.get_ui_button(button_name, state)

    def load_animation_frames(
        self, ruta: str, max_frames: Optional[int] = None
    ) -> List[pygame.Surface]:
        """Delegado a UIAssets.load_animation_frames()"""
        return self.ui_assets.load_animation_frames(ruta, max_frames)

    def clear_cache(self):
        """Delegado a AssetLoader.clear_cache()"""
        self.asset_loader.clear_cache()

    def get_cache_info(self) -> Dict[str, Any]:
        """Delegado a AssetLoader.get_cache_info()"""
        return self.asset_loader.get_cache_info()

    def create_placeholder(
        self, width: int, height: int, scale: float = 1.0
    ) -> pygame.Surface:
        """Delegado a AssetLoader.create_placeholder()"""
        return self.asset_loader.create_placeholder(width, height, scale)

    # ========================================
    # MÉTODOS LEGACY - MANTENIDOS PARA COMPATIBILIDAD
    # ========================================

    def cargar_imagen(self, path: str) -> Optional[pygame.Surface]:
        """Método legacy - Delegado a load_image()"""
        return self.load_image(path)

    def cargar_animacion(
        self, character_name: str, animation: str
    ) -> Optional[List[pygame.Surface]]:
        """Método legacy - Delegado a get_character_animation_frames()"""
        frames = self.get_character_animation_frames(character_name, animation)
        return frames if frames else None

    def cargar_botones_ui(
        self, button_name: str, suffix: str = ""
    ) -> Optional[pygame.Surface]:
        """Método legacy - Delegado a UIAssets.cargar_botones_ui()"""
        return self.ui_assets.cargar_botones_ui(button_name, suffix)

    def cargar_frames(
        self, character_name: str, animation: str
    ) -> List[pygame.Surface]:
        """Método legacy - Delegado a get_character_animation_frames()"""
        return self.get_character_animation_frames(character_name, animation)

    # ========================================
    # PROPIEDADES DE COMPATIBILIDAD
    # ========================================

    @property
    def cache(self):
        """Acceso al caché del AssetLoader para compatibilidad"""
        return self.asset_loader.cache

    @property
    def base_path(self):
        """Acceso al base_path del AssetLoader para compatibilidad"""
        return self.asset_loader.base_path

    @property
    def animation_config(self):
        """Acceso a la configuración de animaciones para compatibilidad"""
        return self.character_assets.animation_config
