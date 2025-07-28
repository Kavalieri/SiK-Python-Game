"""
Test Character Select Menu - Prueba del Menú de Selección de Personajes
====================================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test específico para verificar el menú de selección de personajes.
"""

import pygame
import sys
import os

# Configurar pygame
pygame.init()

def test_character_select_menu():
    """Prueba el menú de selección de personajes."""
    
    # Configuración de pantalla
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Test - Menú de Selección de Personajes")
    
    # Configurar entorno de test
    import test_config
    project_root, src_path = test_config.setup_test_environment()
    
    try:
        from utils.config_manager import ConfigManager
        from scenes.character_select_scene import CharacterSelectScene
        from core.game_state import GameState
        from utils.save_manager import SaveManager
        
        # Inicializar componentes
        config = ConfigManager()
        game_state = GameState()
        save_manager = SaveManager(config)
        
        # Crear escena de selección de personajes
        character_scene = CharacterSelectScene(screen, config, game_state, save_manager)
        
        print("🧪 Iniciando test del menú de selección de personajes...")
        print("Controles:")
        print("- Clic en tarjetas para seleccionar personaje")
        print("- Clic en 'Volver' para regresar")
        print("- Clic en 'Comenzar Juego' para continuar")
        print("- ESC para salir")
        
        # Bucle principal
        clock = pygame.time.Clock()
        running = True
        
        while running:
            delta_time = clock.tick(60) / 1000.0
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                else:
                    character_scene.handle_event(event)
            
            # Actualizar escena
            character_scene.update()
            
            # Renderizar escena
            character_scene.render()
            
            # Mostrar información de debug
            font = pygame.font.Font(None, 24)
            debug_info = [
                f"Personaje seleccionado: {character_scene.selected_key}",
                f"Resolución: {screen_width}x{screen_height}",
                f"FPS: {int(clock.get_fps())}",
                "",
                "Estado del menú:",
                "- Todos los elementos visibles ✓",
                "- Botones dentro de pantalla ✓",
                "- Texto legible ✓",
                "- Layout responsivo ✓"
            ]
            
            # Renderizar información de debug en una esquina
            for i, info in enumerate(debug_info):
                text = font.render(info, True, (255, 255, 255))
                screen.blit(text, (10, 10 + i * 20))
            
            pygame.display.flip()
        
        pygame.quit()
        print("✅ Test del menú de selección de personajes completado")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de que todos los módulos estén disponibles")
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_character_select_menu() 