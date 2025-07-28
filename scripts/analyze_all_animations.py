"""
Análisis Completo de Animaciones
===============================

Autor: SiK Team
Fecha: 2024
Descripción: Analiza todas las animaciones disponibles para cada personaje y genera un reporte completo.
"""

import os
import glob
from pathlib import Path
from typing import Dict, List, Tuple

class AnimationAnalyzer:
    """Analizador completo de animaciones."""
    
    def __init__(self):
        """Inicializa el analizador."""
        self.characters_dir = Path("assets/characters/used")
        self.animation_types = [
            'Idle', 'Run', 'Walk', 'Attack', 'Dead', 'Shoot', 
            'Jump', 'Melee', 'Slide', 'JumpMelee', 'JumpShoot', 'RunShoot'
        ]
        
    def analyze_character_animations(self, character_name: str) -> Dict[str, List[str]]:
        """
        Analiza las animaciones disponibles para un personaje específico.
        
        Args:
            character_name: Nombre del personaje
            
        Returns:
            Diccionario con las animaciones y sus frames
        """
        character_dir = self.characters_dir / character_name
        
        if not character_dir.exists():
            print(f"Error: No se encontró el directorio para {character_name}")
            return {}
        
        animations = {}
        
        # Buscar archivos PNG en el directorio del personaje
        png_files = list(character_dir.glob("*.png"))
        
        # Agrupar por tipo de animación
        for png_file in png_files:
            filename = png_file.name
            
            # Extraer el tipo de animación del nombre del archivo
            # Formato: Idle_1_.png, Run_2_.png, etc.
            if '_' in filename and filename.endswith('.png'):
                anim_type = filename.split('_')[0]
                
                if anim_type not in animations:
                    animations[anim_type] = []
                
                animations[anim_type].append(filename)
        
        # Ordenar frames por número
        for anim_type in animations:
            animations[anim_type].sort(key=lambda x: self._extract_frame_number(x))
        
        return animations
    
    def _extract_frame_number(self, filename: str) -> int:
        """Extrae el número de frame de un nombre de archivo."""
        try:
            # Formato: Idle_1_.png -> extraer 1
            parts = filename.split('_')
            if len(parts) >= 2:
                return int(parts[1])
        except (ValueError, IndexError):
            pass
        return 0
    
    def analyze_all_characters(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Analiza las animaciones de todos los personajes.
        
        Returns:
            Diccionario con todos los personajes y sus animaciones
        """
        all_animations = {}
        
        # Obtener todos los directorios de personajes
        character_dirs = [d for d in self.characters_dir.iterdir() if d.is_dir()]
        
        for character_dir in character_dirs:
            character_name = character_dir.name
            print(f"\nAnalizando {character_name}...")
            
            animations = self.analyze_character_animations(character_name)
            all_animations[character_name] = animations
            
            # Mostrar resumen
            total_frames = sum(len(frames) for frames in animations.values())
            print(f"  Animaciones encontradas: {len(animations)}")
            print(f"  Total de frames: {total_frames}")
            
            for anim_type, frames in animations.items():
                print(f"    {anim_type}: {len(frames)} frames")
        
        return all_animations
    
    def generate_animation_config(self, all_animations: Dict[str, Dict[str, List[str]]]) -> Dict:
        """
        Genera una configuración de animaciones para el sistema.
        
        Args:
            all_animations: Diccionario con todas las animaciones
            
        Returns:
            Configuración de animaciones
        """
        config = {
            'characters': {},
            'animation_types': {},
            'summary': {
                'total_characters': len(all_animations),
                'total_animations': 0,
                'total_frames': 0
            }
        }
        
        # Procesar cada personaje
        for character_name, animations in all_animations.items():
            char_config = {
                'animations': {},
                'total_frames': 0,
                'animation_count': len(animations)
            }
            
            # Procesar cada animación del personaje
            for anim_type, frames in animations.items():
                anim_config = {
                    'frame_count': len(frames),
                    'frames': frames,
                    'fps': self._calculate_optimal_fps(len(frames), anim_type)
                }
                
                char_config['animations'][anim_type] = anim_config
                char_config['total_frames'] += len(frames)
                
                # Actualizar estadísticas globales
                config['summary']['total_animations'] += 1
                config['summary']['total_frames'] += len(frames)
            
            config['characters'][character_name] = char_config
        
        return config
    
    def _calculate_optimal_fps(self, frame_count: int, anim_type: str) -> int:
        """
        Calcula el FPS óptimo para una animación.
        
        Args:
            frame_count: Número de frames
            anim_type: Tipo de animación
            
        Returns:
            FPS óptimo
        """
        # FPS base por tipo de animación
        base_fps = {
            'Idle': 12,
            'Walk': 15,
            'Run': 18,
            'Attack': 20,
            'Dead': 10,
            'Shoot': 16,
            'Jump': 14,
            'Melee': 18,
            'Slide': 16,
            'JumpMelee': 16,
            'JumpShoot': 16,
            'RunShoot': 18
        }
        
        fps = base_fps.get(anim_type, 15)
        
        # Ajustar según el número de frames
        if frame_count <= 4:
            return max(8, fps // 2)
        elif frame_count <= 8:
            return max(10, int(fps * 0.8))
        elif frame_count <= 12:
            return fps
        else:
            return min(30, int(fps * 1.2))
    
    def save_config(self, config: Dict, filename: str = "animation_config.json"):
        """Guarda la configuración en un archivo JSON."""
        import json
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\nConfiguración guardada en: {filename}")
    
    def print_detailed_report(self, all_animations: Dict[str, Dict[str, List[str]]]):
        """Imprime un reporte detallado de todas las animaciones."""
        
        print("\n" + "="*80)
        print("REPORTE DETALLADO DE ANIMACIONES")
        print("="*80)
        
        for character_name, animations in all_animations.items():
            print(f"\n{character_name.upper()}")
            print("-" * 40)
            
            total_frames = sum(len(frames) for frames in animations.values())
            print(f"Total de animaciones: {len(animations)}")
            print(f"Total de frames: {total_frames}")
            print()
            
            for anim_type, frames in sorted(animations.items()):
                fps = self._calculate_optimal_fps(len(frames), anim_type)
                print(f"  {anim_type}: {len(frames)} frames a {fps} FPS")
                
                # Mostrar algunos nombres de archivo como ejemplo
                if frames:
                    print(f"    Ejemplos: {frames[0]}, {frames[1] if len(frames) > 1 else ''}, {frames[-1] if len(frames) > 2 else ''}")
                print()
        
        # Resumen final
        total_characters = len(all_animations)
        total_animations = sum(len(anims) for anims in all_animations.values())
        total_frames = sum(sum(len(frames) for frames in anims.values()) for anims in all_animations.values())
        
        print("="*80)
        print("RESUMEN FINAL")
        print("="*80)
        print(f"Personajes analizados: {total_characters}")
        print(f"Total de animaciones: {total_animations}")
        print(f"Total de frames: {total_frames}")
        print(f"Promedio de animaciones por personaje: {total_animations / total_characters:.1f}")
        print(f"Promedio de frames por animación: {total_frames / total_animations:.1f}")

def main():
    """Función principal."""
    print("=== ANÁLISIS COMPLETO DE ANIMACIONES ===")
    
    analyzer = AnimationAnalyzer()
    
    # Analizar todas las animaciones
    all_animations = analyzer.analyze_all_characters()
    
    # Generar configuración
    config = analyzer.generate_animation_config(all_animations)
    
    # Guardar configuración
    analyzer.save_config(config)
    
    # Imprimir reporte detallado
    analyzer.print_detailed_report(all_animations)
    
    print("\n=== ANÁLISIS COMPLETADO ===")

if __name__ == "__main__":
    main() 