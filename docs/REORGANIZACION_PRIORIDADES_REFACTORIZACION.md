# Reorganización de Prioridades - Refactorización Crítica

## 🎯 Objetivo Completado
Reorganizar las instrucciones de GitHub Copilot para dar **máxima prioridad** a la refactorización de archivos críticos y documentación de funciones.

## 🚨 Cambios Implementados

### 1. **Prioridad Máxima al Inicio**
- Movida sección de refactorización al **primer lugar** en las instrucciones
- Establecido protocolo **OBLIGATORIO** de consulta a archivos de seguimiento
- Definidas responsabilidades primarias en orden de importancia

### 2. **Archivos de Seguimiento Centralizados**
- **Archivo movido**: `refactorizacion_progreso.md` → `docs/refactorizacion_progreso.md`
- **Estado actual**: 23 archivos críticos identificados para división
- **Documentación**: 2231 líneas en `docs/FUNCIONES_DOCUMENTADAS.md`

### 3. **Lista de Archivos Críticos Visible**
Los **11 archivos más críticos** (>300 líneas) están ahora en lugar prominente:
1. `src/entities/entity.py` (479 líneas) - **CRÍTICO**
2. `src/utils/asset_manager.py` (464 líneas) - **CRÍTICO**
3. `src/ui/hud.py` (397 líneas) - **CRÍTICO**
4. `src/entities/player.py` (390 líneas) - **CRÍTICO**
5. `src/entities/player_combat.py` (382 líneas) - **CRÍTICO**
6. `src/utils/desert_background.py` (381 líneas) - **CRÍTICO**
7. `src/entities/enemy.py` (373 líneas) - **CRÍTICO**
8. `src/utils/save_manager.py` (365 líneas) - **CRÍTICO**
9. `src/core/game_engine.py` (352 líneas) - **CRÍTICO**
10. `src/scenes/character_ui.py` (350 líneas) - **CRÍTICO**
11. `src/ui/menu_callbacks.py` (336 líneas) - **CRÍTICO**

### 4. **Protocolo de Trabajo Obligatorio**
Establecido flujo de trabajo que **DEBE** seguirse:
1. **ANTES**: consultar `docs/refactorizacion_progreso.md`
2. **DURANTE**: actualizar `docs/FUNCIONES_DOCUMENTADAS.md`
3. **DESPUÉS**: actualizar ambos archivos de seguimiento
4. **LÍMITE**: 150 líneas máximo por archivo

### 5. **Proceso de División Seguro**
Definido protocolo específico con 6 pasos:
1. Backup del archivo original
2. Tests para validar estado actual
3. División por responsabilidades específicas
4. Validación de funcionalidad completa
5. Commit atómico por archivo dividido
6. Actualización automática de documentación

## 📋 Estructura Actualizada de Instrucciones

### Orden de Prioridad (Nuevo)
1. **🚨 REFACTORIZACIÓN EN CURSO** (Máxima prioridad)
2. **📋 Automantenimiento** (Responsabilidades primarias)
3. **🚨 Archivos Críticos** (Lista específica)
4. **🔧 Proceso de División** (Metodología segura)
5. **📋 Regla Crítica** (Límite 150 líneas)
6. **Resto del contenido** (Contexto, stack, arquitectura, etc.)

### Eliminaciones Realizadas
- **Sección duplicada** de refactorización que estaba más abajo
- **Referencias obsoletas** a ubicaciones anteriores de archivos
- **Información redundante** sobre prioridades

## ✅ Estado Actual

### Archivos de Seguimiento
- ✅ `docs/refactorizacion_progreso.md` - Centralizado y accesible
- ✅ `docs/FUNCIONES_DOCUMENTADAS.md` - 2231 líneas documentadas
- ✅ `.github/copilot-instructions.md` - Reorganizado con máxima prioridad

### Protocolo Activo
- ✅ **Consulta obligatoria** de estado antes de cambios
- ✅ **División inmediata** de archivos >150 líneas
- ✅ **Actualización automática** de documentación
- ✅ **Commits atómicos** por cada refactorización

## 🎯 Próximos Pasos

### Inmediatos
1. **Aplicar** el protocolo en próximas operaciones
2. **Dividir** archivos críticos uno por uno
3. **Documentar** progreso en archivos de seguimiento

### Mediano Plazo
1. **Completar** división de 23 archivos críticos
2. **Alcanzar** límite de 150 líneas en todos los archivos
3. **Finalizar** documentación completa de funciones

### Validación
- Cada operación debe consultar `docs/refactorizacion_progreso.md`
- Cada función nueva debe ir a `docs/FUNCIONES_DOCUMENTADAS.md`
- Cada archivo dividido debe tener commit atómico

---

**Resultado**: Las instrucciones ahora priorizan EXCLUSIVAMENTE la refactorización hasta completar la división de archivos críticos.
