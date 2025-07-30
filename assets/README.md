# assets/ - Recursos del Juego

## 🎨 **PROPÓSITO**
Directorio centralizado que contiene todos los recursos gráficos, audio y visuales del videojuego **SiK Python Game**. Organizado por tipo de recurso para facilitar el desarrollo y la gestión de assets.

## 📊 **ESTADO ACTUAL**
- **6 categorías principales** de recursos organizados
- **Sistema de nomenclatura**: Archivos organizados y limpios
- **Integración con código**: Carga automática mediante AssetManager
- **Assets optimizados**: Resoluciones y formatos apropiados para 2D

---

## 🗂️ **ESTRUCTURA DE RECURSOS**

### 👥 **`characters/` - Personajes y Animaciones**
```
characters/
├── used/          # Personajes activos del juego
│   ├── adventureguirl/
│   ├── guerrero/
│   └── robot/
└── unused/        # Personajes en desarrollo o descartados
```

#### 🎮 **Personajes Activos (used/)**
- **adventureguirl**: Personaje femenino aventurera
  - Animaciones: idle, run, attack, hurt, dead
  - Formato: PNG secuencial por animación
  - Resolución: ~64x64 píxeles

- **guerrero**: Personaje principal guerrero
  - Animaciones: idle, run, attack, hurt, dead
  - Formato: PNG secuencial por animación
  - Resolución: ~64x64 píxeles

- **robot**: Personaje robótico futurista
  - Animaciones: idle, run, attack, hurt, dead
  - Formato: PNG secuencial por animación
  - Resolución: ~64x64 píxeles

#### 📝 **Convención de Nomenclatura**
```
[personaje]/[animacion]/[personaje]_[animacion]_[frame].png
Ejemplo: guerrero/idle/guerrero_idle_1.png
```

### 🎵 **`sounds/` - Audio del Juego**
```
sounds/
├── background_music.mp3    # Música de fondo principal
├── explosion.wav          # Efecto de explosión
└── shoot.wav              # Efecto de disparo
```

#### 🔊 **Archivos de Audio**
- **background_music.mp3**: Música ambiental del juego
  - Formato: MP3, calidad media
  - Duración: Loop continuo
  - Uso: Reproducción de fondo en gameplay

- **explosion.wav**: Efectos de explosión
  - Formato: WAV, alta calidad
  - Duración: Corta (~1 segundo)
  - Uso: Destrucción de enemigos

- **shoot.wav**: Efectos de disparo
  - Formato: WAV, alta calidad
  - Duración: Muy corta (~0.3 segundos)
  - Uso: Disparos del jugador

### 🏺 **`objects/` - Objetos del Mundo**
```
objects/
├── elementos/     # Elementos de decoración del mundo
├── proyectiles/   # Sprites de proyectiles y balas
└── varios/        # Objetos misceláneos
```

#### 🌍 **Elementos del Mundo (elementos/)**
Decoraciones y objetos interactivos distribuidos por el escenario:
- **Vegetación**: árboles, arbustos, cactus
- **Rocas**: diferentes tamaños y formas
- **Estructuras**: ruinas, elementos arquitectónicos
- **Formato**: PNG con transparencia
- **Uso**: WorldGenerator para poblado automático

#### 🎯 **Proyectiles (proyectiles/)**
Sprites para diferentes tipos de munición:
- **Balas**: disparos estándar del jugador
- **Proyectiles especiales**: munición mejorada
- **Efectos**: trails y partículas
- **Formato**: PNG pequeños (~16x16 píxeles)

### 🎨 **`ui/` - Elementos de Interfaz**
```
ui/
├── Health_XX_BarXX.png    # Barras de vida (diferentes estilos)
├── Health_XX.png          # Iconos de vida
├── Hearts_Blue_X.png      # Corazones azules (1-5)
├── Hearts_Red_X.png       # Corazones rojos (1-5)
├── Equipo.png             # Icono de equipo
└── [otros elementos UI]
```

#### 💚 **Sistema de Vida**
- **Health_01_BarXX.png**: Barra de vida estilo 1 (3 estados)
- **Health_03_BarXX.png**: Barra de vida estilo 3 (3 estados)
- **Hearts_Blue/Red_X.png**: Corazones numerados 1-5
- **Uso**: HUD para mostrar vida del jugador

#### 🎮 **Elementos de UI**
- **Botones**: Estados normal, hover, pressed
- **Iconos**: Inventario, menús, indicadores
- **Barras**: Progreso, experiencia, munición
- **Formato**: PNG con transparencia

### 🧩 **`tiles/` - Baldosas del Escenario**
```
tiles/
├── 1.png          # Baldosa tipo 1
├── 2.png          # Baldosa tipo 2
├── ...
└── 16.png         # Baldosa tipo 16
```

#### 🗺️ **Sistema de Tiles**
- **16 tipos diferentes** de baldosas numeradas
- **Formato**: PNG cuadrado (~32x32 píxeles)
- **Uso**: Construcción de niveles y escenarios
- **Integración**: TileSystem para generación de mapas

### 🔤 **`fonts/` - Fuentes del Juego**
```
fonts/
├── arcade.ttf     # Fuente principal estilo arcade
└── README.txt     # Información sobre fuentes
```

#### ✍️ **Fuentes Disponibles**
- **arcade.ttf**: Fuente principal del juego
  - Estilo: Retro/arcade clásico
  - Uso: Títulos, menús, HUD
  - Licencia: Ver README.txt

---

## 🔧 **INTEGRACIÓN CON EL CÓDIGO**

### 📖 **AssetManager - Carga Automática**
```python
# Sistema modular de carga de assets
asset_manager = AssetManager("assets")

# Carga de personajes
sprite = asset_manager.get_character_sprite("guerrero", "idle", frame=1)

# Carga de UI
button = asset_manager.get_ui_button("start", state="normal")

# Carga genérica
image = asset_manager.load_image("objects/elementos/tree1.png")
```

### 🎮 **Sistemas que Usan Assets**

#### **CharacterAssets (src/utils/character_assets.py)**
- Carga animaciones de personajes secuencialmente
- Cache inteligente para optimizar memoria
- Soporte para múltiples escalas y resoluciones

#### **UIAssets (src/utils/ui_assets.py)**
- Gestión de elementos de interfaz
- Estados de botones automáticos
- Carga de barras de vida y indicadores

#### **WorldGenerator (src/utils/world_generator.py)**
- Carga automática desde `objects/elementos/`
- Distribución aleatoria de decoraciones
- Sistema de clusters temáticos

#### **AudioManager (src/managers/audio_manager.py)**
- Carga de música y efectos de sonido
- Control de volúmenes por categoría
- Reproducción con cache y memoria optimizada

---

## 🎯 **CONVENCIONES Y ESTÁNDARES**

### 📁 **Organización de Archivos**
- **Categorización clara**: Por tipo de recurso
- **Subcategorías lógicas**: Por función o tema
- **Nomenclatura consistente**: [categoria]_[tipo]_[variante]
- **Separación used/unused**: Para desarrollo iterativo

### 🖼️ **Formatos de Imagen**
- **PNG**: Para sprites con transparencia
- **Tamaños estándar**:
  - Personajes: 64x64px
  - UI: Variable según elemento
  - Tiles: 32x32px
  - Objetos: Variable según escala

### 🎵 **Formatos de Audio**
- **MP3**: Para música de fondo (tamaño optimizado)
- **WAV**: Para efectos de sonido (calidad alta)
- **Volúmenes normalizados**: Consistencia en niveles de audio

### 🔤 **Fuentes**
- **TTF**: Formato estándar multiplataforma
- **Licencias claras**: Documentación de uso permitido
- **Fallbacks**: Fuentes del sistema como respaldo

---

## 🚀 **DESARROLLO Y EXPANSIÓN**

### 📈 **Assets Futuros**
- **Más personajes**: Expansión del roster jugable
- **Enemigos visuales**: Sprites para tipos de enemigos
- **Efectos de partículas**: Explosiones, humo, magia
- **Backgrounds dinámicos**: Fondos animados por capas
- **Música adicional**: Temas para diferentes niveles

### 🎨 **Mejoras Planificadas**
- **Animaciones mejoradas**: Más frames para fluidez
- **Efectos visuales**: Shaders y post-procesado
- **Audio dinámico**: Música adaptativa al gameplay
- **Assets modulares**: Sistema de combinación de elementos

### 🔧 **Herramientas de Asset Pipeline**
- **Scripts de optimización**: Compresión automática
- **Validación de assets**: Verificación de formatos
- **Generación procedural**: Variantes automáticas
- **Asset bundling**: Empaquetado para distribución

---

## 📊 **MÉTRICAS Y OPTIMIZACIÓN**

### 📈 **Uso de Memoria**
- **Cache inteligente**: Solo assets necesarios en memoria
- **Lazy loading**: Carga bajo demanda
- **Garbage collection**: Liberación automática de recursos
- **Streaming**: Para assets grandes (futuro)

### ⚡ **Rendimiento**
- **Formatos optimizados**: PNG comprimido para sprites
- **Resoluciones apropiadas**: Balance calidad/tamaño
- **Batch loading**: Carga en lotes para eficiencia
- **Preloading selectivo**: Assets críticos pre-cargados

---

## 🔗 **REFERENCIAS**

### 📖 **Documentación Técnica**
- **AssetManager**: `src/utils/asset_manager.py`
- **Configuración**: `config/animations.json`
- **Audio**: `config/audio.json`

### 🎮 **Uso en Juego**
- **Personajes**: Sistemas de animación y combat
- **UI**: Interfaces y menús del juego
- **Mundo**: Generación procedural de escenarios
- **Audio**: Ambientación y feedback del jugador

---

**🎨 ESTADO**: ✅ ASSETS ORGANIZADOS Y SISTEMA DE CARGA OPERATIVO
**📅 ÚLTIMA ACTUALIZACIÓN**: 30 de Julio, 2025
**🎯 ENFOQUE**: Recursos optimizados para desarrollo 2D bullet hell
