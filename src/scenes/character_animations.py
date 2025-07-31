"""
Character Animations - Animaciones de Personajes
==============================================

Autor: SiK Team
Fecha: 2024-12-19
Descripción: Módulo que maneja las animaciones de personajes en la selección.
"""

import logging
from typing import Dict, Optional

import pygame

from src.utils.asset_manager import AssetManager
from .character_data import CharacterData


class CharacterAnimations:
    """Gestiona las animaciones de personajes en la selección."""

    def __init__(self):
        """Inicializa el gestor de animaciones de personajes."""
        self.asset_manager = AssetManager()
        self.logger = logging.getLogger(__name__)

        # Animación de sprites
        self.animation_frames = {}
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 150  # milisegundos entre frames

        # Cargar frames de animación para todos los personajes
        self._load_animation_frames()

    def _load_animation_frames(self):
        """Carga los frames de animación para todos los personajes."""
        characters = ["guerrero", "adventureguirl", "robot"]
        for character in characters:
            self.animation_frames[character] = self._load_character_frames(character)
        self.logger.info("Animaciones cargadas para %d personajes", len(characters))

    def _load_character_frames(self, character_key: str) -> list:
        """Carga los frames de animación para un personaje específico."""
        frames = []
        possible_paths = self._get_possible_paths(character_key)

        for path in possible_paths:
            try:
                frames = self.asset_manager.load_animation_frames(path)
                if frames:
                    self.logger.debug(
                        "Frames cargados para %s desde %s", character_key, path
                    )
                    break
            except FileNotFoundError:
                self.logger.warning("Frames no encontrados en %s", path)
            except ValueError as e:
                self.logger.error("Error cargando frames desde %s: %s", path, e)

        if not frames:
            frames = [self._create_character_placeholder(character_key)]
            self.logger.warning("Usando placeholder para %s", character_key)

        return frames

    def _get_possible_paths(self, character_key: str) -> list:
        """Genera las rutas posibles para buscar frames de un personaje."""
        base_paths = ["characters", "characters/used"]
        subfolders = ["idle", "Idle"]
        return [
            f"{base}/{character_key}/{sub}" for base in base_paths for sub in subfolders
        ]

    def _create_character_placeholder(self, character_key: str) -> pygame.Surface:
        """Crea un sprite placeholder para un personaje."""
        placeholder = pygame.Surface((120, 120))
        char_data = self._get_character_data(character_key)

        color = tuple(char_data.get("color_placeholder", [255, 0, 0]))
        symbol = char_data.get("símbolo", "?")

        placeholder.fill(color)
        self._add_placeholder_border(placeholder)
        self._add_placeholder_symbol(placeholder, symbol)

        return placeholder

    def _get_character_data(self, character_key: str) -> dict:
        """
        Obtiene los datos del personaje desde CharacterData.

        Args:
            character_key: Clave del personaje

        Returns:
            dict: Datos del personaje
        """
        return CharacterData.get_character_data(character_key) or {}

    def _add_placeholder_border(self, surface: pygame.Surface):
        """
        Añade un borde al placeholder.

        Args:
            surface: Superficie del placeholder
        """
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, 120, 120), 3)

    def _add_placeholder_symbol(self, surface: pygame.Surface, symbol: str):
        """Añade un símbolo al placeholder."""
        try:
            font = pygame.font.Font(None, 48)
            text = font.render(symbol, True, (255, 255, 255))
            text_rect = text.get_rect(center=(60, 60))
            surface.blit(text, text_rect)
        except OSError as e:
            self.logger.warning("Error al renderizar símbolo: %s", e)

    def update(self, delta_time: float):
        """Actualiza las animaciones."""
        # Actualizar timer de animación
        self.frame_timer += delta_time * 1000  # Convertir a milisegundos

        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % self._get_max_frames()
            self.frame_timer = 0

    def _get_max_frames(self) -> int:
        """Obtiene el número máximo de frames disponibles."""
        max_frames = 1
        for frames in self.animation_frames.values():
            if frames:
                max_frames = max(max_frames, len(frames))
        return max_frames

    def get_character_image(self, character_key: str) -> Optional[pygame.Surface]:
        """Obtiene la imagen actual del personaje."""
        try:
            if character_key in self.animation_frames:
                frames = self.animation_frames[character_key]
                if frames and len(frames) > 0:
                    # Obtener frame actual
                    frame_index = self.current_frame % len(frames)
                    return frames[frame_index]

            # Fallback: crear placeholder
            return self._create_character_placeholder(character_key)

        except (KeyError, IndexError, ValueError) as e:
            self.logger.error("Error obteniendo imagen de %s: %s", character_key, e)
            return self._create_character_placeholder(character_key)

    def get_character_image_static(
        self, character_key: str
    ) -> Optional[pygame.Surface]:
        """Obtiene la imagen estática del personaje (sin animación)."""
        try:
            if character_key in self.animation_frames:
                frames = self.animation_frames[character_key]
                if frames and len(frames) > 0:
                    return frames[0]  # Primer frame

            # Fallback: crear placeholder
            return self._create_character_placeholder(character_key)

        except (KeyError, IndexError, ValueError) as e:
            self.logger.error(
                "Error obteniendo imagen estática de %s: %s", character_key, e
            )
            return self._create_character_placeholder(character_key)

    def set_animation_speed(self, frame_delay: int):
        """Establece la velocidad de animación."""
        self.frame_delay = max(50, frame_delay)  # Mínimo 50ms

    def reset_animation(self):
        """Reinicia la animación al primer frame."""
        self.current_frame = 0
        self.frame_timer = 0

    def get_animation_info(self) -> Dict[str, object]:
        """Obtiene información sobre las animaciones."""
        return {
            "current_frame": self.current_frame,
            "frame_delay": self.frame_delay,
            "characters_loaded": len(self.animation_frames),
            "max_frames": self._get_max_frames(),
        }
