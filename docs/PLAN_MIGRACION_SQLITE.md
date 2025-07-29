# Plan de Migración a SQLite - SiK Python Game

## � Referencias Cruzadas
- **Documento Central**: [`docs/refactorizacion_progreso.md`](./refactorizacion_progreso.md) - Estado y checklist de refactorización
- **Funciones Catalogadas**: [`docs/FUNCIONES_DOCUMENTADAS.md`](./FUNCIONES_DOCUMENTADAS.md) - Funciones por módulo
- **Índice Rápido**: [`docs/INDICE_MIGRACION_SQLITE.md`](./INDICE_MIGRACION_SQLITE.md) - Vista general del progreso
- **Instrucciones Base**: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) - Reglas del proyecto

## �📋 Estado Actual de Persistencia

### Sistemas Identificados
1. **SaveManager** (365 líneas) - Crítico para refactorización
   - Formato: pickle + zlib + XOR encryption
   - 3 slots de guardado (slot_1.save, slot_2.save, slot_3.save)
   - Metadata con timestamp y descripción
   - Encriptación personalizada

2. **ConfigManager** (264 líneas) - Crítico para refactorización
   - Configuraciones modulares en JSON
   - Archivos: characters.json, enemies.json, gameplay.json, etc.
   - Sistema de validación y carga dinámica

3. **GameState** (151 líneas) - Límite excedido
   - Gestión de estado de juego en tiempo real
   - Score, vidas, nivel, configuraciones
   - Referencias a jugador y entidades

## 🗄️ Esquema SQLite Propuesto

### Tabla 1: partidas_guardadas
```sql
CREATE TABLE partidas_guardadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot INTEGER NOT NULL CHECK(slot IN (1, 2, 3)),
    nombre_jugador TEXT NOT NULL,
    descripcion TEXT,
    nivel_actual INTEGER DEFAULT 1,
    puntuacion INTEGER DEFAULT 0,
    vidas INTEGER DEFAULT 3,
    tiempo_jugado INTEGER DEFAULT 0, -- segundos
    personaje TEXT NOT NULL, -- 'guerrero', etc.
    estado_juego TEXT, -- JSON serializado del estado completo
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(slot)
);
```

### Tabla 2: configuraciones
```sql
CREATE TABLE configuraciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL, -- 'audio', 'display', 'input', etc.
    clave TEXT NOT NULL,
    valor TEXT NOT NULL, -- JSON para objetos complejos
    tipo TEXT NOT NULL CHECK(tipo IN ('string', 'number', 'boolean', 'object')),
    descripcion TEXT,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(categoria, clave)
);
```

### Tabla 3: personajes
```sql
CREATE TABLE personajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL, -- 'guerrero', etc.
    nombre_mostrar TEXT NOT NULL, -- 'Kava'
    tipo TEXT NOT NULL, -- 'Melee', 'Ranged'
    descripcion TEXT,
    stats TEXT NOT NULL, -- JSON: vida, velocidad, daño, etc.
    ataques TEXT NOT NULL, -- JSON array de ataques
    sprite_config TEXT, -- JSON: rutas de sprites y animaciones
    activo BOOLEAN DEFAULT 1,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla 4: enemigos
```sql
CREATE TABLE enemigos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT UNIQUE NOT NULL, -- 'zombie_male', 'zombie_female'
    nombre_mostrar TEXT NOT NULL,
    stats TEXT NOT NULL, -- JSON: vida, velocidad, daño, rangos
    comportamiento TEXT NOT NULL, -- 'perseguir', 'patrullar'
    animaciones TEXT NOT NULL, -- JSON: idle, walk, attack, dead
    variantes TEXT, -- JSON: normal, raro, élite, legendario
    activo BOOLEAN DEFAULT 1,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla 5: estadisticas_juego
```sql
CREATE TABLE estadisticas_juego (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_partida INTEGER NOT NULL,
    tipo_estadistica TEXT NOT NULL, -- 'enemigos_eliminados', 'disparos_acertados', etc.
    valor INTEGER NOT NULL,
    sesion_id TEXT, -- UUID para agrupar estadísticas por sesión
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slot_partida) REFERENCES partidas_guardadas(slot)
);
```

### Tabla 6: configuracion_gameplay
```sql
CREATE TABLE configuracion_gameplay (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL, -- 'niveles', 'combate', 'powerups', 'puntuación'
    configuracion TEXT NOT NULL, -- JSON completo de la categoría
    version INTEGER DEFAULT 1,
    activo BOOLEAN DEFAULT 1,
    actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Plan de Migración en Fases - CHECKLIST

### ✅ FASE 1: Preparación e Infraestructura (Prioridad Crítica)
**Objetivo**: Crear base SQLite sin romper sistema actual
**📋 Referencia**: [Progreso Refactorización - Fase 1](./refactorizacion_progreso.md#fase-1---urgente)

- [ ] **Crear DatabaseManager** (máximo 150 líneas)
  - [ ] Conexión SQLite con connection pooling
  - [ ] Métodos base: conectar, desconectar, ejecutar_query
  - [ ] Manejo de transacciones
  - [ ] Logging de operaciones
  - [ ] Documentar en [FUNCIONES_DOCUMENTADAS.md](./FUNCIONES_DOCUMENTADAS.md)

- [ ] **Crear SchemaManager** (máximo 150 líneas)
  - [ ] Creación automática de tablas
  - [ ] Migraciones de esquema
  - [ ] Validación de integridad
  - [ ] Backup automático antes de cambios
  - [ ] Documentar en [FUNCIONES_DOCUMENTADAS.md](./FUNCIONES_DOCUMENTADAS.md)

- [ ] **Testing paralelo**
  - [ ] Base de datos de pruebas
  - [ ] Validación de rendimiento vs pickle
  - [ ] Tests de integridad de datos
  - [ ] Actualizar [refactorizacion_progreso.md](./refactorizacion_progreso.md)

### 🔥 FASE 2: Migración del ConfigManager (Dividir + Migrar)
**Objetivo**: Mover configuraciones JSON a SQLite
**📋 Referencia**: [Progreso Refactorización - Fase 2](./refactorizacion_progreso.md#fase-2---alta-prioridad)

- [ ] **Dividir ConfigManager** en módulos:
  - [ ] `config_loader.py` (máximo 150 líneas) - Carga desde archivos
  - [ ] `config_database.py` (máximo 150 líneas) - Interfaz SQLite
  - [ ] `config_validator.py` (máximo 150 líneas) - Validaciones
  - [ ] Actualizar [FUNCIONES_DOCUMENTADAS.md](./FUNCIONES_DOCUMENTADAS.md)

- [ ] **Migración de datos**:
  - [ ] characters.json → tabla personajes
  - [ ] enemies.json → tabla enemigos
  - [ ] gameplay.json → tabla configuracion_gameplay
  - [ ] audio.json, display.json, etc. → tabla configuraciones
  - [ ] Proceso automático: `migrar_configuraciones_a_sqlite()`

- [ ] **Compatibilidad dual**:
  - [ ] Leer desde SQLite primero
  - [ ] Fallback a JSON si falla
  - [ ] Modo de migración progresiva
  - [ ] Actualizar [refactorizacion_progreso.md](./refactorizacion_progreso.md)

### 📊 FASE 3: Migración del SaveManager (Dividir + Migrar)
**Objetivo**: Reemplazar pickle con SQLite manteniendo encriptación
**📋 Referencia**: [Progreso Refactorización - Fase 3](./refactorizacion_progreso.md#fase-3---crítica)

- [ ] **Dividir SaveManager** en módulos:
  - [ ] `save_loader.py` (máximo 150 líneas) - Carga/guardado
  - [ ] `save_encryption.py` (máximo 150 líneas) - Encriptación XOR
  - [ ] `save_database.py` (máximo 150 líneas) - Interfaz SQLite
  - [ ] `save_compatibility.py` (máximo 150 líneas) - Migración desde pickle
  - [ ] Actualizar [FUNCIONES_DOCUMENTADAS.md](./FUNCIONES_DOCUMENTADAS.md)

- [ ] **Proceso de migración**:
  - [ ] Migración automática: `migrar_saves_pickle_a_sqlite()`
  - [ ] Mantener compatibilidad con saves antiguos
  - [ ] Encriptar campos sensibles en SQLite

- [ ] **Mejoras en funcionalidad**:
  - [ ] Guardado automático cada X minutos
  - [ ] Historial de partidas por slot
  - [ ] Estadísticas detalladas por sesión
  - [ ] Backup automático preparado para futuro
  - [ ] Actualizar [refactorizacion_progreso.md](./refactorizacion_progreso.md)

### ⚡ FASE 4: Migración del GameState (Refactorizar + Integrar)
**Objetivo**: Dividir GameState e integrar con SQLite
**📋 Referencia**: [Progreso Refactorización - Archivos Críticos](./refactorizacion_progreso.md#archivos-más-críticos)

- [ ] **Dividir GameState** en módulos:
  - [ ] `game_state_core.py` (máximo 150 líneas) - Estado básico
  - [ ] `game_state_persistence.py` (máximo 150 líneas) - Guardado/carga
  - [ ] `game_state_statistics.py` (máximo 150 líneas) - Estadísticas
  - [ ] Actualizar [FUNCIONES_DOCUMENTADAS.md](./FUNCIONES_DOCUMENTADAS.md)

- [ ] **Integración con SQLite**:
  - [ ] Estado persistente en `partidas_guardadas`
  - [ ] Estadísticas en tiempo real en `estadisticas_juego`
  - [ ] Sincronización automática
  - [ ] Finalizar actualización [refactorizacion_progreso.md](./refactorizacion_progreso.md)

## 📊 Elementos a Migrar Identificados

### Desde SaveManager (pickle → SQLite)
- **Datos de partida**: nivel, puntuación, vidas, tiempo
- **Estado del jugador**: posición, inventario, mejoras
- **Configuraciones de partida**: dificultad, personaje seleccionado
- **Metadata**: timestamp, descripción, slot

### Desde ConfigManager (JSON → SQLite)
- **Personajes**: stats, ataques, animaciones (characters.json)
- **Enemigos**: tipos, comportamientos, stats (enemies.json)
- **Gameplay**: niveles, combate, powerups (gameplay.json)
- **Audio**: volúmenes, efectos (audio.json)
- **Display**: resolución, fullscreen (display.json)
- **Input**: controles, sensibilidad (input.json)

### Desde GameState (memoria → SQLite + memoria)
- **Estado temporal**: score actual, vidas actuales
- **Estadísticas**: enemigos eliminados, disparos, tiempo
- **Referencias**: entidades activas (no persistir)

## 🔧 Herramientas de Migración

### Script de Migración Automática
```python
# scripts/migrate_to_sqlite.py
def migrar_todo_a_sqlite():
    """Migración completa del sistema actual a SQLite"""
    # Backup completo del estado actual
    crear_backup_completo()

    # Migrar configuraciones
    migrar_configuraciones()

    # Migrar saves existentes
    migrar_saves_existentes()

    # Validar integridad
    validar_migracion()

    # Generar reporte
    generar_reporte_migracion()
```

### Validaciones de Integridad
- Comparar datos migrados vs originales
- Verificar funcionalidad completa post-migración
- Tests automatizados de carga/guardado
- Benchmark de rendimiento

## 📈 Beneficios de la Migración

### Inmediatos
- **Mejor rendimiento**: Queries específicos vs carga completa
- **Menor uso de memoria**: Carga selectiva de datos
- **Integridad de datos**: Constraints y validaciones SQL
- **Backup incrementales**: Solo cambios recientes

### A Largo Plazo
- **Analytics avanzados**: Estadísticas detalladas de juego
- **Sincronización**: Múltiples dispositivos (futuro)
- **Modding**: API de base de datos para mods
- **Escalabilidad**: Preparado para multijugador

## 🎯 Cronograma Estimado

| Fase | Duración | Entregables |
|------|----------|-------------|
| Fase 1 | 2-3 días | DatabaseManager, SchemaManager, Tests |
| Fase 2 | 3-4 días | ConfigManager dividido + migrado |
| Fase 3 | 4-5 días | SaveManager dividido + migrado |
| Fase 4 | 2-3 días | GameState dividido + integrado |
| **Total** | **11-15 días** | **Sistema completo migrado** |

## 🚨 Consideraciones Críticas

### Compatibilidad Durante Migración
- **Dual-mode**: SQLite + fallback a sistema actual
- **Migración gradual**: Funcionalidad por funcionalidad
- **Rollback**: Posibilidad de volver al sistema anterior

### Refactorización Simultánea
- **Prioridad 1**: Dividir archivos >150 líneas
- **Prioridad 2**: Migrar datos a SQLite
- **Mantener**: Funcionalidad completa en todo momento

### Backup y Seguridad
- **Backup automático**: Antes de cada migración
- **Encriptación**: Mantener XOR para datos sensibles
- **Versionado**: SQLite schema con versiones

---

**✅ PLAN LISTO PARA IMPLEMENTACIÓN**

Este plan garantiza:
- ✅ Refactorización de archivos críticos (SaveManager 365→4x150 líneas)
- ✅ Migración completa de persistencia a SQLite
- ✅ Compatibilidad durante todo el proceso
- ✅ Mejoras significativas en rendimiento y funcionalidad
- ✅ Base sólida para futuras características avanzadas

Siguiente paso: ¿Comenzamos con la Fase 1 (DatabaseManager + SchemaManager)?
