"""
Asset Manager
============

Autor: SiK Team
Fecha: 2024
Descripción: Gestión centralizada de assets del juego con sistema de caché y fallbacks.
"""

import os
import pygame
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

class AssetManager:
    """Gestor centralizado de assets del juego."""
    
    def __init__(self, base_path: str = "assets"):
        """
        Inicializa el AssetManager.
        
        Args:
            base_path: Ruta base de los assets
        """
        self.base_path = Path(base_path)
        self.cache = {}
        self.logger = logging.getLogger(__name__)
        # Cargar configuración de animaciones desde config/animations.json
        self.animation_config = self._load_animation_config()
        
        self.logger.info("AssetManager inicializado")
    
    def _load_animation_config(self):
        config_path = Path("config/animations.json")
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error cargando config/animations.json: {e}")
        # Fallback: estructura vacía
        self.logger.warning("No se pudo cargar config/animations.json, usando configuración vacía.")
        return {"characters": {}, "sprite_paths": []}
    
    def load_image(self, path: str, scale: float = 1.0) -> Optional[pygame.Surface]:
        """
        Carga una imagen con caché.
        
        Args:
            path: Ruta de la imagen
            scale: Factor de escala
            
        Returns:
            Superficie de pygame o None si falla
        """
        cache_key = f"{path}_{scale}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        full_path = self.base_path / path
        
        try:
            if full_path.exists():
                image = pygame.image.load(str(full_path)).convert_alpha()
                if scale != 1.0:
                    new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                    image = pygame.transform.scale(image, new_size)
                
                self.cache[cache_key] = image
                self.logger.debug(f"Imagen cargada: {path}")
                return image
            else:
                self.logger.warning(f"Imagen no encontrada: {path}")
                return self._create_placeholder(64, 64, scale)
        except Exception as e:
            self.logger.error(f"Error cargando imagen {path}: {e}")
            return self._create_placeholder(64, 64, scale)
    
    def load_image_direct(self, path: str) -> Optional[pygame.Surface]:
        """
        Carga una imagen directamente sin caché.
        
        Args:
            path: Ruta de la imagen
            
        Returns:
            Superficie de pygame o None si falla
        """
        try:
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                self.logger.debug(f"Imagen cargada directamente: {path}")
                return image
            else:
                self.logger.warning(f"Imagen no encontrada: {path}")
                return self._create_placeholder(64, 64, 1.0)
        except Exception as e:
            self.logger.error(f"Error cargando imagen {path}: {e}")
            return self._create_placeholder(64, 64, 1.0)
    
    def get_character_sprite(self, character_name: str, animation: str, frame: int = 1, scale: float = 1.0) -> Optional[pygame.Surface]:
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
        if character_name not in self.animation_config['characters']:
            self.logger.warning(f"Personaje no encontrado en configuración: {character_name}")
            return self._create_placeholder(64, 64, scale)
        
        # Leer escala personalizada si no se ha especificado un scale explícito
        if scale == 1.0:
            char_config = self.animation_config['characters'][character_name]
            scale = char_config.get('escala_sprite', 1.0)
        
        # Verificar si la animación existe para este personaje
        available_animations = self.animation_config['characters'][character_name]['animations']
        if animation not in available_animations:
            self.logger.warning(f"Animación '{animation}' no disponible para {character_name}. Disponibles: {available_animations}")
            return self._create_placeholder(64, 64, scale)
        
        # Usar rutas desde config
        sprite_paths = self.animation_config.get("sprite_paths", [
            "characters/used/{character}/{animation}_{frame}_.png",
            "characters/used/{character}/{animation}_{frame}.png",
            "characters/{character}/{animation}_{frame}_.png",
            "characters/{character}/{animation}_{frame}.png"
        ])
        animation_capitalized = animation.capitalize()
        possible_paths = [
            path.format(character=character_name, animation=animation_capitalized, frame=frame)
            for path in sprite_paths
        ]
        
        for path in possible_paths:
            sprite = self.load_image(path, scale)
            if sprite and not self._is_placeholder_sprite(sprite):
                return sprite
        
        self.logger.warning(f"Sprite no encontrado: {character_name}/{animation_capitalized}_{frame}_, creando placeholder")
        return self._create_placeholder(64, 64, scale)
    
    def get_character_animation_frames(self, character_name: str, animation: str, max_frames: int = None) -> List[pygame.Surface]:
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
        if character_name not in self.animation_config['characters']:
            self.logger.warning(f"Personaje no encontrado en configuración: {character_name}")
            return frames
        
        # Verificar si la animación existe para este personaje
        available_animations = self.animation_config['characters'][character_name]['animations']
        if animation not in available_animations:
            self.logger.warning(f"Animación '{animation}' no disponible para {character_name}. Disponibles: {available_animations}")
            return frames
        
        # Obtener el número máximo de frames desde la configuración
        if max_frames is None:
            max_frames = self.animation_config['characters'][character_name].get('total_frames', 10)
        
        # Cargar frames hasta encontrar uno que no exista o alcanzar el máximo
        while frame <= max_frames:
            sprite = self.get_character_sprite(character_name, animation, frame)
            
            if sprite and not self._is_placeholder_sprite(sprite):
                frames.append(sprite)
                frame += 1
            else:
                # Si encontramos un placeholder, asumimos que no hay más frames
                break
        
        self.logger.info(f"Cargados {len(frames)} frames para {character_name}/{animation}")
        return frames
    
    def get_character_animation_info(self, character_name: str) -> Dict[str, Any]:
        """
        Obtiene información completa de las animaciones de un personaje.
        
        Args:
            character_name: Nombre del personaje
            
        Returns:
            Diccionario con información de animaciones
        """
        if character_name not in self.animation_config['characters']:
            return {}
        
        char_config = self.animation_config['characters'][character_name]
        animation_info = {}
        
        for animation in char_config['animations']:
            frames = self.get_character_animation_frames(character_name, animation)
            animation_info[animation] = {
                'frame_count': len(frames),
                'frames': frames,
                'fps': self._calculate_optimal_fps(len(frames), animation)
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
            'Idle': 12,
            'Walk': 15,
            'Run': 18,
            'Attack': 20,
            'Dead': 10,
            'Shoot': 16,
            'Jump': 14,
            'Melee': 18,
            'Slide': 16,
            'JumpMelee': 16,
            'JumpShoot': 16,
            'RunShoot': 18,
            'JumpAttack': 15
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
    
    def _is_placeholder_sprite(self, sprite: pygame.Surface) -> bool:
        """
        Verifica si un sprite es un placeholder.
        
        Args:
            sprite: Superficie de pygame
            
        Returns:
            True si es un placeholder
        """
        if sprite.get_width() == 64 and sprite.get_height() == 64:
            colors = set()
            for x in range(0, 64, 8):
                for y in range(0, 64, 8):
                    color = sprite.get_at((x, y))
                    colors.add((color.r, color.g, color.b, color.a))
            if len(colors) <= 3:
                return True
        return False
    
    def _create_placeholder(self, width: int, height: int, scale: float = 1.0) -> pygame.Surface:
        """
        Crea un sprite placeholder.
        
        Args:
            width: Ancho del placeholder
            height: Alto del placeholder
            scale: Factor de escala
            
        Returns:
            Superficie del placeholder
        """
        scaled_width = int(width * scale)
        scaled_height = int(height * scale)
        
        placeholder = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        placeholder.fill((255, 0, 255, 128))  # Magenta semi-transparente
        
        return placeholder
    
    def clear_cache(self):
        """Limpia la caché de imágenes."""
        self.cache.clear()
        self.logger.info("Caché de imágenes limpiada")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre la caché.
        
        Returns:
            Información de la caché
        """
        return {
            'cache_size': len(self.cache),
            'cached_items': list(self.cache.keys())
        }
    
    def get_ui_button(self, button_name: str, state: str = 'normal') -> Optional[pygame.Surface]:
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
            'normal': '_n',
            'pressed': '_p', 
            'hover': '_h',
            'left': '_l',
            'right': '_r'
        }
        
        suffix = state_suffixes.get(state, '_n')
        
        # Rutas posibles para botones
        possible_paths = [
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}{suffix}.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}_n.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}_p.png",
            f"ui/Buttons/botonescuadrados/slategrey/{button_name}_h.png",
            f"ui/Buttons/Blue/{button_name}{suffix}.png",
            f"ui/Buttons/Green/{button_name}{suffix}.png",
            f"ui/Buttons/Red/{button_name}{suffix}.png"
        ]
        
        for path in possible_paths:
            button = self.load_image(path)
            if button:
                return button
        
        # Fallback: crear placeholder
        self.logger.warning(f"Botón UI no encontrado: {button_name}{suffix}")
        return self._create_placeholder(64, 64, 1.0) 