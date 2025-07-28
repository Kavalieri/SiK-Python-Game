"""
Análisis de Fotogramas de Animación
===================================

Autor: SiK Team
Fecha: 2024
Descripción: Analiza cuántos fotogramas reales tenemos para cada animación.
"""

import sys
import os
import glob
from typing import Dict, List, Tuple

def analyze_character_frames(character_path: str) -> Dict[str, List[str]]:
    """Analiza los fotogramas disponibles para un personaje."""
    animations = {}
    
    # Buscar archivos PNG en el directorio del personaje
    png_files = glob.glob(os.path.join(character_path, "*.png"))
    
    # Agrupar por tipo de animación
    for file_path in png_files:
        filename = os.path.basename(file_path)
        # Extraer el tipo de animación del nombre del archivo
        # Formato: Idle_1_.png, Run_1_.png, etc.
        if '_' in filename:
            parts = filename.split('_')
            if len(parts) >= 2:
                animation_type = parts[0]  # Idle, Run, Attack, etc.
                if animation_type not in animations:
                    animations[animation_type] = []
                animations[animation_type].append(filename)
    
    # Ordenar los archivos por número de frame
    for animation_type in animations:
        animations[animation_type].sort(key=lambda x: int(x.split('_')[1]) if x.split('_')[1].isdigit() else 0)
    
    return animations

def main():
    """Función principal de análisis."""
    print("=== ANÁLISIS DE FOTOGRAMAS DE ANIMACIÓN ===\n")
    
    characters_dir = "assets/characters/used"
    characters = ["guerrero", "adventureguirl", "robot", "zombiemale", "zombieguirl"]
    
    total_analysis = {}
    
    for character in characters:
        character_path = os.path.join(characters_dir, character)
        if os.path.exists(character_path):
            print(f"\n--- {character.upper()} ---")
            animations = analyze_character_frames(character_path)
            total_analysis[character] = animations
            
            for animation_type, files in animations.items():
                print(f"  {animation_type}: {len(files)} fotogramas")
                print(f"    Archivos: {', '.join(files[:5])}{'...' if len(files) > 5 else ''}")
        else:
            print(f"\n--- {character.upper()} --- (No encontrado)")
    
    # Resumen general
    print("\n=== RESUMEN GENERAL ===")
    for character, animations in total_analysis.items():
        print(f"\n{character}:")
        for animation_type, files in animations.items():
            print(f"  {animation_type}: {len(files)} fotogramas")
    
    # Recomendaciones
    print("\n=== RECOMENDACIONES ===")
    print("1. Ajustar FPS según el número de fotogramas disponibles")
    print("2. Implementar interpolación de frames para animaciones suaves")
    print("3. Usar diferentes velocidades de animación según el tipo")
    
    return total_analysis

if __name__ == "__main__":
    main() 