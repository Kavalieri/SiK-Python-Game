# SiK Python Game - Instrucciones de Desarrollo

**Fecha de actualización:** 29/07/2025
**Versión:** v0.1.5-alpha
**Stack tecnológico:** Python 3.11+ | Poetry | Ruff | Pre-commit | PowerShell

---

## 🎯 **FILOSOFÍA DEL PROYECTO**

**SiK Python Game** es un videojuego 2D desarrollado **100% con asistencia de inteligencia artificial**, utilizando las mejores prácticas modernas de desarrollo Python y herramientas de la comunidad.

### Principios Fundamentales:
- **Desarrollo asistido por IA**: Cada línea de código generada/refinada con agentes IA
- **Calidad antes que velocidad**: Código limpio, documentado y mantenible
- **Herramientas modernas**: Stack tecnológico 2025 con Poetry, Ruff, pre-commit
- **Modularidad extrema**: Máximo 150 líneas por archivo
- **Documentación viva**: Actualizada automáticamente con cada cambio

---

## 🛠️ **ENTORNO DE DESARROLLO REQUERIDO**

### Sistema Operativo
- **Windows 11** (entorno principal)
- **PowerShell 5.1+** (terminal exclusiva)
- **Visual Studio Code** (IDE recomendado)

### Herramientas Obligatorias
1. **Python 3.11+**
2. **Poetry** (gestión de dependencias)
3. **Git** (control de versiones)
4. **Ruff** (linting y formateo - instalado automáticamente)
5. **Pre-commit** (hooks de calidad - instalado automáticamente)

---

## 📦 **INSTALACIÓN Y CONFIGURACIÓN**

### 1. Clonar el Repositorio
```powershell
git clone https://github.com/Kavalieri/SiK-Python-Game.git
cd SiK-Python-Game
```

### 2. Instalar Poetry (si no está instalado)
```powershell
# Opción 1: Instalador oficial
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Opción 2: pip (si ya tienes Python)
pip install poetry
```

### 3. Configurar Entorno de Desarrollo
```powershell
# Instalar dependencias
poetry install

# Configurar pre-commit hooks
poetry run pre-commit install

# Verificar instalación
poetry run python src/main.py --version
```

### 4. Configuración de VS Code (Recomendada)
Instalar extensiones:
- Python
- Pylance
- Ruff
- Pre-commit Hook

Configuración en `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "ruff.enable": true,
    "ruff.organizeImports": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    }
}
```

---

## 🎮 **CÓMO EJECUTAR EL JUEGO**

### Ejecución Normal
```powershell
# Activar entorno y ejecutar
poetry run python src/main.py
```

### Ejecución con Debug
```powershell
# Con logging detallado
poetry run python src/main.py --debug

# Con profiling
poetry run python tools/debug_game_engine.py
```

### Ejecutar Tests
```powershell
# Todos los tests
poetry run pytest tests/

# Test específico
poetry run pytest tests/test_config_manager.py

# Con cobertura
poetry run pytest tests/ --cov=src --cov-report=html
```

---

## 📁 **ESTRUCTURA DEL PROYECTO 2025**

```
SiK-Python-Game/
├── .github/                    # GitHub Copilot instrucciones especializadas
│   ├── copilot-*.md           # Instrucciones por módulo/funcionalidad
│   └── MIGRACION_COMPLETA.md  # Historia de migración
├── src/                       # Código fuente principal (MÁXIMO 150 líneas/archivo)
│   ├── core/                  # Motor del juego
│   ├── entities/              # Entidades del juego
│   ├── managers/              # Gestores especializados
│   ├── scenes/                # Escenas del juego
│   ├── ui/                    # Interfaz de usuario
│   ├── utils/                 # Utilidades compartidas
│   └── main.py               # Punto de entrada
├── assets/                    # Recursos del juego
│   ├── characters/           # Sprites de personajes
│   ├── sounds/               # Audio y música
│   ├── ui/                   # Elementos de interfaz
│   └── fonts/                # Fuentes tipográficas
├── config/                    # Configuraciones JSON modulares
├── docs/                      # Documentación técnica
├── tests/                     # Tests unitarios y de integración
├── tools/                     # Herramientas de desarrollo
├── scripts/                   # Scripts de automatización
├── logs/                      # Archivos de log (gitignored)
├── saves/                     # Partidas guardadas (gitignored)
├── releases/                  # Versiones empaquetadas (gitignored)
├── pyproject.toml            # Configuración Poetry
├── .pre-commit-config.yaml   # Configuración pre-commit
└── .gitignore               # Exclusiones Git optimizadas
```

---

## 🔧 **FLUJO DE DESARROLLO**

### 1. Preparación de Funcionalidad
```powershell
# Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# Verificar que todo está limpio
poetry run pre-commit run --all-files
```

### 2. Desarrollo
- **Máximo 150 líneas por archivo**
- **Documentación obligatoria en cada función**
- **Type hints en todas las funciones públicas**
- **Logging detallado para debug**

### 3. Verificación Antes de Commit
```powershell
# Ejecutar tests
poetry run pytest tests/

# Verificar calidad de código (automático con pre-commit)
poetry run ruff check src/
poetry run ruff format src/
```

### 4. Commit y Push
```powershell
# Pre-commit se ejecuta automáticamente
git add .
git commit -m "feat(módulo): descripción clara del cambio"
git push origin feature/nueva-funcionalidad
```

---

## 📋 **CONVENCIONES DE CÓDIGO 2025**

### Idioma y Nomenclatura
- **Idioma principal**: Español
- **Comentarios y documentación**: Español
- **Variables y funciones**: `snake_case` en español
- **Clases**: `PascalCase` en español
- **Constantes**: `UPPER_SNAKE_CASE` en español

### Estilo de Código
- **Formatter**: Ruff (reemplaza Black)
- **Linter**: Ruff (reemplaza Flake8)
- **Longitud de línea**: 88 caracteres
- **Indentación**: 4 espacios (configurado automáticamente)
- **Type hints**: Obligatorios en funciones públicas

### Ejemplo de Código Estándar
```python
"""
Módulo de ejemplo siguiendo convenciones 2025.

Autor: SiK Team + IA
Fecha: 29/07/2025
Versión: v0.1.5-alpha
"""

from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GestorConfiguracion:
    """
    Gestor de configuración modular para el juego.

    Attributes:
        configuracion_actual: Configuración cargada
        ruta_archivo: Ruta al archivo de configuración
    """

    def __init__(self, ruta_archivo: str) -> None:
        """
        Inicializa el gestor de configuración.

        Args:
            ruta_archivo: Ruta al archivo de configuración
        """
        self.ruta_archivo = ruta_archivo
        self.configuracion_actual: Dict[str, Any] = {}
        logger.info(f"Gestor de configuración iniciado: {ruta_archivo}")

    def cargar_configuracion(self) -> bool:
        """
        Carga la configuración desde el archivo.

        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        try:
            # Lógica de carga aquí...
            logger.debug("Configuración cargada exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error al cargar configuración: {e}")
            return False
```

---

## 🧪 **TESTING Y CALIDAD**

### Estructura de Tests
```
tests/
├── __init__.py
├── test_config_manager.py      # Tests del gestor de configuración
├── test_game_engine.py         # Tests del motor principal
├── test_asset_manager.py       # Tests del gestor de assets
└── README.md                   # Documentación de tests
```

### Convenciones de Testing
- **Archivos**: `test_*.py`
- **Clases**: `Test*`
- **Métodos**: `test_*`
- **Cobertura mínima**: 80%
- **Documentación**: Obligatoria en cada test

### Ejecutar Tests
```powershell
# Todos los tests
poetry run pytest tests/ -v

# Con cobertura
poetry run pytest tests/ --cov=src --cov-report=html --cov-report=term

# Tests específicos
poetry run pytest tests/test_config_manager.py -v
```

---

## 🔄 **CONTROL DE VERSIONES**

### Convenciones de Git
- **Commits**: Mensajes descriptivos en español
- **Branches**: `feature/nombre-funcionalidad`
- **Pull Requests**: Revisión obligatoria
- **Merge**: Solo después de tests exitosos y revisión

### Estructura de Commits
```
tipo(módulo): descripción breve en español

Descripción detallada si es necesaria.

- Cambio específico 1
- Cambio específico 2
- Cambio específico 3

Closes #123
```

### Tipos de Commit
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato de código
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Tareas de mantenimiento
- `perf`: Mejoras de rendimiento

---

## 🚨 **REGLAS CRÍTICAS**

### ❌ **PROHIBIDO**
1. **Archivos > 150 líneas** (excepto configuración)
2. **Código sin documentación**
3. **Commits sin pasar pre-commit**
4. **Push directo a main**
5. **Uso de `pip` en lugar de `poetry`**
6. **Imports relativos complejos**
7. **Código sin type hints en funciones públicas**

### ✅ **OBLIGATORIO**
1. **Pre-commit hooks funcionando**
2. **Tests para nueva funcionalidad**
3. **Documentación actualizada**
4. **Logging en funciones críticas**
5. **Gestión de errores robusta**
6. **Rutas absolutas para assets**
7. **Configuración modular en JSON**

---

## 🎯 **OBJETIVOS DE CALIDAD 2025**

### Métricas de Código
- **Cobertura de tests**: ≥80%
- **Complejidad ciclomática**: ≤10 por función
- **Líneas por archivo**: ≤150
- **Errores de linting**: 0
- **Warnings de type checking**: 0

### Métricas de Desarrollo
- **Tiempo de build**: ≤30 segundos
- **Tiempo de tests**: ≤60 segundos
- **Tiempo de startup**: ≤5 segundos
- **Memoria utilizada**: ≤500MB

---

## 🔗 **RECURSOS Y REFERENCIAS**

### Documentación Técnica
- [`docs/COLABORACION.md`](docs/COLABORACION.md) - Guía completa de colaboración
- [`docs/SISTEMA_EMPAQUETADO.md`](docs/SISTEMA_EMPAQUETADO.md) - Empaquetado para distribución
- [`docs/FLUJO_MENUS_GUARDADO.md`](docs/FLUJO_MENUS_GUARDADO.md) - Sistema de menús y guardado
- [`.github/`](.github/) - Instrucciones especializadas GitHub Copilot

### Herramientas
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Pygame-ce Documentation](https://pyga.me/)

### Comunidad
- **Issues**: Reportar bugs y solicitar funcionalidades
- **Discussions**: Preguntas generales y propuestas
- **Pull Requests**: Contribuciones de código
- **Wiki**: Documentación extendida

---

## 📞 **SOPORTE Y CONTACTO**

### Para Desarrolladores
- **Issues del repositorio**: Problemas técnicos
- **Discussions**: Consultas generales
- **Pull Requests**: Contribuciones

### Para Usuarios
- **README.md**: Información de usuario final
- **Releases**: Versiones estables
- **Wiki**: Guías de usuario

---

**© 2025 SiK Team + Inteligencia Artificial. Desarrollado con las mejores prácticas de la comunidad Python.**
