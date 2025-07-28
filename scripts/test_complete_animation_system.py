"""
Test Completo del Sistema de Animaciones
=======================================

Autor: SiK Team
Fecha: 2024
Descripción: Test visual completo de todas las animaciones de todos los personajes.
"""

import pygame
import sys
import os
import time
from pathlib import Path

# Añadir el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.asset_manager import AssetManager
from utils.animation_manager import IntelligentAnimationManager, AnimationPlayer

class CompleteAnimationTester:
    """Testador completo del sistema de animaciones."""
    
    def __init__(self):
        """Inicializa el testador."""
        pygame.init()
        
        # Configuración de la ventana
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Test Completo de Animaciones - SiK Game")
        
        # Inicializar managers
        self.asset_manager = AssetManager()
        self.animation_manager = IntelligentAnimationManager(self.asset_manager)
        
        # Configuración de la interfaz
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 36)
        
        # Estado del test
        self.characters = ["guerrero", "adventureguirl", "robot", "zombiemale", "zombieguirl"]
        self.current_character_index = 0
        self.current_animation_index = 0
        self.animation_players = {}
        
        # Información de animaciones
        self.animation_info = {}
        self.load_all_animations()
        
        # Controles
        self.auto_play = True
        self.show_info = True
        self.last_time = time.time()
        
        # Colores
        self.colors = {
            'background': (30, 30, 30),
            'panel': (50, 50, 50),
            'text': (255, 255, 255),
            'text_secondary': (200, 200, 200),
            'highlight': (100, 150, 255),
            'success': (100, 255, 100),
            'warning': (255, 255, 100),
            'error': (255, 100, 100)
        }
    
    def load_all_animations(self):
        """Carga todas las animaciones de todos los personajes."""
        print("=== CARGANDO TODAS LAS ANIMACIONES ===")
        
        for character in self.characters:
            print(f"\nCargando {character}...")
            
            # Crear player de animación
            self.animation_players[character] = AnimationPlayer(
                self.animation_manager, character, 'Idle'
            )
            
            # Obtener información de animaciones
            char_info = self.asset_manager.get_character_animation_info(character)
            self.animation_info[character] = char_info
            
            # Mostrar resumen
            total_frames = sum(info['frame_count'] for info in char_info.values())
            print(f"  Animaciones: {len(char_info)}")
            print(f"  Total frames: {total_frames}")
            
            for anim_name, info in char_info.items():
                print(f"    {anim_name}: {info['frame_count']} frames a {info['fps']} FPS")
        
        print("\n=== CARGA COMPLETADA ===")
    
    def handle_events(self):
        """Maneja los eventos de pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.auto_play = not self.auto_play
                elif event.key == pygame.K_i:
                    self.show_info = not self.show_info
                elif event.key == pygame.K_LEFT:
                    self.current_character_index = (self.current_character_index - 1) % len(self.characters)
                    self.current_animation_index = 0
                elif event.key == pygame.K_RIGHT:
                    self.current_character_index = (self.current_character_index + 1) % len(self.characters)
                    self.current_animation_index = 0
                elif event.key == pygame.K_UP:
                    self.current_animation_index = (self.current_animation_index - 1) % len(self.get_current_animations())
                elif event.key == pygame.K_DOWN:
                    self.current_animation_index = (self.current_animation_index + 1) % len(self.get_current_animations())
                elif event.key == pygame.K_r:
                    self.reset_animations()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click izquierdo
                    self.handle_click(event.pos)
        
        return True
    
    def handle_click(self, pos):
        """Maneja los clicks del ratón."""
        # Panel de personajes (izquierda)
        if pos[0] < 300:
            char_height = 60
            char_index = pos[1] // char_height
            if char_index < len(self.characters):
                self.current_character_index = char_index
                self.current_animation_index = 0
        
        # Panel de animaciones (derecha)
        elif pos[0] > 900:
            anim_height = 40
            anim_index = (pos[1] - 100) // anim_height
            animations = self.get_current_animations()
            if 0 <= anim_index < len(animations):
                self.current_animation_index = anim_index
    
    def get_current_character(self):
        """Obtiene el personaje actual."""
        return self.characters[self.current_character_index]
    
    def get_current_animations(self):
        """Obtiene las animaciones del personaje actual."""
        character = self.get_current_character()
        return list(self.animation_info[character].keys())
    
    def get_current_animation(self):
        """Obtiene la animación actual."""
        animations = self.get_current_animations()
        if animations:
            return animations[self.current_animation_index]
        return None
    
    def reset_animations(self):
        """Reinicia todas las animaciones."""
        for player in self.animation_players.values():
            player.set_animation('idle')
    
    def update(self, dt):
        """Actualiza el estado del test."""
        if self.auto_play:
            # Cambiar animación automáticamente cada 3 segundos
            current_time = time.time()
            if current_time - self.last_time > 3.0:
                animations = self.get_current_animations()
                if animations:
                    self.current_animation_index = (self.current_animation_index + 1) % len(animations)
                    self.last_time = current_time
        
        # Actualizar animación actual
        character = self.get_current_character()
        animation = self.get_current_animation()
        
        if character and animation:
            player = self.animation_players[character]
            if player.current_animation != animation:
                player.set_animation(animation)
    
    def render(self):
        """Renderiza la interfaz."""
        self.screen.fill(self.colors['background'])
        
        # Panel izquierdo - Lista de personajes
        self.render_character_panel()
        
        # Panel central - Animación actual
        self.render_animation_panel()
        
        # Panel derecho - Lista de animaciones
        self.render_animation_list_panel()
        
        # Información general
        self.render_info_panel()
        
        pygame.display.flip()
    
    def render_character_panel(self):
        """Renderiza el panel de personajes."""
        panel_rect = pygame.Rect(10, 10, 280, 780)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['text'], panel_rect, 2)
        
        # Título
        title = self.title_font.render("PERSONAJES", True, self.colors['text'])
        self.screen.blit(title, (20, 20))
        
        # Lista de personajes
        y = 80
        for i, character in enumerate(self.characters):
            color = self.colors['highlight'] if i == self.current_character_index else self.colors['text']
            
            # Fondo del personaje seleccionado
            if i == self.current_character_index:
                char_rect = pygame.Rect(15, y - 5, 270, 50)
                pygame.draw.rect(self.screen, (70, 70, 70), char_rect)
            
            # Nombre del personaje
            char_text = self.font.render(character.upper(), True, color)
            self.screen.blit(char_text, (20, y))
            
            # Información del personaje
            if character in self.animation_info:
                anim_count = len(self.animation_info[character])
                total_frames = sum(info['frame_count'] for info in self.animation_info[character].values())
                info_text = self.small_font.render(f"{anim_count} anims, {total_frames} frames", True, self.colors['text_secondary'])
                self.screen.blit(info_text, (20, y + 25))
            
            y += 60
    
    def render_animation_panel(self):
        """Renderiza el panel central con la animación actual."""
        panel_rect = pygame.Rect(300, 10, 590, 780)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['text'], panel_rect, 2)
        
        character = self.get_current_character()
        animation = self.get_current_animation()
        
        if not character or not animation:
            return
        
        # Título
        title = self.title_font.render(f"{character.upper()} - {animation.upper()}", True, self.colors['text'])
        self.screen.blit(title, (320, 20))
        
        # Animación actual
        player = self.animation_players[character]
        current_frame = player.get_current_frame()
        
        if current_frame:
            # Centrar la animación
            frame_rect = current_frame.get_rect()
            frame_rect.center = (595, 400)
            self.screen.blit(current_frame, frame_rect)
            
            # Información de la animación
            anim_info = self.animation_info[character][animation]
            info_y = 600
            
            info_lines = [
                f"Frames: {anim_info['frame_count']}",
                f"FPS: {anim_info['fps']}",
                f"Frame actual: {player.current_frame_index + 1}/{anim_info['frame_count']}",
                f"Tiempo: {time.time() - player.animation_start_time:.1f}s"
            ]
            
            for i, line in enumerate(info_lines):
                text = self.font.render(line, True, self.colors['text'])
                self.screen.blit(text, (320, info_y + i * 30))
    
    def render_animation_list_panel(self):
        """Renderiza el panel de lista de animaciones."""
        panel_rect = pygame.Rect(900, 10, 290, 780)
        pygame.draw.rect(self.screen, self.colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.colors['text'], panel_rect, 2)
        
        # Título
        title = self.title_font.render("ANIMACIONES", True, self.colors['text'])
        self.screen.blit(title, (910, 20))
        
        character = self.get_current_character()
        if not character or character not in self.animation_info:
            return
        
        # Lista de animaciones
        y = 100
        animations = self.get_current_animations()
        
        for i, anim_name in enumerate(animations):
            color = self.colors['highlight'] if i == self.current_animation_index else self.colors['text']
            
            # Fondo de la animación seleccionada
            if i == self.current_animation_index:
                anim_rect = pygame.Rect(905, y - 5, 280, 35)
                pygame.draw.rect(self.screen, (70, 70, 70), anim_rect)
            
            # Nombre de la animación
            anim_text = self.font.render(anim_name.upper(), True, color)
            self.screen.blit(anim_text, (910, y))
            
            # Información de la animación
            anim_info = self.animation_info[character][anim_name]
            info_text = self.small_font.render(f"{anim_info['frame_count']} frames, {anim_info['fps']} FPS", True, self.colors['text_secondary'])
            self.screen.blit(info_text, (910, y + 20))
            
            y += 40
    
    def render_info_panel(self):
        """Renderiza el panel de información general."""
        if not self.show_info:
            return
        
        # Panel de información en la parte inferior
        info_rect = pygame.Rect(10, 800 - 120, 1180, 110)
        pygame.draw.rect(self.screen, (20, 20, 20), info_rect)
        pygame.draw.rect(self.screen, self.colors['text'], info_rect, 1)
        
        # Controles
        controls = [
            "CONTROLES:",
            "Flechas ←→: Cambiar personaje",
            "Flechas ↑↓: Cambiar animación",
            "Espacio: Auto-play on/off",
            "R: Reiniciar animaciones",
            "I: Mostrar/ocultar información",
            "ESC: Salir"
        ]
        
        y = 810 - 110
        for i, control in enumerate(controls):
            color = self.colors['highlight'] if i == 0 else self.colors['text_secondary']
            text = self.small_font.render(control, True, color)
            self.screen.blit(text, (20, y + i * 15))
        
        # Estado actual
        status_text = f"Auto-play: {'ON' if self.auto_play else 'OFF'}"
        status_color = self.colors['success'] if self.auto_play else self.colors['warning']
        status_surface = self.small_font.render(status_text, True, status_color)
        self.screen.blit(status_surface, (1000, 810 - 110))
    
    def run(self):
        """Ejecuta el test."""
        print("=== INICIANDO TEST COMPLETO DE ANIMACIONES ===")
        print("Controles:")
        print("  Flechas ←→: Cambiar personaje")
        print("  Flechas ↑↓: Cambiar animación")
        print("  Espacio: Auto-play on/off")
        print("  R: Reiniciar animaciones")
        print("  I: Mostrar/ocultar información")
        print("  ESC: Salir")
        print()
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            running = self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        print("=== TEST COMPLETADO ===")

def main():
    """Función principal."""
    tester = CompleteAnimationTester()
    tester.run()

if __name__ == "__main__":
    main() 