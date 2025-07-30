# Refactorización General

## 🎯 **PRIORIDADES CRÍTICAS** (Consultar PRIMERO)

### 1️⃣ **REFACTORIZACIÓN + MIGRACIÓN SQLITE** (29 archivos críticos)
- **Estado**: 29 archivos exceden 150 líneas → 9 archivos >200 líneas **CRÍTICO**
- **Método**: División funcional preservando 100% funcionalidad + migración SQLite
- **Límite ABSOLUTO**: 150 líneas por archivo - dividir INMEDIATAMENTE si se excede

### 2️⃣ **DOCUMENTACIÓN CENTRAL** (Consultar en orden)
1. [`docs/REFACTORIZACION_ESTADO_ACTUAL.md`](../../docs/REFACTORIZACION_ESTADO_ACTUAL.md) - **DOCUMENTO CENTRAL ACTUALIZADO**
2. [`docs/PLAN_MIGRACION_SQLITE.md`](../../docs/PLAN_MIGRACION_SQLITE.md) - Plan SQLite + checklist
3. [`docs/FUNCIONES_DOCUMENTADAS.md`](../../docs/FUNCIONES_DOCUMENTADAS.md) - **ACTUALIZAR** siempre
4. [`docs/INDICE_MIGRACION_SQLITE.md`](../../docs/INDICE_MIGRACION_SQLITE.md) - Vista rápida

### 3️⃣ **WORKFLOW OBLIGATORIO**
- **ANTES**: Consultar `REFACTORIZACION_ESTADO_ACTUAL.md` + revisar si toca SQLite
- **DURANTE**: Actualizar `FUNCIONES_DOCUMENTADAS.md` + dividir si >150 líneas
- **DESPUÉS**: Commit con `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` + limpieza VS Code

## 📋 **REGLAS FUNDAMENTALES**

### 🔧 **División de Archivos** (CRÍTICO)
**REGLA ABSOLUTA**: Ningún archivo >150 líneas - Dividir INMEDIATAMENTE
1. **División funcional**: Core + Extensions, Manager + Operations
2. **Preservar APIs**: 100% compatibilidad mantenida
3. **Commit atómico**: Por cada archivo dividido
4. **Actualizar**: `FUNCIONES_DOCUMENTADAS.md` automáticamente
