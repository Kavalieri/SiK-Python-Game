# Scripts de Test - SiK Python Game

Esta carpeta contiene todos los scripts de test permanentes para verificar el funcionamiento del juego.

## 🚀 Ejecutor Principal

### `run_tests.py`
Script maestro que permite ejecutar todos los tests desde un menú interactivo.

```bash
python scripts/run_tests.py
```

## 📋 Tests Individuales

### 1. `test_simple_player.py`
**Propósito**: Prueba el movimiento básico del jugador y su comportamiento de idle (versión simplificada).

**Características**:
- Verifica que el jugador se mueva solo cuando se presionan las teclas
- Confirma que se detenga correctamente al soltar las teclas
- Prueba las animaciones de idle, walk y attack
- Muestra información de debug en tiempo real

**Controles**:
- `WASD` - Mover jugador
- `Mouse` - Apuntar
- `Clic izquierdo` - Disparar
- `ESC` - Salir

### 2. `test_desert_background.py`
**Propósito**: Prueba el fondo dinámico de desierto con efectos visuales.

**Características**:
- Verifica la generación de partículas de arena
- Prueba los efectos de dunas con profundidad
- Confirma los efectos atmosféricos (viento, niebla)
- Permite mover la cámara para probar parallax

**Controles**:
- `Flechas` - Mover cámara
- `ESC` - Salir

### 3. `test_world_elements.py`
**Propósito**: Prueba la generación y renderizado de elementos del mundo.

**Características**:
- Verifica la generación de elementos con sprites reales
- Prueba las áreas especiales (oasis, rocas, cactus, ruinas)
- Confirma el sistema de cámara y visibilidad
- Muestra estadísticas de elementos generados

**Controles**:
- `Flechas` - Mover cámara
- `ESC` - Salir

### 4. `test_world_generation.py`
**Propósito**: Prueba la generación completa del mundo con jugador.

**Características**:
- Integra generación de mundo, jugador y cámara
- Prueba el movimiento del jugador en el mundo generado
- Verifica la cámara que sigue al jugador
- Incluye fondo de desierto

**Controles**:
- `WASD` - Mover jugador
- `Mouse` - Apuntar
- `Clic izquierdo` - Disparar
- `ESC` - Salir

### 5. `test_complete_system.py`
**Propósito**: Prueba el sistema completo con todas las mejoras integradas.

**Características**:
- Integra todos los componentes del juego
- Permite cambiar entre modo jugador y cámara libre
- Prueba el mundo completo con todas las áreas especiales
- Verifica el rendimiento y funcionalidad completa

**Controles**:
- `WASD` - Mover jugador (cámara sigue)
- `Flechas` - Mover cámara libre
- `Mouse` - Apuntar
- `Clic izquierdo` - Disparar
- `ESPACIO` - Cambiar modo
- `ESC` - Salir

## 🎯 Cómo Usar

### Ejecutar un test específico:
```bash
python scripts/test_simple_player.py
python scripts/test_desert_background.py
python scripts/test_world_elements.py
python scripts/test_world_generation.py
python scripts/test_complete_system.py
```

### Ejecutar desde el menú principal:
```bash
python scripts/run_tests.py
```

## 📊 Información de Debug

Todos los tests incluyen información de debug en tiempo real:
- Posición del jugador/cámara
- Estado de animación
- Velocidad y dirección
- FPS y rendimiento
- Controles activos
- Estadísticas del mundo

## 🔧 Configuración

Los tests están configurados para:
- **Pantalla**: 1200x800 píxeles (configurable)
- **Mundo**: 4 veces el tamaño de la pantalla
- **FPS**: 60 FPS objetivo
- **Logging**: Nivel INFO

## 🐛 Solución de Problemas

### Error de importación:
Si aparece un error de importación, asegúrate de ejecutar desde el directorio raíz del proyecto:
```bash
cd /ruta/al/proyecto/SiK-Python-Game
python scripts/run_tests.py
```

### Error de assets:
Si faltan sprites o assets, los tests usarán sprites de fallback automáticamente.

### Rendimiento bajo:
- Reduce la resolución de pantalla en los scripts
- Ajusta la densidad de elementos en `world_generator.py`
- Verifica que no haya otros procesos consumiendo recursos

## 📝 Notas de Desarrollo

- Todos los scripts son independientes y pueden ejecutarse por separado
- Los tests están diseñados para ser modificados fácilmente
- Cada test incluye logging detallado para debugging
- Los controles son consistentes entre todos los tests
- Los scripts se pueden usar como base para nuevos tests

## 🔄 Actualizaciones

Para añadir nuevos tests:
1. Crear el archivo en la carpeta `scripts/`
2. Seguir el patrón de los tests existentes
3. Añadir la opción al menú en `run_tests.py`
4. Documentar en este README 