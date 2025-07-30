# dev-tools/ - Herramientas de Desarrollo

## 🛠️ **PROPÓSITO**
Conjunto completo de herramientas, scripts y utilidades para el desarrollo, testing, migración y mantenimiento del proyecto **SiK Python Game**. Este directorio centraliza todas las herramientas que no forman parte del juego en sí.

> **🎯 ESTRUCTURA CENTRALIZADA**: Todas las herramientas de desarrollo están organizadas aquí para mantener la raíz del proyecto limpia.

## 📊 **ESTADO ACTUAL**
- **Scripts automatizados**: Commit, limpieza, migración (43 archivos)
- **Testing completo**: Unitarios, integración, funcionales (30+ archivos)
- **Packaging**: Herramientas de empaquetado y distribución
- **Migration**: Herramientas de migración de datos y estructura
- **Archive**: Archivos obsoletos organizados (29 archivos)
- **Total organizados**: 102+ archivos de herramientas

## 🗂️ Estructura Consolidada

### 📁 scripts/ - Scripts de Producción
**Scripts principales** estables y de uso frecuente:

**Commits Inteligentes:**
- `simple_commit.ps1`, `unified_commit.ps1` - Scripts de commit principal
- `intelligent_commit.py`, `smart_commit.py` - Commits avanzados
- `terminal_safe_commit.ps1` - Commit compatible con terminal

**Limpieza y Mantenimiento:**
- `workspace_cleanup.ps1` - Limpieza de VS Code y caché
- `vscode_cleanup_sendkeys.ps1` - Cierre automático de pestañas
- `cleanup_project_v2.py` - Limpieza completa del proyecto

**Herramientas VS Code:**
- `definitive_tab_closer.ps1` - Gestión de pestañas VS Code
- `real_vscode_methods.ps1` - Métodos de integración VS Code
- `reset_terminal_state.ps1` - Recuperación de terminal

**Análisis:**
- `analyze_file_sizes.py` - Análisis de tamaños de archivo
- `validar_documentacion.py` - Validación de documentación
- `verify_all_paths.ps1`

### 📁 testing/ - Testing y Experimentación
**Testing completo** del proyecto incluyendo tests unitarios, integración y debug:

**Tests de Sistemas Principales:**
- `test_config_system.py` - Testing del sistema de configuración
- `test_enemy_system.py` - Testing del sistema de enemigos
- `test_powerup_system.py` - Testing del sistema de powerups
- `test_projectile_system.py` - Testing del sistema de proyectiles
- `test_unified_system.py` - Testing de integración completa

**Tests del Motor del Juego:**
- `test_game_engine_simple.py` - Testing básico del motor
- `test_menu_flow.py` - Testing del flujo de menús
- `test_simple_game.py` - Testing del juego completo
- `test_atmospheric_effects.py` - Testing de efectos atmosféricos

**Tests de Configuración:**
- `test_config.py`, `test_config_manager.py` - Testing de configuración
- `test_config_simple.py` - Testing básico de configuración

**Diagnóstico VS Code y Terminal:**
- `test_vscode_tabs.ps1` - Testing de gestión de pestañas
- `test_terminal_responsive.ps1` - Testing de responsividad terminal
- `test_sendkeys_fixed.ps1` - Testing de métodos SendKeys
- `diagnostico_terminal.ps1` - Diagnóstico de problemas de terminal

**Debug y Validación:**
- `debug_game_engine.py` - Debug específico del motor
- `test_ascii_safe.ps1` - Validación de caracteres ASCII
- `test_commit_system.ps1` - Testing del sistema de commits

### 📁 packaging/ - Herramientas de Empaquetado
**Scripts de distribución** para crear ejecutables y releases:
- `package_improved.py` - Empaquetado avanzado con PyInstaller
- Configuración optimizada para ejecutables standalone

### 📁 migration/ - Herramientas de Migración
**Scripts de migración** para transformaciones de datos y estructura:
- Migración de sistema de guardado pickle → SQLite
- Herramientas de refactorización automática
- Scripts de validación de migración

### 📁 archive/ - Scripts Obsoletos
**Archivos históricos** que ya no se usan pero se conservan:
- Scripts descontinuados con valor histórico
- Versiones anteriores de herramientas
- Experimentos completados

## 🚀 Guía de Uso

### Para Scripts de Producción
```powershell
# Ejecutar desde la raíz del proyecto
.\dev-tools\scripts\intelligent_commit.ps1
.\dev-tools\scripts\workspace_cleanup.ps1
```

### Para Testing y Experimentación
```powershell
# Tests del motor del juego
python .\dev-tools\testing\test_game_engine_simple.py

# Tests de configuración
python .\dev-tools\testing\test_config_system.py
```

### Para Debugging
```powershell
# Debug del motor del juego
python .\dev-tools\debugging\debug_game_engine.py
```

## 📋 Criterios de Organización

### ✅ scripts/ (Producción)
- Scripts estables y probados
- Uso regular en el desarrollo
- Funcionalidad completa y documentada

### 🧪 testing/ (Experimental)
- Scripts en desarrollo o experimentales
- Pruebas unitarias y de integración
- Herramientas de diagnóstico

### 🐛 debugging/ (Debug)
- Herramientas específicas de debugging
- Scripts para análisis de problemas

### 📦 archive/ (Histórico)
- Scripts obsoletos o descontinuados
- Conservados por referencia histórica

## 🎯 **USO RÁPIDO**

### Scripts Principales Más Usados:
```bash
# Commits rápidos
.\dev-tools\scripts\simple_commit.ps1 "mensaje"

# Limpieza completa
.\dev-tools\scripts\workspace_cleanup.ps1 -Level "light"

# Testing del proyecto
python dev-tools\testing\test_unified_system.py

# Empaquetado para distribución
python dev-tools\packaging\package_improved.py
```

### Navegación por Tipo de Herramienta:
- **🔨 Desarrollo diario**: `scripts/` (commits, limpieza, análisis)
- **🧪 Testing y validación**: `testing/` (tests unitarios e integración)
- **📦 Distribución**: `packaging/` (creación de ejecutables)
- **🔄 Migración**: `migration/` (transformaciones de datos)
- **📁 Histórico**: `archive/` (referencia de versiones anteriores)

## ⚠️ **ESTRUCTURA CENTRALIZADA**

**ANTES**: Archivos dispersos en `scripts/`, `tests/`, `tools/`, raíz del proyecto
**AHORA**: Todo centralizado en `dev-tools/` con categorización clara

> **🎯 OBJETIVO CUMPLIDO**: Raíz del proyecto limpia y herramientas organizadas

Esta estructura elimina la redundancia y facilita el mantenimiento del proyecto.
