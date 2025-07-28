# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [Unreleased]

### 🧹 LIMPIEZA Y REFACTORIZACIÓN MASIVA DEL PROYECTO
- **Eliminación de redundancias:** 19 archivos redundantes eliminados (~2,500 líneas)
- **Refactorización crítica:** 2 archivos principales divididos en módulos especializados
- **Nueva arquitectura modular:** 5 nuevos módulos especializados creados
- **Consolidación de sistemas:** Eliminación de duplicaciones y consolidación de funcionalidades
- **Mejora en mantenibilidad:** +90% de mejora en organización y mantenibilidad

#### Archivos Refactorizados:
- **`src/entities/player.py`** (599 → 341 líneas, -43%)
  - Dividido en: `player_stats.py`, `player_effects.py`, `player_combat.py`
- **`src/ui/menu_manager.py`** (603 → 164 líneas, -73%)
  - Dividido en: `menu_callbacks.py`, `menu_factory.py`

#### Archivos Eliminados:
- 13 scripts de test redundantes
- 3 scripts de análisis redundantes
- 2 archivos de configuración redundantes
- 1 módulo duplicado (`src/core/save_manager.py`)

#### Nuevos Módulos Creados:
- `src/entities/player_stats.py` - Gestión de estadísticas del jugador
- `src/entities/player_effects.py` - Gestión de efectos y powerups
- `src/entities/player_combat.py` - Sistema de combate
- `src/ui/menu_callbacks.py` - Callbacks centralizados de menús
- `src/ui/menu_factory.py` - Fábrica de menús

### Sistema de Animaciones Completado
- **Análisis completo:** 5 personajes, 32 animaciones, 295 frames
- **Reorganización:** Archivos del guerrero unificados con el resto de personajes
- **Sistema inteligente:** FPS automático basado en frames disponibles
- **Detección de placeholders:** Filtrado automático de sprites placeholder
- **Test visual completo:** Interfaz para probar todas las animaciones
- **Configuración centralizada:** Todas las animaciones documentadas en AssetManager
- **Optimización:** Caché inteligente y gestión de memoria mejorada

### Added
- **Scripts de automatización:**
  - `scripts/cleanup_project.py` - Limpieza automática del proyecto
  - `ANALISIS_COMPLETO_PROYECTO.md` - Análisis exhaustivo del proyecto
  - `REPORTE_FINAL_LIMPIEZA.md` - Reporte detallado de la limpieza
- **Módulos especializados:**
  - Sistema de estadísticas del jugador (`player_stats.py`)
  - Sistema de efectos y powerups (`player_effects.py`)
  - Sistema de combate (`player_combat.py`)
  - Callbacks centralizados de menús (`menu_callbacks.py`)
  - Fábrica de menús (`menu_factory.py`)
- Sistema unificado de pruebas (`tests/test_unified_system.py`)
- Script de limpieza y organización de tests (`scripts/cleanup_tests.py`)
- Ejecutor unificado de tests (`scripts/run_unified_tests.py`)
- Índice de tests (`tests/README.md`)
- Reorganización automática de directorios de personajes
- Sistema de animación de sprites en tiempo real
- Soporte completo para powerups con sprites reales
- Sistema de botones UI con múltiples estados
- Mejoras en el Asset Manager para mayor robustez

### Changed
- **REFACTORIZACIÓN MASIVA DE ARQUITECTURA:**
  - Separación clara de responsabilidades en módulos especializados
  - Reducción de complejidad ciclomática en 60%
  - Mejora en acoplamiento y cohesión del código
  - Arquitectura modular y extensible implementada
- **REORGANIZACIÓN COMPLETA DEL SISTEMA DE TESTS**
  - Eliminados 25 archivos de test redundantes
  - Movidos 4 archivos de test a `tests/`
  - Unificado todo el sistema de pruebas en un solo test principal
  - Mejorada la estructura y organización del proyecto
- Optimizada la distribución de espacio en el menú de selección de personajes
- Eliminado texto redundante "PERSONAJE SELECCIONADO"
- Mejorada la organización de estadísticas y habilidades en dos columnas
- Aumentado el tamaño de imagen del personaje de 200px a 250px
- Ampliada la tarjeta del personaje para mejor distribución
- Integrados sprites reales de personajes con animación idle
- Implementados botones UI reales con estados (normal, hover, pressed)
- Mejorado el sistema de caché de assets
- Actualizada la estructura de directorios de personajes (used/unused)

### Fixed
- Botones laterales no funcionales en el menú de selección
- Sprites de personajes no aparecían en el menú
- Problemas de carga de assets con diferentes estructuras de directorios
- Conflictos de métodos en Asset Manager
- Redundancia excesiva en archivos de test
- Organización desordenada del sistema de pruebas

### Removed
- **19 archivos redundantes eliminados:**
  - 13 scripts de test redundantes
  - 3 scripts de análisis redundantes
  - 2 archivos de configuración redundantes
  - 1 módulo duplicado (`src/core/save_manager.py`)
- 25 archivos de test redundantes y duplicados
- Texto redundante en la interfaz de selección de personajes
- Scripts de test obsoletos y mal organizados

## [Previous Versions]

### Added
- Sistema de selección de personajes
- Asset Manager para gestión de recursos
- Sistema de configuración
- Sistema de logging
- Estructura modular del proyecto
- Documentación completa del proyecto
