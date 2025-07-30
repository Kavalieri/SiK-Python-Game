# Instrucciones para GitHub Copilot - SiK Python Game

## 🗄️ PRIORIDAD MÁXIMA: REFACTORIZACIÓN + MIGRACIÓN SQLITE

### Estado Crítico del Proyecto
- **23 archivos CRÍTICOS** exceden límite de 150 líneas
- **11 archivos >300 líneas** requieren división URGENTE
- **Migración SQLite INTEGRADA** con refactorización simultánea
- **Sistema de documentación COHESIVO** con referencias cruzadas obligatorias

### 🔗 Sistema de Documentación Integrado (CONSULTAR EN ORDEN)
1. **`docs/refactorizacion_progreso.md`** - **DOCUMENTO CENTRAL** - Consultar PRIMERO siempre
2. **`docs/PLAN_MIGRACION_SQLITE.md`** - Plan detallado y checklist de migración SQLite
3. **`docs/FUNCIONES_DOCUMENTADAS.md`** - **ACTUALIZAR** con cada función nueva/modificada
4. **`docs/INDICE_MIGRACION_SQLITE.md`** - Vista rápida del progreso de migración
5. **Este archivo** - Reglas base del proyecto

### Protocolo de Trabajo OBLIGATORIO
1. **ANTES de cualquier cambio**: consultar [`docs/refactorizacion_progreso.md`](../docs/refactorizacion_progreso.md)
2. **Si toca persistencia**: revisar [`docs/PLAN_MIGRACION_SQLITE.md`](../docs/PLAN_MIGRACION_SQLITE.md)
3. **DURANTE cualquier edición**: actualizar [`docs/FUNCIONES_DOCUMENTADAS.md`](../docs/FUNCIONES_DOCUMENTADAS.md)
4. **DESPUÉS de cualquier cambio**: actualizar progreso en documentos correspondientes
5. **LÍMITE ABSOLUTO**: 150 líneas por archivo - dividir si se excede GitHub Copilot - SiK Python Game

## � PRIORIDAD MÁXIMA: REFACTORIZACIÓN EN CURSO

### Estado Crítico del Proyecto
- **23 archivos CRÍTICOS** exceden límite de 150 líneas
- **11 archivos >300 líneas** requieren división URGENTE
- **Refactorización OBLIGATORIA** antes de nuevas features
- **Documentación automática** de todas las funciones es MANDATORIA

### Archivos de Seguimiento CRÍTICOS (revisar SIEMPRE)
- `docs/refactorizacion_progreso.md` - **ESTADO ACTUAL** de división de archivos
- `docs/FUNCIONES_DOCUMENTADAS.md` - **CATÁLOGO COMPLETO** de funciones
- `CHANGELOG.md` - **REGISTRO** de cambios importantes
- Este archivo - **BASE** de reglas del proyecto

### Protocolo de Trabajo OBLIGATORIO
1. **ANTES de cualquier cambio**: consultar `docs/refactorizacion_progreso.md`
2. **DURANTE cualquier edición**: actualizar `docs/FUNCIONES_DOCUMENTADAS.md`
3. **DESPUÉS de cualquier cambio**: actualizar ambos archivos de seguimiento
4. **LÍMITE ABSOLUTO**: 150 líneas por archivo - dividir si se excede

## �📋 Automantenimiento y Documentación Crítica

### Responsabilidades Primarias
- **PRIORIDAD 1**: Consultar y actualizar `docs/refactorizacion_progreso.md` en CADA operación
- **PRIORIDAD 2**: Actualizar `docs/FUNCIONES_DOCUMENTADAS.md` con TODAS las funciones nuevas/modificadas
- **PRIORIDAD 3**: Dividir INMEDIATAMENTE cualquier archivo que exceda 150 líneas
- **Mantener actualizado** este archivo con cualquier cambio significativo del proyecto
- **Actualizar automáticamente** `CHANGELOG.md` con cambios importantes
- **Actualizar automáticamente** `README.md` con cambios importantes
- **Documentar decisiones** importantes en archivos correspondientes
- **Reflejar cambios** de arquitectura, reglas o convenciones inmediatamente

### Archivos de Seguimiento Obligatorio
- **`docs/refactorizacion_progreso.md`** - **DOCUMENTO CENTRAL** - Estado de refactorización (23 archivos críticos)
- **`docs/PLAN_MIGRACION_SQLITE.md`** - Plan detallado de migración base de datos con checklist
- **`docs/FUNCIONES_DOCUMENTADAS.md`** - Catálogo completo de funciones por módulo (actualizar siempre)
- **`docs/INDICE_MIGRACION_SQLITE.md`** - Vista rápida del progreso de migración SQLite
- **`CHANGELOG.md`** - Registro de cambios significativos
- **Este archivo** - Base de reglas del proyecto

## 🗄️ Migración SQLite Integrada

### Estrategia de Refactorización con Base de Datos
- **Enfoque dual**: División de archivos + migración a SQLite simultánea
- **Prioridad**: SaveManager (365 líneas) y ConfigManager (264 líneas) primero
- **Objetivo**: Resolver duplicaciones config/src + límites de líneas
- **Referencias**: [`PLAN_MIGRACION_SQLITE.md`](../docs/PLAN_MIGRACION_SQLITE.md) para esquemas y checklist detallado

### Archivos con Migración SQLite Prioritaria
1. **SaveManager** (365 líneas) → 4 módulos + SQLite (partidas_guardadas)
2. **ConfigManager** (264 líneas) → 3 módulos + SQLite (configuraciones, personajes, enemigos)
3. **GameState** (151 líneas) → 3 módulos + SQLite (estadisticas_juego)

## 📋 Regla Crítica: Límite de Líneas
**NINGÚN archivo puede superar 150 líneas**. Dividir inmediatamente si se excede.
**REGLA DE DIVISIÓN**: Dividir SIEMPRE en 2 módulos operativos preservando toda la funcionalidad útil.

## 🚨 Archivos Críticos que Requieren Refactorización URGENTE

### Archivos Críticos (>300 líneas) - División INMEDIATA + Migración SQLite
1. **src/entities/entity.py** (479 líneas) - **CRÍTICO** - Sin migración SQLite (objetos en memoria)
2. **src/utils/asset_manager.py** (464 líneas) - **CRÍTICO** - Posible cache SQLite futuro
3. **src/ui/hud.py** (397 líneas) - **CRÍTICO** - Sin migración SQLite
4. **src/entities/player.py** (390 líneas) - **CRÍTICO** - Sin migración SQLite
5. **src/entities/player_combat.py** (382 líneas) - **CRÍTICO** - Sin migración SQLite
6. **src/utils/desert_background.py** (381 líneas) - **CRÍTICO** - Sin migración SQLite
7. **src/entities/enemy.py** (373 líneas) - **CRÍTICO** - Sin migración SQLite (objetos en memoria)
8. **🗄️ src/utils/save_manager.py** (365 líneas) - **CRÍTICO + MIGRACIÓN SQLITE** - pickle→SQLite
9. **src/core/game_engine.py** (352 líneas) - **CRÍTICO** - Sin migración SQLite
10. **src/scenes/character_ui.py** (350 líneas) - **CRÍTICO** - Sin migración SQLite
11. **src/ui/menu_callbacks.py** (336 líneas) - **CRÍTICO** - Sin migración SQLite

### Archivos Moderados con Migración SQLite Prioritaria
- **🗄️ src/utils/config_manager.py** (264 líneas) - **MIGRACIÓN SQLITE** - JSON→SQLite
- **🗄️ src/core/game_state.py** (151 líneas) - **MIGRACIÓN SQLITE** - Estadísticas→SQLite

### ⚠️ IMPORTANTE: Antes de editar cualquier archivo
1. **Consultar** `docs/refactorizacion_progreso.md` para ver estado actual
2. **Si archivo >150 líneas**: DIVIDIR antes de cualquier cambio
3. **Actualizar** ambos archivos de seguimiento después de cambios

### 🔧 Proceso de División Seguro (OBLIGATORIO)
**REGLA FUNDAMENTAL**: **NUNCA eliminar métodos útiles** - SIEMPRE dividir en 2 partes operativas

1. **Backup** del archivo original en carpeta temporal
2. **Tests** ejecutar para validar estado actual
3. **Dividir en 2 módulos operativos** por responsabilidades claras (NO eliminar funcionalidad)
4. **Mantener APIs completas** - preservar todos los métodos públicos útiles
5. **Validar** funcionalidad completa tras división (100% equivalencia)
6. **Commit** atómico por cada archivo dividido
7. **Actualizar** documentación de funciones automáticamente

#### Estrategia de División (PREFERIR siempre):
- **Opción 1**: División funcional (Core + Extensions, Manager + Operations, etc.)
- **Opción 2**: División por responsabilidad (Input + Output, Data + Logic, etc.)
- **Opción 3**: División temporal (Init + Runtime, Setup + Execution, etc.)
- **EVITAR**: Eliminación de métodos, pérdida de funcionalidad, APIs incompletas

## 🎮 Contexto del Proyecto
Videojuego 2D bullet hell desarrollado con Pygame-ce. El jugador se mueve libremente con cámara fluida, dispara hacia el cursor del ratón y enfrenta oleadas de enemigos con IA avanzada. Desarrollo en **Windows 11 + VS Code** con asistencia 100% IA.

## 🛠️ Stack Tecnológico
- **Python 3.11+** con type hints obligatorios
- **Pygame-ce** (NO pygame estándar)
- **Poetry** para dependencias (NO pip/requirements.txt)
- **Ruff** para linting/formateo
- **Pre-commit** para hooks de calidad
- **PyTest** con cobertura mínima 80%
- **GitHub CLI** para gestión avanzada del repositorio

## 📋 Convenciones de Código

### Idioma y Nomenclatura
- **Idioma**: Español para código, comentarios y documentación
- **Variables/funciones**: `generacion_enemigos`, `jugador`, `velocidad_movimiento`
- **Clases**: PascalCase español (`GestorEnemigos`, `PersonajeJugador`)
- **Constantes**: SNAKE_CASE español (`VELOCIDAD_MAXIMA`, `TIEMPO_RESPAWN`)

### Documentación Obligatoria
- **Docstrings completas** en español para todas las funciones públicas
- **Type hints obligatorios** en parámetros y retornos
- **Comentarios contextuales** antes de lógica compleja
- **Args, Returns, Raises** documentados
- **Actualización automática** de `docs/FUNCIONES_DOCUMENTADAS.md`

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios
```
src/
├── core/          # Motor del juego, scene manager
├── entities/      # Jugador, enemigos, proyectiles
├── scenes/        # Menús, gameplay, transiciones
├── ui/            # HUD, menús, componentes UI
├── utils/         # Assets, configuración, helpers
└── main.py        # Punto de entrada único
```

### Separación de Responsabilidades
- **Un archivo = una responsabilidad específica**
- **Modularización extrema** para mantener límite de 150 líneas
- **APIs claras** entre módulos
- **Dependencias mínimas** entre componentes
- **PRESERVACIÓN TOTAL**: Nunca eliminar métodos útiles durante refactorización
- **DIVISIÓN INTELIGENTE**: Separar en 2 módulos operativos manteniendo funcionalidad completa
- **EQUIVALENCIA FUNCIONAL**: Los módulos divididos deben ofrecer 100% de la funcionalidad original

## ⚙️ Configuración Modular
- **Todas las configuraciones** en `config/` como archivos JSON
- **NO valores hardcoded** en Python
- **ConfigManager** centralizado con validación de esquemas
- **Separación por áreas**: audio, enemies, display, gameplay, ui, input

## 🧪 Calidad y Testing

### Métricas Obligatorias
- **0 errores Ruff** siempre
- **0 advertencias MyPy** siempre
- **100% cobertura tests** mínimo
- **Complejidad ciclomática < 10**
- **100% documentación** en funciones públicas

### Comandos de Validación
- `poetry run ruff check src/ tests/`
- `poetry run ruff format src/ tests/`
- `poetry run mypy src/`
- `poetry run pytest --cov=src tests/`
- `poetry run pre-commit run --all-files`

## 🎯 Sistemas del Juego

### Enemigos
- **Tipos**: zombie masculino/femenino con variantes (normal, raro, élite, legendario)
- **IA**: estados de patrulla, persecución y ataque
- **Detección**: 300px como distancia estándar
- **Comportamiento**: definido en `config/enemies.json`

### Assets y Recursos
- **Estructura obligatoria**: `assets/characters/used/`, `assets/ui/`, `assets/sounds/`
- **Cache centralizado** de imágenes y sonidos
- **Rutas absolutas** siempre
- **Gestión de memoria** eficiente

### HUD y Menús
- **HUD permanente**: vida, mejoras, puntos, cronómetro
- **Menús**: bienvenida, principal, pausa, opciones, mejoras, inventario, guardado
- **Compatibilidad**: todas las resoluciones soportadas
- **Separación**: lógica independiente de representación visual

## 🛠️ Herramientas y Ejecución

### Comandos Principales con Poetry
- **Ejecución del juego**: `poetry run python src/main.py`
- **Instalación dependencias**: `poetry install`
- **Agregar paquetes**: `poetry add package_name`
- **Limpieza de caché**: `poetry cache clear pypi --all`

### Configuración Pygame-ce
- **USAR SOLO**: `poetry add pygame-ce` (NO pygame estándar)
- **Si hay conflictos**: `poetry remove pygame` seguido de `poetry add pygame-ce`
- **Verificar instalación**: confirmar compatibilidad de métodos pygame-ce

### GitHub CLI para Gestión Avanzada (PRIORITARIO)
- **Documentación oficial**: https://cli.github.com/manual/
- **Matriz de decisión completa**: `docs/MATRIZ_DECISIÓN_GH_VS_GIT.md`
- **Regla principal**: SIEMPRE preferir `gh` cuando esté disponible

#### Comandos Esenciales GitHub CLI
- **Repositorio**: `gh repo view`, `gh repo create`, `gh repo fork`, `gh repo clone`
- **Issues**: `gh issue list`, `gh issue create`, `gh issue view --web`
- **Pull Requests**: `gh pr create --fill`, `gh pr list`, `gh pr merge`
- **Releases**: `gh release create`, `gh release upload`, `gh release list`
- **Navegación**: `gh browse` (abrir en navegador), `gh status`
- **Búsqueda**: `gh search repos`, `gh search code`, `gh search issues`
- **Actions**: `gh workflow run`, `gh run list`, `gh workflow list`

#### Git Tradicional (SOLO Local)
- **Staging/Commits**: `git add`, `git commit`, `git commit --amend`
- **Branching local**: `git branch`, `git checkout`, `git switch`
- **Estado local**: `git status`, `git log`, `git diff`

### Scripts Personalizados
- `scripts/run_tests.py` - Testing interactivo
- `scripts/cleanup_project.py` - Limpieza automática
- `scripts/commit_profesional.ps1` - Commits profesionales automatizados
- `tools/package_improved.py` - Build ejecutable

## 🔄 Reglas de Trabajo

### Comandos Terminal PowerShell
- **NO usar `&&`** para encadenar comandos (usar `;` si necesario)
- **Comandos separados** por línea para mayor claridad
- **PowerShell** como shell predeterminado en Windows
- **Filtrado de texto**: `Select-String` en lugar de `grep`
- **Búsqueda en archivos**: `Get-Content archivo.txt | Select-String "patrón"`

### Commits y Push Profesionales
- **Template obligatorio**: `.gitmessage` con Conventional Commits en español
- **Tipos**: feat, fix, docs, refactor, test, chore, perf, style
- **Ámbitos**: core, entities, scenes, ui, utils, config, assets, docs
- **Formato**: `tipo(ámbito): descripción` (máx 50 caracteres)
- **Script automatizado**: `scripts/commit_profesional.ps1` para workflow completo
- **Pre-commit hooks**: validación automática de calidad antes de commit
- **Validación obligatoria**: SIEMPRE verificar éxito del commit con `git status` antes de continuar
- **Staging completo**: Agregar TODOS los cambios relacionados con `git add .` antes del commit
- **Verificación post-commit**: Confirmar que no quedan cambios unstaged después del commit
- **Documentación**: `docs/COMMITS_PROFESIONALES.md` con guía completa

### Gestión de Archivos y Repositorio
- **GitHub CLI prioritario**: usar `gh` para todas las operaciones de repositorio
- **Matriz de decisión**: `docs/MATRIZ_DECISIÓN_GH_VS_GIT.md` (consultar SIEMPRE)
- **Información del repositorio**: `gh repo view` (preferir sobre git status)
- **Gestión de issues/PRs**: `gh issue create`, `gh pr create --fill`
- **Releases y distribución**: `gh release create`, `gh release upload`
- **Git tradicional**: solo para `git add`, `git commit`, operaciones locales
- **Commits atómicos** por cada refactorización o cambio significativo
- **Evitar** movimientos directos en explorador

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
