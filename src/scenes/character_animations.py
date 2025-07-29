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


class CharacterAnimations:
    """
    Gestiona las animaciones de personajes en la selección.
    """

    def __init__(self):
        """Inicializa el gestor de animaciones de personajes."""
        self.asset_manager = AssetManager()  # Usar el import corregido
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
        try:
            # Cargar animaciones para cada personaje
            characters = ["guerrero", "adventureguirl", "robot"]

            for character in characters:
                self.animation_frames[character] = self._load_character_frames(
                    character
                )

            self.logger.info(f"Animaciones cargadas para {len(characters)} personajes")

        except Exception as e:
            self.logger.error(f"Error cargando animaciones: {e}")

    def _load_character_frames(self, character_key: str) -> list:
        """
        Carga los frames de animación para un personaje específico.

        Args:
            character_key: Clave del personaje

        Returns:
            Lista de frames de animación
        """
        try:
            # Intentar cargar animación idle del personaje
            frames = []

            # Buscar frames en diferentes ubicaciones
            possible_paths = [
                f"characters/{character_key}/idle",
                f"characters/{character_key}/Idle",
                f"characters/used/{character_key}/idle",
                f"characters/used/{character_key}/Idle",
            ]

            for path in possible_paths:
                try:
                    frames = self.asset_manager.load_animation_frames(path)
                    if frames:
                        self.logger.debug(
                            f"Frames cargados para {character_key} desde {path}"
                        )
                        break
                except Exception as e:
                    self.logger.warning(f"Error cargando frames desde {path}: {e}")
                    continue

            # Si no se encontraron frames, crear placeholder
            if not frames:
                frames = [self._create_character_placeholder(character_key)]
                self.logger.warning(f"Usando placeholder para {character_key}")

            return frames

        except Exception as e:
            self.logger.error(f"Error cargando frames para {character_key}: {e}")
            return [self._create_character_placeholder(character_key)]

    def _create_character_placeholder(self, character_key: str) -> pygame.Surface:
        """
        Crea un sprite placeholder para un personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            Superficie placeholder
        """
        try:
            # Crear sprite de placeholder
            placeholder = pygame.Surface((120, 120))

            # Obtener datos del personaje desde CharacterData
            from .character_data import CharacterData

            char_data = CharacterData.get_character_data(character_key)

            if char_data:
                # Usar color y símbolo de la configuración
                color_data = char_data.get("color_placeholder", [255, 0, 0])
                color = tuple(color_data)
                symbol = char_data.get("símbolo", "?")
            else:
                # Fallback si no se encuentra en configuración
                color = (255, 0, 0)
                symbol = "?"

            placeholder.fill(color)

            # Añadir borde
            pygame.draw.rect(placeholder, (255, 255, 255), (0, 0, 120, 120), 3)

            # Añadir símbolo
            try:
                font = pygame.font.Font(None, 48)
                text = font.render(symbol, True, (255, 255, 255))
                text_rect = text.get_rect(center=(60, 60))
                placeholder.blit(text, text_rect)
            except Exception as e:
                self.logger.warning(f"Error al renderizar símbolo: {e}")
                pass

            return placeholder

        except Exception as e:
            self.logger.error(f"Error creando placeholder para {character_key}: {e}")
            # Crear placeholder mínimo
            placeholder = pygame.Surface((120, 120))
            placeholder.fill((255, 0, 0))
            return placeholder

    def update(self, delta_time: float):
        """
        Actualiza las animaciones.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        # Actualizar timer de animación
        self.frame_timer += delta_time * 1000  # Convertir a milisegundos

        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % self._get_max_frames()
            self.frame_timer = 0

    def _get_max_frames(self) -> int:
        """
        Obtiene el número máximo de frames disponibles.

        Returns:
            Número máximo de frames
        """
        max_frames = 1
        for frames in self.animation_frames.values():
            if frames:
                max_frames = max(max_frames, len(frames))
        return max_frames

    def get_character_image(self, character_key: str) -> Optional[pygame.Surface]:
        """
        Obtiene la imagen actual del personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            Superficie del personaje o None si no existe
        """
        try:
            if character_key in self.animation_frames:
                frames = self.animation_frames[character_key]
                if frames and len(frames) > 0:
                    # Obtener frame actual
                    frame_index = self.current_frame % len(frames)
                    return frames[frame_index]

            # Fallback: crear placeholder
            return self._create_character_placeholder(character_key)

        except Exception as e:
            self.logger.error(f"Error obteniendo imagen de {character_key}: {e}")
            return self._create_character_placeholder(character_key)

    def get_character_image_static(
        self, character_key: str
    ) -> Optional[pygame.Surface]:
        """
        Obtiene la imagen estática del personaje (sin animación).

        Args:
            character_key: Clave del personaje

        Returns:
            Superficie estática del personaje
        """
        try:
            if character_key in self.animation_frames:
                frames = self.animation_frames[character_key]
                if frames and len(frames) > 0:
                    return frames[0]  # Primer frame

            # Fallback: crear placeholder
            return self._create_character_placeholder(character_key)

        except Exception as e:
            self.logger.error(
                f"Error obteniendo imagen estática de {character_key}: {e}"
            )
            return self._create_character_placeholder(character_key)

    def set_animation_speed(self, frame_delay: int):
        """
        Establece la velocidad de animación.

        Args:
            frame_delay: Tiempo entre frames en milisegundos
        """
        self.frame_delay = max(50, frame_delay)  # Mínimo 50ms

    def reset_animation(self):
        """Reinicia la animación al primer frame."""
        self.current_frame = 0
        self.frame_timer = 0

    def get_animation_info(self) -> Dict[str, any]:
        """
        Obtiene información sobre las animaciones.

        Returns:
            Diccionario con información de animaciones
        """
        return {
            "current_frame": self.current_frame,
            "frame_delay": self.frame_delay,
            "characters_loaded": len(self.animation_frames),
            "max_frames": self._get_max_frames(),
        }

    def load_animation(self):
        character_key = "personaje_ejemplo"  # Definición de ejemplo
        path = "ruta/a/animaciones"  # Definición de ejemplo

        try:
            frames = self.asset_manager.load_animation_frames(path)
            self.logger.debug(
                "Frames cargados para %s desde %s: %d frames",
                character_key,
                path,
                len(frames),
            )
        except FileNotFoundError as e:
            self.logger.warning("Error cargando frames desde %s: %s", path, e)
        except ValueError as e:
            self.logger.error("Error cargando frames para %s: %s", character_key, e)
