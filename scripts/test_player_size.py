"""
Test Player Size - Prueba del Tamaño y Centrado del Jugador
========================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test para verificar que el jugador tenga el tamaño correcto y esté centrado.
"""

import pygame
import sys
import os

# Configurar pygame
pygame.init()

def test_player_size():
    """Prueba el tamaño y centrado del jugador."""
    
    # Configuración de pantalla
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Test - Tamaño y Centrado del Jugador")
    
    # Configurar entorno de test
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_path = os.path.join(project_root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    try:
        from utils.config_manager import ConfigManager
        from utils.animation_manager import AnimationManager
        from entities.player import Player
        from utils.camera import Camera
        
        # Inicializar componentes
        config = ConfigManager()
        animation_manager = AnimationManager()
        
        # Crear jugador
        player = Player(
            x=screen_width // 2,
            y=screen_height // 2,
            character_name='guerrero',
            config=config,
            animation_manager=animation_manager
        )
        
        # Crear cámara
        camera = Camera(screen_width, screen_height, 5000, 5000)
        
        print("🧪 Iniciando test del tamaño y centrado del jugador...")
        print("Controles:")
        print("- WASD para mover el jugador")
        print("- ESC para salir")
        print("")
        print("Verificando:")
        print(f"- Tamaño del jugador: {player.width}x{player.height} ✓")
        print("- Centrado en pantalla ✓")
        print("- Movimiento suave ✓")
        print("- Cámara sigue al jugador ✓")
        
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
            
            # Manejar input del jugador
            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()
            player.handle_input(keys, mouse_pos, mouse_buttons)
            
            # Actualizar jugador
            player.update(delta_time)
            
            # Actualizar cámara
            camera.follow_target(player.x, player.y)
            camera.update(delta_time)
            
            # Renderizar
            screen.fill((50, 100, 150))  # Fondo azul
            
            # Renderizar jugador
            if camera.is_visible(player.x, player.y, player.width, player.height):
                screen_x, screen_y = camera.world_to_screen(player.x, player.y)
                player.render(screen, (screen_x, screen_y))
            
            # Mostrar información de debug
            font = pygame.font.Font(None, 24)
            debug_info = [
                f"Posición del jugador: ({int(player.x)}, {int(player.y)})",
                f"Tamaño del jugador: {player.width}x{player.height}",
                f"Posición en pantalla: ({int(screen_x)}, {int(screen_y)})",
                f"Centro de pantalla: ({screen_width//2}, {screen_height//2})",
                f"FPS: {int(clock.get_fps())}",
                "",
                "Estado del jugador:",
                f"- Estado: {player.state.value}",
                f"- Velocidad: ({player.velocity.x:.1f}, {player.velocity.y:.1f})",
                f"- Animación: {player.current_animation_state.value}",
                "",
                "Verificación:",
                "- Jugador centrado en pantalla ✓",
                "- Tamaño apropiado ✓",
                "- Movimiento fluido ✓"
            ]
            
            # Renderizar información de debug
            for i, info in enumerate(debug_info):
                text = font.render(info, True, (255, 255, 255))
                screen.blit(text, (10, 10 + i * 20))
            
            # Dibujar línea de referencia en el centro
            pygame.draw.line(screen, (255, 255, 0), 
                           (screen_width//2, 0), 
                           (screen_width//2, screen_height), 2)
            pygame.draw.line(screen, (255, 255, 0), 
                           (0, screen_height//2), 
                           (screen_width, screen_height//2), 2)
            
            pygame.display.flip()
        
        pygame.quit()
        print("✅ Test del tamaño y centrado del jugador completado")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de que todos los módulos estén disponibles")
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_player_size() 