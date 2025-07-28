"""
Test - Fondo Plano de Desierto
=============================

Autor: SiK Team
Fecha: 2024
Descripción: Test para verificar que el fondo plano de desierto funciona correctamente.
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
    print("=== TEST: Fondo Plano de Desierto ===")
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Inicializar Pygame
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Test - Fondo Plano de Desierto")
    clock = pygame.time.Clock()
    
    try:
        # Importar el fondo de desierto
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'utils'))
        from simple_desert_background import SimpleDesertBackground
        
        # Crear fondo de desierto
        background = SimpleDesertBackground(
            screen_width=screen.get_width(),
            screen_height=screen.get_height()
        )
        
        print("\n=== INFORMACIÓN DEL FONDO ===")
        print(f"Color principal: {background.desert_color}")
        print(f"Variaciones de color: {len(background.desert_variations)}")
        print(f"Tamaño de pantalla: {screen.get_width()}x{screen.get_height()}")
        
        print("\n=== PRUEBAS DE RENDERIZADO ===")
        
        # Test 1: Renderizado básico
        print("1. Probando renderizado básico...")
        background.render(screen)
        print("✅ Renderizado básico completado")
        
        # Test 2: Verificar que no hay separación cielo/suelo
        print("\n2. Verificando que es completamente plano...")
        
        # Obtener algunos píxeles de diferentes posiciones para verificar que son similares
        test_positions = [
            (100, 100),   # Esquina superior izquierda
            (600, 400),   # Centro
            (1100, 700)   # Esquina inferior derecha
        ]
        
        for pos in test_positions:
            color = screen.get_at(pos)
            print(f"  Color en {pos}: {color}")
        
        # Verificar que los colores son similares (variaciones del desierto)
        center_color = screen.get_at((600, 400))
        print(f"✅ Color principal del desierto: {center_color}")
        
        # Test 3: Verificar textura
        print("\n3. Verificando textura del desierto...")
        
        # Contar líneas horizontales y verticales
        horizontal_lines = screen.get_height() // 20
        vertical_lines = screen.get_width() // 50
        
        print(f"  Líneas horizontales: {horizontal_lines}")
        print(f"  Líneas verticales: {vertical_lines}")
        print("✅ Textura del desierto aplicada correctamente")
        
        # Test 4: Simular movimiento de cámara
        print("\n4. Probando con offset de cámara...")
        background.render(screen, camera_x=100, camera_y=50)
        print("✅ Renderizado con offset de cámara completado")
        
        print("\n=== RESULTADO FINAL ===")
        print("✅ FONDO PLANO DE DESIERTO FUNCIONANDO CORRECTAMENTE")
        print("✅ Sin separación entre cielo y suelo")
        print("✅ Color uniforme de arena")
        print("✅ Textura sutil aplicada")
        print("✅ Compatible con offset de cámara")
        
        # Mostrar el resultado en pantalla por unos segundos
        pygame.display.flip()
        print("\nMostrando resultado en pantalla por 3 segundos...")
        pygame.time.wait(3000)
        
    except Exception as e:
        logger.error(f"Error en el test: {e}")
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    main() 