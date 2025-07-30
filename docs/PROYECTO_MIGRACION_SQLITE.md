# Proyecto Migración SQLite - SiK Python Game

## 📋 Información del Proyecto
**Nombre**: Migración SQLite y Eliminación de Hardcodeo
**Fecha de Inicio**: 30 de Julio, 2025
**Prioridad**: CRÍTICA - Funcionalidad sobre optimización
**Estado**: INICIADO - Infraestructura completa, migración en proceso

## 🎯 Objetivo Principal
**Implementar un sistema mixto inteligente** que elimine las duplicaciones críticas entre archivos JSON y código Python hardcodeado, utilizando:
- **SQLite**: Para datos que requieren persistencia, consultas complejas y almacenamiento
- **Archivos de configuración**: Para variables frecuentemente modificadas y configuraciones simples
- **Eliminación total del hardcodeo**: Separar completamente lógica de configuración

## 📊 Análisis de Duplicaciones Críticas

### 🚨 Problemas Identificados
1. **characters.json** (189 líneas, 4,875 chars) ↔ **character_data.py** (152 líneas)
   - **Impacto**: Duplicación total de datos de personajes
   - **Problema**: Cambios deben hacerse en dos lugares
   - **Riesgo**: Inconsistencias entre JSON y Python

2. **enemies.json** (73 líneas, 1,901 chars) ↔ **enemy_types.py** (230 líneas)
   - **Impacto**: Inconsistencias críticas en estadísticas
   - **Problema**: enemy_types.py ignora enemies.json
   - **Riesgo**: Comportamiento impredecible

3. **powerups.json** (106 líneas, 2,780 chars) ↔ **powerup.py** (161 líneas)
   - **Impacto**: Lógica mezclada con configuración
   - **Problema**: Dificulta modificación de balance
   - **Riesgo**: Código frágil y difícil de mantener

### 💰 Beneficios del Sistema Mixto
- **Flexibilidad**: SQLite para datos complejos, archivos para configuración simple
- **Eficiencia**: Cada sistema usa la tecnología más apropiada
- **Consistencia**: Eliminación completa de duplicaciones hardcodeadas
- **Mantenibilidad**: Separación clara entre lógica, configuración y datos
- **Escalabilidad**: Base de datos para características avanzadas futuras

## 🔧 Estrategia del Sistema Mixto

### 🗄️ Usar SQLite Para:
- **Partidas guardadas**: Slots, estadísticas, progreso (reemplaza pickle)
- **Datos de personajes**: Stats, ataques, habilidades (reemplaza character_data.py hardcodeado)
- **Configuración de enemigos**: Tipos, comportamientos, variantes (reemplaza enemy_types.py hardcodeado)
- **Estadísticas de juego**: Historiales, métricas, analytics
- **Datos que requieren consultas**: Búsquedas, filtros, relaciones

### 📄 Mantener Archivos de Configuración Para:
- **Configuración de usuario**: Volúmenes, controles, resolución (mantener JSON)
- **Configuración de desarrollo**: Opciones de debug, rutas de assets
- **Variables frecuentemente modificadas**: Balance de juego, tiempos, velocidades
- **Configuración simple**: Colores, dimensiones UI, textos estáticos
- **Configuración que necesita versionado fácil**: Nivel por nivel, configuraciones específicas

### ❌ Eliminar Completamente:
- **Código hardcodeado**: Diccionarios con datos en archivos Python
- **Duplicaciones**: Mismos datos en JSON y Python
- **Configuración mezclada con lógica**: Separar completamente

## 🗄️ Arquitectura SQLite Objetivo

### Esquema de Base de Datos
```sql
-- Reemplaza characters.json + character_data.py
CREATE TABLE personajes (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    nombre_mostrar TEXT NOT NULL,
    tipo TEXT NOT NULL,
    stats TEXT NOT NULL, -- JSON
    ataques TEXT NOT NULL, -- JSON
    sprite_config TEXT,
    activo BOOLEAN DEFAULT 1
);

-- Reemplaza enemies.json + enemy_types.py
CREATE TABLE enemigos (
    id INTEGER PRIMARY KEY,
    tipo TEXT UNIQUE NOT NULL,
    nombre_mostrar TEXT NOT NULL,
    stats TEXT NOT NULL, -- JSON
    comportamiento TEXT NOT NULL,
    animaciones TEXT NOT NULL, -- JSON
    variantes TEXT,
    activo BOOLEAN DEFAULT 1
);

-- Reemplaza powerups.json
CREATE TABLE powerups (
    id INTEGER PRIMARY KEY,
    tipo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    efectos TEXT NOT NULL, -- JSON
    duracion INTEGER,
    valor_efecto REAL,
    color TEXT,
    simbolo TEXT,
    activo BOOLEAN DEFAULT 1
);

-- Configuraciones generales (audio.json, display.json, etc.)
CREATE TABLE configuraciones (
    id INTEGER PRIMARY KEY,
    categoria TEXT NOT NULL,
    clave TEXT NOT NULL,
    valor TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    UNIQUE(categoria, clave)
);
```

## 📋 Lista de Tareas Pendientes

### ✅ COMPLETADAS
- [x] **DatabaseManager** - Sistema de conexiones SQLite operativo
- [x] **SchemaManager** - Creación automática de tablas
- [x] **SchemaTables** - Definiciones de esquemas
- [x] **SchemaMigrations** - Sistema de migraciones
- [x] **Testing básico** - Validación de infraestructura

### 🔥 EN PROGRESO

#### FASE 2A: Implementación ConfigDatabase (INMEDIATO)
- [ ] **Crear ConfigDatabase.py**
  - [ ] Interface para operaciones CRUD en SQLite
  - [ ] Métodos: get_character_data(), get_enemy_data(), get_powerup_data()
  - [ ] Sistema de caché opcional para rendimiento

- [ ] **Migrar characters.json → SQLite**
  - [ ] Script de migración automática
  - [ ] Validación de datos migrados
  - [ ] Verificar integridad referencial

- [ ] **Migrar enemies.json → SQLite**
  - [ ] Resolver inconsistencias con enemy_types.py
  - [ ] Unificar estadísticas y comportamientos
  - [ ] Mantener variantes (normal, raro, élite, legendario)

#### FASE 2B: Refactorización de Código (1-2 días)
- [ ] **Modificar character_data.py**
  - [ ] Cambiar de diccionario hardcodeado a lectura SQLite
  - [ ] Mantener API compatible
  - [ ] get_character_data() → ConfigDatabase.get_character_data()

- [ ] **Refactorizar enemy_types.py**
  - [ ] Eliminar configuraciones hardcodeadas
  - [ ] Usar SQLite como fuente única
  - [ ] Preservar lógica de rareza y comportamiento

- [ ] **Actualizar powerup.py**
  - [ ] Separar configuración de lógica
  - [ ] PowerupConfig desde SQLite
  - [ ] PowerupLogic mantiene comportamiento

#### FASE 2C: Sistema Unificado (2-3 días)
- [ ] **ConfigManager como Fachada SQLite**
  - [ ] get_section() → consulta SQLite
  - [ ] set() → actualización SQLite
  - [ ] Caché inteligente para rendimiento

- [ ] **Eliminación de Redundancias**
  - [ ] Backup de archivos JSON originales
  - [ ] Eliminación progresiva de duplicados
  - [ ] Validación completa de funcionalidad

- [ ] **Testing Integral**
  - [ ] Tests de migración de datos
  - [ ] Tests de compatibilidad API
  - [ ] Tests de rendimiento SQLite vs JSON

### 🚀 FUTURAS FASES

#### FASE 3: Migración SaveManager (3-4 días)
- [ ] Migrar sistema pickle → SQLite
- [ ] Mantener encriptación XOR
- [ ] Sistema de partidas guardadas

#### FASE 4: GameState Dinámico (2-3 días)
- [ ] Estado persistente en SQLite
- [ ] Estadísticas en tiempo real
- [ ] Analytics de jugabilidad

## 🔧 Scripts y Herramientas

### Scripts de Migración
```bash
# Migración completa automática
python scripts/migrate_to_sqlite.py

# Migración por fases
python scripts/migrate_characters.py
python scripts/migrate_enemies.py
python scripts/migrate_powerups.py

# Validación post-migración
python scripts/validate_migration.py
```

### Scripts de Testing
```bash
# Testing infraestructura SQLite
python scripts/test_simple_sqlite.py

# Testing migración específica
python scripts/test_config_migration.py

# Testing compatibilidad API
python scripts/test_api_compatibility.py
```

## 📈 Métricas de Progreso

### Estado Actual
- **✅ Infraestructura SQLite**: 100% completa
- **🔥 Migración de Configuraciones**: 0% (iniciando)
- **⏳ Eliminación de Hardcodeo**: 0% (pendiente)
- **⏳ Sistema Unificado**: 0% (pendiente)

### Objetivos de Entregas
- **Semana 1**: ConfigDatabase + migración characters.json
- **Semana 2**: Migración enemies.json + powerups.json
- **Semana 3**: Eliminación completa de hardcodeo
- **Semana 4**: Testing integral + documentación

## 🔗 Referencias del Proyecto
- **📖 Plan Técnico**: [`PLAN_MIGRACION_SQLITE.md`](./PLAN_MIGRACION_SQLITE.md)
- **📋 Estado General**: [`REFACTORIZACION_ESTADO_ACTUAL.md`](./REFACTORIZACION_ESTADO_ACTUAL.md)
- **📚 Funciones**: [`FUNCIONES_DOCUMENTADAS.md`](./FUNCIONES_DOCUMENTADAS.md)
- **⚙️ Instrucciones**: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md)

## 🎯 Próximo Paso Inmediato
**Crear ConfigDatabase.py** con interfaz para operaciones SQLite y comenzar migración de characters.json como caso de prueba piloto.

---

**🚀 OBJETIVO**: Transformar SiK Python Game en un sistema moderno, configurable y escalable con SQLite como columna vertebral de toda la configuración.
