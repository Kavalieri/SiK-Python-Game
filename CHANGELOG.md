# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

## [Unreleased]

### Sistema de Animaciones Completado
- **Análisis completo:** 5 personajes, 32 animaciones, 295 frames
- **Reorganización:** Archivos del guerrero unificados con el resto de personajes
- **Sistema inteligente:** FPS automático basado en frames disponibles
- **Detección de placeholders:** Filtrado automático de sprites placeholder
- **Test visual completo:** Interfaz para probar todas las animaciones
- **Configuración centralizada:** Todas las animaciones documentadas en AssetManager
- **Optimización:** Caché inteligente y gestión de memoria mejorada

### Added
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
