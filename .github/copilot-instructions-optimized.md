# Instrucciones para GitHub Copilot - SiK Python Game

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

### Regla Crítica: Máximo 150 líneas por archivo
**NINGÚN archivo puede superar 150 líneas**. Dividir inmediatamente si se excede.

### Idioma y Nomenclatura
- **Idioma**: Español para código, comentarios y documentación
- **Variables/funciones**: `generacion_enemigos`, `jugador`, `velocidad_movimiento`
- **Clases**: PascalCase español (`GestorEnemigos`, `PersonajeJugador`)
- **Constantes**: SNAKE_CASE español (`VELOCIDAD_MAXIMA`, `TIEMPO_RESPAWN`)

### Documentación Obligatoria
```python
def procesar_movimiento_jugador(
    posicion_actual: tuple[int, int],
    direccion: str,
    velocidad: int = 5
) -> tuple[int, int]:
    """
    Procesa el movimiento del jugador en la pantalla.

    Calcula nueva posición aplicando restricciones de límites.

    Args:
        posicion_actual: Coordenadas (x, y) actuales
        direccion: "izquierda", "derecha", "arriba", "abajo"
        velocidad: Píxeles por frame

    Returns:
        Nueva posición (x, y)

    Example:
        >>> nueva_pos = procesar_movimiento_jugador((100, 200), "derecha", 5)
        >>> print(nueva_pos)  # (105, 200)
    """
```

## ⚙️ Configuración Modular
- **Todas las configuraciones** en `config/` (JSON por área: audio, enemies, display, etc.)
- **NO valores hardcoded** en Python
- **ConfigManager** centralizado con validación de esquemas
- **Documentar cambios** en `CHANGELOG.md`

## 🏗️ Arquitectura
```
src/
├── core/          # Motor del juego, scene manager
├── entities/      # Jugador, enemigos, proyectiles
├── scenes/        # Menús, gameplay, transiciones
├── ui/            # HUD, menús, componentes UI
├── utils/         # Assets, configuración, helpers
└── main.py        # Punto de entrada único
```

## 🎯 Sistemas del Juego

### Personajes
```python
class PersonajeJugador:
    """Personaje controlado por el jugador."""

    def __init__(self, posicion_inicial: tuple[int, int]):
        self.posicion = posicion_inicial
        self.vida_actual = 100
        self.velocidad = 5
        self.estado_actual = "idle"

    def mover(self, direccion: str) -> None:
        """Mueve el personaje."""

    def disparar(self) -> Optional['Proyectil']:
        """Crea proyectil desde posición actual."""
```

### Enemigos
- **Tipos**: zombie masculino/femenino (normal, raro, élite, legendario)
- **IA**: patrulla, persecución, ataque
- **Detección**: 300px estándar

### Assets
```python
class GestorAssets:
    """Cache centralizado de recursos."""

    def __init__(self):
        self._cache_imagenes: dict[str, pygame.Surface] = {}
        self._cache_sonidos: dict[str, pygame.mixer.Sound] = {}
```

**Estructura obligatoria:**
```
assets/
├── characters/used/    # Activos
├── characters/unused/  # Desarrollo
├── ui/                # Interfaz
├── sounds/            # Audio
├── fonts/             # Tipografías
├── objects/           # Proyectiles, powerups
└── tiles/             # Escenarios
```

## 🧪 Calidad y Testing

### Métricas Obligatorias
- **0 errores Ruff**
- **0 advertencias MyPy**
- **80% cobertura tests**
- **Complejidad < 10**
- **100% documentación pública**

### Comandos Esenciales
```powershell
# Ejecución
python -m src.main

# Calidad completa
poetry run ruff check src/ tests/
poetry run ruff format src/ tests/
poetry run mypy src/
poetry run pytest --cov=src tests/

# Pre-commit
poetry run pre-commit run --all-files
```

## 🎯 Refactorización Crítica

### Archivos Prioritarios (>300 líneas)
1. `src/utils/asset_manager.py` (464 líneas) - **CRÍTICO**
2. `src/ui/hud.py` (397 líneas) - **CRÍTICO**
3. `src/ui/menu_callbacks.py` (336 líneas) - **CRÍTICO**
4. `src/scenes/gameplay.py` (350 líneas) - **ALTO**
5. `src/entities/entity.py` (332 líneas) - **ALTO**

### Proceso Seguro
1. **Backup** del archivo original
2. **Tests** antes de cambios
3. **Dividir** por responsabilidades
4. **Validar** funcionalidad
5. **Commit** atómico

## 🖥️ HUD y Menús
- **HUD**: vida, mejoras, puntos, cronómetro (siempre visible)
- **Menús**: bienvenida, principal, pausa, opciones, mejoras, inventario, guardado
- **Compatibilidad**: todas las resoluciones soportadas
- **Separación**: lógica independiente de representación visual

## 🤖 Optimización para IA

### Patrones para Copilot
- **Nombres autodescriptivos** en español
- **Funciones pequeñas** (máx 30 líneas)
- **Comentarios contextuales** antes de lógica compleja
- **Type hints completos** para mejor inferencia
- **Ejemplos en docstrings**

### Documentación Automática
- **Archivo**: `docs/FUNCIONES_DOCUMENTADAS.md`
- **Actualización**: con cada función nueva/modificada
- **Organización**: por módulos y responsabilidad

## 🛠️ Herramientas y Flujo

### Ejecución Estándar
```powershell
# Sin configurar PYTHONPATH
python -m src.main

# Limpieza de caché antes de cambios críticos
pip cache purge
```

### Pygame-ce Específico
- **Instalar**: `poetry add pygame-ce`
- **Desinstalar pygame**: `pip uninstall pygame -y`
- **Verificar**: compatibilidad de métodos con pygame-ce

### Scripts Personalizados
- `scripts/run_tests.py` - Tests interactivos
- `scripts/cleanup_project.py` - Limpieza automática
- `tools/package_improved.py` - Build ejecutable

## 🔄 Reglas de Trabajo

### Comandos Terminal
- **NO usar `&&`** para encadenar
- **Comandos separados** por línea
- **PowerShell** como shell predeterminado

### Movimientos de Archivos
- **SIEMPRE usar Git**: `git mv origen destino`
- **Evitar** mover archivos directamente en explorador

### Flujo Autónomo
- **Continuar automáticamente** hasta punto de prueba
- **Resolver errores** de forma autónoma
- **Documentar cambios** significativos

### Estrategia para Problemas
- **Comentar líneas** problemáticas temporalmente
- **Probar sin conflictos** para identificar impacto
- **Documentar soluciones** implementadas

## 🤖 Proyecto 100% IA

### Preservación Crítica
- **NUNCA eliminar** `.github/` ni este archivo
- **Mantener actualizadas** todas las reglas
- **Reflejar cambios** significativos inmediatamente

### Automatización
- **Procesos repetitivos** → scripts automáticos
- **Documentación** → generación automática
- **Validaciones** → hooks pre-commit
- **Organización** → scripts de limpieza

---

**Estas instrucciones son la base fundamental del proyecto. Mantenlas actualizadas y nunca las elimines.**
