# Plan de Migración a SQLite - SiK Python Game

## 🔗 Referencias Cruzadas Actualizadas
- **Documento Central**: [`docs/REFACTORIZACION_ESTADO_ACTUAL.md`](./REFACTORIZACION_ESTADO_ACTUAL.md) - Estado actualizado sin redundancias
- **Funciones Catalogadas**: [`docs/FUNCIONES_DOCUMENTADAS.md`](./FUNCIONES_DOCUMENTADAS.md) - Funciones por módulo
- **Proyecto SQLite**: [`docs/PROYECTO_MIGRACION_SQLITE.md`](./PROYECTO_MIGRACION_SQLITE.md) - Plan ejecutivo del proyecto
- **Instrucciones Base**: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) - Reglas del proyecto

## 🎯 CAMBIO DE PRIORIDAD: SQLite y Eliminación de Hardcodeo

### 🚨 Problema Crítico Identificado
El proyecto tiene **duplicaciones masivas** entre configuración JSON y código hardcodeado que requieren un **sistema mixto inteligente**:
- **characters.json** (189 líneas, 4,875 caracteres) ↔ **character_data.py** (152 líneas) → **MIGRAR A SQLite**
- **enemies.json** (73 líneas, 1,901 caracteres) ↔ **enemy_types.py** (230 líneas) → **MIGRAR A SQLite**
- **powerups.json** (106 líneas, 2,780 caracteres) ↔ **powerup.py** (161 líneas) → **SEPARAR**: config JSON + lógica Python
- **gameplay.json** (34 líneas, 769 caracteres) ↔ Múltiples archivos de escenas → **MANTENER JSON**, eliminar hardcodeo
- **audio.json** (32 líneas, 969 caracteres) ↔ Módulos de audio → **MANTENER JSON**, usar configuración

### ⚡ Nueva Estrategia: Sistema Mixto Inteligente
1. **SQLite para datos complejos**: Partidas, personajes, enemigos, estadísticas
2. **Archivos JSON para configuración**: Variables modificables, configuración de usuario
3. **Eliminar hardcodeo**: Separar lógica de configuración completamente
4. **Optimización posterior**: Solo después de funcionalidad operativa

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

### ✅ FASE 1: Infraestructura SQLite (COMPLETADA ✅)
**Objetivo**: Base SQLite funcional sin romper sistema actual
**Estado**: Sistema modular implementado y funcional

#### Componentes Implementados:
- [x] **DatabaseManager** (169 líneas) - Gestor principal ✅
- [x] **SchemaManager** (169 líneas) - Manager de esquemas ✅
- [x] **SchemaCore** (164 líneas) - Núcleo del sistema ✅
- [x] **SchemaTables** (160 líneas) - Definiciones de tablas ✅
- [x] **SchemaMigrations** (171 líneas) - Sistema de migraciones ✅

#### Funcionalidades Operativas:
- [x] Connection pooling SQLite optimizado
- [x] Sistema completo de tablas definido
- [x] Migraciones automáticas de esquema
- [x] Validación de integridad
- [x] Backup automático antes de cambios
- [x] Testing básico completado (`scripts/test_simple_sqlite.py`)

**📊 RESULTADO**: Infraestructura SQLite lista para migración de datos

### 🔥 FASE 2: Migración de Configuraciones (EN PROCESO)
**Objetivo**: Migrar JSON hardcodeado a SQLite como fuente única
**Prioridad**: CRÍTICA - Eliminar duplicaciones masivas

#### 📊 Duplicaciones Identificadas:
1. **characters.json** (189 líneas) ↔ **character_data.py** (152 líneas)
   - **Problema**: Datos idénticos en dos formatos diferentes
   - **Solución**: SQLite como fuente única, eliminar character_data.py
   - **Impacto**: 4,875 caracteres de configuración vs código hardcodeado

2. **enemies.json** (73 líneas) ↔ **enemy_types.py** (230 líneas)
   - **Problema**: Inconsistencias críticas entre JSON y código
   - **Solución**: Migrar a tabla `enemigos`, usar solo SQLite
   - **Impacto**: 1,901 caracteres JSON vs 230 líneas Python

3. **powerups.json** (106 líneas) ↔ **powerup.py** (161 líneas)
   - **Problema**: Duplicación parcial con lógica mezclada
   - **Solución**: Separar configuración (SQLite) de lógica (Python)
   - **Impacto**: 2,780 caracteres de configuración

#### ⚡ Plan de Implementación Inmediata:

##### PASO 1: Sistema Mixto Inteligente (INMEDIATO)
- [ ] **Implementar ConfigDatabase** - Nueva interfaz SQLite para datos complejos
- [ ] **Migrar characters.json → tabla personajes** (eliminar character_data.py hardcodeado)
- [ ] **Migrar enemies.json → tabla enemigos** (eliminar enemy_types.py hardcodeado)
- [ ] **Mantener powerups.json** como configuración, eliminar hardcodeo en powerup.py
- [ ] **Mantener gameplay.json** como configuración, eliminar valores hardcodeados en escenas
- [ ] **Sistema de compatibilidad** durante la transición

##### PASO 2: Eliminación de Hardcodeo (1-2 días)
- [ ] **Modificar character_data.py** - Leer desde SQLite en lugar de diccionario hardcodeado
- [ ] **Refactorizar enemy_types.py** - Usar tabla SQLite enemigos
- [ ] **Actualizar powerup.py** - Separar completamente lógica de configuración JSON
- [ ] **Actualizar escenas de juego** - Usar gameplay.json en lugar de valores hardcodeados
- [ ] **Testing completo** - Verificar funcionalidad idéntica con nuevo sistema

##### PASO 3: Sistema Unificado (2-3 días)
- [ ] **API híbrida de configuración** - ConfigManager que use SQLite + JSON según corresponda
- [ ] **Documentación de criterios** - Cuándo usar SQLite vs JSON
- [ ] **Optimización del sistema** - Caché inteligente y performance
- [ ] **Documentación actualizada** - Nuevas funciones en FUNCIONES_DOCUMENTADAS.md

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

## 📊 Elementos del Sistema Mixto

### 🗄️ Migrar a SQLite
- **Partidas guardadas**: nivel, puntuación, vidas, tiempo (reemplaza pickle)
- **Datos de personajes**: stats, ataques, animaciones (reemplaza character_data.py hardcodeado)
- **Configuración de enemigos**: tipos, comportamientos, stats (reemplaza enemy_types.py hardcodeado)
- **Estadísticas de juego**: enemigos eliminados, disparos, tiempo por sesión
- **Metadata de partidas**: timestamp, descripción, slot

### 📄 Mantener en JSON
- **Configuración de usuario**: volúmenes, efectos (audio.json)
- **Configuración de pantalla**: resolución, fullscreen (display.json)
- **Configuración de controles**: teclas, sensibilidad (input.json)
- **Balance de gameplay**: timers, multiplicadores, probabilidades (gameplay.json)
- **Configuración de powerups**: duraciones, efectos, spawn rates (powerups.json)
- **Configuración de UI**: colores, dimensiones, fuentes (ui.json)

### ❌ Eliminar Hardcodeo de
- **character_data.py**: Diccionario CHARACTER_DATA → usar SQLite
- **enemy_types.py**: Clases hardcodeadas → usar SQLite + lógica separada
- **Escenas de juego**: Valores hardcodeados → usar gameplay.json
- **Módulos de audio**: Configuración hardcodeada → usar audio.json
- **Sistemas de powerup**: Stats hardcodeados → usar powerups.json

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
