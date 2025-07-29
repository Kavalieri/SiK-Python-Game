# REGLAS ACTUALIZADAS - SiK Python Game

## 🎯 REGLAS PRIORITARIAS DEL PROYECTO

### 🔧 Desarrollo y Testing
- **Funcionalidad primero**: Arrancar código real antes de tests, solo tests necesarios y controlados
- **Validación exhaustiva**: Verificar funcionamiento completo tras cada cambio
- **Logging detallado**: Capturar todas las pulsaciones y acciones de interfaz para debug
- **Modularización**: Máximo 200 líneas por archivo, dividir antes de superar este límite

### 🏗️ Arquitectura y Estructura
- **Rutas absolutas**: Usar rutas absolutas para todo acceso a archivos
- **Scripts para tareas complejas**: Automatizar procesos pesados o repetitivos
- **Control de versiones**: Documentar todos los cambios, NO hacer PUSH automático
- **Timeout de 10 segundos**: Para comandos que no tengan escape pero hayan terminado

### 📚 Documentación
- **Mantener actualizados**: README.md, CHANGELOG.md, COLABORACION.md
- **Documentación modular**: Generar README.md específico para módulos con entidad propia
- **Cabeceras obligatorias**: Todos los scripts deben tener cabecera con nombre, autor, fecha, descripción

---

## 🎮 SISTEMA DE JUEGO ESPECÍFICO

### 👤 Personajes Jugables (3 seleccionables)
- **Guerrero**: Personaje balanceado
- **Adventure Girl**: Personaje ágil  
- **Robot**: Personaje tecnológico
- **Características**: Stats únicos, animaciones específicas, mejoras personalizadas

### 🧟 Enemigos
- **Tipos base**: Zombie Male, Zombie Girl
- **Variantes**: Normal, Raro, Élite, Legendario
- **IA**: Patrulla, persecución, ataque, detección de rango (300 píxeles)

### ⚡ Powerups
- **Tipos**: Velocidad, daño, escudo, doble disparo, dispersión, explosión, metralla
- **Efectos**: Temporales con duración específica
- **Spawn**: Generación automática en el mundo

### 🎮 Mecánicas de Juego
- **Estilo**: Bullet Hell 2D / Top-down shooter
- **Movimiento**: WASD/flechas, cámara que sigue al jugador de forma fluida
- **Disparo**: Hacia cursor del ratón
- **Colisiones**: Sistema de daño y salud
- **Progresión**: Puntos por enemigos derrotados según nivel
- **Rondas**: Tiempo limitado o hasta derrota del jugador

---

## 🎨 INTERFAZ Y HUD

### 🖥️ HUD Profesional (Siempre Visible)
- **Elementos obligatorios**: Vida, mejoras, powerups activos, puntos, temporizador
- **Espacio reservado**: Cada elemento con su espacio claramente indicado
- **Debug en tiempo real**: Posiciones, eventos, errores en consola

### 🎛️ Sistema de Menús
- **Pantalla de bienvenida**: Obligatoria al inicio
- **Menú principal**: Nuevo juego, continuar, cargar, opciones, salir
- **Selección de personaje**: 3 personajes con estadísticas detalladas
- **Menú de pausa**: Durante el juego
- **Menú de mejoras**: Entre rondas (si el jugador sobrevive)
- **Menú de inventario**: Equipación y gestión de items
- **Menú de opciones**: Gráficos, sonido, interfaz
- **Menú de gestión de guardado**: 3 slots, eliminar partidas

---

## 💾 SISTEMA DE GUARDADO

### 🔐 Características Obligatorias
- **Guardado automático**: Continuo durante el juego
- **3 slots**: Para múltiples partidas
- **Cifrado**: En producción, JSON visualizable en desarrollo
- **Detección de rutas**: Compatible con empaquetado .exe
- **Fallback**: Sistema robusto con recuperación de errores

### 🎯 Comportamiento al Lanzar
- **"Continuar"**: Carga el último slot automáticamente
- **"Nuevo juego"**: Crea archivo limpio
- **"Cargar"**: Selección entre 3 slots disponibles

---

## 🏗️ ARQUITECTURA TÉCNICA

### 🐍 Tecnologías Base
- **Lenguaje**: Python 3.8+
- **Motor**: Pygame-ce 2.4.0+
- **Físicas**: Pymunk 6.6.0+
- **UI**: pygame-menu + pygame-gui
- **Patrón**: Arquitectura modular con separación de responsabilidades

### 📁 Estructura de Directorios
```
src/
├── core/              # Motor del juego (GameEngine, GameState, SceneManager)
├── entities/          # Entidades (Player, Enemy, Projectile, Powerup)
├── scenes/            # Escenas (Welcome, Menu, CharacterSelect, Game, Pause)
├── ui/                # Interfaz (MenuManager, HUD, MenuFactory)
├── utils/             # Utilidades (AssetManager, ConfigManager, Logger)
├── managers/          # Gestores especializados
└── main.py            # Punto de entrada
```

### ⚙️ Configuración Modular
```
config/
├── audio.json         # Configuración de audio
├── characters.json    # Datos de personajes
├── enemies.json       # Tipos de enemigos
├── gameplay.json      # Mecánicas de juego
├── powerups.json      # Tipos de powerups
├── ui.json           # Interfaz de usuario
├── display.json      # Configuración gráfica
└── input.json        # Controles
```

---

## 🤖 REGLAS PARA IA Y DESARROLLO ASISTIDO

### 🎯 Comportamiento de la IA
- **Instrucciones claras**: Evitar redundancia y ambigüedad
- **Herramientas comunitarias**: Priorizar pygame-menu, pygame-gui, pygame-tools
- **Convenciones**: Seguir estándares de Python y pygame
- **Funciones completas**: Propósito claro, comentarios, gestión de errores robusta

### 🔄 Flujo de Desarrollo
- **Análisis antes de implementar**: Entender requisitos completamente
- **Implementación modular**: Dividir en componentes manejables
- **Testing incremental**: Verificar cada componente
- **Documentación continua**: Actualizar README, CHANGELOG, etc.

### 🛠️ Herramientas de Desarrollo
- **Formateo**: Black
- **Linting**: Flake8
- **Type checking**: MyPy
- **Testing**: Pytest
- **Comandos verbose**: Siempre que sea posible

---

## 🎨 SISTEMA DE ASSETS

### 📁 Organización
```
assets/
├── characters/        # Personajes jugables y enemigos
│   ├── used/         # Personajes activos
│   └── unused/       # Personajes no implementados
├── objects/          # Objetos del juego
├── ui/               # Elementos de interfaz
├── sounds/           # Audio del juego
├── fonts/            # Tipografías
└── tiles/            # Texturas del mundo
```

### 🎭 Sistema de Animaciones
- **Detección automática**: FPS basado en frames disponibles
- **Escalado inteligente**: Ajuste automático de tamaños
- **Volteo dinámico**: Basado en dirección de movimiento
- **Caché optimizado**: Gestión eficiente de memoria
- **Placeholders**: Sistema robusto para assets faltantes

---

## 🧪 TESTING Y CALIDAD

### 📊 Objetivos de Calidad
- **Cobertura de tests**: >80%
- **Documentación**: 100% de funciones públicas
- **Mantenibilidad**: <200 líneas por archivo
- **Rendimiento**: 60 FPS estables

### 🛠️ Herramientas de Testing
- **Pytest**: Framework principal
- **Scripts automatizados**: Verificación de funcionalidad
- **Tests visuales**: Verificación de UI y animaciones
- **Tests de rendimiento**: Optimización de sistemas

---

## 📚 DOCUMENTACIÓN Y GESTIÓN

### 📖 Documentación Obligatoria
- **README.md**: Documentación principal del proyecto
- **CHANGELOG.md**: Registro de cambios y versiones
- **COLABORACION.md**: Guías de desarrollo y colaboración
- **commit_message.txt**: Mensajes de commit documentados

### 🔄 Control de Versiones
- **Commits documentados**: Mensajes descriptivos en español
- **Changelog mantenido**: Registro de todas las versiones
- **Backups automáticos**: Sistema de respaldo en directorio backups/
- **Gestión de dependencias**: pyproject.toml actualizado

---

## 🚀 ESTADO ACTUAL Y FUNCIONALIDAD

### ✅ Sistemas Funcionales
- **Motor del juego**: Bucle principal y gestión de eventos
- **Sistema de menús**: Navegación completa entre escenas
- **Selección de personajes**: Interfaz funcional con 3 personajes
- **Sistema de enemigos**: IA de zombies operativa
- **Animaciones**: Sistema completo con detección automática
- **Configuración**: Sistema modular y extensible
- **Logging**: Sistema completo con rotación
- **Guardado**: Sistema de partidas funcional

### 🎮 Flujo Verificado
- **Arranque**: `python src/main.py` sin errores
- **Pantalla de bienvenida**: Botón funcional
- **Menú principal**: Navegación completa
- **Selección de personaje**: Interfaz operativa
- **Juego principal**: Bucle jugable completo
- **Sistema de enemigos**: Spawn y IA funcionando
- **Colisiones**: Sistema de daño operativo

---

## 🎯 MÉTRICAS Y OBJETIVOS

### 📈 Métricas de Progreso
- **Funcionalidad**: 85% completada
- **Estabilidad**: 90% estable
- **Documentación**: 80% completada
- **Testing**: 70% cubierto

### 🚀 Próximos Pasos
- **Consolidar tests**: Eliminar redundancias
- **Optimizar archivos largos**: Refactorización final
- **Ampliar documentación**: Guías de usuario
- **Mejorar rendimiento**: Optimización de sistemas críticos

---

**Documento basado en análisis completo del proyecto SiK Python Game**  
**Versión**: 0.1.3  
**Estado**: Alpha funcional con arquitectura completa  
**Última actualización**: 2024-12-19 