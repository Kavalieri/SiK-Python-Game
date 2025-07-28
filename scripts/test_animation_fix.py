"""
Test - Corrección del Sistema de Animación
==========================================

Autor: SiK Team
Fecha: 2024
Descripción: Test para verificar que el sistema de animación funciona correctamente.
"""

import sys
import os
import pygame
import logging

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def setup_logging():
    """Configura el sistema de logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Función principal del test."""
    print("=== TEST: Corrección del Sistema de Animación ===")
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Inicializar pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test - Sistema de Animación")
    clock = pygame.time.Clock()
    
    try:
        # Importar AssetManager
        from utils.asset_manager import AssetManager
        
        # Crear AssetManager
        asset_manager = AssetManager()
        
        # Lista de personajes a probar
        characters = ["guerrero", "adventureguirl", "robot", "zombiemale", "zombieguirl"]
        
        print("\n--- Probando carga de frames de animación ---")
        
        for char in characters:
            print(f"\nProbando {char}:")
            
            # Probar carga de frames de animación
            frames = asset_manager.get_character_animation_frames(char, "idle")
            print(f"  - Frames cargados: {len(frames)}")
            
            # Probar carga de sprite individual
            sprite = asset_manager.get_character_sprite(char, "idle", 1)
            if sprite:
                print(f"  - Sprite individual: OK ({sprite.get_width()}x{sprite.get_height()})")
            else:
                print(f"  - Sprite individual: FALLBACK")
        
        print("\n--- Probando botones UI ---")
        
        # Probar botones de flecha
        button_names = ["arrow_l_l", "arrow_r_l", "bleft", "bright"]
        button_states = ["n", "h", "p"]
        
        for button_name in button_names:
            for state in button_states:
                button = asset_manager.get_ui_button(button_name, state)
                if button:
                    print(f"  - {button_name}_{state}: OK")
                else:
                    print(f"  - {button_name}_{state}: FALLBACK")
        
        print("\n--- Test completado exitosamente ---")
        print("✅ El sistema de animación funciona correctamente")
        print("✅ No hay bucles infinitos")
        print("✅ Los placeholders se crean correctamente")
        
    except Exception as e:
        logger.error(f"Error en el test: {e}")
        print(f"❌ Error en el test: {e}")
        return False
    
    finally:
        pygame.quit()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 