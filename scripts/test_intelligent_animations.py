"""
Test - Sistema de Animación Inteligente
======================================

Autor: SiK Team
Fecha: 2024
Descripción: Test del nuevo sistema de animación que ajusta FPS automáticamente.
"""

import sys
import os
import pygame
import logging
from typing import Dict, List

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class IntelligentAnimationTester:
    """Testador del sistema de animación inteligente."""
    
    def __init__(self):
        """Inicializa el testador."""
        self.logger = logging.getLogger(__name__)
        pygame.init()
        
        # Configuración de pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Test - Sistema de Animación Inteligente")
        
        # Importar el nuevo sistema
        from utils.animation_manager import IntelligentAnimationManager
        self.animation_manager = IntelligentAnimationManager()
        
        # Personajes a testear
        self.characters = ["guerrero", "adventureguirl", "robot", "zombiemale", "zombieguirl"]
        self.current_character = 0
        self.current_animation = 0
        
        # Animaciones disponibles
        self.animation_types = [
            'idle', 'run', 'walk', 'attack', 'shoot', 'dead', 'jump', 
            'melee', 'slide', 'jumpmelee', 'jumpshoot', 'runshoot'
        ]
        
        # Crear reproductores de animación
        self.animation_players = {}
        for character in self.characters:
            self.animation_players[character] = self.animation_manager.create_animation_player(character, 'idle')
        
        # Tiempo de inicio
        self.start_time = pygame.time.get_ticks()
        
        # Fuente para texto
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        self.logger.info("Testador de animación inteligente inicializado")
    
    def render_info_panel(self):
        """Renderiza el panel de información."""
        # Fondo del panel
        panel_rect = pygame.Rect(10, 10, 400, 200)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 2)
        
        # Información del personaje actual
        character = self.characters[self.current_character]
        animation = self.animation_types[self.current_animation]
        
        # Obtener datos de la animación
        animation_data = self.animation_manager.animation_cache.get(f"{character}_{animation}")
        
        y_offset = 20
        texts = [
            f"Personaje: {character}",
            f"Animación: {animation}",
            f"Frames: {animation_data['frame_count'] if animation_data else 'N/A'}",
            f"FPS: {animation_data['fps'] if animation_data else 'N/A'}",
            f"Duración: {animation_data['total_duration'] if animation_data else 'N/A'} ms",
            "",
            "Controles:",
            "Flechas: Cambiar personaje",
            "Espacio: Cambiar animación",
            "ESC: Salir"
        ]
        
        for text in texts:
            if text:
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (20, y_offset))
            y_offset += 25
    
    def render_animation_grid(self):
        """Renderiza una cuadrícula con todas las animaciones del personaje actual."""
        character = self.characters[self.current_character]
        player = self.animation_players[character]
        
        # Obtener todas las animaciones disponibles
        animations = player.animations
        
        # Configurar cuadrícula
        cols = 4
        rows = (len(animations) + cols - 1) // cols
        cell_width = 150
        cell_height = 120
        start_x = 450
        start_y = 50
        
        # Renderizar cada animación
        for i, (anim_type, anim_data) in enumerate(animations.items()):
            row = i // cols
            col = i % cols
            
            x = start_x + col * cell_width
            y = start_y + row * cell_height
            
            # Fondo de la celda
            cell_rect = pygame.Rect(x, y, cell_width - 10, cell_height - 10)
            pygame.draw.rect(self.screen, (50, 50, 50), cell_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, 1)
            
            # Cambiar a esta animación para mostrar el primer frame
            player.set_animation(anim_type)
            frame = player.get_current_frame()
            
            if frame:
                # Centrar el sprite en la celda
                frame_rect = frame.get_rect()
                frame_rect.center = (x + cell_width // 2 - 5, y + cell_height // 2 - 5)
                self.screen.blit(frame, frame_rect)
            
            # Texto de la animación
            text = self.small_font.render(anim_type, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + cell_width // 2 - 5, y + cell_height - 20))
            self.screen.blit(text, text_rect)
            
            # Información de FPS
            fps_text = self.small_font.render(f"{anim_data['fps']} FPS", True, (200, 200, 200))
            fps_rect = fps_text.get_rect(center=(x + cell_width // 2 - 5, y + 15))
            self.screen.blit(fps_text, fps_rect)
    
    def render_current_animation(self):
        """Renderiza la animación actual en grande."""
        character = self.characters[self.current_character]
        animation = self.animation_types[self.current_animation]
        player = self.animation_players[character]
        
        # Cambiar a la animación actual
        player.set_animation(animation)
        frame = player.get_current_frame()
        
        if frame:
            # Centrar en la pantalla
            frame_rect = frame.get_rect()
            frame_rect.center = (self.screen_width // 2, self.screen_height // 2)
            self.screen.blit(frame, frame_rect)
            
            # Borde alrededor del sprite
            pygame.draw.rect(self.screen, (255, 255, 0), frame_rect, 2)
    
    def handle_events(self):
        """Maneja los eventos de entrada."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_LEFT:
                    self.current_character = (self.current_character - 1) % len(self.characters)
                    self.logger.info(f"Cambiando a personaje: {self.characters[self.current_character]}")
                
                elif event.key == pygame.K_RIGHT:
                    self.current_character = (self.current_character + 1) % len(self.characters)
                    self.logger.info(f"Cambiando a personaje: {self.characters[self.current_character]}")
                
                elif event.key == pygame.K_SPACE:
                    self.current_animation = (self.current_animation + 1) % len(self.animation_types)
                    self.logger.info(f"Cambiando a animación: {self.animation_types[self.current_animation]}")
        
        return True
    
    def run(self):
        """Ejecuta el test."""
        self.logger.info("Iniciando test de animación inteligente")
        
        running = True
        clock = pygame.time.Clock()
        
        while running:
            running = self.handle_events()
            
            # Limpiar pantalla
            self.screen.fill((30, 30, 30))
            
            # Renderizar elementos
            self.render_info_panel()
            self.render_animation_grid()
            self.render_current_animation()
            
            # Actualizar pantalla
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        self.logger.info("Test de animación inteligente finalizado")

def main():
    """Función principal."""
    print("=== TEST: Sistema de Animación Inteligente ===")
    setup_logging()
    
    tester = IntelligentAnimationTester()
    tester.run()
    
    print("=== TEST FINALIZADO ===")

if __name__ == "__main__":
    main() 