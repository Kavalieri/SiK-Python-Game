# config/ - Configuración del Juego

## ⚙️ **PROPÓSITO**
Directorio centralizado que contiene todas las configuraciones del videojuego **SiK Python Game** en formato JSON. Este sistema modular permite ajustar el comportamiento del juego sin modificar el código fuente.

## 📊 **ESTADO ACTUAL**
- **10 archivos de configuración** especializados
- **Sistema modular**: Cada aspecto del juego configurado por separado
- **Formato JSON**: Fácil edición y validación
- **Integración SQLite**: Algunos datos migrados a base de datos

---

## 🗂️ **ARCHIVOS DE CONFIGURACIÓN**

### 🎮 **`characters.json`** (189 líneas)
**Propósito**: Configuración completa de personajes jugables
```json
{
  "characters": {
    "guerrero": {
      "nombre_mostrar": "Kava",
      "tipo": "Melee",
      "stats": { "vida": 100, "velocidad": 5, "daño": 25 },
      "ataques": [ /* configuración de ataques */ ],
      "habilidades": [ /* habilidades especiales */ ]
    }
  }
}
```

**✅ Estado**: Migrado a SQLite tabla `personajes`
**🔗 Integración**: `src/utils/config_database.py`

### 👾 **`enemies.json`** (73 líneas)
**Propósito**: Configuración de tipos de enemigos y comportamiento
```json
{
  "tipos_enemigos": {
    "zombie_male": {
      "stats": { "vida": 50, "velocidad": 2, "daño": 15 },
      "comportamiento": "perseguir",
      "animaciones": { "idle": 4, "walk": 8, "attack": 6, "dead": 6 }
    }
  }
}
```

**✅ Estado**: Migrado a SQLite tabla `enemigos`
**🔗 Integración**: `src/entities/enemy_behavior.py`

### 🎵 **`audio.json`** (32 líneas)
**Propósito**: Configuración de volúmenes y archivos de audio
```json
{
  "volúmenes": {
    "maestro": 0.7,
    "música": 0.5,
    "efectos": 0.8
  },
  "archivos_audio": {
    "música_fondo": "assets/sounds/background_music.mp3",
    "disparo": "assets/sounds/shoot.wav"
  }
}
```

**📱 Estado**: Mantiene formato JSON (configuración de usuario)
**🔗 Integración**: `src/managers/audio_manager.py`

### 🖥️ **`display.json`** (24 líneas)
**Propósito**: Configuración de pantalla y gráficos
```json
{
  "resolución": {
    "ancho": 1280,
    "alto": 720
  },
  "pantalla_completa": false,
  "fps": 60,
  "vsync": true
}
```

**📱 Estado**: Mantiene formato JSON (configuración de usuario)

### 🎮 **`input.json`** (28 líneas)
**Propósito**: Configuración de controles y teclas
```json
{
  "controles": {
    "mover_arriba": "w",
    "mover_abajo": "s",
    "mover_izquierda": "a",
    "mover_derecha": "d",
    "atacar": "space",
    "pausa": "escape"
  }
}
```

**📱 Estado**: Mantiene formato JSON (configuración de usuario)
**🔗 Integración**: `src/utils/input_manager.py`

### 🎯 **`gameplay.json`** (34 líneas)
**Propósito**: Mecánicas de juego y balance
```json
{
  "niveles": {
    "duración_base": 120,
    "escalado_dificultad": 1.2
  },
  "combate": {
    "daño_base": 25,
    "tiempo_invulnerabilidad": 1.5
  },
  "puntuación": {
    "por_enemigo": 100,
    "multiplicador_combo": 1.5
  }
}
```

**📱 Estado**: Mantiene formato JSON (balance del juego)
**🔗 Integración**: Múltiples archivos de `src/scenes/`

### 💎 **`powerups.json`** (106 líneas)
**Propósito**: Configuración de powerups y efectos
```json
{
  "tipos_powerup": {
    "velocidad": {
      "duración": 10,
      "multiplicador": 1.5,
      "probabilidad_spawn": 0.15
    },
    "daño": {
      "duración": 8,
      "multiplicador": 2.0,
      "probabilidad_spawn": 0.10
    }
  }
}
```

**📱 Estado**: Mantiene formato JSON (configuración de gameplay)
**🔗 Integración**: `src/entities/powerup.py`

### 🎨 **`ui.json`** (42 líneas)
**Propósito**: Configuración de interfaz de usuario
```json
{
  "colores": {
    "fondo": [20, 20, 30],
    "texto": [255, 255, 255],
    "botón_normal": [100, 100, 150],
    "botón_hover": [150, 150, 200]
  },
  "fuentes": {
    "título": 48,
    "normal": 24,
    "pequeña": 16
  }
}
```

**📱 Estado**: Mantiene formato JSON (configuración visual)
**🔗 Integración**: `src/ui/` (todos los archivos)

### 🎬 **`animations.json`** (67 líneas)
**Propósito**: Configuración de animaciones de personajes
```json
{
  "characters": {
    "guerrero": {
      "idle": { "frames": 4, "fps": 8 },
      "run": { "frames": 8, "fps": 12 },
      "attack": { "frames": 6, "fps": 10 }
    }
  }
}
```

**📱 Estado**: Mantiene formato JSON (configuración de assets)
**🔗 Integración**: `src/utils/animation_manager.py`

### 📱 **`loading_screen.json`** (18 líneas)
**Propósito**: Configuración de pantalla de carga
```json
{
  "duración_mínima": 2.0,
  "texto_carga": "Cargando...",
  "progreso_simulado": true,
  "color_fondo": [10, 10, 20]
}
```

**📱 Estado**: Mantiene formato JSON (configuración de UI)
**🔗 Integración**: `src/scenes/loading_scene.py`

---

## 🗄️ **SISTEMA MIXTO INTELIGENTE**

### ✅ **Migrado a SQLite**
- **`characters.json`** → Tabla `personajes`
- **`enemies.json`** → Tabla `enemigos`
- **Gestión**: `src/utils/config_database.py`

### 📱 **Mantiene JSON**
- **Configuración de usuario**: audio, display, input
- **Balance de gameplay**: gameplay, powerups
- **Configuración visual**: ui, animations, loading_screen

### 🎯 **Criterios de Decisión**
- **SQLite**: Datos complejos, relacionales, que cambian por código
- **JSON**: Configuración simple, modificable por usuario, balance

---

## 🔧 **INTEGRACIÓN CON EL CÓDIGO**

### 📖 **Sistema de Carga**
```python
# ConfigManager carga automáticamente todos los JSON
config = ConfigManager()

# Acceso directo a configuraciones
audio_config = config.get_section("audio")
display_config = config.get_section("display")

# Integración SQLite para datos complejos
character_data = config_database.get_character_data("guerrero")
```

### 🔗 **Archivos de Integración**
- **`src/utils/config_manager.py`**: Carga y gestión de JSON
- **`src/utils/config_database.py`**: Interfaz SQLite (único >250 líneas)
- **Múltiples archivos**: Cada sistema usa su configuración específica

---

## 🎯 **VENTAJAS DEL SISTEMA**

### ✅ **Modularidad**
- **Configuración separada** por aspecto del juego
- **Fácil modificación** sin tocar código fuente
- **Testing simplificado** con configuraciones de prueba

### 🔄 **Flexibilidad**
- **Balance del juego**: Ajustes rápidos en `gameplay.json`
- **Personalización**: Usuario puede modificar controles y audio
- **Desarrollo**: Configuraciones específicas para desarrollo/producción

### 🛡️ **Seguridad**
- **Validación**: ConfigManager valida formatos JSON
- **Fallbacks**: Valores por defecto si faltan configuraciones
- **Tipo safety**: Type hints en todas las configuraciones

---

## 🚀 **DESARROLLO FUTURO**

### 🎯 **Próximas Configuraciones**
- **`multiplayer.json`**: Configuración multijugador
- **`achievements.json`**: Sistema de logros
- **`modding.json`**: Soporte para mods
- **`analytics.json`**: Configuración de métricas

### 📊 **Mejoras Planificadas**
- **Editor visual**: Herramienta para editar configuraciones
- **Validación avanzada**: Esquemas JSON más robustos
- **Hot reload**: Recarga de configuración sin reiniciar
- **Exportación**: Compartir configuraciones entre usuarios

---

## 📚 **REFERENCIAS**

### 📖 **Documentación**
- **ConfigManager**: `src/utils/config_manager.py`
- **ConfigDatabase**: `src/utils/config_database.py`
- **Sistema mixto**: `docs/ANALISIS_POST_MODERNIZACION.md`

### 🔧 **Uso en Desarrollo**
- **Modificación**: Editar JSON y reiniciar juego
- **Testing**: Usar configuraciones específicas para tests
- **Balance**: Ajustar valores de gameplay sin recompilar

---

**⚙️ ESTADO**: ✅ SISTEMA MODULAR COMPLETO Y OPERATIVO
**📅 ÚLTIMA ACTUALIZACIÓN**: 30 de Julio, 2025
**🎯 ENFOQUE**: Configuración flexible y sistema mixto inteligente
