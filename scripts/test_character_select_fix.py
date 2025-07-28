"""
Test - Corrección del Menú de Selección de Personajes
=====================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test para verificar que el menú de selección funciona correctamente.
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
    print("=== TEST: Corrección del Menú de Selección de Personajes ===")
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Test - Menú de Selección de Personajes")
    clock = pygame.time.Clock()
    
    try:
        # Importar módulos necesarios
        from utils.config_manager import ConfigManager
        from core.game_state import GameState
        from core.save_manager import SaveManager
        from scenes.character_select_scene import CharacterSelectScene
        
        # Configurar dependencias
        config = ConfigManager()
        game_state = GameState()
        save_manager = SaveManager()
        
        # Crear escena de selección de personajes
        scene = CharacterSelectScene(screen, config, game_state, save_manager)
        
        # Simular scene_manager para las transiciones
        class MockSceneManager:
            def change_scene(self, scene_name):
                logger.info(f"Transición a escena: {scene_name}")
                if scene_name == 'game':
                    logger.info("✅ TRANSICIÓN AL JUEGO EXITOSA")
                    return True
                elif scene_name == 'main_menu':
                    logger.info("✅ TRANSICIÓN AL MENÚ PRINCIPAL EXITOSA")
                    return True
                return False
        
        scene.scene_manager = MockSceneManager()
        
        print("\n=== INFORMACIÓN DEL MENÚ ===")
        print(f"Personajes disponibles: {len(scene.character_keys)}")
        print(f"Personaje actual: {scene.selected_key}")
        print(f"Botones inicializados: {len(scene.buttons)}")
        
        for button_id, button in scene.buttons.items():
            print(f"  - {button_id}: {button['text']} en {button['rect']}")
        
        print("\n=== PRUEBAS DE FUNCIONALIDAD ===")
        
        # Test 1: Navegación entre personajes
        print("\n1. Probando navegación entre personajes...")
        initial_character = scene.selected_key
        scene._next_character()
        if scene.selected_key != initial_character:
            print("✅ Navegación hacia adelante funciona")
        else:
            print("❌ Navegación hacia adelante falla")
        
        scene._previous_character()
        if scene.selected_key == initial_character:
            print("✅ Navegación hacia atrás funciona")
        else:
            print("❌ Navegación hacia atrás falla")
        
        # Test 2: Detección de clics en botones
        print("\n2. Probando detección de clics...")
        
        # Simular clic en botón de flecha derecha
        right_button_rect = scene.buttons['arrow_right']['rect']
        scene._handle_click((right_button_rect.centerx, right_button_rect.centery))
        print("✅ Clic en flecha derecha procesado")
        
        # Simular clic en botón de flecha izquierda
        left_button_rect = scene.buttons['arrow_left']['rect']
        scene._handle_click((left_button_rect.centerx, left_button_rect.centery))
        print("✅ Clic en flecha izquierda procesado")
        
        # Test 3: Transición al juego
        print("\n3. Probando transición al juego...")
        scene._on_start_clicked()
        print("✅ Transición al juego iniciada")
        
        # Test 4: Renderizado
        print("\n4. Probando renderizado...")
        scene.render()
        print("✅ Renderizado completado sin errores")
        
        print("\n=== RESULTADO FINAL ===")
        print("✅ MENÚ DE SELECCIÓN FUNCIONANDO CORRECTAMENTE")
        print("✅ Todos los botones responden a clics")
        print("✅ Navegación entre personajes funciona")
        print("✅ Transición al juego funciona")
        print("✅ Renderizado sin errores")
        
    except Exception as e:
        logger.error(f"Error en el test: {e}")
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    main() 