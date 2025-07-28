"""
Generador de Reporte Final de Animaciones
========================================

Autor: SiK Team
Fecha: 2024
Descripción: Genera un reporte final completo de todas las animaciones y actualiza la documentación.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def generate_final_report():
    """Genera el reporte final de animaciones."""
    
    print("=== GENERANDO REPORTE FINAL DE ANIMACIONES ===")
    
    # Cargar la configuración generada por el análisis
    config_file = "animation_config.json"
    
    if not os.path.exists(config_file):
        print(f"Error: No se encontró el archivo de configuración {config_file}")
        return
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Generar reporte en markdown
    report_content = f"""# Reporte Final de Animaciones - SiK Game

**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Resumen General

- **Total de personajes:** {config['summary']['total_characters']}
- **Total de animaciones:** {config['summary']['total_animations']}
- **Total de frames:** {config['summary']['total_frames']}
- **Promedio de animaciones por personaje:** {config['summary']['total_animations'] / config['summary']['total_characters']:.1f}
- **Promedio de frames por animación:** {config['summary']['total_frames'] / config['summary']['total_animations']:.1f}

## Detalle por Personaje

"""
    
    # Procesar cada personaje
    for character_name, char_config in config['characters'].items():
        report_content += f"### {character_name.upper()}\n\n"
        report_content += f"- **Animaciones disponibles:** {char_config['animation_count']}\n"
        report_content += f"- **Total de frames:** {char_config['total_frames']}\n\n"
        
        report_content += "| Animación | Frames | FPS | Duración (ms) |\n"
        report_content += "|-----------|--------|-----|---------------|\n"
        
        for anim_name, anim_config in char_config['animations'].items():
            duration = 1000 / anim_config['fps']
            report_content += f"| {anim_name} | {anim_config['frame_count']} | {anim_config['fps']} | {duration:.1f} |\n"
        
        report_content += "\n"
    
    # Añadir sección de optimizaciones
    report_content += """## Optimizaciones Implementadas

### 1. Cálculo Inteligente de FPS
- **FPS base por tipo de animación:** Cada tipo tiene un FPS base optimizado
- **Ajuste por número de frames:** Se reduce el FPS para animaciones con pocos frames
- **Límites de FPS:** Mínimo 8 FPS, máximo 30 FPS

### 2. Detección de Placeholders
- **Detección automática:** Se identifican y filtran sprites placeholder
- **Criterios:** Tamaño 64x64 y pocos colores únicos
- **Fallback:** Se crean placeholders cuando no se encuentran sprites

### 3. Estructura Unificada
- **Reorganización del guerrero:** Se movieron archivos de subdirectorios al directorio principal
- **Formato consistente:** Todos los personajes usan el mismo formato de nombres
- **Configuración centralizada:** Todas las animaciones están documentadas en el AssetManager

### 4. Sistema de Caché
- **Caché de imágenes:** Evita recargar sprites ya cargados
- **Caché de animaciones:** Almacena información de animaciones procesadas
- **Gestión de memoria:** Limpieza automática de caché

## Tipos de Animación Disponibles

### Personajes Jugables
- **Guerrero:** Attack, Dead, Idle, Jump, JumpAttack, Run, Walk
- **Adventure Girl:** Dead, Idle, Jump, Melee, Run, Shoot, Slide
- **Robot:** Dead, Idle, Jump, JumpMelee, JumpShoot, Melee, RunShoot, Run, Shoot, Slide

### Enemigos
- **Zombie Male:** Attack, Dead, Idle, Walk
- **Zombie Girl:** Attack, Dead, Idle, Walk

## FPS Recomendados por Tipo

| Tipo de Animación | FPS Base | Rango Ajustado |
|-------------------|----------|----------------|
| Idle | 12 | 8-15 |
| Walk | 15 | 10-18 |
| Run | 18 | 12-22 |
| Attack | 20 | 10-25 |
| Dead | 10 | 8-12 |
| Shoot | 16 | 8-20 |
| Jump | 14 | 10-17 |
| Melee | 18 | 12-22 |
| Slide | 16 | 10-19 |
| JumpMelee | 16 | 10-19 |
| JumpShoot | 16 | 10-19 |
| RunShoot | 18 | 12-22 |
| JumpAttack | 15 | 10-18 |

## Archivos Generados

- `animation_config.json`: Configuración completa de todas las animaciones
- `scripts/analyze_all_animations.py`: Script de análisis de animaciones
- `scripts/test_complete_animation_system.py`: Test visual completo
- `src/utils/asset_manager.py`: AssetManager actualizado con configuración
- `src/utils/animation_manager.py`: Sistema de animación inteligente

## Próximos Pasos

1. **Integración en el juego:** Usar el sistema en las escenas del juego
2. **Optimización de rendimiento:** Monitorear el uso de memoria y CPU
3. **Nuevas animaciones:** Añadir animaciones adicionales según sea necesario
4. **Tests automatizados:** Crear tests unitarios para el sistema de animación

---
*Reporte generado automáticamente por el sistema de análisis de animaciones de SiK Game*
"""
    
    # Guardar el reporte
    report_file = "ANIMATION_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Reporte guardado en: {report_file}")
    
    # Actualizar el CHANGELOG
    update_changelog(config)
    
    # Actualizar commit message
    update_commit_message(config)
    
    print("=== REPORTE FINAL GENERADO ===")

def update_changelog(config):
    """Actualiza el CHANGELOG con la información de animaciones."""
    
    changelog_file = "CHANGELOG.md"
    
    if not os.path.exists(changelog_file):
        print(f"Warning: No se encontró {changelog_file}")
        return
    
    with open(changelog_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la sección de [Unreleased]
    if "[Unreleased]" in content:
        # Añadir información de animaciones
        animation_info = f"""
### Sistema de Animaciones Completado
- **Análisis completo:** {config['summary']['total_characters']} personajes, {config['summary']['total_animations']} animaciones, {config['summary']['total_frames']} frames
- **Reorganización:** Archivos del guerrero unificados con el resto de personajes
- **Sistema inteligente:** FPS automático basado en frames disponibles
- **Detección de placeholders:** Filtrado automático de sprites placeholder
- **Test visual completo:** Interfaz para probar todas las animaciones
- **Configuración centralizada:** Todas las animaciones documentadas en AssetManager
- **Optimización:** Caché inteligente y gestión de memoria mejorada

"""
        
        # Insertar después de [Unreleased]
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == "[Unreleased]":
                lines.insert(i + 1, animation_info)
                break
        
        content = '\n'.join(lines)
        
        with open(changelog_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"CHANGELOG actualizado: {changelog_file}")

def update_commit_message(config):
    """Actualiza el commit message con la información de animaciones."""
    
    commit_file = "commit_message.txt"
    
    commit_message = f"""feat: Sistema de animaciones completo y optimizado

## Análisis y Reorganización
- Análisis completo de {config['summary']['total_characters']} personajes
- {config['summary']['total_animations']} animaciones identificadas
- {config['summary']['total_frames']} frames totales
- Reorganización de archivos del guerrero para estructura unificada

## Sistema Inteligente de Animaciones
- FPS automático basado en número de frames disponibles
- Detección y filtrado de sprites placeholder
- Caché inteligente para optimización de rendimiento
- Configuración centralizada en AssetManager

## Tests y Documentación
- Test visual completo con interfaz interactiva
- Reporte detallado de todas las animaciones
- Documentación actualizada en CHANGELOG
- Scripts de análisis y reorganización

## Personajes y Animaciones
- Guerrero: 7 animaciones (Attack, Dead, Idle, Jump, JumpAttack, Run, Walk)
- Adventure Girl: 7 animaciones (Dead, Idle, Jump, Melee, Run, Shoot, Slide)
- Robot: 10 animaciones (Dead, Idle, Jump, JumpMelee, JumpShoot, Melee, RunShoot, Run, Shoot, Slide)
- Zombie Male: 4 animaciones (Attack, Dead, Idle, Walk)
- Zombie Girl: 4 animaciones (Attack, Dead, Idle, Walk)

## Archivos Modificados
- src/utils/asset_manager.py: Configuración de animaciones integrada
- src/utils/animation_manager.py: Sistema inteligente de FPS
- scripts/analyze_all_animations.py: Análisis completo
- scripts/test_complete_animation_system.py: Test visual
- scripts/reorganize_guerrero.py: Reorganización de archivos
- ANIMATION_REPORT.md: Reporte final completo
- CHANGELOG.md: Documentación actualizada

## Próximos Pasos
- Integración en escenas del juego
- Tests automatizados
- Optimización de rendimiento
- Nuevas animaciones según necesidades
"""
    
    with open(commit_file, 'w', encoding='utf-8') as f:
        f.write(commit_message)
    
    print(f"Commit message actualizado: {commit_file}")

def main():
    """Función principal."""
    generate_final_report()

if __name__ == "__main__":
    main() 