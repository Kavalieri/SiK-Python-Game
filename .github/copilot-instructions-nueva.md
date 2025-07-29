# Instrucciones para GitHub Copilot - SiK Python Game

## 📋 Automantenimiento y Documentación Crítica

### Responsabilidades Primarias
- **Mantener actualizado** este archivo con cualquier cambio significativo del proyecto
- **Actualizar automáticamente** `docs/FUNCIONES_DOCUMENTADAS.md` con todas las funciones nuevas o modificadas
- **Actualizar automáticamente** `docs/refactorizacion_progreso.md` (será renombrado tras completar refactorización)
- **Documentar decisiones** importantes en archivos correspondientes
- **Reflejar cambios** de arquitectura, reglas o convenciones inmediatamente

### Archivos de Seguimiento Obligatorio
- `docs/FUNCIONES_DOCUMENTADAS.md` - Catálogo completo de funciones por módulo
- `docs/refactorizacion_progreso.md` - Estado actual de refactorización del proyecto
- `CHANGELOG.md` - Registro de cambios significativos
- Este archivo - Base de reglas del proyecto

## 📋 Regla Crítica: Límite de Líneas
**NINGÚN archivo puede superar 150 líneas**. Dividir inmediatamente si se excede.

## 🎮 Contexto del Proyecto
Videojuego 2D bullet hell desarrollado con Pygame-ce. El jugador se mueve libremente con cámara fluida, dispara hacia el cursor del ratón y enfrenta oleadas de enemigos con IA avanzada. Desarrollo en **Windows 11 + VS Code** con asistencia 100% IA.

## 🛠️ Stack Tecnológico
- **Python 3.11+** con type hints obligatorios
- **Pygame-ce** (NO pygame estándar)
- **Poetry** para dependencias (NO pip/requirements.txt)
- **Ruff** para linting/formateo
- **Pre-commit** para hooks de calidad
- **PyTest** con cobertura mínima 80%

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

## ⚙️ Configuración Modular
- **Todas las configuraciones** en `config/` como archivos JSON
- **NO valores hardcoded** en Python
- **ConfigManager** centralizado con validación de esquemas
- **Separación por áreas**: audio, enemies, display, gameplay, ui, input
- **Documentar cambios** en `CHANGELOG.md`

## 🧪 Calidad y Testing

### Métricas Obligatorias
- **0 errores Ruff** siempre
- **0 advertencias MyPy** siempre
- **80% cobertura tests** mínimo
- **Complejidad ciclomática < 10**
- **100% documentación** en funciones públicas

### Comandos de Validación
- `poetry run ruff check src/ tests/`
- `poetry run ruff format src/ tests/`
- `poetry run mypy src/`
- `poetry run pytest --cov=src tests/`
- `poetry run pre-commit run --all-files`

## 🎯 Refactorización Prioritaria

### Archivos Críticos (>300 líneas)
1. `src/utils/asset_manager.py` (464 líneas) - **URGENTE**
2. `src/ui/hud.py` (397 líneas) - **URGENTE**
3. `src/ui/menu_callbacks.py` (336 líneas) - **URGENTE**
4. `src/scenes/gameplay.py` (350 líneas) - **ALTO**
5. `src/entities/entity.py` (332 líneas) - **ALTO**

### Proceso de División Seguro
1. **Backup** del archivo original
2. **Tests** antes de cambios
3. **Dividir** por responsabilidades claras
4. **Validar** funcionalidad completa
5. **Commit** atómico por archivo

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

### Ejecución del Proyecto
- **Comando principal**: `python -m src.main`
- **NO configurar** PYTHONPATH manualmente
- **Limpieza de caché**: `pip cache purge` antes de cambios críticos

### Pygame-ce Específico
- **Instalación**: `poetry add pygame-ce`
- **Eliminar pygame estándar**: `pip uninstall pygame -y`
- **Verificar compatibilidad** de métodos específicos

### Scripts Personalizados
- `scripts/run_tests.py` - Testing interactivo
- `scripts/cleanup_project.py` - Limpieza automática
- `tools/package_improved.py` - Build ejecutable

## 🔄 Reglas de Trabajo

### Comandos Terminal
- **NO usar `&&`** para encadenar comandos
- **Comandos separados** por línea
- **PowerShell** como shell predeterminado

### Gestión de Archivos
- **Git obligatorio**: `git mv origen destino` para mover archivos
- **Evitar** movimientos directos en explorador
- **Commits atómicos** por cada refactorización

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
- **Mantener actualizadas** todas las reglas constantemente
- **Automatización máxima** de procesos repetitivos
- **Documentación automática** de funciones y cambios

---

**Base fundamental del proyecto. Mantener actualizado siempre.**
