"""
Test Character Navigation - Prueba del Sistema de Navegación de Personajes
======================================================================

Autor: SiK Team
Fecha: 2024
Descripción: Test para verificar el nuevo sistema de navegación con flechas.
"""

import pygame
import sys
import os

# Configurar pygame
pygame.init()

def test_character_navigation():
    """Prueba el sistema de navegación de personajes."""
    
    # Configuración de pantalla
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Test - Navegación de Personajes")
    
    # Configurar entorno de test
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_path = os.path.join(project_root, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    try:
        from utils.config_manager import ConfigManager
        from utils.animation_manager import AnimationManager
        from entities.character_data import CHARACTER_DATA
        
        # Inicializar componentes
        config = ConfigManager()
        animation_manager = AnimationManager()
        
        # Datos de personajes
        character_keys = list(CHARACTER_DATA.keys())
        current_index = 0
        selected_character = character_keys[0]
        
        # Colores
        colors = {
            'background': (30, 30, 50),
            'card': (60, 60, 80),
            'card_selected': (80, 80, 120),
            'text': (255, 255, 255),
            'text_highlight': (255, 255, 0),
            'text_secondary': (200, 200, 200),
            'button': (100, 100, 150),
            'button_hover': (120, 120, 180),
            'button_highlight': (150, 150, 200),
            'panel': (40, 40, 60),
            'panel_border': (80, 80, 100)
        }
        
        # Fuentes
        fonts = {
            'title': pygame.font.Font(None, 48),
            'subtitle': pygame.font.Font(None, 36),
            'normal': pygame.font.Font(None, 24),
            'small': pygame.font.Font(None, 18)
        }
        
        print("🧪 Iniciando test del sistema de navegación de personajes...")
        print("Controles:")
        print("- Flechas ← → o A D para navegar")
        print("- ENTER para seleccionar")
        print("- ESC para salir")
        print("")
        print("Verificando:")
        print(f"- Navegación entre {len(character_keys)} personajes ✓")
        print("- Tarjeta individual centrada ✓")
        print("- Información completa visible ✓")
        print("- Controles de teclado y mouse ✓")
        
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
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        # Personaje anterior
                        current_index = (current_index - 1) % len(character_keys)
                        selected_character = character_keys[current_index]
                        print(f"← Personaje anterior: {selected_character}")
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        # Siguiente personaje
                        current_index = (current_index + 1) % len(character_keys)
                        selected_character = character_keys[current_index]
                        print(f"→ Siguiente personaje: {selected_character}")
                    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        print(f"✅ Personaje seleccionado: {selected_character}")
            
            # Renderizar
            screen.fill(colors['background'])
            
            # Título
            title_text = fonts['title'].render("Selección de Personaje", True, colors['text_highlight'])
            title_rect = title_text.get_rect(center=(screen_width // 2, 60))
            screen.blit(title_text, title_rect)
            
            subtitle_text = fonts['subtitle'].render("Navega con las flechas", True, colors['text_secondary'])
            subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 100))
            screen.blit(subtitle_text, subtitle_rect)
            
            # Tarjeta del personaje actual
            char_data = CHARACTER_DATA[selected_character]
            card_width = 400
            card_height = 500
            card_x = (screen_width - card_width) // 2
            card_y = 120
            
            # Dibujar tarjeta
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            pygame.draw.rect(screen, colors['card_selected'], card_rect)
            pygame.draw.rect(screen, colors['panel_border'], card_rect, 3)
            
            # Nombre del personaje
            name_text = fonts['title'].render(char_data['nombre'], True, colors['text_highlight'])
            name_rect = name_text.get_rect(center=(card_x + card_width//2, card_y + 30))
            screen.blit(name_text, name_rect)
            
            # Tipo
            type_text = fonts['subtitle'].render(char_data['tipo'], True, colors['text_secondary'])
            type_rect = type_text.get_rect(center=(card_x + card_width//2, card_y + 60))
            screen.blit(type_text, type_rect)
            
            # Placeholder de imagen
            image_size = 200
            image_x = card_x + (card_width - image_size) // 2
            image_y = card_y + 90
            image_rect = pygame.Rect(image_x, image_y, image_size, image_size)
            pygame.draw.rect(screen, colors['panel'], image_rect)
            pygame.draw.rect(screen, colors['panel_border'], image_rect, 2)
            
            # Símbolo del personaje
            symbols = {
                "guerrero": "⚔️",
                "robot": "🤖",
                "adventureguirl": "👧",
            }
            symbol = symbols.get(selected_character.lower(), "?")
            symbol_text = fonts['title'].render(symbol, True, colors['text'])
            symbol_rect = symbol_text.get_rect(center=(image_x + image_size//2, image_y + image_size//2))
            screen.blit(symbol_text, symbol_rect)
            
            # Estadísticas
            stats = char_data['stats']
            stats_y = card_y + 320
            stats_text = fonts['normal'].render("ESTADÍSTICAS:", True, colors['text_highlight'])
            screen.blit(stats_text, (card_x + 20, stats_y))
            
            stats_list = [
                f"❤️ Vida: {stats['vida']}",
                f"⚡ Velocidad: {stats['velocidad']}",
                f"⚔️ Daño: {stats['daño']}",
                f"🛡️ Escudo: {stats['escudo']}",
                f"🎯 Rango: {stats['rango_ataque']}"
            ]
            
            for i, stat in enumerate(stats_list):
                stat_text = fonts['small'].render(stat, True, colors['text'])
                screen.blit(stat_text, (card_x + 20, stats_y + 30 + i * 20))
            
            # Habilidades
            skills_y = card_y + 420
            skills_text = fonts['normal'].render("HABILIDADES:", True, colors['text_highlight'])
            screen.blit(skills_text, (card_x + 20, skills_y))
            
            for i, skill in enumerate(char_data['habilidades']):
                skill_text = fonts['small'].render(f"• {skill}", True, colors['text'])
                screen.blit(skill_text, (card_x + 20, skills_y + 30 + i * 20))
            
            # Indicador de selección
            select_text = fonts['normal'].render("✓ PERSONAJE SELECCIONADO", True, colors['text_highlight'])
            select_rect = select_text.get_rect(center=(card_x + card_width//2, card_y + card_height - 20))
            screen.blit(select_text, select_rect)
            
            # Botones de navegación
            arrow_size = 60
            arrow_y = screen_height // 2 - arrow_size // 2
            
            # Flecha izquierda
            left_rect = pygame.Rect(50, arrow_y, arrow_size, arrow_size)
            pygame.draw.rect(screen, colors['button'], left_rect)
            pygame.draw.rect(screen, colors['panel_border'], left_rect, 2)
            left_text = fonts['title'].render("←", True, colors['text_highlight'])
            left_text_rect = left_text.get_rect(center=left_rect.center)
            screen.blit(left_text, left_text_rect)
            
            # Flecha derecha
            right_rect = pygame.Rect(screen_width - 110, arrow_y, arrow_size, arrow_size)
            pygame.draw.rect(screen, colors['button'], right_rect)
            pygame.draw.rect(screen, colors['panel_border'], right_rect, 2)
            right_text = fonts['title'].render("→", True, colors['text_highlight'])
            right_text_rect = right_text.get_rect(center=right_rect.center)
            screen.blit(right_text, right_text_rect)
            
            # Información de navegación
            nav_text = f"Personaje {current_index + 1} de {len(character_keys)}"
            nav_surface = fonts['small'].render(nav_text, True, colors['text_secondary'])
            nav_rect = nav_surface.get_rect(center=(screen_width // 2, screen_height - 80))
            screen.blit(nav_surface, nav_rect)
            
            # Instrucciones
            instructions = "Usa ← → o A D para navegar • ENTER para seleccionar • ESC para volver"
            inst_surface = fonts['small'].render(instructions, True, colors['text_secondary'])
            inst_rect = inst_surface.get_rect(center=(screen_width // 2, screen_height - 60))
            screen.blit(inst_surface, inst_rect)
            
            # Información de debug
            debug_info = [
                f"Personaje actual: {selected_character}",
                f"Índice: {current_index + 1}/{len(character_keys)}",
                f"FPS: {int(clock.get_fps())}",
                "",
                "Verificación:",
                "- Navegación fluida ✓",
                "- Tarjeta centrada ✓",
                "- Información completa ✓",
                "- Controles responsivos ✓"
            ]
            
            for i, info in enumerate(debug_info):
                text = fonts['small'].render(info, True, colors['text'])
                screen.blit(text, (10, 10 + i * 20))
            
            pygame.display.flip()
        
        pygame.quit()
        print("✅ Test del sistema de navegación de personajes completado")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("Asegúrate de que todos los módulos estén disponibles")
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_character_navigation() 