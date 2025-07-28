"""
Test - Todas las Animaciones de Personajes y Enemigos
==================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test completo para verificar todas las animaciones disponibles.
"""

import sys
import os
import pygame
import logging
from typing import Dict, List, Tuple

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class AnimationTester:
    """Testador completo de animaciones."""
    
    def __init__(self):
        """Inicializa el testador."""
        self.logger = logging.getLogger(__name__)
        
        # Inicializar Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 900))
        pygame.display.set_caption("Test - Todas las Animaciones")
        self.clock = pygame.time.Clock()
        
        # Importar el asset manager
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'utils'))
        from asset_manager import AssetManager
        self.asset_manager = AssetManager()
        
        # Definir todos los personajes y sus animaciones
        self.characters = {
            "guerrero": {
                "animations": ["idle", "walk", "run", "jump", "attack", "dead"],
                "color": (139, 69, 19)
            },
            "adventureguirl": {
                "animations": ["idle", "run", "jump", "melee", "shoot", "slide", "dead"],
                "color": (255, 182, 193)
            },
            "robot": {
                "animations": ["idle", "run", "jump", "melee", "shoot", "slide", "runshoot", "jumpshoot", "jumpmelee", "dead"],
                "color": (128, 128, 128)
            },
            "zombiemale": {
                "animations": ["idle", "walk", "attack", "dead"],
                "color": (34, 139, 34)
            },
            "zombieguirl": {
                "animations": ["idle", "walk", "attack", "dead"],
                "color": (218, 112, 214)
            }
        }
        
        # Estado del test
        self.current_character = 0
        self.current_animation = 0
        self.current_frame = 0
        self.animation_frames = {}
        self.test_results = {}
        
        # Cargar todas las animaciones
        self._load_all_animations()
    
    def _load_all_animations(self):
        """Carga todas las animaciones de todos los personajes."""
        print("=== CARGANDO TODAS LAS ANIMACIONES ===")
        
        for char_name, char_data in self.characters.items():
            print(f"\n--- {char_name.upper()} ---")
            char_results = {}
            
            for animation in char_data["animations"]:
                print(f"  Cargando {animation}...")
                
                try:
                    frames = self.asset_manager.get_character_animation_frames(char_name, animation)
                    char_results[animation] = {
                        "frames": frames,
                        "count": len(frames),
                        "status": "OK" if len(frames) > 0 else "ERROR"
                    }
                    
                    # Guardar frames para el test visual
                    key = f"{char_name}_{animation}"
                    self.animation_frames[key] = frames
                    
                    print(f"    ✅ {len(frames)} frames cargados")
                    
                except Exception as e:
                    char_results[animation] = {
                        "frames": [],
                        "count": 0,
                        "status": f"ERROR: {e}"
                    }
                    print(f"    ❌ Error: {e}")
            
            self.test_results[char_name] = char_results
    
    def _get_current_animation_key(self) -> str:
        """Obtiene la clave de la animación actual."""
        char_names = list(self.characters.keys())
        if self.current_character >= len(char_names):
            return None
        
        char_name = char_names[self.current_character]
        char_data = self.characters[char_name]
        animations = char_data["animations"]
        
        if self.current_animation >= len(animations):
            return None
        
        animation = animations[self.current_animation]
        return f"{char_name}_{animation}"
    
    def _render_animation(self):
        """Renderiza la animación actual."""
        self.screen.fill((50, 50, 50))
        
        animation_key = self._get_current_animation_key()
        if not animation_key or animation_key not in self.animation_frames:
            return
        
        frames = self.animation_frames[animation_key]
        if not frames:
            return
        
        # Obtener información actual
        char_names = list(self.characters.keys())
        char_name = char_names[self.current_character]
        char_data = self.characters[char_name]
        animations = char_data["animations"]
        animation = animations[self.current_animation]
        
        # Renderizar frame actual
        frame = frames[self.current_frame % len(frames)]
        
        # Centrar el sprite en la pantalla
        sprite_rect = frame.get_rect()
        sprite_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.screen.blit(frame, sprite_rect)
        
        # Renderizar información
        self._render_info(char_name, animation, len(frames))
    
    def _render_info(self, char_name: str, animation: str, frame_count: int):
        """Renderiza información sobre la animación actual."""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Título principal
        title = f"{char_name.upper()} - {animation.upper()}"
        title_surface = font.render(title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_surface, title_rect)
        
        # Información de frames
        frame_info = f"Frame {self.current_frame + 1} de {frame_count}"
        frame_surface = small_font.render(frame_info, True, (200, 200, 200))
        frame_rect = frame_surface.get_rect(center=(self.screen.get_width() // 2, 80))
        self.screen.blit(frame_surface, frame_rect)
        
        # Controles
        controls = [
            "CONTROLES:",
            "Flechas: Cambiar personaje/animación",
            "Espacio: Pausar/Reanudar",
            "R: Reiniciar frame",
            "ESC: Salir"
        ]
        
        y_offset = self.screen.get_height() - 150
        for i, control in enumerate(controls):
            color = (255, 255, 255) if i == 0 else (180, 180, 180)
            control_surface = small_font.render(control, True, color)
            control_rect = control_surface.get_rect(left=20, top=y_offset + i * 25)
            self.screen.blit(control_surface, control_rect)
        
        # Lista de personajes
        char_names = list(self.characters.keys())
        for i, name in enumerate(char_names):
            color = (255, 255, 0) if i == self.current_character else (150, 150, 150)
            char_surface = small_font.render(f"{i+1}. {name}", True, color)
            char_rect = char_surface.get_rect(left=self.screen.get_width() - 200, top=100 + i * 30)
            self.screen.blit(char_surface, char_rect)
    
    def handle_events(self) -> bool:
        """Maneja los eventos del test."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_LEFT:
                    self.current_animation = (self.current_animation - 1) % len(self.characters[list(self.characters.keys())[self.current_character]]["animations"])
                    self.current_frame = 0
                
                elif event.key == pygame.K_RIGHT:
                    char_data = self.characters[list(self.characters.keys())[self.current_character]]
                    self.current_animation = (self.current_animation + 1) % len(char_data["animations"])
                    self.current_frame = 0
                
                elif event.key == pygame.K_UP:
                    self.current_character = (self.current_character - 1) % len(self.characters)
                    self.current_animation = 0
                    self.current_frame = 0
                
                elif event.key == pygame.K_DOWN:
                    self.current_character = (self.current_character + 1) % len(self.characters)
                    self.current_animation = 0
                    self.current_frame = 0
                
                elif event.key == pygame.K_SPACE:
                    # Pausar/reanudar (implementar si es necesario)
                    pass
                
                elif event.key == pygame.K_r:
                    self.current_frame = 0
        
        return True
    
    def update(self):
        """Actualiza el estado del test."""
        # Avanzar frame automáticamente
        animation_key = self._get_current_animation_key()
        if animation_key and animation_key in self.animation_frames:
            frames = self.animation_frames[animation_key]
            if frames:
                self.current_frame = (self.current_frame + 1) % len(frames)
    
    def run(self):
        """Ejecuta el test completo."""
        print("\n=== TEST DE ANIMACIONES INICIADO ===")
        print("Usa las flechas para navegar entre personajes y animaciones")
        print("Presiona ESC para salir")
        
        running = True
        while running:
            running = self.handle_events()
            
            self.update()
            self._render_animation()
            
            pygame.display.flip()
            self.clock.tick(10)  # 10 FPS para ver mejor las animaciones
        
        self._print_final_results()
        pygame.quit()
    
    def _print_final_results(self):
        """Imprime los resultados finales del test."""
        print("\n=== RESULTADOS FINALES ===")
        
        total_animations = 0
        successful_animations = 0
        
        for char_name, char_results in self.test_results.items():
            print(f"\n--- {char_name.upper()} ---")
            
            for animation, result in char_results.items():
                total_animations += 1
                if result["status"] == "OK":
                    successful_animations += 1
                    print(f"  ✅ {animation}: {result['count']} frames")
                else:
                    print(f"  ❌ {animation}: {result['status']}")
        
        print(f"\n=== RESUMEN ===")
        print(f"Animaciones exitosas: {successful_animations}/{total_animations}")
        print(f"Porcentaje de éxito: {(successful_animations/total_animations)*100:.1f}%")

def main():
    """Función principal del test."""
    setup_logging()
    
    try:
        tester = AnimationTester()
        tester.run()
    except Exception as e:
        print(f"❌ ERROR EN EL TEST: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 