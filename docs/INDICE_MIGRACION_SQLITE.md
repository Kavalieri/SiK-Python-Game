# Índice de Migración SQLite - SiK Python Game

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

### ✅ FASE 1: Infraestructura Base (2-3 días)
**📋 Detalle**: Ver [Plan SQLite - Fase 1](./PLAN_MIGRACION_SQLITE.md#fase-1-preparación-e-infraestructura)
- [ ] **DatabaseManager.py** (máximo 150 líneas)
- [ ] **SchemaManager.py** (máximo 150 líneas)
- [ ] **Tests de infraestructura**
- [ ] **Benchmark vs sistema actual**
- [ ] **Actualizar** [`refactorizacion_progreso.md`](./refactorizacion_progreso.md) - Fase 1

### 🔥 FASE 2: ConfigManager (3-4 días)
**📋 Detalle**: Ver [Plan SQLite - Fase 2](./PLAN_MIGRACION_SQLITE.md#fase-2-migración-del-configmanager)
- [ ] **Dividir ConfigManager** (264→3x150 líneas)
- [ ] **Migrar JSON a SQLite**
- [ ] **Resolver duplicaciones config/src**
- [ ] **Sistema de compatibilidad dual**
- [ ] **Actualizar** [`FUNCIONES_DOCUMENTADAS.md`](./FUNCIONES_DOCUMENTADAS.md)

### 📊 FASE 3: SaveManager (4-5 días)
**📋 Detalle**: Ver [Plan SQLite - Fase 3](./PLAN_MIGRACION_SQLITE.md#fase-3-migración-del-savemanager)
- [ ] **Dividir SaveManager** (365→4x150 líneas)
- [ ] **Migrar pickle a SQLite**
- [ ] **Mantener encriptación XOR**
- [ ] **Migración automática saves existentes**
- [ ] **Documentar** todas las funciones nuevas

### ⚡ FASE 4: GameState (2-3 días)
**📋 Detalle**: Ver [Plan SQLite - Fase 4](./PLAN_MIGRACION_SQLITE.md#fase-4-migración-del-gamestate)
- [ ] **Dividir GameState** (151→3x150 líneas)
- [ ] **Integrar con SQLite**
- [ ] **Estadísticas en tiempo real**
- [ ] **Testing completo del sistema**
- [ ] **Finalizar** documentación en [`refactorizacion_progreso.md`](./refactorizacion_progreso.md)

## 📊 Métricas de Progreso

### Archivos Refactorizados
- [ ] SaveManager: 365 líneas → 4x150 líneas
- [ ] ConfigManager: 264 líneas → 3x150 líneas
- [ ] GameState: 151 líneas → 3x150 líneas

### Datos Migrados
- [ ] Partidas guardadas (pickle → SQLite)
- [ ] Configuraciones (JSON → SQLite)
- [ ] Personajes y enemigos (JSON → SQLite)
- [ ] Sistema de estadísticas (nuevo)

## 🔗 Documentos Relacionados
- **Plan completo**: `docs/PLAN_MIGRACION_SQLITE.md`
- **Progreso refactorización**: `docs/refactorizacion_progreso.md`
- **Funciones documentadas**: `docs/FUNCIONES_DOCUMENTADAS.md`
- **Instrucciones proyecto**: `.github/copilot-instructions.md`

## 🚀 Siguiente Paso
**Comenzar Fase 1**: Crear DatabaseManager y SchemaManager como base del nuevo sistema.

---
**🎯 OBJETIVO**: Sistema moderno, escalable y mantenible con SQLite como eje central
