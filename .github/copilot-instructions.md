# Instrucciones para GitHub Copilot - SiK Python Game---

**Base fundamental del proyecto. Mantener actualizado siempre.**

**📚 Referencia completa**: Consultar instrucciones específicas en `.github/instructions/` para detalles por módulo. **PRIORIDAD DE INSTRUCCIONES**
```
Prioridad: instrucciones del usuario > instrucciones de repositorio > instrucciones de organización
```

## 🎯 **INSTRUCCIONES PRINCIPALES**

Estas son las instrucciones principales para el repositorio SiK Python Game. Las instrucciones específicas se encuentran organizadas en módulos separados en `.github/instructions/`.

### �🚨 **FLUJO POST-OPERACIÓN OBLIGATORIO**
**Ejecutar SIEMPRE tras**: commits, pruebas, errores, objetivos completados
```powershell
.\dev-tools\scripts\vscode_cleanup_sendkeys.ps1 -Level "light"
```

### 🎯 **DIRECTRICES CRÍTICAS INMEDIATAS**
- **CONSULTAR PRIMERO**: `docs/REFACTORIZACION_ESTADO_ACTUAL.md` antes de CUALQUIER cambio
- **LÍMITE ABSOLUTO**: 250 líneas por archivo - dividir INMEDIATAMENTE si se excede
- **ACTUALIZAR SIEMPRE**: `docs/FUNCIONES_DOCUMENTADAS.md` con cada función nueva
- **Commits**: Solo `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` (método unificado)

## 📁 **INSTRUCCIONES ESPECÍFICAS**

Las instrucciones detalladas están organizadas en módulos específicos:

### 🔄 **Refactorización y Migración**
- [📋 Refactorización General](instructions/refactorizacion.instructions.md)
- [🗄️ Migración SQLite](instructions/migracion-sqlite.instructions.md)

### 🛠️ **Herramientas y Desarrollo**
- [⚡ Sistemas Automatizados](instructions/sistemas-automatizados.instructions.md)
- [🧹 Limpieza y Optimización](instructions/limpieza-optimizacion.instructions.md)
- [📝 Control de Versiones](instructions/control-versiones.instructions.md)

### 🎮 **Proyecto Específico**
- [🎯 Arquitectura y Convenciones](instructions/arquitectura-convenciones.instructions.md)
- [🎮 Contexto del Juego](instructions/contexto-juego.instructions.md)
- [🤖 Optimización IA](instructions/optimizacion-ia.instructions.md)

### ⚙️ **Configuración y Reglas**
- [🔧 Reglas Fundamentales](instructions/reglas-fundamentales.instructions.md)
- [🏗️ Stack y Herramientas](instructions/stack-herramientas.instructions.md)
- [🧪 Testing y Calidad](instructions/testing-calidad.instructions.md)

## 🎯 **CONTEXTO DEL PROYECTO**

**Videojuego 2D bullet hell** - Pygame-ce + Python 3.11+ + Poetry
Desarrollo **100% IA** en Windows 11 + VS Code + GitHub CLI

**Estado actual**: ✅ REFACTORIZACIÓN MASIVA COMPLETADA (99.3% archivos compliant)
**Prioridad**: 🎮 DESARROLLO DE CARACTERÍSTICAS DEL JUEGO

---

**Base fundamental del proyecto. DESARROLLO DE JUEGO PRIORITARIO. Mantener actualizado siempre.**

**📚 Referencia completa**: Consultar instrucciones específicas en `instructions/` para detalles por módulo.

## � **PRIORIDADES ACTUALES** (Post-Modernización)

### 1️⃣ **DESARROLLO DE CARACTERÍSTICAS** (Prioridad principal)
- **Estado**: Infraestructura técnica ✅ COMPLETADA
- **Solo 1 archivo crítico**: config_database.py (297 líneas) - Sistema SQLite funcional
- **Enfoque**: Nuevas mecánicas, gameplay, contenido del juego

### 2️⃣ **DOCUMENTACIÓN ACTUALIZADA** (Consultar en orden)
1. [`docs/ANALISIS_POST_MODERNIZACION.md`](../docs/ANALISIS_POST_MODERNIZACION.md) - **ANÁLISIS ACTUAL**
2. [`docs/PLAN_LIMPIEZA_Y_DESARROLLO.md`](../docs/PLAN_LIMPIEZA_Y_DESARROLLO.md) - Próximas fases
3. [`docs/FUNCIONES_DOCUMENTADAS.md`](../docs/FUNCIONES_DOCUMENTADAS.md) - **ACTUALIZAR** siempre
4. *Documentos obsoletos*: REFACTORIZACION_ESTADO_ACTUAL.md, PLAN_MIGRACION_SQLITE.md

### 3️⃣ **WORKFLOW ACTUAL**
- **ANTES**: Consultar `ANALISIS_POST_MODERNIZACION.md` para estado actual
- **DURANTE**: Desarrollar características, mantener límite de 250 líneas
- **DESPUÉS**: Commit con `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` + limpieza VS Code

## ⚡ **SISTEMAS AUTOMATIZADOS**

### 🔄 **Commits y Versionado**
- **Diario**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` (Conventional Commits automático)
- **Completo**: `.\dev-tools\scripts\unified_commit.ps1 "mensaje" -Type "feat" -Scope "ui" -Push`
- **Pre-commit**: Hooks ejecutados ANTES staging (resuelve conflictos)

### 🧹 **Limpieza Post-Operación** (INTEGRADO ARRIBA)
**RECORDATORIO**: Usar `.\dev-tools\scripts\vscode_cleanup_sendkeys.ps1 -Level "light"` tras operaciones importantes.

### 🗄️ **Sistema SQLite** (✅ COMPLETADO)
- **Sistema mixto inteligente**: SQLite para datos complejos, JSON para configuración
- **DatabaseManager**: ✅ Operativo y funcional
- **SchemaManager**: ✅ Sistema completo implementado
- **ConfigDatabase**: ✅ Interfaz SQLite funcional (único archivo >250 líneas)
- **SaveManager**: ✅ Migrado exitosamente desde pickle
- **Duplicaciones eliminadas**: ✅ JSON ↔ Python unificados

## 📋 **REGLAS FUNDAMENTALES**

### 🔧 **División de Archivos** (CRÍTICO)
**REGLA ABSOLUTA**: Ningún archivo >250 líneas - Dividir INMEDIATAMENTE
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

### ✅ **Estado Técnico Post-Modernización**
- **99.3% archivos compliant** (133/134 archivos bajo 250 líneas)
- **Solo 1 archivo crítico**: config_database.py (297 líneas) - Sistema SQLite funcional
- **Refactorización masiva**: ✅ COMPLETADA exitosamente
- **Sistema SQLite**: ✅ IMPLEMENTADO y operativo
- **Infraestructura**: ✅ Lista para desarrollo de características

**📊 NUEVA PRIORIDAD**: Desarrollo de características del juego
## 🔄 **REGLAS DE TRABAJO**

### ⚡ **Comandos y Herramientas**
- **Poetry**: `poetry run python src/main.py`, `poetry install`, `poetry add package_name`
- **PowerShell**: Shell predeterminado (NO `&&`, usar `;`)
- **GitHub CLI prioritario**: `gh repo view` > `git status`

### � **Commits y Gestión**
- **Diario**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` para commits cotidianos
- **GitHub CLI**: `gh` para repo, issues, PRs, releases
- **Git local**: Solo `git add`, `git commit`, branching
- **Commits atómicos**: Por cada refactorización

### 🎯 **Calidad y Testing**
- **0 errores Ruff** + **0 advertencias MyPy** siempre
- **100% cobertura tests** mínimo
- **Complejidad < 10** por función
- **Funciones <30 líneas** para IA optimal
- **Búsqueda en archivos**: `Get-Content archivo.txt | Select-String "patrón"`

### Configuración Terminal VS Code (CRÍTICO)
- **Terminal optimizado**: Ver `docs/CONFIGURACION_TERMINAL_OPTIMIZADA.md` para configuración completa
- **Usar terminal existente** cuando esté disponible en lugar de crear nuevos
- **Scripts PowerShell ASCII-only**: **PROHIBIDOS emojis, Unicode y caracteres especiales**
- **Timeouts automáticos**: Todos los comandos largos deben tener timeout (30-45s máximo)
- **Detección de output**: Usar `isBackground=false` para comandos que requieren respuesta inmediata
- **Scripts terminal-safe**: OBLIGATORIO usar `scripts/terminal_safe_commit.ps1` para commits
- **Recuperación automática**: Si hay problemas, usar `scripts/reset_terminal_state.ps1`
- **Validación pre-comando**: Verificar responsividad con `scripts/test_ascii_safe.ps1`
- **Estado validado**: Terminal completamente funcional (30 jul 2025) - ver documentación

### Reglas PowerShell Scripts (OBLIGATORIO)
- **NUNCA usar emojis** (🚀, ✅, ❌, etc.) - causan problemas encoding
- **NUNCA usar Unicode** - solo caracteres ASCII básicos
- **Usar [OK], [ERROR], [WARN]** en lugar de símbolos
- **Usar Write-Host con -ForegroundColor** para colores
- **Incluir timeouts** en todos los comandos que pueden colgarse
- **Validar estado terminal** antes de operaciones complejas

### Método de Commit Unificado (NUEVO - OBLIGATORIO)
- **Script principal**: `scripts/unified_commit.ps1` para commits completos con validaciones
- **Script simple**: `scripts/simple_commit.ps1` para uso cotidiano
- **Flujo optimizado**: pre-commit → staging → commit → push (resuelve conflictos de hooks)
- **Conventional Commits**: Formato automático `tipo(ámbito): descripción`
- **Tipos**: feat, fix, docs, refactor, test, chore, perf, style
- **Ámbitos**: core, entities, scenes, ui, utils, config, assets, docs
- **Pre-commit hooks**: Ejecutados ANTES del staging para evitar conflictos
- **Documentación completa**: `docs/METODO_COMMIT_UNIFICADO.md` con guía detallada
- **Uso diario**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"`
- **Uso completo**: `.\dev-tools\scripts\unified_commit.ps1 "mensaje" -Type "feat" -Scope "ui" -Push`

### Optimización de Entorno de Trabajo (NUEVO - RECOMENDADO)
- **Script de limpieza**: `scripts/workspace_cleanup.ps1` para optimizar VS Code y caché
- **Configuración automática**: `scripts/setup_auto_cleanup.ps1` para integrar limpieza
- **Niveles de limpieza**: light (diario), deep (semanal), complete (mensual)
- **Capacidades VS Code**: Cierre automático de pestañas con comandos workbench
- **Limpieza de caché**: Python (__pycache__), Poetry, Git, VS Code workspaceStorage
- **Optimización memoria**: Garbage collection .NET y análisis de uso de memoria
- **Integración commits**: Limpieza automática después de commits exitosos
- **Atajos de teclado**: Ctrl+K Ctrl+L (light), Ctrl+K Ctrl+T (tabs), Ctrl+K Ctrl+D (deep)
- **Documentación**: `docs/OPTIMIZACION_ENTORNO_TRABAJO.md` con guía completa
- **Uso recomendado**: `.\dev-tools\scripts\workspace_cleanup.ps1 -Level "light"` después de cada commit

### Gestión de Archivos y Repositorio
- **GitHub CLI prioritario**: usar `gh` para todas las operaciones de repositorio
- **Matriz de decisión**: `docs/MATRIZ_DECISIÓN_GH_VS_GIT.md` (consultar SIEMPRE)
- **Información del repositorio**: `gh repo view` (preferir sobre git status)
- **Gestión de issues/PRs**: `gh issue create`, `gh pr create --fill`
- **Releases y distribución**: `gh release create`, `gh release upload`
- **Git tradicional**: solo para `git add`, `git commit`, operaciones locales
- **Commits atómicos** por cada refactorización o cambio significativo
- **Evitar** movimientos directos en explorador

### 📁 **Gestión Documental Organizada** (NUEVO - OBLIGATORIO)
- **Lógica de archivo**: Ver `docs/LOGICA_GESTION_DOCUMENTAL.md` para proceso completo
- **Directorio activo**: `docs/` SOLO para documentos de trabajo en curso
- **Sistema de archivo**: `docs/ARCHIVO/2025/[categoria]/` para documentos completados
- **Categorías de archivo**: refactorizacion, migracion-sqlite, terminal-powershell, commits-github, configuracion
- **Proceso obligatorio**: Mover documentos completados/sustituidos a archivo correspondiente
- **Mantener docs/ limpio**: Máximo documentos activos esenciales para desarrollo actual
- **Archivar tras completar**: Cada fase/proyecto → mover documentación a ARCHIVO
- **Consulta histórica**: Estructura organizada por año y tema en docs/ARCHIVO/

### Priorización: GitHub CLI vs Git Tradicional
**Usar GitHub CLI (`gh`) para:**
- Obtener información del repositorio y estado general
- Gestionar issues, pull requests y releases
- Navegar rápidamente al repositorio en navegador
- Clonar repositorios y gestionar forks
- Buscar repositorios y contenido en GitHub
- Ejecutar y monitorear GitHub Actions

**Usar Git tradicional solo para:**
- Operaciones locales básicas: `git add`, `git commit`
- Control de versiones local y staging
- Branching local: `git branch`, `git checkout`
- Consultar logs y diferencias locales
- **OBLIGATORIO**: Verificar cambios staged con `git status` antes de cada commit
- **Usar método unificado**: `.\dev-tools\scripts\simple_commit.ps1 "mensaje"` para commits cotidianos

### Flujo Autónomo
- **Continuar automáticamente** hasta puntos de prueba
- **Resolver errores** de forma autónoma
- **Documentar cambios** significativos inmediatamente

### Estrategia para Problemas
- **Comentar líneas** problemáticas temporalmente
- **Probar sin conflictos** para identificar impacto real
- **Documentar soluciones** implementadas

## 🤖 Optimización para IA

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
