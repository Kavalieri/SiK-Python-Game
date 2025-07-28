"""
Gestor de Animaciones Inteligente
=================================

Autor: SiK Team
Fecha: 2024
Descripción: Sistema de animación que ajusta la velocidad según los fotogramas disponibles.
"""

import pygame
import logging
from typing import List, Optional, Dict, Tuple
from .asset_manager import AssetManager

class IntelligentAnimationManager:
    """Gestor de animaciones que ajusta la velocidad automáticamente."""
    
    def __init__(self, asset_manager: AssetManager = None):
        """Inicializa el gestor de animaciones."""
        self.logger = logging.getLogger(__name__)
        self.asset_manager = asset_manager if asset_manager else AssetManager()
        
        # Configuración de FPS base y ajustes por tipo de animación
        self.base_fps = 20
        self.animation_speeds = {
            'idle': 0.8,      # Más lento para idle
            'walk': 1.0,      # Normal para caminar
            'run': 1.2,       # Más rápido para correr
            'attack': 1.5,    # Rápido para ataques
            'shoot': 1.3,     # Rápido para disparos
            'dead': 0.6,      # Lento para muerte
            'jump': 1.1,      # Normal para saltos
            'melee': 1.4,     # Rápido para melee
            'slide': 1.0,     # Normal para deslizar
        }
        
        # Cache de animaciones
        self.animation_cache = {}
        
    def get_optimal_fps(self, animation_type: str, frame_count: int) -> int:
        """
        Calcula el FPS óptimo para una animación basado en el número de fotogramas.
        
        Args:
            animation_type: Tipo de animación (idle, run, attack, etc.)
            frame_count: Número de fotogramas disponibles
            
        Returns:
            FPS óptimo para la animación
        """
        # FPS base ajustado por tipo de animación
        base_speed = self.animation_speeds.get(animation_type.lower(), 1.0)
        adjusted_fps = int(self.base_fps * base_speed)
        
        # Si tenemos muy pocos fotogramas, reducir FPS para que se vea bien
        if frame_count <= 3:
            return max(8, adjusted_fps // 2)  # Mínimo 8 FPS
        elif frame_count <= 5:
            return max(10, adjusted_fps // 1.5)
        elif frame_count <= 8:
            return max(12, adjusted_fps // 1.2)
        else:
            return adjusted_fps
    
    def load_character_animations(self, character_name: str) -> Dict[str, Dict]:
        """
        Carga todas las animaciones disponibles para un personaje.
        
        Args:
            character_name: Nombre del personaje
            
        Returns:
            Diccionario con las animaciones cargadas
        """
        animations = {}
        
        # Tipos de animación a verificar (usar mayúsculas para coincidir con AssetManager)
        animation_types = [
            'Idle', 'Run', 'Walk', 'Attack', 'Dead', 'Shoot', 
            'Jump', 'Melee', 'Slide', 'JumpMelee', 'JumpShoot', 'RunShoot'
        ]
        
        for anim_type in animation_types:
            frames = self.asset_manager.get_character_animation_frames(character_name, anim_type)
            
            # Solo cargar si hay frames reales (no solo placeholders)
            real_frames = [frame for frame in frames if not self._is_placeholder(frame)]
            
            if real_frames:
                # Calcular FPS óptimo basado en el número de frames
                optimal_fps = self._calculate_optimal_fps(len(real_frames), anim_type)
                
                animations[anim_type] = {
                    'frames': real_frames,
                    'frame_count': len(real_frames),
                    'fps': optimal_fps,
                    'frame_duration': 1000 / optimal_fps  # en milisegundos
                }
                
                self.logger.info(f"Animación cargada: {character_name}/{anim_type} - {len(real_frames)} frames a {optimal_fps} FPS")
            else:
                self.logger.debug(f"No se encontraron frames reales para {character_name}/{anim_type}")
        
        self.logger.info(f"Cargadas {len(animations)} animaciones para {character_name}")
        return animations
    
    def _is_placeholder(self, surface: pygame.Surface) -> bool:
        """
        Verifica si una superficie es un placeholder.
        
        Args:
            surface: Superficie a verificar
            
        Returns:
            True si es un placeholder, False si no
        """
        # Los placeholders tienen un tamaño específico y color
        if surface.get_width() == 64 and surface.get_height() == 64:
            # Verificar si es un color sólido (placeholder)
            colors = set()
            for x in range(0, 64, 8):
                for y in range(0, 64, 8):
                    color = surface.get_at((x, y))
                    colors.add((color.r, color.g, color.b, color.a))
            
            # Si hay muy pocos colores, probablemente es un placeholder
            if len(colors) <= 3:
                return True
        
        return False
    
    def _calculate_optimal_fps(self, frame_count: int, anim_type: str) -> int:
        """
        Calcula el FPS óptimo basado en el número de frames y tipo de animación.
        
        Args:
            frame_count: Número de frames disponibles
            anim_type: Tipo de animación
            
        Returns:
            FPS óptimo calculado
        """
        # FPS base por tipo de animación
        base_fps = self.animation_speeds.get(anim_type, 1.0) * self.base_fps
        
        # Ajustar según el número de frames
        if frame_count <= 4:
            # Pocos frames: FPS más bajo para que se vea fluido
            return max(8, int(base_fps * 0.6))
        elif frame_count <= 8:
            # Frames moderados: FPS medio
            return max(12, int(base_fps * 0.8))
        elif frame_count <= 12:
            # Buen número de frames: FPS estándar
            return int(base_fps)
        else:
            # Muchos frames: FPS alto
            return min(30, int(base_fps * 1.2))
    
    def get_all_character_animations(self, character_name: str) -> Dict[str, Dict]:
        """
        Carga todas las animaciones disponibles para un personaje.
        
        Args:
            character_name: Nombre del personaje
            
        Returns:
            Diccionario con todas las animaciones
        """
        # Usar el nuevo sistema que solo carga animaciones reales
        return self.load_character_animations(character_name)
    
    def create_animation_player(self, character_name: str, initial_animation: str = 'Idle'):
        """
        Crea un reproductor de animación para un personaje.
        
        Args:
            character_name: Nombre del personaje
            initial_animation: Animación inicial
            
        Returns:
            Reproductor de animación
        """
        return AnimationPlayer(self, character_name, initial_animation)

class AnimationPlayer:
    """Reproductor de animaciones para un personaje específico."""
    
    def __init__(self, manager: IntelligentAnimationManager, character_name: str, initial_animation: str = 'Idle'):
        """Inicializa el reproductor."""
        self.manager = manager
        self.character_name = character_name
        self.current_animation = initial_animation
        self.animation_start_time = pygame.time.get_ticks()
        self.animations = self.manager.get_all_character_animations(character_name)
        
    def set_animation(self, animation_type: str):
        """Cambia la animación actual."""
        if animation_type != self.current_animation and animation_type in self.animations:
            self.current_animation = animation_type
            self.animation_start_time = pygame.time.get_ticks()
            self.manager.logger.debug(f"Cambiando animación a: {animation_type}")
    
    def get_current_frame(self) -> pygame.Surface:
        """Obtiene el frame actual de la animación."""
        if self.current_animation not in self.animations:
            return None
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        
        animation_data = self.animations[self.current_animation]
        frame_duration = animation_data['frame_duration']
        frame_count = animation_data['frame_count']
        
        # Calcular frame actual
        current_frame = int((elapsed_time // frame_duration) % frame_count)
        
        return animation_data['frames'][current_frame]
    
    @property
    def current_frame_index(self) -> int:
        """Obtiene el índice del frame actual."""
        if self.current_animation not in self.animations:
            return 0
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        
        animation_data = self.animations[self.current_animation]
        frame_duration = animation_data['frame_duration']
        frame_count = animation_data['frame_count']
        
        return int((elapsed_time // frame_duration) % frame_count)
    
    def is_animation_completed(self) -> bool:
        """Verifica si la animación actual se completó."""
        if self.current_animation not in self.animations:
            return True
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        
        animation_data = self.animations[self.current_animation]
        frame_duration = animation_data['frame_duration']
        frame_count = animation_data['frame_count']
        
        # Verificar si la animación se completó
        return elapsed_time >= frame_duration * frame_count 