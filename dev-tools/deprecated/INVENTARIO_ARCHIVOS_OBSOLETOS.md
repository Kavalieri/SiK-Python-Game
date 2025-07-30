# Inventario de Archivos Obsoletos - SiK Python Game

## 📋 Análisis Completo de Archivos Obsoletos
**Fecha de análisis**: 30 de Julio, 2025
**Estado**: Proyecto post-modernización con 99.3% archivos compliant

## 🎯 **OBJETIVO**
Mover todos los archivos obsoletos, de respaldo, testing y duplicados fuera de `src/` para mantener un código base limpio y enfocado en desarrollo.

## 📊 **RESUMEN EJECUTIVO**
- **Total archivos obsoletos identificados**: 47 archivos
- **Categorías principales**: backup/original (32), old (6), new/duplicate (5), testing (4)
- **Tamaño total estimado**: ~15,000 líneas de código obsoleto
- **Impacto en `src/`**: Limpieza masiva requerida

---

## 🗂️ **CATEGORÍAS DE ARCHIVOS OBSOLETOS**

### 📦 **1. ARCHIVOS BACKUP/ORIGINAL** (32 archivos)
**Ubicación destino**: `dev-tools/deprecated/backup-original-files/`

#### 🔧 **src/utils/** (20 archivos)
```
src/utils/asset_manager_original_backup.py        → 464 líneas
src/utils/character_assets_original_backup.py     → 214 líneas
src/utils/atmospheric_effects_original.py         → 197 líneas
src/utils/desert_background_original.py           → 381 líneas
src/utils/world_generator_original.py             → 277 líneas
src/utils/schema_manager_original.py              → 290 líneas
src/utils/save_manager_original.py                → 365 líneas
src/utils/save_compatibility_original.py          → 278 líneas
src/utils/config_manager_original.py              → 264 líneas
src/utils/database_manager_original.py            → 153 líneas
src/utils/database_manager_backup.py              → 194 líneas
src/utils/schema_migrations_backup.py             → 169 líneas
```

#### 🎮 **src/entities/** (3 archivos)
```
src/entities/player_original.py                   → 324 líneas
src/entities/player_combat_original.py            → 323 líneas
src/entities/powerup_original.py                  → 231 líneas
src/entities/entity_core_backup.py                → 237 líneas
src/entities/enemy_types_backup.py                → 240 líneas
```

#### 🎬 **src/scenes/** (2 archivos)
```
src/scenes/character_ui_original.py               → 350 líneas
src/scenes/loading_scene_original.py              → 275 líneas
```

#### 🖥️ **src/ui/** (1 archivo)
```
src/ui/hud_original_backup.py                     → 397 líneas
```

### 🕰️ **2. ARCHIVOS OLD** (6 archivos)
**Ubicación destino**: `dev-tools/deprecated/old-versions/`

```
src/core/game_engine_old.py                       → 299 líneas
src/entities/enemy_old.py                         → 307 líneas
src/ui/menu_callbacks_old.py                      → 336 líneas
```

### 🔄 **3. ARCHIVOS DUPLICATE/NEW** (5 archivos)
**Ubicación destino**: `dev-tools/deprecated/duplicate-versions/`

```
src/utils/world_generator_new.py                  → Duplicado de world_generator.py
src/utils/asset_manager_new.py                    → Duplicado de asset_manager.py
src/utils/atmospheric_effects_new.py              → Duplicado de atmospheric_effects.py
src/core/game_engine_new.py                       → Duplicado de game_engine.py
src/ui/menu_callbacks_new.py                      → Duplicado de menu_callbacks.py
src/ui/hud_new.py                                  → Duplicado de hud.py
```

### 🔧 **4. ARCHIVOS TESTING EN SRC/** (4 archivos)
**Ubicación destino**: `dev-tools/testing/moved-from-src/`

```
debug_game_engine.py                              → Script de debug en raíz
test_game_engine_simple.py                        → Test en raíz
test_menu_flow.py                                  → Test en raíz
test_simple_game.py                                → Test en raíz
```

---

## 📁 **DIRECTORIO HTMLCOV**
**Tipo**: Reporte de cobertura de código (coverage.py)
**Estado**: SEGURO PARA ELIMINAR - Se regenera automáticamente
**Acción**: Añadir a `.gitignore` si no está ya
**Razón**: Los reportes HTML de cobertura son generados y no deben versionarse

---

## 🛠️ **PLAN DE LIMPIEZA**

### ✅ **FASE 1: Mover Archivos Backup/Original**
```bash
# Mover archivos _original_backup, _original, _backup
mv src/utils/*_original*.py dev-tools/deprecated/backup-original-files/utils/
mv src/entities/*_original*.py dev-tools/deprecated/backup-original-files/entities/
mv src/scenes/*_original*.py dev-tools/deprecated/backup-original-files/scenes/
mv src/ui/*_original*.py dev-tools/deprecated/backup-original-files/ui/
mv src/utils/*_backup*.py dev-tools/deprecated/backup-original-files/utils/
mv src/entities/*_backup*.py dev-tools/deprecated/backup-original-files/entities/
```

### ✅ **FASE 2: Mover Archivos Old**
```bash
# Mover archivos _old
mv src/core/*_old.py dev-tools/deprecated/old-versions/core/
mv src/entities/*_old.py dev-tools/deprecated/old-versions/entities/
mv src/ui/*_old.py dev-tools/deprecated/old-versions/ui/
```

### ✅ **FASE 3: Resolver Duplicados New**
```bash
# Verificar diferencias y mover archivos _new
mv src/utils/*_new.py dev-tools/deprecated/duplicate-versions/utils/
mv src/core/*_new.py dev-tools/deprecated/duplicate-versions/core/
mv src/ui/*_new.py dev-tools/deprecated/duplicate-versions/ui/
```

### ✅ **FASE 4: Limpiar Tests en Raíz**
```bash
# Mover tests de la raíz al sistema de testing
mv debug_game_engine.py dev-tools/testing/moved-from-src/
mv test_*.py dev-tools/testing/moved-from-src/
```

### ✅ **FASE 5: Limpiar htmlcov**
```bash
# Eliminar reporte de cobertura (se regenera)
rm -rf htmlcov/
echo "htmlcov/" >> .gitignore  # Si no está ya
```

---

## 📊 **MÉTRICAS POST-LIMPIEZA**

### 🎯 **Impacto Esperado**
- **Archivos eliminados de src/**: 47 archivos
- **Líneas de código reducidas**: ~15,000 líneas
- **Estructura src/ final**: Solo archivos activos y operativos
- **Mantenibilidad**: Considerablemente mejorada

### 📁 **Estructura src/ Final** (archivos activos únicamente)
```
src/
├── main.py
├── core/
│   ├── game_engine.py
│   ├── game_engine_core.py
│   ├── game_engine_events.py
│   ├── game_engine_scenes.py
│   ├── game_state.py
│   └── scene_manager.py
├── entities/
│   ├── character_data.py
│   ├── enemy.py
│   ├── enemy_behavior.py
│   ├── player.py
│   ├── [otros archivos activos...]
├── scenes/
│   ├── character_select_scene.py
│   ├── game_scene.py
│   ├── [otros archivos activos...]
├── ui/
│   ├── hud.py
│   ├── menu_callbacks.py
│   ├── [otros archivos activos...]
└── utils/
    ├── asset_manager.py
    ├── config_manager.py
    ├── save_manager.py
    └── [otros archivos activos...]
```

---

## 🚨 **VALIDACIONES PRE-LIMPIEZA**

### ✅ **Verificaciones Obligatorias**
1. **Verificar imports**: Ningún archivo activo importa archivos obsoletos
2. **Ejecutar tests**: Todos los tests pasan antes de mover archivos
3. **Backup completo**: Crear backup del estado actual
4. **Validar git**: Working directory limpio antes de comenzar

### ⚠️ **Advertencias**
- **NO eliminar**: Solo mover a `dev-tools/deprecated/`
- **Verificar dependencias**: Revisar imports cruzados
- **Mantener historial**: Los archivos mantienen su historial en git

---

## 🎯 **RESULTADO FINAL**

### ✅ **Proyecto Limpio y Organizado**
- **src/**: Solo código activo y operativo
- **dev-tools/deprecated/**: Archivos históricos organizados por categoría
- **Mantenibilidad**: Considerablemente mejorada
- **Claridad**: Código base enfocado en desarrollo futuro

### 📈 **Beneficios Inmediatos**
1. **Navegación mejorada**: Menos archivos confusos en src/
2. **IDE más rápido**: Menos archivos para indexar
3. **Claridad de propósito**: Solo código activo visible
4. **Desarrollo enfocado**: Sin distracciones de archivos obsoletos

---

**🎯 ESTADO**: PLAN LISTO PARA EJECUCIÓN
**📅 DURACIÓN ESTIMADA**: 30-45 minutos para ejecución completa
**🔒 RIESGO**: BAJO (solo movimientos, no eliminaciones)
