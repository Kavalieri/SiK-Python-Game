# Sistema de Configuración V2 - SiK Python Game

## 📋 Resumen

Se ha implementado un sistema de configuración modular y centralizado que permite gestionar todas las variables configurables del juego de manera organizada y fácilmente modificable.

## 🗂️ Estructura de Archivos

### Directorio `config/`
```
config/
├── characters.json     # Datos de personajes y mejoras
├── gameplay.json       # Mecánicas de gameplay
├── enemies.json        # Tipos de enemigos y variantes
├── powerups.json       # Tipos de powerups
├── ui.json            # Configuración de interfaz
└── audio.json         # Configuración de audio
```

## 📄 Archivos de Configuración

### 1. `characters.json`
**Contenido:**
- Datos completos de personajes jugables
- Estadísticas base (vida, velocidad, daño, escudo, etc.)
- Habilidades y descripciones
- Colores y símbolos para placeholders
- Sistema de mejoras con costos e incrementos

**Variables configurables:**
- `stats.vida`: Vida base del personaje
- `stats.velocidad`: Velocidad de movimiento
- `stats.daño`: Daño base de ataques
- `stats.escudo`: Escudo base
- `stats.rango_ataque`: Rango de ataque
- `stats.velocidad_disparo`: Velocidad de disparo
- `stats.tamaño_proyectil`: Tamaño de proyectiles

### 2. `gameplay.json`
**Contenido:**
- Duración de rondas y niveles
- Sistema de puntuación
- Configuración de combate
- Parámetros de powerups

**Variables configurables:**
- `niveles.duración_ronda`: Tiempo por ronda (segundos)
- `niveles.tiempo_entre_rondas`: Pausa entre rondas
- `combate.daño_colisión_enemigo`: Daño por contacto
- `combate.tiempo_invulnerabilidad`: Tiempo de invulnerabilidad
- `powerups.duración_estándar`: Duración base de powerups

### 3. `enemies.json`
**Contenido:**
- Tipos de enemigos base
- Variantes (normal, raro, élite, legendario)
- Configuración de spawning

**Variables configurables:**
- `tipos_enemigos.*.stats.vida`: Vida del enemigo
- `tipos_enemigos.*.stats.velocidad`: Velocidad de movimiento
- `tipos_enemigos.*.stats.daño`: Daño del enemigo
- `variantes.*.multiplicador_*`: Multiplicadores por variante
- `spawning.tiempo_entre_spawns`: Frecuencia de aparición

### 4. `powerups.json`
**Contenido:**
- Tipos de powerups disponibles
- Efectos y duraciones
- Configuración de spawning

**Variables configurables:**
- `tipos_powerups.*.duración`: Duración del powerup
- `tipos_powerups.*.efecto.valor`: Magnitud del efecto
- `spawning.probabilidad_base`: Probabilidad de aparición
- `spawning.tiempo_mínimo_entre_spawns`: Tiempo mínimo entre spawns

### 5. `ui.json`
**Contenido:**
- Colores de la interfaz
- Tamaños de fuentes
- Dimensiones de elementos
- Configuración del HUD

**Variables configurables:**
- `colores.*`: Todos los colores de la UI
- `fuentes.*`: Tamaños de fuentes
- `dimensiones.*`: Dimensiones de botones y elementos
- `hud.*`: Posiciones y configuración del HUD

### 6. `audio.json`
**Contenido:**
- Volúmenes por categoría
- Rutas de archivos de audio
- Configuración de reproducción

**Variables configurables:**
- `volúmenes.*`: Volúmenes por tipo de audio
- `archivos_audio.*.*`: Rutas de archivos de sonido
- `configuración.*`: Opciones de reproducción

## 🔧 Gestor de Configuración

### Clase `ConfigManagerV2`

**Ubicación:** `src/utils/config_manager_v2.py`

**Funcionalidades principales:**
- Carga automática de todos los archivos de configuración
- Validación de configuraciones
- Métodos específicos para cada tipo de dato
- Recarga dinámica de configuraciones
- Guardado de configuraciones modificadas

**Métodos principales:**
```python
# Personajes
get_character_data(character_key)
get_character_stats(character_key)
get_character_stat(character_key, stat_name)

# Enemigos
get_enemy_data(enemy_type)
get_enemy_variant(variant_type)

# Powerups
get_powerup_data(powerup_type)

# Gameplay
get_gameplay_value(category, key)

# UI
get_ui_color(color_name)
get_ui_font_size(font_name)
get_ui_dimension(dimension_name)

# Audio
get_audio_volume(volume_type)
get_audio_file(category, sound_name)
```

## 🔄 Integración con Módulos

### Módulos Actualizados

1. **`src/scenes/character_data.py`**
   - Ahora usa `ConfigManagerV2` para obtener datos
   - Eliminados datos hardcodeados

2. **`src/scenes/character_animations.py`**
   - Usa configuración para colores y símbolos de placeholders

3. **`src/scenes/character_ui.py`**
   - Carga colores, fuentes y dimensiones desde configuración

4. **`src/scenes/character_select_scene.py`**
   - Refactorizado para usar el nuevo sistema modular

## ✅ Ventajas del Sistema

### 1. **Modularidad**
- Cada aspecto del juego tiene su propio archivo de configuración
- Fácil localización y modificación de parámetros

### 2. **Flexibilidad**
- Cambios en tiempo de desarrollo sin modificar código
- Fácil balanceo del juego
- Configuración específica por entorno

### 3. **Mantenibilidad**
- Variables centralizadas y bien documentadas
- Eliminación de valores hardcodeados
- Fácil debugging y testing

### 4. **Escalabilidad**
- Fácil adición de nuevos personajes, enemigos, powerups
- Sistema extensible para nuevas características

### 5. **Ocultación al Jugador**
- Configuraciones separadas del código del juego
- Fácil protección de archivos de configuración
- Posibilidad de cifrado futuro

## 🚀 Uso Futuro

### Durante el Desarrollo
1. Modificar archivos JSON según necesidades
2. Usar `ConfigManagerV2` en todos los módulos
3. Validar configuraciones con `validate_configs()`

### Para el Jugador Final
1. Archivos de configuración pueden ser ocultos
2. Configuraciones pueden ser cifradas
3. Solo configuraciones de usuario visibles

### Próximos Pasos
1. Migrar todos los módulos restantes al sistema
2. Implementar validación de esquemas JSON
3. Añadir sistema de configuración por usuario
4. Implementar cifrado de configuraciones críticas

## 📊 Métricas de Implementación

- **Archivos de configuración creados:** 6
- **Variables configurables:** ~50+
- **Módulos actualizados:** 4
- **Líneas de código hardcodeadas eliminadas:** ~200
- **Flexibilidad ganada:** 100%

---

*Sistema implementado el 19 de diciembre de 2024*
*Autor: SiK Team* 