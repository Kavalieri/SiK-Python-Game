# Instrucciones para GitHub Copilot - SiK Python Game

## � **PRIORIDADES CRÍTICAS** (Consultar PRIMERO)

### 1️⃣ **REFACTORIZACIÓN + MIGRACIÓN SQLITE** (23 archivos críticos)
- **Estado**: 23 archivos exceden 150 líneas → 11 >300 líneas **URGENTE**
- **Método**: División funcional preservando 100% funcionalidad + migración SQLite
- **Límite ABSOLUTO**: 150 líneas por archivo - dividir INMEDIATAMENTE si se excede

### 2️⃣ **DOCUMENTACIÓN CENTRAL** (Consultar en orden)
1. [`docs/refactorizacion_progreso.md`](../docs/refactorizacion_progreso.md) - **DOCUMENTO CENTRAL**
2. [`docs/PLAN_MIGRACION_SQLITE.md`](../docs/PLAN_MIGRACION_SQLITE.md) - Plan SQLite + checklist
3. [`docs/FUNCIONES_DOCUMENTADAS.md`](../docs/FUNCIONES_DOCUMENTADAS.md) - **ACTUALIZAR** siempre
4. [`docs/INDICE_MIGRACION_SQLITE.md`](../docs/INDICE_MIGRACION_SQLITE.md) - Vista rápida

### 3️⃣ **WORKFLOW OBLIGATORIO**
- **ANTES**: Consultar `refactorizacion_progreso.md` + revisar si toca SQLite
- **DURANTE**: Actualizar `FUNCIONES_DOCUMENTADAS.md` + dividir si >150 líneas
- **DESPUÉS**: Commit con `.\scripts\simple_commit.ps1 "mensaje"` + limpieza VS Code

## ⚡ **SISTEMAS AUTOMATIZADOS**

### 🔄 **Commits y Versionado**
- **Diario**: `.\scripts\simple_commit.ps1 "mensaje"` (Conventional Commits automático)
- **Completo**: `.\scripts\unified_commit.ps1 "mensaje" -Type "feat" -Scope "ui" -Push`
- **Pre-commit**: Hooks ejecutados ANTES staging (resuelve conflictos)

### 🧹 **Limpieza Post-Operación** (NUEVO - INTEGRADO)
**Ejecutar SIEMPRE tras**: commits, pruebas, errores, objetivos completados
```powershell
.\scripts\vscode_cleanup_sendkeys.ps1 -Level "light"
```
- **Método validado**: SendKeys (Ctrl+K U)
- **Preserva**: Pestañas pinned y modificadas
- **Libera**: Caché VS Code (272+ MB comprobados)
- **Sin efectos**: No cambia tamaño ventana

### 🗄️ **Migración SQLite** (Fase 1 ✅ - Fase 2-4 pendiente)
- **DatabaseManager**: Modularizado y funcional
- **SchemaManager**: Sistema completo de tablas
- **Próximo**: ConfigManager (264→3x150 líneas) + SaveManager (365→4x150 líneas)

## 📋 **REGLAS FUNDAMENTALES**

### 🔧 **División de Archivos** (CRÍTICO)
**REGLA ABSOLUTA**: Ningún archivo >150 líneas - Dividir INMEDIATAMENTE
1. **División funcional**: Core + Extensions, Manager + Operations
2. **Preservar APIs**: 100% compatibilidad mantenida
3. **Commit atómico**: Por cada archivo dividido
4. **Actualizar**: `FUNCIONES_DOCUMENTADAS.md` automáticamente

### 🛠️ **Stack y Herramientas**
- **Python 3.11+** + **Pygame-ce** (NO pygame estándar) + **Poetry**
- **GitHub CLI prioritario**: `gh` > git tradicional
- **PowerShell**: Shell predeterminado (NO `&&`, usar `;`)
- **Español**: Código, comentarios, variables, funciones

### 🏗️ **Arquitectura Modular**
```
src/core/     # Motor, scene manager
src/entities/ # Jugador, enemigos, proyectiles
src/scenes/   # Menús, gameplay, transiciones
src/ui/       # HUD, componentes UI
src/utils/    # Assets, config, helpers
```

### 🎯 **Convenciones**
- **Variables**: `generacion_enemigos`, `velocidad_movimiento`
- **Clases**: `GestorEnemigos`, `PersonajeJugador` (PascalCase español)
- **Type hints**: Obligatorios en parámetros y retornos
- **Docstrings**: Español completo con Args/Returns/Raises
## 🎮 **CONTEXTO DEL PROYECTO**

**Videojuego 2D bullet hell** - Pygame-ce + Python 3.11+ + Poetry
Desarrollo **100% IA** en Windows 11 + VS Code + GitHub CLI

### 🚨 **Archivos Críticos que Requieren Refactorización URGENTE**
1. **src/entities/entity.py** (479 líneas) - **CRÍTICO** - Sin migración SQLite
2. **src/utils/asset_manager.py** (464 líneas) - **CRÍTICO** - Cache SQLite futuro
3. **src/ui/hud.py** (397 líneas) - **CRÍTICO** - Sin migración SQLite
4. **🗄️ src/utils/save_manager.py** (365 líneas) - **CRÍTICO + MIGRACIÓN SQLITE**
5. **🗄️ src/utils/config_manager.py** (264 líneas) - **MIGRACIÓN SQLITE**

**⚠️ IMPORTANTE**: Consultar `docs/refactorizacion_progreso.md` antes de editar
## 🔄 **REGLAS DE TRABAJO**

### ⚡ **Comandos y Herramientas**
- **Poetry**: `poetry run python src/main.py`, `poetry install`, `poetry add package_name`
- **PowerShell**: Shell predeterminado (NO `&&`, usar `;`)
- **GitHub CLI prioritario**: `gh repo view` > `git status`

### � **Commits y Gestión**
- **Diario**: `.\scripts\simple_commit.ps1 "mensaje"`
- **GitHub CLI**: `gh` para repo, issues, PRs, releases
- **Git local**: Solo `git add`, `git commit`, branching
- **Commits atómicos**: Por cada refactorización

### 🎯 **Calidad y Testing**
- **0 errores Ruff** + **0 advertencias MyPy** siempre
- **100% cobertura tests** mínimo
- **Complejidad < 10** por función
- **Funciones <30 líneas** para IA optimal
## 🤖 **OPTIMIZACIÓN PARA IA**

### Patrones para GitHub Copilot
- **Nombres autodescriptivos** en español
- **Funciones pequeñas** (máximo 30 líneas)
- **Comentarios contextuales** antes de lógica compleja
- **Type hints completos** para mejor inferencia
- **Consistencia** en nomenclatura y estructura

### Proyecto 100% IA
- **NUNCA eliminar** `.github/` ni este archivo
- **PRIORIDAD ABSOLUTA**: Completar refactorización antes que cualquier feature
- **Mantener actualizadas** todas las reglas constantemente
- **Automatización máxima** de procesos repetitivos
- **Documentación automática** de funciones y cambios

---

**Base fundamental del proyecto. REFACTORIZACIÓN PRIORITARIA. Mantener actualizado siempre.**
