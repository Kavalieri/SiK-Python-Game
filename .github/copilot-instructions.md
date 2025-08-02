# Instruc###  **VERIFICAR ANTES DE CONFIRMAR**: No dar por buenas soluciones sin leer la salida de consola o logs. Si no se detecta salida, se priorizará incluir### **GESTIÓN DE DOCUMENTACIÓN**
- **Referencia única**: `docs/README.md` como índice centralizado
- **Registro histórico**: `docs/registro/` con timestamps por bloque de cambios
- **Archivo organizacional**: `ARCHIVE/2025/` por categorías (dev-tools, docs, etc.)
- **SIEMPRE archivar elementos obsoletos**: Preservar versiones antiguas en ARCHIVE/
- **Mantener docs/ limpio**: Solo documentos activos esenciales + registroas de control para depurar el problema.

###  **ESPERAR RESPUESTAS DE COMANDOS**: NUNCA tomar decisiones o ejecutar comandos adicionales sin esperar y leer completamente la respuesta del comando anterior. Cada comando debe completarse y su salida debe ser analizada antes de proceder.iones GitHub Copilot - SiK Python Game

##  **COMPORTAMIENTO OBLIGATORIO**

###  **IDIOMA Y COMUNICACIÓN**
- **SIEMPRE EN ESPAÑOL**: Respuestas, razonamiento, comentarios, documentación
- **SER CRÍTICO Y ESCÉPTICO**: Cuestionar implementaciones, buscar problemas potenciales
- **NO SER COMPLACIENTE**: Señalar errores, mejoras posibles, code smells
- **ANALIZAR ANTES DE IMPLEMENTAR**: Revisar impacto, dependencias, alternativas
- **VERIFICAR ANTES DE CONFIRMAR**: No dar por buenas soluciones sin leer la salida de consola o logs. Si no se detecta salida, se priorizará incluir líneas de control para depurar el problema.

###  **PROHIBICIONES ABSOLUTAS**
- **NUNCA HARDCODEAR**: Usar configuración, constantes, variables de entorno
- **NUNCA eliminar** `.github/` ni archivos de instrucciones
- **NUNCA usar emojis/Unicode** en scripts PowerShell (solo ASCII)
- **NUNCA usar `&&`** en PowerShell (usar `;`)
- **NUNCA crear archivos temporales en raíz**: Usar `dev-tools/testing/temp/` o directorios específicos

## 🚨 **PREVENCIÓN ARCHIVOS FANTASMA**

### **REGLAS ANTI-FANTASMA OBLIGATORIAS**
- **NUNCA crear archivos temporales** con nombres como: test_*, demo_*, setup_*, example_*
- **NUNCA mencionar rutas** de archivos que no existen realmente sin verificar
- **ANTES de sugerir crear un archivo**, verificar que es necesario permanentemente
- **USAR carpetas temp/** para archivos temporales, NUNCA raíz del proyecto
- **SOLO crear archivos** con contenido real y funcional, NUNCA vacíos

### **UBICACIONES PROHIBIDAS para archivos temporales**
- ❌ Raíz del proyecto (archivos sueltos)
- ❌ Archivos .env.example vacíos
- ❌ Archivos de prueba en ubicaciones principales
- ❌ Documentación temporal en raíz

### **SI NECESITAS ARCHIVO TEMPORAL**
1. **Ubicación**: `tmp/` para archivos temporales generales, `test/` para pruebas automatizadas con pytest
2. **Contenido**: SIEMPRE con contenido real, nunca vacío
3. **Documentar**: Por qué es necesario y cuándo eliminar
4. **Limpiar**: Mover a ARCHIVE/ cuando termine su función

## **GESTIÓN DEL REPOSITORIO**

### **DIRECTORIOS LOCALES (NO GIT)**
- **ARCHIVE/**: Archivos obsoletos organizados por año y categoría
- **save/**: Datos de guardado generados por el juego (NO heredar del proyecto)
- **data/**: Base de datos y datos del juego (generados automáticamente)
- **tmp/**: Archivos temporales de desarrollo
- **test/**: Tests automatizados para pytest
- **.vscode/**: Configuración personal de VS Code

### **DIRECTORIOS SINCRONIZADOS (CON GIT)**
- **src/**: Código fuente del juego
- **assets/**: Recursos del juego (imágenes, sonidos, etc.)
- **config/**: Configuración del juego
- **docs/**: Documentación activa y registro histórico
- **dev-tools/**: Herramientas de desarrollo actuales y necesarias

### **GESTIÓN DE ARCHIVOS OBSOLETOS**
- **Archivar inmediatamente**: Elementos no utilizados van a ARCHIVE/
- **Organización ARCHIVE/**: Por año y categoría (ARCHIVE/2025/dev-tools/, ARCHIVE/2025/docs/)
- **docs/ limpio**: Solo documentación activa esencial + docs/registro/ para histórico
- **dev-tools/ limpio**: Solo herramientas necesarias para desarrollo actual

##  **REGLAS FUNDAMENTALES**

###  **LÍMITES Y ESTRUCTURA**
- **Límite de archivo**: 250 líneas máximo - dividir si se excede
- **Funciones pequeñas**: máximo 30 líneas para IA optimal
- **Complejidad < 10** por función
- **0 errores Ruff** + **0 advertencias MyPy** siempre

###  **ANTI-HARDCODING**
- **Configuración externa**: JSON, YAML, SQLite, variables de entorno
- **Constantes nombradas**: `VELOCIDAD_MAXIMA = 100` no `if speed > 100:`
- **Rutas configurables**: No rutas absolutas hardcodeadas
- **Valores mágicos**: Siempre usar constantes con nombres descriptivos

###  **GESTIÓN DE RUTAS PARA EMPAQUETADO**
- **SIEMPRE rutas relativas**: Compatibilidad con empaquetado .exe
- **✅ Usar `pathlib.Path` y `__file__`**: Referencias dinámicas robustas
- **Ejecutar desde raíz**: `poetry run python src\main.py` (simula entorno empaquetado)
- **❌ Evitar rutas absolutas**: No funcionan al distribuir
- **Patrón recomendado**: `PROJECT_ROOT = Path(__file__).parent.parent`

###  **IMPORTACIONES PARA EMPAQUETADO**
- **✅ IMPORTACIONES ABSOLUTAS**: `from utils.config_manager import ConfigManager`
- **❌ IMPORTACIONES RELATIVAS**: `from ..utils.config_manager import ConfigManager`
- **Dentro del mismo paquete**: `from .game_engine_core import GameEngineCore` (OK)
- **Entre paquetes diferentes**: `from entities.player import Player` (desde src como raíz)
- **Razón**: Las importaciones relativas fallan al ejecutar desde raíz en empaquetado

###  **CONVENCIONES OBLIGATORIAS**
- **Variables**: `generacion_enemigos`, `velocidad_movimiento` (snake_case español)
- **Clases**: `GestorEnemigos`, `PersonajeJugador` (PascalCase español)
- **Type hints**: Obligatorios en parámetros y retornos
- **Docstrings**: Español completo con Args/Returns/Raises
- **Indentación**: SIEMPRE tabuladores, NUNCA espacios
- **Ejecutar scripts con Poetry**: `poetry run python <script.py>` para scripts y el juego.
- **Trabajar siempre desde el directorio raíz del proyecto**.

##  **FLUJOS AUTOMATIZADOS OBLIGATORIOS**

###  **SISTEMA DE ACTIVADORES AUTOMATICOS**
```powershell
# NUEVO: Sistema de activadores inteligentes que evalua contexto automaticamente

# Comando principal (recomendado)
.\dev-tools\scripts\sik.ps1                    # Auto-evalua y ejecuta workflow
.\dev-tools\scripts\sik.ps1 -Status           # Ver estado del repositorio
.\dev-tools\scripts\sik.ps1 -Mensaje "desc"   # Con descripcion de cambios
.\dev-tools\scripts\sik.ps1 -Forzar          # Sin confirmacion

# Sistema de deteccion automatica de cambios:
# - HOTFIX: "hotfix|urgente|critico|security" → nueva rama hotfix/ → directo a main
# - BUGFIX: "fix|bug|error|corrige" → nueva rama bugfix/ → PR normal  
# - FEATURE: "feature|nueva|implementa" → nueva rama feature/ → PR normal
# - DOCS: solo archivos docs/ → commit directo (configurable)
# - CONFIG: solo archivos config/ → nueva rama config/
# - DEV-TOOLS: solo dev-tools/ → commit directo (configurable)

# Evaluacion de contexto:
# - Si estas en main + cambios → Crea nueva rama automaticamente
# - Si estas en rama + cambios → Completa trabajo en rama actual  
# - Si estas en rama + sin cambios → Merge y release automatico
```

###  **WORKFLOW MANUAL (Control total)**
```powershell
# Para casos especiales que requieren control manual
.\dev-tools\scripts\workflow_automation.ps1 -Accion nueva-rama -RamaNombre "feature/nombre" -Mensaje "descripción"
.\dev-tools\scripts\workflow_automation.ps1 -Accion completar -Mensaje "cambios completados"
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release -TipoVersion minor -Mensaje "descripción final"
.\dev-tools\scripts\workflow_automation.ps1 -Accion status

# Desarrollo rapido simplificado (obsoleto - usar sik.ps1)
.\dev-tools\scripts\dev_helper.ps1 start|save|finish
```

###  **CHANGELOG AUTOMÁTICO**
- **Generación automática**: Changelog actualizado en cada release
- **Archivado**: Versiones en `docs/changelogs/`
- **Integración GitHub**: Releases automáticos con tags
- **NUNCA editar CHANGELOG.md manualmente**: Sistema automatizado se encarga

###  **CONFIGURACIÓN TERMINAL**
- **NO abrir nuevas consolas innecesariamente**: Usar la terminal activa si es posible.
- **Solo caracteres ASCII** en scripts PowerShell
- **GitHub CLI prioritario**: `gh` > git tradicional

##  **ARQUITECTURA Y PROYECTO**

###  **ESTRUCTURA MODULAR**
```
src/core/		# Motor, scene manager
src/entities/	# Jugador, enemigos, proyectiles
src/scenes/		# Menús, gameplay, transiciones
src/ui/			# HUD, componentes UI
src/dev-tools/	# Assets, config, helpers
src/assets/		#
```

###  **CONTEXTO DEL PROYECTO**
**Videojuego 2D bullet hell** - Pygame-ce + Python 3.11+ + Poetry
**Desarrollo 100% IA** en Windows 11 + VS Code + GitHub CLI
**Estado**:  ✅ Refactorización completada (100% archivos compliant)
**Prioridad**:  **DESARROLLO DE CARACTERÍSTICAS DEL JUEGO**

###  **STACK TÉCNICO**
- **Python 3.11+** + **Pygame-ce** (NO pygame estándar) + **Poetry**
- **SQLite** para datos complejos + **JSON** para configuración simple
- **GitHub CLI**: `gh repo view`, `gh issue create`, `gh pr create`
- **Git local**: Solo `git add`, `git commit`, operaciones locales
- **Ejecución con Poetry**: Usar `poetry run python <script.py>` para ejecutar scripts y el juego.

##  **OPTIMIZACIÓN PARA IA**

###  **CÓDIGO ÓPTIMO PARA COPILOT**
- **Nombres autodescriptivos** en español: `calcular_daño_proyectil()`
- **Type hints completos**: `def mover_jugador(x: float, y: float) -> bool:`
- **Comentarios contextuales** antes de lógica compleja
- **Consistencia** en nomenclatura y estructura
- **Documentación automática** de funciones y cambios

###  **FLUJO AUTÓNOMO CON ACTIVADORES**
- **Evaluar contexto SIEMPRE**: Antes de cada cambio, usar `.\dev-tools\scripts\sik.ps1 -Status`
- **Auto-deteccion de tipo**: El sistema identifica automaticamente si es hotfix/bugfix/feature/docs
- **Ramas automaticas**: Crea ramas segun el tipo detectado (feature/, bugfix/, hotfix/, etc.)
- **Commits inteligentes**: Formato convencional automatico segun tipo de cambio
- **Merge automatico**: Cuando no hay cambios pendientes, ejecuta merge + release
- **Resolver errores** de forma autónoma sin consultar constantemente
- **Commits preventivos**: Usar `.\dev-tools\scripts\sik.ps1` antes de cada cambio mayor
- **Testing**: Validar funcionalidad antes de dar por finalizada una tarea
- **Documentar cambios** significativos inmediatamente en `docs/registro/`
- **Organización de archivos**: Scripts temporales/pruebas en `tmp/` NUNCA en raíz

###  **GESTIÓN DE DOCUMENTACIÓN**
- **Referencia única**: `docs/README.md` como índice centralizado
- **Archivo histórico**: `docs/ARCHIVO/2025/` por categorías.
- **SIEMPRE archivar elementos obsoletos**: Preservar versiones antiguas.
- **Mantener docs/ limpio**: Solo documentos activos esenciales.

##  **PRIORIDADES ACTUALES**

### 1 **DESARROLLO DE CARACTERÍSTICAS** (Principal)
- **Infraestructura técnica**:  ✅ COMPLETADA
- **Sistema SQLite**:  ✅ Implementado y funcional
- **Compliance de código**: ✅ 100% (todos los archivos <250 líneas)
- **Enfoque**: Nuevas mecánicas, gameplay, contenido del juego

### 2 **CALIDAD CONTINUA**
- **División de archivos** si exceden 250 líneas
- **Preservar APIs** al refactorizar (100% compatibilidad)
- **Commits atómicos** por cada cambio significativo

---

**Base fundamental del proyecto. Desarrollo ágil prioritario.**
