# 🚀 SiK Workflow System - Guía de Migración a Otros Proyectos

## **Para Agentes de IA y Desarrolladores**

Esta guía permite implementar el **Sistema de Workflow SiK** en cualquier repositorio de Git, proporcionando un flujo de desarrollo profesional, robusto y completamente automatizado.

---

## **📋 ¿Qué es el Sistema SiK Workflow?**

Es un sistema de comandos unificado que **SIEMPRE** obliga a seguir el flujo:

**`Rama → Cambios → PR → Review → Merge → Release`**

### **✅ Características Principales:**
- ✅ **Elimina commits directos a main** - SIEMPRE pasa por PR
- ✅ **Workflow consistente** - 7 comandos simples
- ✅ **Gestión automática de ramas** - Creación, limpieza, navegación
- ✅ **PRs vinculados a issues** - Tracking automático
- ✅ **Releases con builds automáticos** - Ejecutables en GitHub
- ✅ **Gestión de múltiples tareas** - Ramas separadas por contexto
- ✅ **Stash inteligente** - Mueve cambios entre contextos

---

## **🔧 Instalación en Nuevo Proyecto**

### **Paso 1: Copiar Archivos Base**

```bash
# En el proyecto destino, crear estructura
mkdir -p dev-tools/scripts

# Copiar archivos principales desde SiK-Python-Game
cp dev-tools/scripts/sik-flow.ps1 [NUEVO_PROYECTO]/dev-tools/scripts/
cp dev-tools/scripts/build_professional.ps1 [NUEVO_PROYECTO]/dev-tools/scripts/  # Opcional

# Crear archivo de versión
echo "0.1.0" > VERSION.txt
```

### **Paso 2: Configurar Prerrequisitos**

```bash
# GitHub CLI (REQUERIDO)
winget install GitHub.cli
# o
choco install gh

# Configurar autenticación
gh auth login

# Configurar Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### **Paso 3: Configurar PowerShell (Solo primera vez)**

```powershell
# Permitir ejecución de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar configuración
.\dev-tools\scripts\sik-flow.ps1 status
```

---

## **⚙️ Adaptaciones por Tipo de Proyecto**

### **Proyectos Python**
```powershell
# Mantener build_professional.ps1 para ejecutables
# Asegurar structure:
# - src/main.py (punto de entrada)
# - requirements.txt o pyproject.toml
# - VERSION.txt
```

### **Proyectos Node.js**
```powershell
# Modificar build_professional.ps1 para npm/yarn
# Cambiar en línea 18-19:
EntryPoint = "index.js"  # o "src/index.js"
# Añadir package.json como archivo requerido
```

### **Proyectos .NET**
```powershell
# Modificar build_professional.ps1 para dotnet publish
# Cambiar en línea 18-19:
EntryPoint = "Program.cs"  # o archivo principal
# Añadir *.csproj como archivo requerido
```

### **Proyectos Solo Web (No Builds)**
```powershell
# Usar solo sik-flow.ps1 sin build_professional.ps1
# El comando 'release' funcionará sin generar ejecutables
```

---

## **🎯 Configuración Específica del Proyecto**

### **Modificar Variables Principales**

En `sik-flow.ps1`, líneas 14-16:
```powershell
$ProjectRoot = $PWD
$MainBranch = "main"        # Cambiar si usas 'master' o 'develop'
$VersionFile = Join-Path $ProjectRoot "VERSION.txt"  # Ruta al archivo de versión
```

### **Adaptar Sistema de Build**

En `build_professional.ps1`, líneas 24-32:
```powershell
$BuildConfig = @{
    ProjectName = "TU-PROYECTO-AQUI"      # Nombre del proyecto
    EntryPoint = "src\main.py"            # Archivo principal
    OutputDir = "dist"                    # Directorio de salida
    BuildDir = "build"                    # Directorio temporal
    AssetsDir = "assets"                  # Recursos (opcional)
    ConfigDir = "config"                  # Configuración (opcional)
    IconFile = "assets\icon.ico"          # Icono (opcional)
    RequiredPython = "3.11"               # Versión mínima Python
}
```

### **Personalizar Comandos de Build**

Para otros lenguajes, modificar la función `Invoke-NuitkaBuild` en `build_professional.ps1`:

```powershell
# Para Node.js:
function Invoke-NodeBuild {
    npm run build
    # Lógica específica
}

# Para .NET:
function Invoke-DotnetBuild {
    dotnet publish -c Release
    # Lógica específica
}
```

---

## **📝 Uso del Sistema (Para Agentes de IA)**

### **Comando Básicos Obligatorios**

```powershell
# 1. SIEMPRE verificar estado primero
.\dev-tools\scripts\sik-flow.ps1 status

# 2. Crear nueva rama para cada tarea diferente
.\dev-tools\scripts\sik-flow.ps1 new -Rama "feature/nueva-funcionalidad" -Mensaje "Descripción clara"

# 3. Guardar cambios frecuentemente
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "Descripción específica" -Push

# 4. Crear PR cuando esté completo
.\dev-tools\scripts\sik-flow.ps1 pr -Mensaje "Funcionalidad completa" -Issue 123

# 5. Mergear solo después de review
.\dev-tools\scripts\sik-flow.ps1 merge -Mensaje "Merge nueva funcionalidad"

# 6. Release en hitos importantes
.\dev-tools\scripts\sik-flow.ps1 release -Version "1.1.0" -Mensaje "Nueva versión con X"
```

### **Gestión de Múltiples Tareas**

**REGLA FUNDAMENTAL**: Una rama = Una tarea. NO mezclar contextos.

```powershell
# ❌ INCORRECTO: Mezclar login + menú en misma rama
# ✅ CORRECTO: Separar en ramas diferentes

# Ejemplo: Trabajando en login pero necesitas arreglar menú urgente
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "WIP: login progress" -Push
.\dev-tools\scripts\sik-flow.ps1 switch -Rama main
.\dev-tools\scripts\sik-flow.ps1 new -Rama "bugfix/fix-menu" -Mensaje "Arreglar menú crítico"
# [Arreglar menú]
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "Fix menú crítico" -Push
.\dev-tools\scripts\sik-flow.ps1 pr -Mensaje "Fix: Corregir crash en menú"
.\dev-tools\scripts\sik-flow.ps1 merge -Mensaje "Fix menú crítico"
# [Volver a login]
.\dev-tools\scripts\sik-flow.ps1 switch -Rama "feature/login"
```

### **Manejo de Cambios Pendientes**

```powershell
# Si tienes cambios y quieres nueva tarea:
# OPCIÓN 1: Mover cambios a nueva rama
.\dev-tools\scripts\sik-flow.ps1 new -Rama "feature/nueva-tarea" -Mensaje "Nueva tarea" -TakeChanges

# OPCIÓN 2: Guardar cambios primero
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "WIP: progreso actual" -Push
.\dev-tools\scripts\sik-flow.ps1 switch -Rama main
.\dev-tools\scripts\sik-flow.ps1 new -Rama "feature/nueva-tarea" -Mensaje "Nueva tarea"
```

---

## **🎨 Convenciones de Nomenclatura**

### **Nombres de Ramas (SEGUIR ESTRICTAMENTE)**

```bash
feature/descripcion-clara     # Nuevas funcionalidades
bugfix/fix-descripcion       # Correcciones de bugs
hotfix/urgente-descripcion   # Correcciones urgentes
docs/actualizar-descripcion  # Cambios de documentación
refactor/optimizar-parte     # Refactorización
test/añadir-tests-parte      # Tests nuevos
chore/mantener-parte         # Mantenimiento
```

### **Mensajes de Commit (Conventional Commits)**

```bash
feat: añadir sistema de login
fix: corregir crash en menú principal
docs: actualizar README con nuevas instrucciones
refactor: optimizar renderizado de sprites
test: añadir tests unitarios para login
chore: actualizar dependencias
```

### **Versionado Semántico**

```bash
Major (X.0.0): Cambios incompatibles, reescrituras grandes
Minor (1.X.0): Nuevas funcionalidades compatibles
Patch (1.1.X): Correcciones de bugs, hotfixes
```

---

## **⚠️ Reglas Obligatorias para Agentes de IA**

### **🚫 NUNCA Hacer:**
- ❌ Commits directos a main
- ❌ Mezclar funcionalidades en una rama
- ❌ Omitir el flujo rama → PR → merge
- ❌ Crear ramas sin descripción clara
- ❌ Merge sin review (excepto hotfixes críticos)

### **✅ SIEMPRE Hacer:**
- ✅ Verificar estado con `status` antes de cualquier operación
- ✅ Crear rama nueva para cada bloque de trabajo diferente
- ✅ Usar `-TakeChanges` cuando cambies de contexto con cambios pendientes
- ✅ Commits frecuentes con mensajes descriptivos
- ✅ PRs con mensajes claros y vinculación a issues
- ✅ Merge solo después de confirmar que el PR es correcto

### **🔄 Flujo de Emergencia (Solo para Hotfixes)**

```powershell
# Solo para correcciones críticas urgentes
.\dev-tools\scripts\sik-flow.ps1 new -Rama "hotfix/critical-security" -Mensaje "Parche seguridad crítico"
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "fix: aplicar parche seguridad" -Push
.\dev-tools\scripts\sik-flow.ps1 pr -Mensaje "URGENT: Parche seguridad crítico"
# Review rápido
.\dev-tools\scripts\sik-flow.ps1 merge -Mensaje "Aplicar parche seguridad urgente"
.\dev-tools\scripts\sik-flow.ps1 release -Version "1.2.1" -Mensaje "URGENT: Parche seguridad"
```

---

## **🔧 Solución de Problemas Comunes**

### **Error: "No se reconoce el comando gh"**
```powershell
# Instalar GitHub CLI
winget install GitHub.cli
gh auth login
```

### **Error: "Execution Policy"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "Cambios sin commitear"**
```powershell
# Ver qué cambios hay
.\dev-tools\scripts\sik-flow.ps1 status
# Guardar cambios
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "Descripción de cambios" -Push
```

### **Error: Build falla**
```powershell
# El sistema continuará y creará release sin ejecutable
# Revisar configuración de Python/Node/.NET según proyecto
```

### **Error: "No hay PR abierto"**
```powershell
# Crear PR primero
.\dev-tools\scripts\sik-flow.ps1 pr -Mensaje "Descripción del PR"
# Luego mergear
.\dev-tools\scripts\sik-flow.ps1 merge -Mensaje "Merge descripción"
```

---

## **📊 Validación de Migración Exitosa**

### **Test del Flujo Completo**
```powershell
# 1. Estado inicial
.\dev-tools\scripts\sik-flow.ps1 status

# 2. Crear rama de prueba
.\dev-tools\scripts\sik-flow.ps1 new -Rama "test/migration-validation" -Mensaje "Validar migración del sistema"

# 3. Hacer cambio menor (ej: actualizar README)
echo "# Test de migración" >> MIGRATION_TEST.md

# 4. Guardar cambios
.\dev-tools\scripts\sik-flow.ps1 save -Mensaje "test: validar sistema de workflow" -Push

# 5. Crear PR
.\dev-tools\scripts\sik-flow.ps1 pr -Mensaje "Test: Validación de migración de workflow"

# 6. Mergear
.\dev-tools\scripts\sik-flow.ps1 merge -Mensaje "Merge test de validación"

# 7. Release de prueba
.\dev-tools\scripts\sik-flow.ps1 release -Version "0.1.1" -Mensaje "Test: Release de validación"

# ✅ Si todos los pasos funcionan = Migración exitosa
```

---

## **🎉 Beneficios del Sistema Migrado**

### **Para Desarrollo Individual:**
- ✅ Workflow predecible y sin errores
- ✅ Historial limpio y profesional
- ✅ Releases automáticos con ejecutables
- ✅ Gestión elegante de múltiples tareas

### **Para Equipos:**
- ✅ Estándar unificado de desarrollo
- ✅ Review obligatorio de todos los cambios
- ✅ Trazabilidad completa via issues
- ✅ Releases consistentes y profesionales

### **Para Agentes de IA:**
- ✅ Comandos simples y sin ambigüedad
- ✅ Validaciones automáticas que previenen errores
- ✅ Flujo obligatorio que garantiza calidad
- ✅ Capacidad de gestionar múltiples contextos sin conflictos

---

**El Sistema SiK Workflow transforma cualquier repositorio en un entorno de desarrollo profesional, seguro y eficiente. Una vez migrado, es imposible romper el flujo de calidad.**
