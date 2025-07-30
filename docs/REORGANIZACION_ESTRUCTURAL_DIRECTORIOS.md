# Reorganización Estructural de Directorios - SiK Python Game

## 🎯 Problema Identificado
La raíz del proyecto tiene demasiados directorios sueltos y archivos de test/debug que dificultan la navegación y mantenimiento.

## 📁 Nueva Estructura Propuesta

### `dev-tools/` - Herramientas de Desarrollo
Consolidar herramientas de desarrollo y scripts utilitarios:

#### `dev-tools/scripts/` - Scripts de Producción
- Scripts de commit (simple_commit.ps1, unified_commit.ps1)
- Scripts de limpieza (workspace_cleanup.ps1, vscode_cleanup_sendkeys.ps1)
- Scripts de análisis (analyze_file_sizes.py, file_analyzer.py)

#### `dev-tools/testing/` - Scripts de Prueba
- Todos los test_*.py/ps1 de scripts/
- Archivos de debugging y diagnóstico

#### `dev-tools/migration/` - Scripts de Migración SQLite
- initialize_schema.py (raíz)
- run_migration_step2.py (raíz)
- check_system.py (raíz)
- test_config_database.py (scripts/)

#### `dev-tools/archive/` - Scripts Obsoletos
- Scripts descontinuados pero con valor histórico
- Documentación de métodos probados

### `tests/` - Reorganizar Tests
Mantener pero limpiar:
- Tests de producción activos
- Mover tests experimentales a dev-tools/testing/

### `tools/` - Integrar en dev-tools/
- package_improved.py → dev-tools/packaging/
- debug_game_engine.py → dev-tools/debugging/

### `test_files/` - Eliminar o Integrar
- Archivos temporales → dev-tools/testing/fixtures/
- O eliminar si son obsoletos

## 📋 Archivos Raíz para Reorganizar

### Migración SQLite (→ dev-tools/migration/)
- `check_system.py`
- `initialize_schema.py`
- `run_migration_step2.py`
- `test_atmospheric_effects.py` (test temporal)

### Documentos Completados (→ docs/ARCHIVO/)
- `BANCO_PRUEBAS_COMPLETADO.md`
- `REFACTORIZACION_HUD_COMPLETADA.md`
- `refactorizacion_progreso.md` (si está obsoleto)

### Directorios Temporales
- `cleanup_temp_20250729/` → eliminar o archivar
- `backups__DISABLED/` → ya está deshabilitado

## 🎯 Estructura Final Deseada

```
📁 SiK-Python-Game/
├── 📁 src/                    # Código fuente del juego
├── 📁 config/                 # Configuraciones JSON
├── 📁 assets/                 # Assets del juego
├── 📁 tests/                  # Tests de producción únicamente
├── 📁 docs/                   # Documentación activa
├── 📁 docs/ARCHIVO/           # Documentación archivada
├── 📁 dev-tools/              # Herramientas desarrollo (NUEVO)
│   ├── 📁 scripts/            # Scripts producción
│   ├── 📁 testing/            # Scripts de prueba
│   ├── 📁 migration/          # Scripts migración SQLite
│   ├── 📁 packaging/          # Scripts empaquetado
│   ├── 📁 debugging/          # Tools debugging
│   └── 📁 archive/            # Scripts obsoletos
├── 📁 logs/                   # Logs del sistema
├── 📁 saves/                  # Archivos de guardado
├── 📁 releases/               # Releases empaquetados
├── 📄 pyproject.toml          # Configuración Python/Poetry
├── 📄 README.md               # Documentación principal
└── 📄 ... (archivos config raíz)
```

## ✅ Beneficios

1. **Navegación simplificada**: Menos directorios en raíz
2. **Organización lógica**: Herramientas agrupadas por función
3. **Separación clara**: Desarrollo vs producción
4. **Mantenibilidad**: Fácil identificar qué archivar/eliminar
5. **Escalabilidad**: Estructura preparada para crecimiento

## 🚀 Plan de Implementación

1. Crear estructura dev-tools/
2. Mover scripts por categorías
3. Reorganizar archivos raíz
4. Limpiar directorios obsoletos
5. Actualizar referencias en documentación
6. Commit estructural

## 📊 Métricas Esperadas

- **Directorios raíz**: ~15 → ~10 (33% reducción)
- **Archivos raíz sueltos**: ~8 → ~4 (50% reducción)
- **Organización scripts**: 100+ archivos organizados temáticamente
- **Mantenibilidad**: Sistema claro de archivo/obsolescencia
