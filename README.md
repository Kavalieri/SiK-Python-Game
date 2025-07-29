# SiK Python Game

Un videojuego 2D desarrollado **100% con agentes de inteligencia artificial y asistentes**, utilizando Python y Pygame-ce, siguiendo las mejores prácticas de la comunidad.

## 🤖 Desarrollo con Inteligencia Artificial

**Este proyecto es un experimento pionero en desarrollo de videojuegos asistido por IA.** Todo el código, documentación, arquitectura y decisiones de diseño han sido generados y refinados mediante la colaboración entre desarrolladores humanos y agentes de inteligencia artificial avanzados.

### Características del Desarrollo con IA:
- **Arquitectura completa**: Diseñada y implementada por agentes de IA
- **Código optimizado**: Generado con mejores prácticas y patrones de diseño
- **Documentación automática**: Comentarios y documentación generados por IA
- **Testing inteligente**: Scripts de prueba creados automáticamente
- **Iteración continua**: Mejoras basadas en feedback y análisis de IA

### Tecnologías de IA Utilizadas:
- **Asistentes de código**: Generación y refactorización de código
- **Análisis de patrones**: Optimización de arquitectura y rendimiento
- **Generación de documentación**: Comentarios y guías automáticas
- **Testing automatizado**: Scripts de verificación inteligentes

## 🎮 Descripción

SiK Python Game es un proyecto de videojuego 2D que utiliza Python como lenguaje principal y Pygame-ce como motor gráfico. El proyecto está diseñado con una arquitectura modular y escalable, siguiendo las convenciones de la comunidad Python, y representa un hito en el desarrollo de software asistido por inteligencia artificial.

## 🚀 Características

- **Arquitectura modular**: Código organizado en paquetes y módulos bien estructurados
- **Sistema de escenas**: Gestión eficiente de diferentes pantallas del juego
- **Gestión de assets**: Carga y caché optimizado de recursos
- **Sistema de entrada**: Soporte para teclado, ratón y gamepad
- **Configuración flexible**: Sistema de configuración basado en JSON
- **Logging completo**: Sistema de logging con rotación de archivos
- **Físicas realistas**: Integración con Pymunk para físicas 2D
- **Interfaz moderna**: Uso de pygame-menu y pygame-gui para interfaces

## 📋 Requisitos

- Python 3.8 o superior
- Pygame-ce 2.4.0 o superior
- Dependencias listadas en `requirements.txt`

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd SiK-Python-Game
   ```

2. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Cómo Ejecutar

El punto de entrada principal del juego es `src/main.py`:

```bash
python src/main.py
```

## 📁 Estructura del Proyecto

```
SiK-Python-Game/
├── src/                    # Código fuente principal
│   ├── core/              # Motor del juego
│   │   ├── game_engine.py # Motor principal
│   │   ├── game_state.py  # Estado global
│   │   └── scene_manager.py # Gestor de escenas
│   ├── entities/          # Entidades del juego
│   ├── managers/          # Gestores especializados
│   ├── ui/               # Interfaz de usuario
│   ├── utils/            # Utilidades
│   └── main.py           # Punto de entrada
├── assets/               # Recursos del juego
├── docs/                 # Documentación
├── tools/                # Herramientas de desarrollo
├── logs/                 # Archivos de log
├── saves/                # Partidas guardadas
└── config.json           # Configuración del juego
```

## 🔧 Configuración

El juego utiliza un sistema de configuración basado en JSON. El archivo `config.json` se crea automáticamente en la primera ejecución con valores por defecto.

### Configuración por defecto:

```json
{
    "game": {
        "title": "SiK Python Game",
        "version": "0.1.0",
        "debug": false
    },
    "display": {
        "width": 1280,
        "height": 720,
        "fps": 60,
        "fullscreen": false,
        "vsync": true
    },
    "audio": {
        "master_volume": 1.0,
        "music_volume": 0.7,
        "sfx_volume": 0.8,
        "enabled": true
    }
}
```

## 🎮 Controles

### Teclado:
- **WASD / Flechas**: Movimiento
- **Espacio**: Saltar
- **J / Enter**: Atacar
- **E**: Interactuar
- **Escape**: Pausa/Menú

### Ratón:
- **Clic izquierdo**: Seleccionar/Interactuar
- **Clic derecho**: Menú contextual

### Gamepad:
- **Stick izquierdo**: Movimiento
- **A**: Saltar
- **X**: Atacar
- **B**: Interactuar
- **Start**: Pausa

## 🛠️ Desarrollo

### Convenciones de Código

- **Idioma**: Español para comentarios y documentación
- **Estilo**: PEP 8 con tabulación
- **Nomenclatura**: Variables y funciones en español
- **Documentación**: Docstrings en todas las funciones y clases

### Herramientas de Desarrollo

- **Formateo**: Black
- **Linting**: Flake8
- **Type checking**: MyPy
- **Testing**: Pytest

### Comandos de Desarrollo

```bash
# Formatear código
black src/

# Verificar estilo
flake8 src/

# Verificar tipos
mypy src/

# Ejecutar tests
pytest tests/
```

## 📝 Logging

El juego incluye un sistema de logging completo que registra:
- Información de inicialización
- Eventos del juego
- Errores y excepciones
- Rendimiento y debug

Los logs se guardan en `logs/game.log` con rotación automática.

## 🎨 Assets

Los assets del juego se organizan en la carpeta `assets/`:
- `images/`: Imágenes y sprites
- `sounds/`: Efectos de sonido y música
- `fonts/`: Fuentes tipográficas
- `ui/`: Elementos de interfaz

## 🔄 Control de Versiones

- **Commits**: Documentados con `commit_message.txt`
- **Changelog**: Mantenido en `CHANGELOG.md`
- **Colaboración**: Guías en `docs/COLABORACION.md`

## 📄 Licencia

Este proyecto está bajo la licencia especificada en `LICENSE`.

## 👥 Colaboración

Para contribuir al proyecto, consulta `docs/COLABORACION.md` para las guías de desarrollo y colaboración.

## 🐛 Reportar Problemas

Si encuentras algún problema o tienes una sugerencia, por favor:
1. Revisa los logs en `logs/game.log`
2. Verifica la configuración en `config.json`
3. Consulta la documentación en `docs/`

## 🆕 Nuevas Características Implementadas

### 🎭 Sistema de Animaciones del Jugador
- **Animaciones fluidas**: Idle, walk, attack con transiciones suaves
- **Rotación dinámica**: El jugador rota según la dirección del movimiento y posición del mouse
- **Estados de animación**: Sistema de estados que cambia automáticamente según las acciones
- **Timer de ataque**: Animación de ataque que se activa al disparar

### 🏜️ Fondo Dinámico de Desierto
- **Gradientes atmosféricos**: Cielo con gradiente de azul a naranja atardecer
- **Dunas procedimentales**: Dunas generadas dinámicamente con formas naturales
- **Partículas de arena**: Sistema de partículas que simula arena en el viento
- **Efectos atmosféricos**: Ondulación de calor y efectos de viento
- **Parallax**: Diferentes capas con movimiento a distintas velocidades

### 🎮 Menú de Selección Mejorado
- **Interfaz visual**: Diseño moderno con paneles y botones funcionales
- **Información detallada**: Estadísticas y habilidades de cada personaje
- **Selección interactiva**: Clics funcionales con feedback visual
- **Navegación fluida**: Botones de volver y comenzar juego operativos

### 🔧 Mejoras Técnicas
- **Sistema de animaciones robusto**: Gestión centralizada de animaciones
- **Optimización de rendimiento**: Fondos dinámicos eficientes
- **Gestión de errores**: Manejo robusto de assets faltantes
- **Tests automatizados**: Scripts de verificación de funcionalidad

## 🔬 Investigación y Desarrollo

Este proyecto forma parte de una investigación sobre el potencial de la inteligencia artificial en el desarrollo de software. Demuestra cómo los agentes de IA pueden:

- **Comprender requisitos complejos** y traducirlos en arquitectura de software
- **Generar código de calidad** siguiendo estándares profesionales
- **Mantener consistencia** en patrones de diseño y convenciones
- **Iterar y mejorar** basándose en feedback y análisis
- **Documentar automáticamente** el código y procesos

### Metodología de Desarrollo:
1. **Análisis de requisitos** por agentes de IA
2. **Diseño de arquitectura** automatizado
3. **Generación de código** con mejores prácticas
4. **Testing automatizado** y verificación
5. **Documentación continua** y actualización

## 📊 Estadísticas del Proyecto

- **Líneas de código**: Generadas 100% por IA
- **Arquitectura**: Diseñada por agentes de IA
- **Documentación**: Creada automáticamente
- **Tests**: Generados inteligentemente
- **Optimizaciones**: Aplicadas por análisis de IA

---

**Desarrollado con 🤖 Inteligencia Artificial por el equipo SiK**

*Este proyecto representa el futuro del desarrollo de software asistido por IA*

# Registro de restauración y políticas de formato

## Restauración crítica (2024-12-19)

- Se restauró el proyecto tras un error masivo de formato que eliminó los saltos de línea en todos los archivos `.py`, `.md`, `.json`, `.txt`.
- Se recuperaron los archivos desde el último commit y se reaplicaron todos los cambios funcionales realizados en la sesión:
  - Flujo avanzado de menús y guardado (selección de slots, callbacks, navegación, diferenciación de botón Salir y cierre de ventana).
  - Restauración y refactorización de `slot_selection_scene.py` y `options_scene.py`.
  - Actualización de la documentación y diagrama Mermaid en `docs/FLUJO_MENUS_GUARDADO.md`.
  - Pruebas de navegación y funcionamiento correctas.

## Políticas de formato y control de cambios

- **Indentación:**
  - Todo el proyecto usa **tabulaciones** para la indentación en los scripts Python.
  - Se revisará cualquier archivo nuevo para mantener la coherencia.
- **Saltos de línea:**
  - Se utiliza `.gitattributes` para forzar `LF` en el repositorio y evitar problemas de diffs por saltos de línea.
  - Los archivos locales pueden verse en `CRLF` en Windows, pero el repo siempre tendrá `LF`.

## Estado actual

- El flujo de menús, guardado y navegación está funcional y documentado.
- El botón "Salir" y el cierre de ventana están diferenciados en los logs.
- El código está limpio y estructurado tras la restauración.

## Próximos pasos

- Limpieza de código y refactorización adicional.
- Manejo y corrección de los elementos que todavía no funcionan.
- Refuerzo de testing y documentación continua.

---

> **Este registro deja constancia de la recuperación y las políticas de formato para futuras referencias y colaboración segura.**

