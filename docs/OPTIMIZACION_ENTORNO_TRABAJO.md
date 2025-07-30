# Optimización del Entorno de Trabajo - VS Code

## 🧹 Sistema de Limpieza Automática

### Scripts Implementados

#### 1. `workspace_cleanup.ps1` - Limpieza Principal
```powershell
# Limpieza ligera (pestañas + caché básico)
.\scripts\workspace_cleanup.ps1 -Level "light"

# Limpieza profunda (+ optimización Git/Poetry)
.\scripts\workspace_cleanup.ps1 -Level "deep"

# Limpieza completa (+ caché VS Code + memoria)
.\scripts\workspace_cleanup.ps1 -Level "complete"

# Acciones específicas
.\scripts\workspace_cleanup.ps1 -CloseTabs
.\scripts\workspace_cleanup.ps1 -ClearCache
.\scripts\workspace_cleanup.ps1 -OptimizeMemory
```

### Capacidades de VS Code

#### Comandos de Pestañas Disponibles:
- ✅ **`workbench.action.closeAllEditors`** - Cerrar todas las pestañas
- ✅ **`workbench.action.closeOtherEditors`** - Cerrar otras pestañas
- ✅ **`workbench.action.closeUnmodifiedEditors`** - Cerrar pestañas no modificadas
- ✅ **`workbench.action.closeAllGroups`** - Reorganizar grupos de editores

#### Tipos de Limpieza:

**🟢 LIGHT (Diario)**
- Cierra pestañas no modificadas
- Limpia caché Python (__pycache__, .pytest_cache, etc.)
- Limpia archivos temporales (.pyc, .pyo)

**🟡 DEEP (Semanal)**
- Todo lo anterior +
- Optimización Git (gc, prune)
- Limpieza caché Poetry
- Optimización de memoria

**🔴 COMPLETE (Mensual)**
- Todo lo anterior +
- Cierra TODAS las pestañas
- Limpia caché VS Code (workspaceStorage, logs)
- Limpieza forzada de archivos grandes

### Integración con Flujo de Trabajo

#### Automático por Fases:
```powershell
# Al terminar cada tarea
.\scripts\workspace_cleanup.ps1 -CloseTabs

# Al terminar cada día
.\scripts\workspace_cleanup.ps1 -Level "light"

# Al terminar cada sprint/fase
.\scripts\workspace_cleanup.ps1 -Level "deep"

# Mantenimiento mensual
.\scripts\workspace_cleanup.ps1 -Level "complete" -Force
```

### Configuración de Limpieza Automática

#### Hooks del Sistema de Commits:
El script se puede integrar automáticamente en el flujo de commits:

```powershell
# En unified_commit.ps1 - al final del commit exitoso
if ($CleanupAfterCommit) {
    .\scripts\workspace_cleanup.ps1 -Level "light"
}
```

### Beneficios del Sistema

#### Rendimiento:
- ✅ **Reduce uso de memoria** eliminando pestañas innecesarias
- ✅ **Acelera VS Code** limpiando cachés acumulados
- ✅ **Optimiza Git** con garbage collection automático
- ✅ **Libera espacio** eliminando archivos temporales

#### Productividad:
- ✅ **Entorno limpio** sin pestañas acumuladas
- ✅ **Navegación rápida** con menos archivos abiertos
- ✅ **Menos distracciones** con workspace organizado
- ✅ **Startup más rápido** con caché optimizado

### Monitoreo y Métricas

El script proporciona información detallada:
- 📊 Tamaño del proyecto actual
- 📊 Archivos Python en el proyecto
- 📊 Estado de memoria del sistema
- 📊 Cachés eliminados y espacio liberado

### Seguridad

#### Protecciones Implementadas:
- 🛡️ **No elimina archivos modificados** sin confirmación
- 🛡️ **Preserva configuración VS Code** importante
- 🛡️ **Backup automático** antes de limpieza completa
- 🛡️ **Modo -Force** requerido para operaciones destructivas

### Uso Recomendado

```powershell
# Workflow diario recomendado:

# 1. Al iniciar trabajo
.\scripts\workspace_cleanup.ps1 -Level "light"

# 2. Al hacer commits importantes
.\scripts\unified_commit.ps1 "mensaje" -Type "feat" -Scope "ui"
.\scripts\workspace_cleanup.ps1 -CloseTabs

# 3. Al terminar fase/sprint
.\scripts\workspace_cleanup.ps1 -Level "deep"
```

## 🔄 Integración con Método de Commit Unificado

El sistema de limpieza está diseñado para integrarse perfectamente con el **Método de Commit Unificado** establecido en el proyecto, manteniendo un entorno de trabajo optimizado durante todo el flujo de desarrollo.
