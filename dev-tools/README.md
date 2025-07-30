# dev-tools/ - Herramientas de Desarrollo

## 🛠️ **PROPÓSITO**
Conjunto completo de herramientas, scripts y utilidades para el desarrollo, testing, migración y mantenimiento del proyecto **SiK Python Game**. Este directorio centraliza todas las herramientas que no forman parte del juego en sí.

> **🎯 ESTRUCTURA UNIFICADA**: Todos los elementos de los antiguos directorios `scripts/`, `tests/`, `tools/` y archivos de debugging han sido organizados aquí.

## 📊 **ESTADO ACTUAL**
- **Scripts automatizados**: Commit, limpieza, migración
- **Testing completo**: Unitarios, integración, funcionales
- **Migración SQLite**: Herramientas de migración de datos
- **Archivos obsoletos**: Sistema de archivo organizado (29 archivos movidos)
- **Total organizados**: 102+ archivos de herramientas
- **debugging/**: 1 archivo (debug del motor)
- **archive/**: 9 archivos (scripts obsoletos)
- **packaging/**: 1 archivo (empaquetado)
- **fixtures/**: 5 archivos (datos de prueba)

## 🗂️ Estructura Detallada

### 📁 scripts/ - Scripts de Producción (43 archivos)
**TODOS** los scripts estables y de uso frecuente del proyecto:

**Gestión de Commits Inteligentes:**
- `intelligent_commit.ps1`, `intelligent_commit.py`
- `professional_commit.py`, `robust_commit.py`
- `smart_commit.py`, `smart_commit_system.py`
- `simple_commit.ps1`, `unified_commit.ps1`
- `quick_commit.py`

**Limpieza y Mantenimiento:**
- `cleanup_project.py`, `cleanup_project_v2.py`
- `cleanup_tests.py`, `cleanup_commit_scripts.py`
- `workspace_cleanup.ps1`, `workspace_cleanup_fixed.ps1`
- `clean_asset_names.py`

**Herramientas VS Code:**
- `close_vscode_tabs.ps1`, `definitive_tab_closer.ps1`
- `simple_tab_closer.ps1`, `working_tab_closer.ps1`
- `smart_tab_manager.ps1`, `simple_uri_closer.ps1`
- `real_vscode_methods.ps1`, `vscode_cleanup_sendkeys.ps1`

**Análisis y Organización:**
- `analyze_file_sizes.py`, `file_analyzer.py`
- `reorganize_characters.py`, `reorganize_guerrero.py`
- `validar_documentacion.py`

**Automatización y Setup:**
- `setup_auto_cleanup.ps1`, `setup_dev_tools.sh`
- `pre_commit_check.py`, `reset_terminal_state.ps1`
- `verify_all_paths.ps1`

**Herramientas de Testing y Debug:**
- `run_tests.py`, `run_unified_tests.py`
- `final_cleanup_demo.ps1`

### 📁 testing/ - Scripts de Pruebas y Experimentación (37 archivos)
**TODOS** los scripts experimentales y de testing del proyecto:

**Tests del Motor del Juego:**
- `test_game_engine_simple.py`
- `test_menu_flow.py`
- `test_simple_game.py`
- `test_atmospheric_effects.py`

**Tests de Sistemas:**
- `test_config.py`, `test_config_manager.py`
- `test_config_simple.py`, `test_config_system.py`
- `test_enemy_system.py`, `test_powerup_system.py`
- `test_projectile_system.py`, `test_unified_system.py`
- `test_simple_config.py`

**Tests de Funcionalidad:**
- `test_game_functionality.py`
- `test_game_launch.py`

**Tests de VS Code y Terminal (PowerShell):**
- `test_vscode_tabs.ps1`, `test_controlled_tabs.ps1`
- `test_final_method.ps1`, `test_final_method_fixed.ps1`
- `test_sendkeys_fixed.ps1`, `test_sendkeys_only.ps1`
- `test_terminal_responsive.ps1`, `test_terminal_simple.ps1`
- `test_uri_only.ps1`, `test_palette_only.ps1`

**Diagnóstico y Debug:**
- `debug_vscode_path.ps1`, `diagnose_vscode_problem.ps1`
- `diagnostico_terminal.ps1`, `investigate_vscode_api.ps1`
- `test_commit_system.ps1`, `test_integration.ps1`
- `test_detection_behavior.ps1`, `test_problema_especifico.ps1`
- `test_ascii_safe.ps1`

**Subdirectorio fixtures/ (5 archivos):**
- Datos de prueba y configuraciones temporales

### 📁 debugging/ - Herramientas de Debugging (1 archivo)
Scripts específicos para debugging del motor del juego:
- `debug_game_engine.py` - Debug específico del motor de juego

### 📁 migration/ - Herramientas de Migración (6 archivos)
Scripts relacionados con SQLite y migraciones de datos:
- Herramientas de base de datos
- Scripts de migración de sistema de guardado

### 📁 packaging/ - Herramientas de Empaquetado (1 archivo)
Scripts para generar distribuciones del juego:
- Empaquetado de releases

### 📁 archive/ - Scripts Obsoletos (9 archivos)
Scripts que ya no se usan pero se conservan por valor histórico:
- Scripts descontinuados
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

## ⚠️ Directorio Unificado

**ANTES**: Archivos dispersos en `scripts/`, `tests/`, `tools/`, raíz del proyecto
**AHORA**: Todo centralizado en `dev-tools/` con categorización clara

Esta estructura elimina la redundancia y facilita el mantenimiento del proyecto.
