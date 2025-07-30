# src/ - Código Fuente Principal

## 🎯 **PROPÓSITO**
Directorio principal que contiene todo el código fuente operativo del videojuego **SiK Python Game**. Tras la limpieza masiva del 30 de julio de 2025, este directorio contiene únicamente archivos activos y funcionales.

## 📊 **ESTADO ACTUAL**
- **135 archivos Python** operativos
- **99.3% compliance** con límite de 250 líneas por archivo
- **Solo 1 archivo crítico**: `config_database.py` (297 líneas)
- **Completamente limpio**: Sin archivos backup, obsoletos o duplicados

---

## 🗂️ **ESTRUCTURA DE DIRECTORIOS**

### 📁 **`core/`** - Motor del juego
**Propósito**: Sistemas fundamentales del motor de juego
```
core/
├── game_engine.py          # Motor principal (fachada integrada)
├── game_engine_core.py     # Núcleo del motor
├── game_engine_events.py   # Manejo de eventos
├── game_engine_scenes.py   # Gestión de escenas
├── game_state.py           # Estado global del juego
└── scene_manager.py        # Manager de transiciones de escenas
```

### 🎮 **`entities/`** - Entidades del juego
**Propósito**: Todos los objetos interactivos del juego
```
entities/
├── character_data.py       # Datos de personajes jugables
├── enemy.py               # Sistema de enemigos (fachada)
├── enemy_behavior.py      # IA y comportamiento de enemigos
├── enemy_core.py          # Núcleo del sistema de enemigos
├── enemy_manager.py       # Gestión de spawning y grupos
├── player.py              # Jugador principal (fachada)
├── player_combat.py       # Sistema de combate del jugador
├── player_effects.py      # Efectos y powerups
├── player_stats.py        # Estadísticas del jugador
├── powerup.py             # Sistema de powerups (fachada)
├── projectile.py          # Proyectiles y balas
└── tile.py                # Elementos del escenario
```

### 🎬 **`scenes/`** - Pantallas del juego
**Propósito**: Todas las pantallas e interfaces del juego
```
scenes/
├── character_select_scene.py    # Selección de personaje
├── game_scene.py               # Pantalla principal de juego
├── loading_scene.py            # Pantalla de carga
├── main_menu_scene.py          # Menú principal
├── options_scene.py            # Configuración y opciones
├── pause_scene.py              # Menú de pausa
└── slot_selection_scene.py     # Selección de slot de guardado
```

### 🖥️ **`ui/`** - Interfaz de usuario
**Propósito**: Componentes de la interfaz de usuario
```
ui/
├── hud.py                 # HUD principal (fachada)
├── hud_core.py           # Núcleo del HUD
├── hud_elements.py       # Elementos base del HUD
├── hud_rendering.py      # Renderizado especializado
├── menu_callbacks.py     # Callbacks de menús
├── menu_configuration.py # Configuración de menús
├── menu_factory.py       # Fábrica de menús
└── menu_manager.py       # Gestor de menús
```

### 🛠️ **`utils/`** - Utilidades y herramientas
**Propósito**: Sistemas de soporte y utilidades
```
utils/
├── animation_manager.py      # Gestión de animaciones
├── asset_manager.py         # Gestión de assets (fachada)
├── atmospheric_effects.py   # Efectos atmosféricos
├── camera.py                # Sistema de cámara
├── config_database.py       # Interfaz SQLite (único archivo >250 líneas)
├── config_manager.py        # Gestión de configuración
├── database_manager.py      # Gestión de base de datos
├── desert_background.py     # Fondo del desierto
├── input_manager.py         # Gestión de entrada
├── logger.py               # Sistema de logging
├── save_manager.py          # Gestión de guardado
└── world_generator.py       # Generación procedural del mundo
```

### 🔧 **`managers/`** - Gestores especializados
**Propósito**: Sistemas de gestión específicos
```
managers/
├── audio_manager.py       # Gestión de audio y sonido
└── resource_manager.py    # Gestión de recursos del sistema
```

---

## 🎯 **PRINCIPIOS DE ORGANIZACIÓN**

### ✅ **Reglas de Compliance**
- **Límite estricto**: 250 líneas por archivo
- **Arquitectura modular**: División funcional con fachadas
- **API compatibility**: 100% compatibilidad mantenida
- **Type hints**: Obligatorios en todos los parámetros y retornos
- **Español**: Código, comentarios, variables en español

### 🏗️ **Patrón Arquitectónico**
- **Fachadas**: Archivos principales que integran módulos especializados
- **Núcleos**: Sistemas core con funcionalidad esencial
- **Especializados**: Módulos para funcionalidades específicas
- **Gestores**: Coordinación entre sistemas

### 📋 **Convenciones**
- **Variables**: `generacion_enemigos`, `velocidad_movimiento`
- **Clases**: `GestorEnemigos`, `PersonajeJugador` (PascalCase español)
- **Archivos**: snake_case con sufijos descriptivos (_core, _manager, etc.)

---

## 🚀 **DESARROLLO FUTURO**

### 🎮 **Próximas Características**
- **Nuevas mecánicas**: El código base está preparado
- **Sistemas de combate**: Expandir `entities/`
- **Efectos visuales**: Ampliar `utils/atmospheric_effects.py`
- **Niveles procedurales**: Extender `world_generator.py`

### 📊 **Métricas de Salud**
- **135 archivos operativos** - Completamente funcional
- **99.3% compliance** - Excelente mantenibilidad
- **Arquitectura modular** - Fácil extensión
- **APIs estables** - Compatible con futuras mejoras

---

## 📚 **REFERENCIAS**
- **Documentación**: `docs/FUNCIONES_DOCUMENTADAS.md`
- **Estado del proyecto**: `docs/ANALISIS_POST_MODERNIZACION.md`
- **Instrucciones de desarrollo**: `.github/copilot-instructions.md`

---

**🎯 ESTADO**: ✅ LISTO PARA DESARROLLO DE CARACTERÍSTICAS
**📅 ÚLTIMA LIMPIEZA**: 30 de Julio, 2025
**🎮 ENFOQUE**: Desarrollo de videojuego bullet hell 2D
