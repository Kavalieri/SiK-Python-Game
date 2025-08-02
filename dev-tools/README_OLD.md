# Dev Tools - SiK Python Game

## 📁 Estructura de Herramientas de Desarrollo

Este directorio contiene todas las herramientas, scripts y utilidades para el desarrollo del proyecto SiK Python Game.

### 📋 Organización por Categorías

#### `scripts/` - Scripts de Producción Activos
Scripts estables y utilizados regularmente en el desarrollo:
- **Commits**: `simple_commit.ps1`, `unified_commit.ps1`
- **Limpieza**: `workspace_cleanup.ps1`, `vscode_cleanup_sendkeys.ps1`
- **Análisis**: `analyze_file_sizes.py`, `file_analyzer.py`
- **Organización**: `reorganize_*.py`

#### `testing/` - Scripts de Prueba y Testing
Scripts para pruebas, debugging y validación:
- **Tests PowerShell**: `test_*.ps1`
- **Tests Python**: `test_*.py` (experimentales)
- **Diagnósticos**: `diagnose_*.ps1`, `debug_*.ps1`
- **Fixtures**: Archivos de prueba temporales

#### `migration/` - Scripts de Migración SQLite
Scripts específicos para la migración a SQLite:
- **Inicialización**: `initialize_schema.py`
- **Migración**: `run_migration_step2.py`
- **Verificación**: `check_system.py`
- **Tests**: `test_*_database.py`

#### `packaging/` - Herramientas de Empaquetado
Scripts para generar releases y distribuciones:
- **Empaquetado**: `package_improved.py`
- **Distribución**: Scripts de release

#### `debugging/` - Herramientas de Debug
Herramientas para debugging del juego:
- **Debug Game**: `debug_game_engine.py`
- **Análisis**: Herramientas de análisis de rendimiento

#### `archive/` - Scripts Obsoletos
Scripts que ya no se usan pero se conservan por valor histórico:
- Scripts descontinuados
- Versiones anteriores de herramientas
- Experimentos completados

## 🚀 Uso

### Scripts de Producción
```powershell
# Commit rápido
.\dev-tools\scripts\simple_commit.ps1 "mensaje"

# Limpieza workspace
.\dev-tools\scripts\workspace_cleanup.ps1 -Level "light"

# Análisis de archivos
python .\dev-tools\scripts\analyze_file_sizes.py
```

### Testing y Debugging
```powershell
# Tests de integración
.\dev-tools\testing\test_commit_system.ps1

# Debugging del juego
python .\dev-tools\debugging\debug_game_engine.py
```

### Migración SQLite
```powershell
# Inicializar esquema
python .\dev-tools\migration\initialize_schema.py

# Ejecutar migración
python .\dev-tools\migration\run_migration_step2.py
```

## 📋 Migración desde Estructura Anterior

### Desde `scripts/`
- Scripts activos → `dev-tools/scripts/`
- Tests → `dev-tools/testing/`
- Scripts obsoletos → `dev-tools/archive/`

### Desde `tools/`
- Herramientas packaging → `dev-tools/packaging/`
- Herramientas debug → `dev-tools/debugging/`

### Desde raíz
- Scripts migración SQLite → `dev-tools/migration/`
- Tests temporales → `dev-tools/testing/`

## 🎯 Criterios de Organización

### `scripts/` (Producción)
- ✅ Scripts utilizados regularmente
- ✅ Funcionalidad estable y probada
- ✅ Documentados y mantenidos

### `testing/` (Experimental)
- ⚠️ Scripts de prueba
- ⚠️ Herramientas de diagnóstico
- ⚠️ Tests experimentales

### `archive/` (Obsoleto)
- 📦 Scripts descontinuados
- 📦 Versiones antiguas
- 📦 Experimentos completados

## 🔄 Mantenimiento

1. **Revisión mensual**: Evaluar scripts en testing/ para promoción o archivo
2. **Limpieza trimestral**: Mover scripts obsoletos a archive/
3. **Documentación**: Mantener este README actualizado
4. **Referencias**: Actualizar rutas en documentación del proyecto

---

**Nota**: Esta reorganización mejora la mantenibilidad y claridad del proyecto, separando herramientas de desarrollo del código principal del juego.
