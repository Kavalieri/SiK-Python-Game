"""
Test - Animaciones Óptimas
=========================

Autor: SiK Team
Fecha: 2024
Descripción: Test que solo carga animaciones existentes y verifica FPS óptimos.
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

class OptimalAnimationTester:
    """Testador de animaciones óptimas."""
    
    def __init__(self):
        """Inicializa el testador."""
        self.logger = logging.getLogger(__name__)
        pygame.init()
        
        # Configuración de pantalla
        self.screen_width = 1400
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Test - Animaciones Óptimas")
        
        # Importar el sistema
        from utils.animation_manager import IntelligentAnimationManager
        self.animation_manager = IntelligentAnimationManager()
        
        # Personajes a testear
        self.characters = ["guerrero", "adventureguirl", "robot", "zombiemale", "zombieguirl"]
        self.current_character = 0
        
        # Crear reproductores de animación
        self.animation_players = {}
        for character in self.characters:
            self.animation_players[character] = self.animation_manager.create_animation_player(character, 'idle')
        
        # Tiempo de inicio
        self.start_time = pygame.time.get_ticks()
        
        # Fuente para texto
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        self.logger.info("Testador de animaciones óptimas inicializado")
    
    def render_info_panel(self):
        """Renderiza el panel de información."""
        # Fondo del panel
        panel_rect = pygame.Rect(10, 10, 500, 300)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), panel_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 2)
        
        # Información del personaje actual
        character = self.characters[self.current_character]
        player = self.animation_players[character]
        
        y_offset = 20
        texts = [
            f"Personaje: {character}",
            f"Animación actual: {player.current_animation}",
            f"Animaciones disponibles: {len(player.animations)}",
            "",
            "Animaciones cargadas:"
        ]
        
        for text in texts:
            if text:
                text_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(text_surface, (20, y_offset))
            y_offset += 25
        
        # Listar animaciones disponibles
        for anim_type, anim_data in player.animations.items():
            text = f"  {anim_type}: {anim_data['frame_count']} frames a {anim_data['fps']} FPS"
            text_surface = self.small_font.render(text, True, (200, 200, 200))
            self.screen.blit(text_surface, (20, y_offset))
            y_offset += 20
        
        y_offset += 10
        texts = [
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
        cols = 5
        rows = (len(animations) + cols - 1) // cols
        cell_width = 120
        cell_height = 100
        start_x = 550
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
        player = self.animation_players[character]
        
        frame = player.get_current_frame()
        
        if frame:
            # Centrar en la pantalla
            frame_rect = frame.get_rect()
            frame_rect.center = (self.screen_width // 2, self.screen_height // 2)
            self.screen.blit(frame, frame_rect)
            
            # Borde alrededor del sprite
            pygame.draw.rect(self.screen, (255, 255, 0), frame_rect, 2)
            
            # Información de la animación actual
            anim_data = player.animations[player.current_animation]
            info_text = f"{player.current_animation} - {anim_data['frame_count']} frames a {anim_data['fps']} FPS"
            text_surface = self.font.render(info_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
            self.screen.blit(text_surface, text_rect)
    
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
                    player = self.animation_players[self.characters[self.current_character]]
                    animations = list(player.animations.keys())
                    if animations:
                        current_index = animations.index(player.current_animation)
                        next_index = (current_index + 1) % len(animations)
                        player.set_animation(animations[next_index])
                        self.logger.info(f"Cambiando a animación: {animations[next_index]}")
        
        return True
    
    def run(self):
        """Ejecuta el test."""
        self.logger.info("Iniciando test de animaciones óptimas")
        
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
        self.logger.info("Test de animaciones óptimas finalizado")

def main():
    """Función principal."""
    print("=== TEST: Animaciones Óptimas ===")
    setup_logging()
    
    tester = OptimalAnimationTester()
    tester.run()
    
    print("=== TEST FINALIZADO ===")

if __name__ == "__main__":
    main() 