```````instructions
`````instructions
# Instrucciones para GitHub Copilot - SiK Python Game

## 🎮 Contexto del Proyecto
Este es un videojuego 2D de disparos desarrollado con Pygame-ce. El objetivo es destruir enemigos que caen desde la parte superior de la pantalla.

## 🎮 Tipo de Juego

- El juego debe ser de tipo **bullet hell 2D**.
- El jugador se mueve libremente con cámara fluida centrada en él.
- El disparo se dirige hacia el cursor del ratón.
- Implementar IA de enemigos, generación de powerups y mejoras entre rondas.
- El desarrollo se realiza en entorno **Windows 11 + Visual Studio Code**.

## 🛠️ Stack Tecnológico 2025
- **Python 3.11+** con type hints obligatorios
- **Pygame-ce** para el motor del juego
- **Poetry** para gestión de dependencias
- **Ruff** para linting y formateo
- **Pre-commit** para hooks de calidad
- **PyTest** para testing con cobertura mínima 80%

## 📋 Convenciones de Código

### Idioma y Nomenclatura
- **Idioma principal**: Español para código, comentarios y documentación
- **Variables y funciones**: En español (`generacion_enemigos`, `jugador`, `velocidad_movimiento`)
- **Clases**: PascalCase en español (`GestorEnemigos`, `PersonajeJugador`)
- **Constantes**: SNAKE_CASE en español (`VELOCIDAD_MAXIMA`, `TIEMPO_RESPAWN`)

### Estructura de Archivos
- **Máximo 150 líneas** por archivo
- **Arquitectura modular** con separación clara de responsabilidades
- **src/** como directorio principal de código
- **main.py** como punto de entrada

### Documentación
```python
def procesar_movimiento_jugador(
    posicion_actual: tuple[int, int],
    direccion: str,
    velocidad: int = 5
) -> tuple[int, int]:
    """
    Procesa el movimiento del jugador en la pantalla.

    Calcula la nueva posición basada en la dirección y velocidad,
    aplicando las restricciones de los límites de pantalla.

    Args:
        posicion_actual: Coordenadas (x, y) actuales del jugador
        direccion: Dirección de movimiento ("izquierda", "derecha", "arriba", "abajo")
        velocidad: Píxeles por frame de movimiento

    Returns:
        Nueva posición (x, y) después del movimiento

    Example:
        >>> nueva_pos = procesar_movimiento_jugador((100, 200), "derecha", 5)
        >>> print(nueva_pos)  # (105, 200)
    """
```

## ⚙️ Configuración Modular

- Todas las configuraciones del juego deben residir en `config/`.
- Dividir por áreas: audio, input, enemigos, personajes, display, gameplay, etc.
- Evitar valores hardcoded en los scripts Python.
- Actualizar los JSON conforme evolucionen las mecánicas.
- `pyproject.toml` como configuración principal del proyecto (Poetry).
- `.pre-commit-config.yaml` para configuración de calidad de código.
- Usar `ConfigManager` centralizado para acceso a configuraciones.
- Validación de esquemas JSON en carga de configuración.
- Configuraciones de desarrollo vs. producción claramente separadas.
- Documentar cambios de configuración en `CHANGELOG.md`.

## 🏗️ Estructura Técnica

- **Máximo 150 líneas** por archivo (crítico para mantenibilidad).
- Separar lógicamente `core`, `entidades`, `escenas`, `UI` y utilidades.
- Respetar nombres y propósitos de carpetas establecidas.
- Evitar archivos con más de una responsabilidad.
- `main.py` debe actuar como punto de entrada al juego.
- Usar Poetry para gestión de dependencias (NO pip/requirements.txt).
- Pre-commit hooks deben pasar antes de cualquier commit.
- Type hints obligatorios en funciones públicas.
- Documentación obligatoria en cada función/clase.
- Logging detallado para debug y trazabilidad.
- Rutas absolutas para assets y configuración.
- Modularización extrema: dividir archivos grandes en submódulos.

## 🎯 Sistemas Específicos del Juego

### Sistema de Personajes
```python
class PersonajeJugador:
    """Representa al personaje controlado por el jugador."""

    def __init__(self, posicion_inicial: tuple[int, int]):
        self.posicion = posicion_inicial
        self.vida_actual = 100
        self.vida_maxima = 100
        self.velocidad = 5
        self.animaciones = {}
        self.estado_actual = "idle"

    def mover(self, direccion: str) -> None:
        """Mueve el personaje en la dirección especificada."""

    def disparar(self) -> Optional['Proyectil']:
        """Crea un proyectil desde la posición del jugador."""

    def recibir_dano(self, cantidad: int) -> bool:
        """Aplica daño al jugador. Retorna True si sigue vivo."""
```

### Sistema de Enemigos
```python
class GestorEnemigos:
    """Gestiona la generación y comportamiento de enemigos."""

    def __init__(self):
        self.enemigos_activos: list[Enemigo] = []
        self.tiempo_ultimo_spawn = 0
        self.dificultad_actual = 1

    def generar_oleada(self, cantidad: int) -> None:
        """Genera una oleada de enemigos."""

    def actualizar(self, delta_time: float) -> None:
        """Actualiza todos los enemigos activos."""
```

### Sistema de Assets
```python
class GestorAssets:
    """Gestiona la carga y cache de recursos del juego."""

    def __init__(self):
        self._cache_imagenes: dict[str, pygame.Surface] = {}
        self._cache_sonidos: dict[str, pygame.mixer.Sound] = {}

    def cargar_imagen(self, ruta: str) -> pygame.Surface:
        """Carga una imagen con cache automático."""

    def cargar_sonido(self, ruta: str) -> pygame.mixer.Sound:
        """Carga un sonido con cache automático."""
```

## 🎨 Sistema de Assets

### Estructura Obligatoria
```
assets/
├── characters/used/     # Personajes activos en el juego
├── characters/unused/   # Personajes en desarrollo
├── ui/                  # Elementos de interfaz (botones, barras, iconos)
├── sounds/              # Audio y música
├── fonts/               # Fuentes tipográficas
├── objects/             # Objetos del juego (proyectiles, powerups)
└── tiles/               # Elementos de escenario
```

### Gestión de Rutas
- Usar **SIEMPRE** rutas absolutas en el código.
- `AssetManager` centralizado para carga de recursos.
- Caché inteligente para optimizar memoria.
- Validación de existencia de archivos antes de carga.

### Organización
- Separar assets activos de experimentales.
- Nomenclatura consistente en español.
- Formatos estándar: PNG para sprites, MP3 para audio, TTF para fuentes.
- Reutilizar texturas o fuentes temporales como placeholders.
- Evitar duplicación innecesaria de recursos.

### Exclusiones
- Assets >50MB deben estar en `.gitignore`.
- No subir archivos de trabajo (PSD, AI, etc.).
- Comprimir imágenes antes de incluir en repositorio.

## 🧪 Testing y Calidad

### Estrategia de Testing
- Cobertura mínima: 80% en `src/`.
- Tests unitarios para cada módulo.
- Tests de integración para flujos críticos.
- Tests de sistema para gameplay completo.
- Mock para recursos externos (archivos, sonidos).

### Métricas de Calidad
- **0 errores de Ruff** obligatorio.
- **0 advertencias** de type checking.
- **Máximo 150 líneas** por archivo.
- **Complejidad ciclomática < 10**.
- **Documentación al 100%** en funciones públicas.

### Herramientas de Calidad
```powershell
# Ejecutar todos los checks
poetry run ruff check src/ tests/
poetry run ruff format src/ tests/
poetry run mypy src/
poetry run pytest --cov=src tests/

# Pre-commit automático
poetry run pre-commit install
poetry run pre-commit run --all-files
```

### Estructura de Tests
```python
import pytest
import pygame
from unittest.mock import Mock, patch
from src.managers.asset_manager import AssetManager

class TestAssetManager:
    """Tests para el gestor de assets del juego."""

    @pytest.fixture
    def asset_manager(self):
        """Fixture que proporciona una instancia de AssetManager."""
        pygame.init()
        return AssetManager()
```

## 🚀 Workflow de Desarrollo

### Comandos Principales
```bash
# Ejecutar juego
poetry run python src/main.py

# Ejecutar tests
poetry run pytest tests/

# Análisis completo
poetry run pre-commit run --all-files

# Build ejecutable
poetry run python tools/package_improved.py
```

### Pre-commit Hooks
- Ruff linting y formateo automático
- MyPy type checking
- Tests automáticos
- Validación de archivos de configuración

## 🎯 Objetivos de Refactorización

### Métricas Actuales (Julio 2025)
- **32 errores Ruff** pendientes de corrección
- **Varios archivos >150 líneas** necesitan división
- **Type hints incompletos** en algunos módulos
- **Cobertura tests <80%** en algunas áreas

### Proceso de Mejora
1. **Dividir archivos grandes** manteniendo funcionalidad
2. **Corregir errores Ruff** uno por uno
3. **Añadir type hints faltantes**
4. **Aumentar cobertura de tests**
5. **Documentar funciones sin docstrings**

## 🔧 Refactorización Sistemática

### Objetivo Crítico
- Ningún archivo debe superar **150 líneas**.

### Archivos Identificados para Refactorización
- `src/entities/entity.py` (>300 líneas) - **Alta prioridad**
- `src/ui/menu_factory.py` (>300 líneas) - **Alta prioridad**
- `src/ui/menu_callbacks.py` (>300 líneas) - **Alta prioridad**
- `src/utils/world_generator.py` (>300 líneas) - **Media prioridad**
- `src/utils/animation_manager.py` (>280 líneas) - **Media prioridad**

### Estrategia de División
1. Identificar responsabilidades separadas dentro del archivo.
2. Crear submódulos específicos por responsabilidad.
3. Mantener API pública intacta para evitar breaking changes.
4. Crear tests unitarios para cada submódulo.
5. Verificar funcionalidad completa después de división.

### Proceso Seguro
1. Crear backup del archivo original.
2. Ejecutar tests antes de refactorización.
3. Dividir archivo manteniendo funcionalidad.
4. Ejecutar tests después de cada división.
5. Actualizar imports en archivos dependientes.
6. Verificar ejecución completa del juego.
7. Commit atómico por cada archivo refactorizado.

### Reglas Críticas
- **NO** cambiar comportamiento público de clases/funciones.
- Mantener backward compatibility.
- Tests deben pasar después de cada refactorización.
- Documentar cambios en `CHANGELOG.md`.
- Actualizar imports en archivos dependientes.

## 🤖 Optimización para GitHub Copilot

### Sugerencias Inteligentes
- Docstrings detalladas en español para contexto.
- Comentarios explicativos antes de lógica compleja.
- Nomenclatura descriptiva en español.
- Type hints completos para mejor inferencia.
- Ejemplos de uso en docstrings.

### Formato de Documentación
```python
def procesar_animacion_personaje(
    nombre_personaje: str,
    estado_animacion: str,
    velocidad_fps: int = 30
) -> Optional[AnimacionFrames]:
    """
    Procesa y carga los frames de animación para un personaje específico.

    Este método busca los archivos de sprite correspondientes al personaje
    y estado solicitado, los carga en memoria y configura la animación.

    Args:
        nombre_personaje: Nombre del personaje (ej: "guerrero", "mago")
        estado_animacion: Estado de la animación (ej: "idle", "run", "attack")
        velocidad_fps: Frames por segundo de la animación

    Returns:
        Objeto AnimacionFrames con los frames cargados, o None si hay error

    Example:
        >>> animacion = procesar_animacion_personaje("guerrero", "idle", 15)
        >>> if animacion:
        >>>     animacion.reproducir()
    """
```

### Patrones para IA
- Usar nombres de variables autodescriptivos.
- Agrupar lógica relacionada en funciones pequeñas.
- Comentarios de contexto antes de bloques complejos.
- Manejo explícito de errores con logging.
- Estructura predecible y consistente.

---

Esta documentación debe mantenerse actualizada con cada cambio significativo en el proyecto.

## 👾 Enemigos

- Diseñar enemigos tipo zombie masculino y femenino.
- Incluir variantes: normal, raro, élite, legendario.
- La IA debe incluir patrulla, persecución y ataque.
- Detectar al jugador a 300px como referencia estándar.

## 🖥️ HUD y Menús

- Mostrar HUD constantemente con vida, mejoras, puntos y cronómetro.
- Diseñar menús: bienvenida, principal, selección, pausa, opciones, mejoras, inventario y guardado.
- Asegurar compatibilidad visual en todas las resoluciones soportadas.
- Separar lógica de menú de su representación visual.

## 🤖 Proyecto 100% IA

Este proyecto está diseñado y desarrollado como un proyecto 100% asistido por IA. Todas las reglas, configuraciones y estándares están optimizados para herramientas de inteligencia artificial como GitHub Copilot y Copilot Chat.

### Preservación de Instrucciones
- **Nunca eliminar** este archivo ni el directorio `.github`.
- Mantener siempre actualizadas las instrucciones y reglas aquí documentadas.
- Asegurar que cualquier cambio significativo en el proyecto se refleje en este archivo.

## 🛠️ Herramientas y Configuración

### Herramientas Principales
- **Poetry**: Gestión de dependencias y entornos virtuales.
- **Ruff**: Linting y formateo.
- **Pre-commit**: Hooks automáticos de calidad.
- **Pytest**: Testing con cobertura.
- **Pyinstaller**: Empaquetado del juego.

### Extensiones de VS Code
- **GitHub Copilot**: Asistencia de IA avanzada.
- **Configuración personalizada**: Archivos de prompts en `.github/` para modularidad y soporte avanzado.

### Scripts Personalizados
- **`run_tests.py`**: Script maestro para ejecutar todos los tests desde un menú interactivo.
- **Tests Individuales**: Scripts en `scripts/` para pruebas específicas y limpieza.
- **Limpieza y Organización**: Scripts como `cleanup_project.py` y `reorganize_characters.py` para mantener el proyecto ordenado.

### Reglas para Movimientos de Ficheros
- **Siempre usar Git** para mover o renombrar ficheros dentro del proyecto.
- Esto asegura que los cambios se reflejen correctamente en el historial de Git y evita problemas de sincronización.
- Ejemplo:
  ```bash
  git mv <archivo_origen> <archivo_destino>
  ```

## 🔄 Flujo de Trabajo Autónomo

- Los flujos de trabajo deben continuar de la forma más autónoma posible hasta llegar a un punto donde se puedan realizar pruebas pertinentes.
- Esto incluye la resolución de errores, ajustes en el código y validaciones preliminares.
- Documentar cualquier cambio significativo realizado durante este proceso.

## 🛠️ Reglas para Comandos de Terminal

- Evitar el uso de `&&` para encadenar comandos en terminal.
- Usar comandos separados por líneas para mayor claridad y robustez.
- Ejemplo:
  ```bash
  git add .
  git commit -m "Mensaje de commit"
  git push
  ```

## 🔄 Reglas para Pruebas

- Antes de ejecutar cualquier banco de pruebas, reinicia el servidor del entorno virtual (venv) para evitar cargar elementos o memoria no deseados.
- Esto asegura que las pruebas se ejecuten en un entorno limpio y controlado.
``````
