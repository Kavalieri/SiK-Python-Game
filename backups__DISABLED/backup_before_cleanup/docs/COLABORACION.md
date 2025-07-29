# Guía de Colaboración - SiK Python Game

## 📋 Introducción

Esta guía establece las normas y procedimientos para colaborar en el desarrollo de SiK Python Game. Sigue las mejores prácticas de la comunidad Python y asegura la calidad y consistencia del código.

## 🎯 Objetivos del Proyecto

- Desarrollar un videojuego 2D completo y funcional
- Mantener código limpio, documentado y mantenible
- Seguir las convenciones de la comunidad Python
- Facilitar la colaboración y escalabilidad del proyecto

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
SiK-Python-Game/
├── src/                    # Código fuente principal
│   ├── core/              # Motor del juego
│   │   ├── game_engine.py # Motor principal
│   │   ├── game_state.py  # Estado global
│   │   └── scene_manager.py # Gestor de escenas
│   ├── entities/          # Entidades del juego
│   ├── managers/          # Gestores especializados
│   ├── ui/               # Interfaz de usuario
│   ├── utils/            # Utilidades
│   └── main.py           # Punto de entrada
├── assets/               # Recursos del juego
├── docs/                 # Documentación
├── tools/                # Herramientas de desarrollo
├── tests/                # Pruebas unitarias
├── logs/                 # Archivos de log
├── saves/                # Partidas guardadas
└── config.json           # Configuración del juego
```

### Componentes Principales

1. **Core**: Motor principal del juego
   - `GameEngine`: Bucle principal y gestión de eventos
   - `GameState`: Estado global del juego
   - `SceneManager`: Gestión de escenas

2. **Utils**: Utilidades y herramientas
   - `ConfigManager`: Gestión de configuración
   - `AssetManager`: Carga y gestión de recursos
   - `InputManager`: Gestión de entrada
   - `Logger`: Sistema de logging

3. **Entities**: Entidades del juego
   - Jugador, enemigos, objetos, etc.

4. **Managers**: Gestores especializados
   - Audio, física, colisiones, etc.

5. **UI**: Interfaz de usuario
   - Menús, HUD, elementos de interfaz

## 📝 Convenciones de Código

### Idioma y Nomenclatura

- **Idioma principal**: Español
- **Comentarios**: Español
- **Documentación**: Español
- **Variables y funciones**: Español
- **Clases**: Español con CamelCase
- **Módulos y archivos**: Español con snake_case

### Estilo de Código

- **Formato**: PEP 8 con tabulación
- **Longitud de línea**: 88 caracteres (Black)
- **Docstrings**: Google style
- **Type hints**: Obligatorios en funciones públicas

### Ejemplo de Código

```python
"""
Ejemplo de clase siguiendo las convenciones del proyecto.
"""

from typing import Optional, Dict, Any
import logging


class GestorEjemplo:
	"""
	Gestor de ejemplo que muestra las convenciones del proyecto.
	
	Attributes:
		configuracion: Configuración del gestor
		logger: Logger para el gestor
	"""
	
	def __init__(self, configuracion: Dict[str, Any]):
		"""
		Inicializa el gestor de ejemplo.
		
		Args:
			configuracion: Configuración inicial del gestor
		"""
		self.configuracion = configuracion
		self.logger = logging.getLogger(__name__)
		self.logger.info("Gestor de ejemplo inicializado")
	
	def procesar_datos(self, datos: str) -> Optional[str]:
		"""
		Procesa los datos de entrada.
		
		Args:
			datos: Datos a procesar
			
		Returns:
			Datos procesados o None si hay error
		"""
		try:
			resultado = datos.upper()
			self.logger.debug(f"Datos procesados: {resultado}")
			return resultado
		except Exception as e:
			self.logger.error(f"Error al procesar datos: {e}")
			return None
```

## 🔧 Herramientas de Desarrollo

### Herramientas Obligatorias

1. **Black**: Formateo de código
2. **Flake8**: Linting y verificación de estilo
3. **MyPy**: Verificación de tipos
4. **Pytest**: Testing

### Comandos de Desarrollo

```bash
# Formatear código
black src/

# Verificar estilo
flake8 src/

# Verificar tipos
mypy src/

# Ejecutar tests
pytest tests/

# Ejecutar tests con cobertura
pytest tests/ --cov=src --cov-report=html
```

### Configuración de IDE

#### Visual Studio Code

Recomendamos las siguientes extensiones:
- Python
- Pylance
- Black Formatter
- Flake8
- Python Test Explorer

Configuración recomendada en `.vscode/settings.json`:

```json
{
	"python.formatting.provider": "black",
	"python.linting.enabled": true,
	"python.linting.flake8Enabled": true,
	"python.linting.mypyEnabled": true,
	"editor.formatOnSave": true,
	"editor.codeActionsOnSave": {
		"source.organizeImports": true
	}
}
```

## 🧪 Testing

### Estructura de Tests

```
tests/
├── __init__.py
├── test_config_manager.py
├── test_game_engine.py
├── test_asset_manager.py
└── test_input_manager.py
```

### Convenciones de Testing

- **Nombres de archivos**: `test_*.py`
- **Nombres de clases**: `Test*`
- **Nombres de métodos**: `test_*`
- **Cobertura mínima**: 80%

### Ejemplo de Test

```python
"""
Test de ejemplo siguiendo las convenciones del proyecto.
"""

import pytest
from src.utils.config_manager import ConfigManager


class TestConfigManager:
	"""Pruebas para el ConfigManager."""
	
	def test_default_config(self):
		"""Prueba que la configuración por defecto se carga correctamente."""
		config = ConfigManager()
		
		assert "game" in config.config
		assert config.get("game", "title") == "SiK Python Game"
	
	def test_set_value(self):
		"""Prueba establecer un valor de configuración."""
		config = ConfigManager()
		
		config.set("game", "debug", True)
		assert config.get("game", "debug") == True
```

## 📚 Documentación

### Documentación de Código

- **Docstrings**: Obligatorios en todas las funciones y clases
- **Comentarios**: Explicar el "por qué", no el "qué"
- **README**: Mantener actualizado
- **CHANGELOG**: Documentar todos los cambios

### Documentación de Funciones

```python
def funcion_ejemplo(parametro1: str, parametro2: int = 10) -> bool:
	"""
	Descripción breve de la función.
	
	Descripción más detallada si es necesaria.
	
	Args:
		parametro1: Descripción del primer parámetro
		parametro2: Descripción del segundo parámetro (opcional)
		
	Returns:
		Descripción del valor de retorno
		
	Raises:
		ValueError: Cuando el parámetro1 es inválido
		
	Example:
		>>> funcion_ejemplo("test", 5)
		True
	"""
	pass
```

## 🔄 Control de Versiones

### Convenciones de Git

- **Commits**: Mensajes descriptivos en español
- **Branches**: `feature/nombre-funcionalidad`
- **Pull Requests**: Requieren revisión
- **Merge**: Solo después de tests exitosos

### Estructura de Commits

```
tipo(alcance): descripción breve

Descripción detallada si es necesaria.

- Cambio 1
- Cambio 2
- Cambio 3

Fixes #123
```

Tipos de commit:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato de código
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Tareas de mantenimiento

### Ejemplo de Commit

```
feat(core): añadir sistema de escenas

Implementa el sistema de gestión de escenas para el juego.
Permite cambiar entre diferentes pantallas (menú, juego, pausa).

- Añade SceneManager para gestionar escenas
- Implementa clase base Scene
- Añade transiciones entre escenas
- Incluye tests unitarios

Fixes #45
```

## 🚀 Flujo de Trabajo

### 1. Preparación

1. Fork del repositorio
2. Clone del fork local
3. Crear entorno virtual
4. Instalar dependencias

### 2. Desarrollo

1. Crear branch para la funcionalidad
2. Implementar cambios siguiendo convenciones
3. Escribir tests
4. Ejecutar herramientas de calidad

### 3. Testing

1. Ejecutar tests unitarios
2. Verificar cobertura de código
3. Ejecutar linting y type checking
4. Probar funcionalidad manualmente

### 4. Pull Request

1. Crear PR con descripción detallada
2. Incluir screenshots si es necesario
3. Referenciar issues relacionados
4. Esperar revisión y aprobación

## 🐛 Reporte de Bugs

### Plantilla de Bug Report

```
**Descripción del Bug**
Descripción clara y concisa del problema.

**Pasos para Reproducir**
1. Ir a '...'
2. Hacer clic en '...'
3. Scroll hasta '...'
4. Ver error

**Comportamiento Esperado**
Descripción de lo que debería pasar.

**Comportamiento Actual**
Descripción de lo que realmente pasa.

**Capturas de Pantalla**
Si es aplicable, añadir capturas.

**Información del Sistema**
- OS: [ej. Windows 11]
- Python: [ej. 3.11.0]
- Pygame-ce: [ej. 2.4.0]

**Logs**
Incluir logs relevantes de `logs/game.log`

**Contexto Adicional**
Cualquier otra información relevante.
```

## 💡 Sugerencias de Mejora

### Plantilla de Feature Request

```
**Descripción de la Sugerencia**
Descripción clara de la funcionalidad deseada.

**Problema que Resuelve**
Explicar por qué esta funcionalidad es necesaria.

**Solución Propuesta**
Descripción de la implementación sugerida.

**Alternativas Consideradas**
Otras soluciones que se han considerado.

**Contexto Adicional**
Cualquier otra información relevante.
```

## 📞 Comunicación

### Canales de Comunicación

- **Issues**: Bugs y feature requests
- **Discussions**: Preguntas generales
- **Pull Requests**: Revisión de código
- **Wiki**: Documentación adicional

### Normas de Comunicación

- Respeto mutuo
- Comunicación clara y constructiva
- Uso de español
- Inclusión y diversidad

## 🎯 Metas de Calidad

### Métricas Objetivo

- **Cobertura de tests**: >80%
- **Deuda técnica**: <5%
- **Tiempo de respuesta**: <24h
- **Documentación**: 100% de funciones públicas

### Revisión de Código

- **Revisión obligatoria**: Todos los PRs
- **Aprobación mínima**: 1 reviewer
- **Criterios**: Funcionalidad, estilo, tests, documentación

## 📋 Checklist de PR

- [ ] Código sigue convenciones del proyecto
- [ ] Tests incluidos y pasando
- [ ] Documentación actualizada
- [ ] No hay warnings de linting
- [ ] Type checking pasa
- [ ] Funcionalidad probada manualmente
- [ ] Commits siguen convenciones
- [ ] Descripción clara del PR

---

**¡Gracias por contribuir a SiK Python Game! 🎮**
