# Índice de Migración SQLite - SiK Python Game

## 📋 Sistema de Documentación Integrado
- **📋 Documento Central**: [`REFACTORIZACION_ESTADO_ACTUAL.md`](./REFACTORIZACION_ESTADO_ACTUAL.md) - **CONSULTAR PRIMERO**
- **📖 Plan Detallado**: [`PLAN_MIGRACION_SQLITE.md`](./PLAN_MIGRACION_SQLITE.md) - Esquemas y checklist completo
- **🚀 Proyecto SQLite**: [`PROYECTO_MIGRACION_SQLITE.md`](./PROYECTO_MIGRACION_SQLITE.md) - **PROYECTO PRINCIPAL**
- **📚 Funciones**: [`FUNCIONES_DOCUMENTADAS.md`](./FUNCIONES_DOCUMENTADAS.md) - Catálogo actualizable
- **⚙️ Instrucciones**: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) - Reglas base del proyecto

## 🎯 CAMBIO DE PRIORIDAD: Sistema Mixto Inteligente

### ⚡ Nueva Estrategia (30 Julio 2025)
- **Prioridad 1**: Eliminar duplicaciones JSON ↔ Python (CRÍTICO)
- **Prioridad 2**: Sistema mixto: SQLite para datos complejos, JSON para configuración
- **Prioridad 3**: Funcionalidad operativa completa
- **Prioridad 4**: Optimización de líneas (después)

## 📊 Estado Actual
- **Fecha inicio**: 30 de Julio, 2025
- **Sistema actual**: pickle + zlib + XOR (SaveManager) + JSON modular (ConfigManager)
- **Duplicaciones críticas**: 5 archivos JSON ↔ Python con inconsistencias
- **Infraestructura SQLite**: ✅ 100% COMPLETADA

## 🚨 Duplicaciones Críticas Identificadas

### 📋 Problemas de Hardcodeo
1. **characters.json** (189 líneas, 4,875 chars) ↔ **character_data.py** (152 líneas)
   - **Estado**: DUPLICACIÓN TOTAL
   - **Impacto**: Cambios en dos lugares, riesgo de inconsistencias
   - **Acción**: Migrar a tabla `personajes`

2. **enemies.json** (73 líneas, 1,901 chars) ↔ **enemy_types.py** (230 líneas)
   - **Estado**: INCONSISTENCIAS CRÍTICAS
   - **Impacto**: enemy_types.py ignora enemies.json
   - **Acción**: Unificar en tabla `enemigos`

3. **powerups.json** (106 líneas, 2,780 chars) ↔ **powerup.py** (161 líneas)
   - **Estado**: LÓGICA MEZCLADA
   - **Impacto**: Configuración y lógica entrelazadas
   - **Acción**: Separar configuración (JSON) + lógica (Python)

4. **gameplay.json** (34 líneas, 769 chars) ↔ Multiple scene files
   - **Estado**: VALORES HARDCODEADOS
   - **Impacto**: Configuración ignorada en código
   - **Acción**: Usar gameplay.json, eliminar hardcodeo

5. **audio.json** (32 líneas, 969 chars) ↔ Audio modules
   - **Estado**: CONFIGURACIÓN IGNORADA
   - **Impacto**: Configuración no utilizada
   - **Acción**: Usar audio.json, eliminar hardcodeo

## � Sistema de Documentación Integrado
- **📋 Documento Central**: [`refactorizacion_progreso.md`](./refactorizacion_progreso.md) - **CONSULTAR PRIMERO**
- **📖 Plan Detallado**: [`PLAN_MIGRACION_SQLITE.md`](./PLAN_MIGRACION_SQLITE.md) - Esquemas y checklist completo
- **📚 Funciones**: [`FUNCIONES_DOCUMENTADAS.md`](./FUNCIONES_DOCUMENTADAS.md) - Catálogo actualizable
- **⚙️ Instrucciones**: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) - Reglas base del proyecto

## �📋 Estado Actual
- **Fecha inicio planificación**: 20 de Enero, 2025
- **Sistema actual**: pickle + zlib + XOR (SaveManager) + JSON modular (ConfigManager)
- **Archivos críticos identificados**: 23 archivos >150 líneas
- **Elementos a migrar**: Partidas, configuraciones, personajes, enemigos, estadísticas

## 🎯 Cronograma de Implementación

### ✅ FASE 1: Infraestructura Base (COMPLETADA)
**📋 Detalle**: Ver [Plan SQLite - Fase 1](./PLAN_MIGRACION_SQLITE.md#fase-1-infraestructura-sqlite)
- [x] **DatabaseManager.py** - Gestor de conexiones SQLite
- [x] **SchemaManager.py** - Manager de esquemas y tablas
- [x] **SchemaCore.py** - Núcleo del sistema
- [x] **SchemaTables.py** - Definiciones de tablas
- [x] **SchemaMigrations.py** - Sistema de migraciones
- [x] **Testing básico** - Validación de infraestructura

### 🔥 FASE 2: Migración de Configuraciones (EN PROCESO)
**📋 Detalle**: Ver [Proyecto SQLite](./PROYECTO_MIGRACION_SQLITE.md)
- [ ] **ConfigDatabase.py** - Nueva interfaz SQLite
- [ ] **Migrar characters.json → tabla personajes**
- [ ] **Migrar enemies.json → tabla enemigos**
- [ ] **Migrar powerups.json → tabla powerups**
- [ ] **Sistema de compatibilidad dual**
- [ ] **Eliminación progresiva de hardcodeo**

### 📊 FASE 3: SaveManager (3-4 días)
**📋 Detalle**: Ver [Plan SQLite - Fase 3](./PLAN_MIGRACION_SQLITE.md#fase-3-migración-del-savemanager)
- [ ] **Dividir SaveManager** (365→4x150 líneas)
- [ ] **Migrar pickle a SQLite**
- [ ] **Mantener encriptación XOR**
- [ ] **Migración automática saves existentes**

### ⚡ FASE 4: GameState (2-3 días)
**📋 Detalle**: Ver [Plan SQLite - Fase 4](./PLAN_MIGRACION_SQLITE.md#fase-4-migración-del-gamestate)
- [ ] **Dividir GameState** (151→3x150 líneas)
- [ ] **Integrar con SQLite**
- [ ] **Estadísticas en tiempo real**
- [ ] **Testing completo del sistema**

## 📊 Métricas de Progreso

### 🎯 Objetivos Cuantificables
- **✅ Infraestructura SQLite**: 100% completa
- **🔥 Eliminación de Duplicaciones**: 0% (iniciando)
- **⏳ Migración de Datos**: 0% (pendiente)
- **⏳ Sistema Unificado**: 0% (pendiente)

### 📈 Progreso por Duplicación
- **characters.json ↔ character_data.py**: 0% migrado
- **enemies.json ↔ enemy_types.py**: 0% migrado
- **powerups.json ↔ powerup.py**: 0% migrado
- **gameplay.json ↔ scene files**: 0% migrado
- **audio.json ↔ audio modules**: 0% migrado

## 🔗 Documentos Relacionados
- **Plan completo**: `docs/PLAN_MIGRACION_SQLITE.md`
- **Progreso refactorización**: `docs/refactorizacion_progreso.md`
- **Funciones documentadas**: `docs/FUNCIONES_DOCUMENTADAS.md`
- **Instrucciones proyecto**: `.github/copilot-instructions.md`

## 🚀 Siguiente Paso
**Comenzar Fase 1**: Crear DatabaseManager y SchemaManager como base del nuevo sistema.

---
**🎯 OBJETIVO**: Sistema moderno, escalable y mantenible con SQLite como eje central
