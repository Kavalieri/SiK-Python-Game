# Criterios del Sistema Mixto - SiK Python Game

## 🎯 Objetivo del Sistema Mixto
Utilizar la tecnología más apropiada para cada tipo de dato y configuración, optimizando eficiencia, mantenibilidad y flexibilidad.

## 🗄️ Usar SQLite Para:

### ✅ Datos que Requieren Persistencia
- **Partidas guardadas**: Slots, progreso, estadísticas
- **Historiales de juego**: Mejores puntuaciones, tiempo jugado
- **Datos de personajes**: Stats, habilidades, ataques (que no cambian frecuentemente)
- **Configuración de enemigos**: Tipos, comportamientos, stats

### ✅ Datos que Requieren Consultas Complejas
- **Estadísticas de juego**: Filtros por fecha, tipo, jugador
- **Analytics**: Métricas de comportamiento, análisis de rendimiento
- **Búsquedas**: Personajes por tipo, enemigos por nivel
- **Relaciones entre datos**: Personaje → ataques → efectos

### ✅ Datos que Requieren Integridad Referencial
- **Relaciones padre-hijo**: Personaje → habilidades
- **Constraints**: Validaciones de datos complejas
- **Transacciones**: Operaciones que deben ser atómicas

### ✅ Datos que Crecen Dinámicamente
- **Logs de eventos**: Se acumulan con el tiempo
- **Estadísticas por sesión**: Se generan cada partida
- **Historiales**: Crecen indefinidamente

## 📄 Usar Archivos de Configuración (JSON) Para:

### ✅ Configuración de Usuario
- **Volúmenes**: Música, efectos, voces
- **Controles**: Mapeo de teclas, sensibilidad
- **Pantalla**: Resolución, fullscreen, vsync
- **Preferencias**: Idioma, dificultad por defecto

### ✅ Variables Frecuentemente Modificadas
- **Balance de juego**: Velocidades, daños, duraciones
- **Tiempos y cooldowns**: Spawn rates, recarga de habilidades
- **Probabilidades**: Chance de drop, spawn de powerups
- **Multiplicadores**: Puntuación, experiencia

### ✅ Configuración de Desarrollo
- **Rutas de assets**: Directorios de sprites, sonidos
- **Opciones de debug**: Logging, visualizaciones
- **Configuración por entorno**: Desarrollo vs producción

### ✅ Datos Simples y Estáticos
- **Colores de UI**: Paletas, themes
- **Dimensiones**: Tamaños de botones, márgenes
- **Textos estáticos**: Títulos, mensajes de error
- **Configuración de animaciones**: FPS, transiciones

## ❌ Eliminar Completamente (Hardcodeo):

### ❌ Diccionarios en Código Python
- **CHARACTER_DATA** en character_data.py → SQLite tabla personajes
- **ENEMY_TYPES** en enemy_types.py → SQLite tabla enemigos
- **Configuraciones hardcodeadas** en cualquier archivo .py

### ❌ Valores Mágicos
- **Números hardcodeados**: 100, 50, 0.5 → configuración JSON
- **Strings hardcodeados**: "Warrior", "Fast" → configuración
- **Configuración mezclada con lógica**: Separar completamente

### ❌ Duplicaciones
- **Mismos datos en JSON y Python**: Elegir una fuente única
- **Configuraciones repetidas**: Centralizar en un lugar
- **Lógica duplicada**: Reutilizar funciones comunes

## 🔧 Criterios de Decisión

### ¿Cuándo usar SQLite?
1. **¿Los datos crecen con el tiempo?** → SQLite
2. **¿Necesito hacer consultas complejas?** → SQLite
3. **¿Los datos tienen relaciones?** → SQLite
4. **¿Necesito transacciones?** → SQLite
5. **¿Es información del jugador/partida?** → SQLite

### ¿Cuándo usar JSON?
1. **¿El usuario puede modificarlo?** → JSON
2. **¿Cambia frecuentemente en desarrollo?** → JSON
3. **¿Es configuración simple?** → JSON
4. **¿No necesita consultas complejas?** → JSON
5. **¿Es mejor editable en texto plano?** → JSON

### ¿Cuándo eliminar hardcodeo?
1. **¿Está duplicado en otro lugar?** → Eliminar
2. **¿Es un valor mágico?** → Mover a configuración
3. **¿Podría cambiar en el futuro?** → Externalizar
4. **¿Dificulta el mantenimiento?** → Separar lógica de datos

## 📊 Ejemplos de Aplicación

### ✅ Migrar a SQLite
```python
# ANTES (hardcodeado)
CHARACTER_DATA = {
    "guerrero": {"vida": 100, "velocidad": 50}
}

# DESPUÉS (SQLite)
def get_character_data(name):
    return db.query("SELECT * FROM personajes WHERE nombre = ?", [name])
```

### ✅ Mantener en JSON
```json
// gameplay.json
{
    "powerups": {
        "speed_boost_duration": 5.0,
        "damage_multiplier": 2.0,
        "spawn_probability": 0.1
    }
}
```

### ✅ Eliminar Hardcodeo
```python
# ANTES
SPEED_BOOST_DURATION = 5.0  # Hardcodeado

# DESPUÉS
config = load_config("gameplay.json")
duration = config["powerups"]["speed_boost_duration"]
```

## 🎯 Resultado Esperado
- **Flexibilidad**: Cada tipo de dato usa la tecnología óptima
- **Mantenibilidad**: Separación clara entre lógica y configuración
- **Eficiencia**: Consultas SQL para datos complejos, JSON para configuración simple
- **Escalabilidad**: Base sólida para características futuras
- **Consistencia**: Eliminación total de duplicaciones y hardcodeo
