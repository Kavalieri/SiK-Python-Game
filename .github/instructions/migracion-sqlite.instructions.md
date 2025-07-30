# Migración SQLite

## 🗄️ **Migración SQLite** (Fase 1 ✅ - Fase 2-4 pendiente)
- **Sistema mixto inteligente**: SQLite para datos complejos, JSON para configuración
- **DatabaseManager**: Modularizado y funcional
- **SchemaManager**: Sistema completo de tablas
- **Próximo**: ConfigManager (264→3x150 líneas) + SaveManager (365→4x150 líneas)
- **Eliminar hardcodeo**: Separar lógica de configuración completamente

## 🚨 **Archivos Críticos que Requieren Refactorización URGENTE**
1. **src/utils/atmospheric_effects.py** (249 líneas) - **CRÍTICO** - Sin migración SQLite
2. **src/utils/input_manager.py** (244 líneas) - **CRÍTICO** - Sin migración SQLite
3. **src/utils/desert_background.py** (233 líneas) - **CRÍTICO** - Sin migración SQLite
4. **🗄️ src/ui/menu_creators.py** (230 líneas) - **CRÍTICO** - UI optimization
5. **🗄️ src/entities/enemy_types.py** (230 líneas) - **MIGRACIÓN SQLITE** (config/enemies.json)

**⚠️ IMPORTANTE**: Consultar `docs/REFACTORIZACION_ESTADO_ACTUAL.md` antes de editar
