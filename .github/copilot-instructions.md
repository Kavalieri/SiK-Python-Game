# Instruc###  **VERIFICAR ANTES DE CONFIRMAR**: No dar por buenas soluciones sin leer la salida de consola o logs. Si no se detecta salida, se priorizará incluir líneas de control para depurar el problema.

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

###  **COMMITS Y VERSIONADO**
```powershell
# Método principal para commits cotidianos
.\dev-tools\scripts\robust_commit.ps1 "mensaje"

# Con push automático
.\dev-tools\scripts\robust_commit.ps1 "mensaje" -Push

```

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

###  **FLUJO AUTÓNOMO**
- **Continuar iterando** hasta puntos de prueba que requieran resolución del usuario a menos que esperemos una respuesta por la terminal.
- **Resolver errores** de forma autónoma sin consultar constantemente.
- **Commits preventivos**: Realizar commits antes de cada cambio, borrado o refactorización importante.
- **Testing**: Crear y ejecutar scripts de testeo para validar la funcionalidad antes de dar por finalizada una tarea.
- **Documentar cambios** significativos inmediatamente.
- **Mantener actualizadas** las reglas constantemente.
- **Organización de archivos**: Scripts temporales/pruebas en `dev-tools/testing/temp/` NUNCA en raíz.

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
