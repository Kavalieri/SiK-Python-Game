# Especificación del .gitignore - SiK Python Game

## 📋 Propósito del Documento
Especifica las reglas de exclusión de archivos y directorios para el control de versiones, asegurando que solo los archivos esenciales del proyecto sean trackeados.

## 🎯 Principios de Inclusión
**Solo se incluyen en el repositorio archivos que cumplan TODOS estos criterios:**
1. **Esenciales para reproducir el proyecto**: Código fuente, configuración básica, documentación
2. **No generables automáticamente**: El programa debe poder regenerar automáticamente cualquier archivo externo necesario
3. **Independientes del entorno**: No específicos de un desarrollador o sistema particular
4. **Versionables**: Cambian intencionalmente y requieren historial

## 📁 Estructura de Exclusiones

### 🐍 Python Estándar
```gitignore
# Bytecode compilado
__pycache__/
*.py[cod]
*$py.class

# Distribución y empaquetado
build/
dist/
*.egg-info/
*.egg

# Testing y coverage
.pytest_cache/
.coverage
htmlcov/
coverage.xml

# Entornos virtuales
.venv/
venv/
env/

# Herramientas de desarrollo
.mypy_cache/
.ruff_cache/
```

### 🛠️ Dev-Tools Centralizados
```gitignore
# Coverage y testing generados
dev-tools/coverage/htmlcov/
dev-tools/coverage/coverage.xml
dev-tools/testing/reports/
dev-tools/testing/fixtures/temp/

# Benchmarking y profiling
dev-tools/benchmarking/results/
dev-tools/benchmarking/.benchmarks/

# Archive temporal
dev-tools/archive/temp/
dev-tools/archive/backups/auto/

# Debugging temporal
dev-tools/debugging/temp/
dev-tools/debugging/dumps/
dev-tools/debugging/profiles/

# Packaging generado
dev-tools/packaging/dist/
dev-tools/packaging/build/
dev-tools/packaging/releases/
```

### 🎮 Específicos del Proyecto
```gitignore
# Datos del juego generados
saves/
logs/

# Releases
releases/

# Archivos temporales
cleanup_*/
backup_*/
*.temp
*.tmp
*.bak
*.old
commit_message.txt
```

### 💻 Editores y Entornos
```gitignore
# VS Code (selectivo)
.vscode/
!.vscode/settings.json
!.vscode/launch.json
!.vscode/tasks.json

# PyCharm/IntelliJ
.idea/

# Cursor AI
.cursor/
.cursorignore
```

### 🖥️ Sistema Operativo
```gitignore
# Windows
Thumbs.db
Desktop.ini
$RECYCLE_BIN/

# macOS
.DS_Store
._*

# Linux
*~
.Trash-*
```

## ✅ Archivos Incluidos (Excepciones Importantes)

### 📁 Estructura Dev-Tools Base
**Se incluyen los directorios base y archivos de configuración:**
- `dev-tools/README.md`
- `dev-tools/scripts/` (scripts esenciales)
- `dev-tools/docs/` (documentación de desarrollo)
- `dev-tools/testing/` (configuración de tests)
- `dev-tools/packaging/` (configuración de empaquetado)

### ⚙️ Configuración Esencial
**Se incluyen archivos de configuración del proyecto:**
- `.vscode/settings.json` (configuración compartida del proyecto)
- `.vscode/launch.json` (configuración de debug compartida)
- `.vscode/tasks.json` (tareas específicas del proyecto)
- `pyproject.toml` (configuración de Python/Poetry)
- `config/` (configuración del juego)

### 📚 Documentación y Assets
**Se incluyen todos los assets y documentación:**
- `assets/` (sprites, sonidos, fuentes)
- `docs/` (documentación del proyecto)
- `README.md`
- `CHANGELOG.md`

## 🔄 Archivos Regenerables Automáticamente

### 📊 Reports y Análisis
**El programa debe regenerar automáticamente:**
- Reports de coverage HTML y XML
- Reports de benchmarking
- Logs de testing
- Profiles de debugging
- Releases compiladas

### 💾 Datos de Usuario
**El juego debe crear automáticamente:**
- Directorio `saves/` para partidas guardadas
- Directorio `logs/` para logs del juego
- Archivos de configuración de usuario (si no existen)

### 🛠️ Herramientas de Desarrollo
**Los scripts deben crear automáticamente:**
- Directorios temporales en dev-tools
- Archivos de backup automático
- Caches de herramientas de desarrollo

## 📋 Validación del .gitignore

### ✅ Comandos de Verificación
```powershell
# Verificar archivos ignorados
git status --ignored

# Buscar archivos problemáticos trackeados
git ls-files | Select-String -Pattern "\.(log|tmp|temp|bak|old)$"

# Verificar que los archivos de configuración esencial estén incluidos
git ls-files | Select-String -Pattern "\.vscode/settings\.json|pyproject\.toml|config/"
```

### 🎯 Criterios de Éxito
- ✅ No hay archivos temporales o generados en `git ls-files`
- ✅ Los directorios `saves/`, `logs/`, `releases/` aparecen en `git status --ignored`
- ✅ Los archivos de configuración esencial están en el repositorio
- ✅ La estructura dev-tools base está incluida pero no los temporales

## 🔧 Mantenimiento

### 📅 Revisión Periódica
- **Mensual**: Verificar que nuevos archivos temporales estén siendo ignorados
- **Por Release**: Asegurar que los releases no incluyan archivos innecesarios
- **Por Nueva Herramienta**: Actualizar exclusiones para nuevas herramientas de desarrollo

### 🚨 Señales de Problemas
- Archivos `.tmp`, `.bak`, `.old` aparecen en `git status`
- El tamaño del repositorio crece innecesariamente
- Los desarrolladores reportan conflictos con archivos que no deberían estar trackeados

## 📖 Referencias
- [GitHub Git Ignore Templates](https://github.com/github/gitignore)
- [Python Git Ignore](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Documentación del proyecto](../README.md)

---

**Actualizado**: 30 de Julio, 2025
**Versión**: 1.0
**Próxima revisión**: 30 de Agosto, 2025
