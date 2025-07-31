"""
UI Assets - Gestión de Assets de Interfaz de Usuario
===================================================

Autor: SiK Team
Fecha: Julio 2025
Descripción: Gestión especializada de elementos de interfaz (botones, iconos, etc.).
"""

import logging
from typing import List, Optional

import pygame

from .asset_loader import AssetLoader


class UIAssets:
    """Gestor especializado de assets de interfaz de usuario."""

    def __init__(self, asset_loader: AssetLoader):
        """
        Inicializa el gestor de assets de UI.

        Args:
            asset_loader: Instancia del cargador base
        """
        self.asset_loader = asset_loader
        self.logger = logging.getLogger(__name__)
        self.logger.info("UIAssets inicializado")

    def get_ui_button(
        self, button_name: str, state: str = "normal"
    ) -> Optional[pygame.Surface]:
        """
        Carga un botón de UI.

        Args:
            button_name: Nombre del botón (ej: 'arrow_r', 'arrow_l')
            state: Estado del botón ('normal', 'pressed', 'hover')

        Returns:
            Superficie del botón o None si falla
        """
        # Mapeo de estados a sufijos
        state_suffixes = {
            "normal": "_n",
            "pressed": "_p",
            "hover": "_h",
            "left": "_l",
            "right": "_r",
        }

        suffix = state_suffixes.get(state, "_n")

        # Rutas posibles para botones
        possible_paths = [
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}{suffix}.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}_n.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}_p.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}_h.png",
            f"ui/Buttons/Blue/{button_name}{suffix}.png",
            f"ui/Buttons/Green/{button_name}{suffix}.png",
            f"ui/Buttons/Red/{button_name}{suffix}.png",
        ]

        for path in possible_paths:
            button = self.asset_loader.load_image(path)
            if button and not self.asset_loader.is_placeholder_sprite(button):
                return button

        # Fallback: crear placeholder
        self.logger.warning("Botón UI no encontrado: %s%s", button_name, suffix)
        return self.asset_loader.create_placeholder(64, 64, 1.0)

    def load_animation_frames(
        self, ruta: str, max_frames: Optional[int] = None
    ) -> List[pygame.Surface]:
        """
        Carga los frames de animación desde una ruta específica.

        Args:
            ruta: Ruta relativa dentro de la carpeta de assets
            max_frames: Número máximo de frames a cargar (opcional)

        Returns:
            Una lista de superficies de Pygame representando los frames de animación

        Raises:
            FileNotFoundError: Si la ruta no existe o no contiene imágenes
        """
        ruta_completa = self.asset_loader.base_path / ruta
        if not ruta_completa.exists():
            raise FileNotFoundError(f"La ruta {ruta_completa} no existe.")

        frames = []

        # Buscar archivos con patrón Idle_*.png (para personajes en modo idle)
        idle_files = sorted(ruta_completa.glob("Idle_*.png"))
        if idle_files:
            for archivo in idle_files:
                frame = pygame.image.load(archivo).convert_alpha()
                frames.append(frame)
        else:
            # Fallback: buscar cualquier archivo .png
            for archivo in sorted(ruta_completa.glob("*.png")):
                frame = pygame.image.load(archivo).convert_alpha()
                frames.append(frame)

        if max_frames is not None:
            frames = frames[:max_frames]

        if not frames:
            raise FileNotFoundError(f"No se encontraron imágenes en {ruta_completa}.")

        return frames

    def cargar_botones_ui(
        self, button_name: str, suffix: str = ""
    ) -> Optional[pygame.Surface]:
        """
        Carga un botón de la interfaz de usuario.

        Args:
            button_name: Nombre del botón
            suffix: Sufijo adicional

        Returns:
            Superficie del botón o None si falla
        """
        try:
            button_path = f"ui/{button_name}{suffix}.png"
            button_surface = self.asset_loader.load_image(button_path)
            if not button_surface or self.asset_loader.is_placeholder_sprite(
                button_surface
            ):
                self.logger.warning("Botón UI no encontrado: %s%s", button_name, suffix)
            return button_surface
        except OSError as e:
            self.logger.error(
                "Error de E/S al cargar botón UI %s%s: %s", button_name, suffix, e
            )
            return None
