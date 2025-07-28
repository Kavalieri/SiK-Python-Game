# PLAN DE REFACTORIZACIÓN V2 - LÍMITE 150 LÍNEAS

**Fecha**: 2025-07-29 00:24:32

## 📊 RESUMEN

- **Archivos a refactorizar**: 23
- **Módulos nuevos a crear**: ~69
- **Objetivo**: Todos los archivos < 150 líneas

## 🔧 ARCHIVOS A REFACTORIZAR


### src/scenes/character_select_scene.py (530 líneas)
**Dividir en:**
- character_ui.py, character_data.py, character_animations.py

**Prioridad:** ALTA

### src/scenes/game_scene.py (509 líneas)
**Dividir en:**
- game_logic.py, game_rendering.py, game_entities.py

**Prioridad:** ALTA

### src/entities/entity.py (434 líneas)
**Dividir en:**
- entity_base.py, entity_physics.py, entity_renderer.py

**Prioridad:** ALTA

### src/utils/save_manager.py (426 líneas)
**Dividir en:**
- save_encryption.py, save_validation.py, save_serializer.py

**Prioridad:** ALTA

### src/utils/desert_background.py (408 líneas)
**Dividir en:**
- background_renderer.py, background_generator.py, background_tiles.py

**Prioridad:** ALTA

### src/ui/hud.py (399 líneas)
**Dividir en:**
- hud_renderer.py, hud_data.py, hud_widgets.py

**Prioridad:** MEDIA

### src/utils/asset_manager.py (362 líneas)
**Dividir en:**
- asset_loader.py, asset_cache.py, asset_organizer.py

**Prioridad:** MEDIA

### src/entities/player.py (341 líneas)
**Dividir en:**
- player_controller.py, player_animations.py, player_ui.py

**Prioridad:** MEDIA

### src/entities/enemy.py (338 líneas)
**Dividir en:**
- enemy_ai.py, enemy_combat.py, enemy_spawner.py

**Prioridad:** MEDIA

### src/utils/world_generator.py (315 líneas)
**Dividir en:**
- world_builder.py, world_tiles.py, world_objects.py

**Prioridad:** MEDIA

### src/ui/menu_callbacks.py (306 líneas)
**Dividir en:**
- menu_navigation.py, menu_actions.py, menu_validation.py

**Prioridad:** MEDIA

### src/ui/menu_factory.py (303 líneas)
**Dividir en:**
- menu_builder.py, menu_themes.py, menu_widgets.py

**Prioridad:** MEDIA

### src/utils/animation_manager.py (288 líneas)
**Dividir en:**
- animation_loader.py, animation_player.py, animation_cache.py

**Prioridad:** MEDIA

### src/entities/powerup.py (246 líneas)
**Dividir en:**
- powerup_types.py, powerup_effects.py, powerup_spawner.py

**Prioridad:** BAJA

### src/entities/player_combat.py (243 líneas)
**Dividir en:**
- combat_mechanics.py, combat_weapons.py, combat_effects.py

**Prioridad:** BAJA

### src/scenes/loading_scene.py (241 líneas)
**Dividir en:**
- loading_ui.py, loading_logic.py, loading_assets.py

**Prioridad:** BAJA

### src/utils/input_manager.py (240 líneas)
**Dividir en:**
- input_handler.py, input_mapping.py, input_validation.py

**Prioridad:** BAJA

### src/entities/enemy_types.py (232 líneas)
**Dividir en:**
- enemy_definitions.py, enemy_stats.py, enemy_abilities.py

**Prioridad:** BAJA

### src/core/game_engine.py (209 líneas)
**Dividir en:**
- engine_core.py, engine_loop.py, engine_events.py

**Prioridad:** BAJA

### src/entities/tile.py (207 líneas)
**Dividir en:**
- tile_types.py, tile_renderer.py, tile_collision.py

**Prioridad:** BAJA

### src/entities/player_effects.py (175 líneas)
**Dividir en:**
- effects_manager.py, effects_types.py, effects_ui.py

**Prioridad:** BAJA

### src/ui/menu_manager.py (164 líneas)
**Dividir en:**
- menu_controller.py, menu_state.py

**Prioridad:** BAJA

### src/utils/config_manager.py (164 líneas)
**Dividir en:**
- config_loader.py, config_validator.py, config_defaults.py

**Prioridad:** BAJA

## 📋 ESTRATEGIA DE REFACTORIZACIÓN

### Fase 1: Archivos Críticos (>400 líneas)
1. character_select_scene.py
2. game_scene.py
3. entity.py

### Fase 2: Archivos Importantes (250-400 líneas)
1. save_manager.py
2. desert_background.py
3. hud.py
4. asset_manager.py
5. player.py
6. enemy.py

### Fase 3: Archivos Restantes (150-250 líneas)
- Todos los demás archivos

## 🎯 OBJETIVOS

1. **Modularidad máxima**: Cada módulo con responsabilidad única
2. **Reutilización**: Componentes intercambiables
3. **Mantenibilidad**: Código fácil de entender y modificar
4. **Testabilidad**: Módulos independientes y testeables

---
*Plan generado automáticamente por cleanup_project_v2.py*
