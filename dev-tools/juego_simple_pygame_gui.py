#!/usr/bin/env python3
"""
Juego simple para probar pygame-gui sin conflictos
"""

import pygame
import pygame_gui
import sys

def main():
    pygame.init()
    
    # Configurar pantalla
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("SiK Game - pygame-gui Test")
    
    # UI Manager
    ui_manager = pygame_gui.UIManager((800, 600), theme_path="assets/ui/theme.json")
    
    # Botones de prueba
    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(300, 200, 200, 50),
        text="Jugar",
        manager=ui_manager
    )
    
    options_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(300, 270, 200, 50),
        text="Opciones",
        manager=ui_manager
    )
    
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(300, 340, 200, 50),
        text="Salir",
        manager=ui_manager
    )
    
    # Título
    title_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(250, 100, 300, 60),
        text="SiK PYTHON GAME",
        manager=ui_manager
    )
    
    clock = pygame.time.Clock()
    running = True
    
    print("Juego iniciado con pygame-gui")
    print("Presiona los botones o ESC para salir")
    
    while running:
        time_delta = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == play_button:
                    print("¡Botón Jugar presionado!")
                elif event.ui_element == options_button:
                    print("¡Botón Opciones presionado!")
                elif event.ui_element == exit_button:
                    print("¡Botón Salir presionado!")
                    running = False
            
            ui_manager.process_events(event)
        
        ui_manager.update(time_delta)
        
        # Renderizar
        screen.fill((20, 20, 40))  # Fondo azul oscuro
        ui_manager.draw_ui(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    print("Juego terminado")

if __name__ == "__main__":
    main()
