# scripts/ - Scripts de Utilidad

## ⚙️ **PROPÓSITO**
Directorio de scripts de utilidad para desarrollo, testing, análisis y mantenimiento del videojuego **SiK Python Game**. Herramientas auxiliares que facilitan el desarrollo y la validación del proyecto.

## 📊 **ESTADO ACTUAL**
- **15+ scripts especializados** para diferentes aspectos del desarrollo
- **Enfoque modular**: Scripts específicos para tareas concretas
- **Integración con proyecto**: Scripts que conocen la estructura del juego
- **Automatización**: Herramientas para tareas repetitivas

---

## 🗂️ **CATEGORÍAS DE SCRIPTS**

### 🧪 **Scripts de Testing**

#### **`test_config_simple.py`**
**Propósito**: Validación básica del sistema de configuración
```python
# Testing rápido de ConfigManager
def test_config_loading():
    config = ConfigManager()
    assert config.get("display", "fps") == 60
    print("✅ ConfigManager funcionando correctamente")
```
**Uso**: `python scripts/test_config_simple.py`

#### **`test_config_system.py`**
**Propósito**: Testing completo del sistema de configuración modular
- Validación de carga de todos los JSON
- Verificación de integridad de configuraciones
- Testing de fallbacks y valores por defecto

#### **`test_game_functionality.py`**
**Propósito**: Testing de funcionalidad principal del juego
- Inicialización de GameEngine
- Carga de escenas principales
- Validación de sistemas críticos

#### **`test_game_launch.py`**
**Propósito**: Validación de lanzamiento completo del juego
- Testing del ciclo completo de inicialización
- Verificación de dependencias
- Validación de recursos críticos

#### **`run_tests.py`**
**Propósito**: Ejecutor centralizado de tests individuales
- Ejecuta tests específicos por módulo
- Reporte de resultados por categoría
- Logging detallado de errores

#### **`run_unified_tests.py`**
**Propósito**: Suite completa de testing automatizado
- Ejecuta todos los tests del proyecto
- Validación completa del sistema
- Reporte consolidado de estado

#### **`cleanup_tests.py`**
**Propósito**: Limpieza de archivos temporales de testing
- Elimina archivos generados por tests
- Limpia logs de testing
- Resetea estado para nuevos tests

### 🔍 **Scripts de Análisis**

#### **`analyze_file_sizes.py`**
**Propósito**: Análisis de tamaños de archivos del proyecto
```python
# Analiza archivos por tamaño y detecta problemas
def analyze_project_files():
    for file in get_python_files():
        lines = count_lines(file)
        if lines > 250:
            print(f"🔴 CRÍTICO: {file} ({lines} líneas)")
```
**Uso**: `python scripts/analyze_file_sizes.py`
**Output**: Reporte de archivos que exceden límites

### 🧹 **Scripts de Limpieza**

#### **`cleanup_project.py`**
**Propósito**: Limpieza general del proyecto
- Elimina archivos temporales (__pycache__, .pyc)
- Limpia logs antiguos
- Organiza archivos dispersos

#### **`cleanup_project_v2.py`**
**Propósito**: Versión mejorada del sistema de limpieza
- Limpieza más inteligente y selectiva
- Preserva archivos importantes
- Logging detallado de acciones

### 🎨 **Scripts de Assets**

#### **`clean_asset_names.py`**
**Propósito**: Normalización de nombres de archivos de assets
```python
# Limpia nombres de archivos para consistencia
def clean_asset_names():
    for asset_file in get_asset_files():
        clean_name = normalize_filename(asset_file)
        if clean_name != asset_file:
            rename_file(asset_file, clean_name)
```
**Uso**: `python scripts/clean_asset_names.py`

#### **`reorganize_characters.py`**
**Propósito**: Reorganización de assets de personajes
- Mueve archivos a estructura estándar
- Valida integridad de animaciones
- Detecta assets faltantes

#### **`reorganize_guerrero.py`**
**Propósito**: Reorganización específica del personaje guerrero
- Script especializado para assets del guerrero
- Validación de animaciones completas
- Organización por convención establecida

---

## 📋 **DOCUMENTACIÓN INCLUIDA**

### 📚 **`README.md`**
**Propósito**: Documentación general de scripts disponibles
- Lista de scripts con descripciones
- Instrucciones de uso
- Dependencias y requisitos

### 📈 **`MEJORAS_IMPLEMENTADAS.md`**
**Propósito**: Registro de mejoras aplicadas por scripts
- Historial de optimizaciones realizadas
- Métricas de mejoras aplicadas
- Changelog de modificaciones automatizadas

---

## 🎯 **FLUJOS DE TRABAJO**

### 🧪 **Testing Completo**
```bash
# Secuencia completa de testing
python scripts/run_unified_tests.py        # Testing completo
python scripts/test_game_launch.py         # Validación de lanzamiento
python scripts/cleanup_tests.py            # Limpieza post-testing
```

### 🔍 **Análisis de Proyecto**
```bash
# Análisis de estado del proyecto
python scripts/analyze_file_sizes.py       # Verificar límites de líneas
python scripts/test_config_system.py       # Validar configuraciones
```

### 🧹 **Mantenimiento**
```bash
# Limpieza y organización
python scripts/cleanup_project_v2.py       # Limpieza general
python scripts/clean_asset_names.py        # Normalizar assets
python scripts/reorganize_characters.py    # Organizar personajes
```

---

## ⚡ **CARACTERÍSTICAS DE LOS SCRIPTS**

### 🔧 **Automatización Inteligente**
- **Detección automática**: Scripts detectan estructura del proyecto
- **Validación previa**: Verifican estado antes de ejecutar cambios
- **Backup automático**: Crean respaldos antes de modificaciones
- **Logging detallado**: Registro completo de acciones realizadas

### 🛡️ **Seguridad**
- **Dry-run mode**: Simulación sin cambios reales
- **Confirmación usuario**: Solicita confirmación para cambios críticos
- **Reversibilidad**: Operaciones reversibles cuando es posible
- **Validación post-cambio**: Verificación de integridad después de modificaciones

### 📊 **Reporting**
- **Métricas cuantificables**: Reportes con números específicos
- **Categorización**: Organización de resultados por tipo
- **Formato legible**: Output estructurado y comprensible
- **Persistencia**: Guardado de resultados para comparación histórica

---

## 🔧 **INTEGRACIÓN CON DESARROLLO**

### 🎮 **Conocimiento del Proyecto**
Los scripts están diseñados específicamente para **SiK Python Game**:
- **Estructura conocida**: Scripts conocen organización del proyecto
- **Configuraciones**: Usan mismo ConfigManager que el juego
- **Convenciones**: Respetan estándares de nomenclatura del proyecto
- **Assets**: Entienden estructura de recursos del juego

### 🔄 **Integración con Git**
- **Respeto a .gitignore**: No interfieren con control de versiones
- **Commits inteligentes**: Algunos scripts pueden crear commits automáticos
- **Branch awareness**: Detectan estado de git para operaciones seguras

### 📝 **Logging Integrado**
```python
# Los scripts usan el mismo sistema de logging que el juego
from src.utils.logger import setup_logger
logger = setup_logger("Scripts", "logs/scripts.log")
```

---

## 🚀 **DESARROLLO DE NUEVOS SCRIPTS**

### 📋 **Plantilla Estándar**
```python
#!/usr/bin/env python3
"""
Script de utilidad para SiK Python Game
Descripción: [propósito del script]
Uso: python scripts/[nombre_script].py
"""

import sys
import os
from pathlib import Path

# Añadir src al path para imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from utils.logger import setup_logger

def main():
    """Función principal del script"""
    logger = setup_logger("ScriptName", "logs/script.log")

    try:
        # Lógica del script
        logger.info("Script ejecutado exitosamente")
    except Exception as e:
        logger.error(f"Error en script: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 🎯 **Mejores Prácticas**
- **Documentación**: Docstrings claros con propósito y uso
- **Error handling**: Manejo robusto de errores y excepciones
- **Logging**: Uso del sistema de logging del proyecto
- **Validación**: Verificación de precondiciones antes de ejecutar
- **Help**: Opción --help con descripción detallada

---

## 📊 **MÉTRICAS DE SCRIPTS**

### 📈 **Scripts de Testing**
- **Cobertura**: Tests cubren aspectos críticos del juego
- **Tiempo ejecución**: Tests rápidos para desarrollo iterativo
- **Fiabilidad**: Tests consistentes y repetibles

### 🧹 **Scripts de Limpieza**
- **Archivos procesados**: Cantidad de archivos organizados
- **Espacio liberado**: MB liberados por limpieza
- **Errores corregidos**: Problemas detectados y solucionados

### 🔍 **Scripts de Análisis**
- **Problemas detectados**: Issues identificados en el código
- **Métricas calculadas**: Estadísticas del proyecto
- **Tendencias**: Evolución de métricas en el tiempo

---

## 🔗 **REFERENCIAS**

### 📖 **Documentación del Proyecto**
- **Configuración**: `config/` - Configuraciones que usan los scripts
- **Logging**: `src/utils/logger.py` - Sistema de logging compartido
- **Estructura**: `src/` - Código que analizan y validan los scripts

### 🛠️ **Herramientas Relacionadas**
- **dev-tools/**: Herramientas más avanzadas de desarrollo
- **tests/**: Tests unitarios del proyecto
- **logs/**: Logs generados por scripts

---

**⚙️ ESTADO**: ✅ SUITE COMPLETA DE SCRIPTS DE UTILIDAD
**📅 ÚLTIMA ACTUALIZACIÓN**: 30 de Julio, 2025
**🎯 ENFOQUE**: Automatización y validación para desarrollo eficiente
