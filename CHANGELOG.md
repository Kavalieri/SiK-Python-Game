# Changelog - SiK Python Game

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sistema de HUD profesional con información del jugador
- Sistema de guardado con cifrado y gestión de múltiples archivos
- Sistema de menús completo con pygame-menu
- Clase base Entity para todas las entidades del juego
- Escenas del juego (bienvenida, menú principal, etc.)
- Gestor de menús con callbacks y navegación
- Sistema de guardado automático y manual
- Exportación/importación de archivos de guardado para debug
- Interfaz de usuario moderna y responsive

### Changed
- Motor del juego actualizado con nuevos sistemas
- Integración completa de pygame-menu para menús
- Sistema de logging mejorado con más información

### Technical Details
- **HUD**: Sistema profesional con barras de vida, puntuación, powerups
- **Guardado**: Cifrado XOR, compresión zlib, serialización pickle
- **Menús**: 8 menús diferentes con navegación completa
- **Entidades**: Clase base abstracta con sistema de estados y efectos
- **Escenas**: Sistema modular para diferentes pantallas del juego

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [0.1.0] - 2024-07-28

### Added
- **Estructura del Proyecto**: Establecimiento de la arquitectura base del videojuego
  - Directorio `src/` con estructura modular
  - Paquete `core/` con motor principal
  - Paquete `utils/` con utilidades
  - Paquete `tests/` para pruebas unitarias
  - Directorios `logs/`, `saves/` para datos del juego

- **Motor del Juego**: Implementación del sistema base
  - `GameEngine`: Bucle principal del juego
  - `GameState`: Gestión del estado global
  - `SceneManager`: Sistema de escenas

- **Utilidades**: Herramientas fundamentales
  - `ConfigManager`: Gestión de configuración JSON
  - `AssetManager`: Carga y caché de recursos
  - `InputManager`: Gestión de entrada de usuario
  - `Logger`: Sistema de logging con rotación

- **Configuración del Proyecto**:
  - `requirements.txt` con dependencias
  - `pyproject.toml` con configuración de herramientas
  - `README.md` completo con documentación
  - `docs/COLABORACION.md` con guías de desarrollo

- **Herramientas de Desarrollo**:
  - Configuración de Black para formateo
  - Configuración de Flake8 para linting
  - Configuración de MyPy para type checking
  - Configuración de Pytest para testing

- **Tests Unitarios**:
  - Tests básicos para ConfigManager
  - Estructura de testing establecida

### Technical Details
- **Arquitectura**: Modular y escalable
- **Idioma**: Español en código y documentación
- **Estilo**: PEP 8 con tabulación
- **Type Hints**: Obligatorios en funciones públicas
- **Logging**: Sistema completo con niveles y rotación
- **Configuración**: Basada en JSON con valores por defecto

### Dependencies
- pygame-ce>=2.4.0
- pygame-menu>=4.4.0
- pygame-gui>=0.6.9
- pygame-tools>=0.1.0
- pygame-extra>=0.1.0
- pymunk>=6.6.0
- numpy>=1.24.0
- pillow>=10.0.0

### Development Dependencies
- pytest>=7.4.0
- pytest-cov>=4.1.0
- black>=23.0.0
- flake8>=6.0.0
- mypy>=1.5.0
- pyinstaller>=5.13.0
- cx-freeze>=6.15.0

---

## Tipos de Cambios

- **Added**: Para nuevas funcionalidades
- **Changed**: Para cambios en funcionalidades existentes
- **Deprecated**: Para funcionalidades que serán eliminadas
- **Removed**: Para funcionalidades eliminadas
- **Fixed**: Para correcciones de bugs
- **Security**: Para vulnerabilidades de seguridad

## Convenciones

- Cada versión debe tener una fecha de lanzamiento
- Los cambios se agrupan por tipo
- Se incluyen detalles técnicos cuando es relevante
- Se documentan las dependencias añadidas o modificadas
- Se mantiene un historial completo de cambios
