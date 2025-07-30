# Configuración Optimizada de PowerShell para VS Code

## 🎯 **Resumen de Optimización**

Esta configuración optimiza VS Code para trabajar eficientemente con nuestros scripts PowerShell del proyecto SiK Python Game, especialmente nuestros scripts de automatización como `simple_commit.ps1` y `unified_commit.ps1`.

## ⚙️ **Configuraciones Implementadas**

### 🔧 **Settings.json (.vscode/settings.json)**

#### PowerShell Configuration
- **Terminal por defecto**: PowerShell con argumentos optimizados
- **Ejecución sin perfil**: `-NoProfile -ExecutionPolicy Bypass`
- **Soporte PowerShell Core**: Configuración adicional para pwsh.exe
- **IntelliSense mejorado**: Autocompletado específico para PowerShell

#### Editor Optimization
- **Límite de líneas**: 150 (nuestro estándar de refactorización)
- **Rulers visuales**: Línea indicadora en columna 150
- **Formateo automático**: Al guardar archivos
- **Word wrap**: Limitado a 150 caracteres

#### Terminal Enhancement
- **ScrollBack**: 10,000 líneas de historial
- **Fuente optimizada**: Tamaño 14 para mejor legibilidad
- **Sessions**: Deshabilitadas para mejor rendimiento

### 📋 **PSScriptAnalyzer (.vscode/PSScriptAnalyzerSettings.psd1)**

#### Reglas Habilitadas
- **Mejores prácticas**: Cmdlets aprobados, verbos correctos
- **Seguridad**: Evitar contraseñas en texto plano
- **Consistencia**: Indentación, espaciado, llaves
- **Documentación**: Comentarios de ayuda requeridos

#### Reglas Específicas
- **Indentación**: 4 espacios (consistente con Python)
- **Llaves**: Mismo línea, nueva línea después
- **Espaciado**: Consistente en operadores y pipes
- **Comentarios**: Bloque al inicio de funciones

### 📋 **Tasks.json (.vscode/tasks.json)**

#### Tareas Principales
1. **🔄 Simple Commit**: Ejecuta nuestro script de commit simple
2. **🔧 Unified Commit**: Script completo con validaciones
3. **🧹 VS Code Cleanup**: Limpieza automática post-operación
4. **🐍 Run Python Game**: Ejecuta el juego usando Poetry
5. **📋 Analyze PowerShell Scripts**: Análisis de calidad de scripts

#### Inputs Configurados
- **Mensaje de commit**: Prompt personalizable
- **Tipo de commit**: feat, fix, docs, refactor, etc.
- **Ámbito**: core, entities, scenes, ui, utils, etc.

## 🚀 **Beneficios Implementados**

### ✅ **IntelliSense Mejorado**
- Autocompletado específico para cmdlets PowerShell
- Sugerencias contextuales para nuestros scripts
- Detección de errores en tiempo real

### ✅ **Debugging Integrado**
- Breakpoints en scripts .ps1
- Inspección de variables
- Stack trace detallado
- Debugging paso a paso

### ✅ **Análisis de Código**
- PSScriptAnalyzer integrado
- Reglas personalizadas para nuestro proyecto
- Warnings y errores en tiempo real
- Sugerencias de mejores prácticas

### ✅ **Workflow Optimizado**
- Tareas predefinidas para operaciones comunes
- Shortcuts para commits y limpieza
- Terminal optimizado para PowerShell
- Configuración específica del proyecto

## 🎯 **Casos de Uso Específicos**

### 1. **Debugging de Scripts de Commit**
```powershell
# Ahora puedes poner breakpoints en:
.\scripts\simple_commit.ps1
.\scripts\unified_commit.ps1
```

### 2. **Análisis de Calidad**
```powershell
# Ejecutar análisis desde Command Palette:
Ctrl+Shift+P → "Tasks: Run Task" → "📋 Analyze PowerShell Scripts"
```

### 3. **Commits Interactivos**
```powershell
# Ejecutar desde Command Palette:
Ctrl+Shift+P → "Tasks: Run Task" → "🔄 Simple Commit"
```

### 4. **Limpieza Automática**
```powershell
# Ejecutar desde Command Palette:
Ctrl+Shift+P → "Tasks: Run Task" → "🧹 VS Code Cleanup"
```

## 📊 **Métricas de Mejora**

### Antes de la Optimización
- ❌ Sin IntelliSense para PowerShell
- ❌ Sin debugging de scripts
- ❌ Sin análisis de código
- ❌ Terminal básico sin optimización

### Después de la Optimización
- ✅ IntelliSense completo para PowerShell
- ✅ Debugging integrado de scripts
- ✅ PSScriptAnalyzer con reglas personalizadas
- ✅ Terminal optimizado con historial extendido
- ✅ Tareas predefinidas para workflow común
- ✅ Configuración específica del proyecto

## 🔄 **Uso Diario Recomendado**

### 1. **Al iniciar VS Code**
- Terminal PowerShell se abre automáticamente
- IntelliSense habilitado para todos los scripts
- PSScriptAnalyzer analiza código en tiempo real

### 2. **Durante desarrollo**
- F5 para debugging de scripts .ps1
- Ctrl+Shift+P → Tasks para operaciones comunes
- Análisis automático de calidad de código

### 3. **Al hacer commits**
- Usar tarea "🔄 Simple Commit" para commits rápidos
- Usar tarea "🔧 Unified Commit" para commits completos
- Limpieza automática con "🧹 VS Code Cleanup"

## 📁 **Archivos de Configuración**

```
.vscode/
├── settings.json              # Configuración principal
├── tasks.json                 # Tareas automatizadas
└── PSScriptAnalyzerSettings.psd1  # Reglas de análisis
```

## 🎯 **Próximos Pasos**

1. **Reiniciar VS Code**: Para que tome todas las configuraciones
2. **Probar IntelliSense**: Abrir cualquier script .ps1
3. **Ejecutar tareas**: Ctrl+Shift+P → "Tasks: Run Task"
4. **Debugging**: F5 en cualquier script PowerShell
5. **Análisis**: Verificar warnings/errores automáticos

---

**🎮 Configuración optimizada para SiK Python Game - Workflow PowerShell mejorado**
