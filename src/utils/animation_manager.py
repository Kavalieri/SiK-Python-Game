"""
Animation Manager - Gestor de Animaciones Refactorizado
======================================================

Autor: SiK Team
Fecha: 2025-07-30
Descripción: Fachada principal que coordina el sistema de animaciones modular.
             Mantiene 100% compatibilidad con la API original.
"""

import logging
from typing import Dict, Optional

import pygame

from .animation_core import AnimationCore
from .animation_loader import AnimationLoader
from .animation_player import AnimationPlayer
from .asset_manager import AssetManager


class IntelligentAnimationManager:
    """
    Gestor de animaciones que coordina todos los módulos especializados.

    Fachada que mantiene compatibilidad total con la API original mientras
    delega responsabilidades a módulos especializados:
    - AnimationCore: Configuración y cálculos
    - AnimationLoader: Carga de animaciones
    - AnimationPlayer: Reproducción individual
    """

    def __init__(self, asset_manager: Optional[AssetManager] = None):
        """Inicializa el gestor de animaciones."""
        self.logger = logging.getLogger(__name__)
        self.asset_manager = asset_manager if asset_manager else AssetManager()

        # Inicializar módulos especializados
        self.animation_core = AnimationCore()
        self.animation_loader = AnimationLoader(self.asset_manager, self.animation_core)

        # Cache de reproductores activos
        self.active_players = {}

        self.logger.info("IntelligentAnimationManager inicializado con sistema modular")

    # ============================================================================
    # MÉTODOS PRINCIPALES DE LA API ORIGINAL
    # ============================================================================

    def get_optimal_fps(self, animation_type: str, frame_count: int) -> int:
        """Calcula el FPS óptimo - delegado a AnimationCore."""
        return self.animation_core.get_optimal_fps(animation_type, frame_count)

    def load_character_animations(self, character_name: str) -> Dict[str, Dict]:
        """Carga animaciones de personaje - delegado a AnimationLoader."""
        return self.animation_loader.load_character_animations(character_name)

    def get_all_character_animations(self, character_name: str) -> Dict[str, Dict]:
        """Obtiene todas las animaciones - alias para compatibilidad."""
        return self.load_character_animations(character_name)

    def create_animation_player(
        self, character_name: str, initial_animation: str = "Idle"
    ):
        """Crea un reproductor de animación."""
        animations = self.load_character_animations(character_name)
        player = AnimationPlayer(character_name, animations, initial_animation)

        # Guardar en caché de reproductores activos
        player_key = f"{character_name}_{initial_animation}"
        self.active_players[player_key] = player

        return player

    def get_current_sprite(
        self, character_name: str, animation_type: str = "Idle"
    ) -> Optional[pygame.Surface]:
        """Obtiene el sprite actual de un personaje."""
        # Buscar reproductor existente o crear uno temporal
        player_key = f"{character_name}_{animation_type}"
        if player_key not in self.active_players:
            player = self.create_animation_player(character_name, animation_type)
        else:
            player = self.active_players[player_key]

        return player.get_current_frame()

    # ============================================================================
    # MÉTODOS DE COMPATIBILIDAD CON LA API ORIGINAL
    # ============================================================================

    def update_character_animation(self, character_name: str, delta_time: float):
        """Método de compatibilidad - la actualización es automática en AnimationPlayer."""
        # Los AnimationPlayer se actualizan automáticamente, este método se mantiene por compatibilidad
        _ = delta_time  # Argumento mantenido por compatibilidad de API
        self.logger.debug("update_character_animation llamado para %s", character_name)

    def set_animation_state(self, character_name: str, animation_state: str):
        """Método de compatibilidad - usar create_animation_player o player.set_animation."""
        # Implementación básica de compatibilidad que busca o crea un player
        player_key = f"{character_name}_{animation_state}"
        if player_key in self.active_players:
            self.active_players[player_key].set_animation(animation_state)
        else:
            self.logger.warning(
                "Player no encontrado para %s_%s", character_name, animation_state
            )

    # ============================================================================
    # MÉTODOS DE GESTIÓN Y UTILIDAD
    # ============================================================================

    def clear_cache(self):
        """Limpia todas las cachés del sistema."""
        self.animation_loader.clear_cache()
        self.active_players.clear()
        self.logger.info("Caché del sistema de animaciones limpiado")

    def get_system_info(self) -> Dict:
        """Obtiene información del sistema de animaciones."""
        loader_info = self.animation_loader.get_cache_info()
        core_config = self.animation_core.get_animation_config_summary()

        return {
            "active_players": len(self.active_players),
            "cached_characters": loader_info["cached_characters"],
            "total_animations": loader_info["total_animations"],
            "base_fps": core_config["base_fps"],
            "animation_types": core_config["animation_types"],
        }

    def preload_characters(self, character_names: list):
        """Precarga animaciones para múltiples personajes."""
        self.animation_loader.preload_character_animations(character_names)

    @property
    def base_fps(self) -> int:
        """Propiedad de compatibilidad para acceso al FPS base."""
        return self.animation_core.base_fps

    @property
    def animation_speeds(self) -> Dict[str, float]:
        """Propiedad de compatibilidad para acceso a velocidades."""
        return self.animation_core.animation_speeds

    @property
    def animation_cache(self) -> Dict:
        """Propiedad de compatibilidad para acceso al caché."""
        return self.animation_loader.animation_cache
