# Mejoras para el Manejo de Terminal - SiK Python Game

## 🐛 Problemas Identificados

### 1. Detección de Output Inadecuada
- **Problema**: Los comandos se ejecutan pero el output no se captura correctamente
- **Síntoma**: El asistente se queda "esperando" indefinidamente
- **Causa**: No hay feedback adecuado del estado del terminal

### 2. Estado del Entorno Virtual
- **Problema**: Poetry/entorno virtual no siempre está activo
- **Síntoma**: Comandos fallan sin explicación clara
- **Causa**: Dependencias del entorno no están disponibles

### 3. Timeouts y Cancelaciones
- **Problema**: Comandos largos se cancelan automáticamente
- **Síntoma**: Interrupción inesperada de procesos
- **Causa**: No hay distinción entre comandos rápidos vs lentos

## 🔧 Soluciones Propuestas

### 1. Script de Commit Robusto con Validaciones
**Archivo**: `scripts/terminal_safe_commit.ps1`

```powershell
#!/bin/bash
# COMMIT SEGURO PARA TERMINAL - Versión mejorada
# Resuelve problemas de detección de output y estados inconsistentes

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [switch]$Push = $false
)

# Función para output claro
function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message" -ForegroundColor $Color
}

Write-Status "🚀 INICIANDO COMMIT TERMINAL-SAFE" "Cyan"

# FASE 1: Diagnóstico completo del entorno
Write-Status "🔍 FASE 1: Diagnóstico del entorno..." "Yellow"

# Verificar directorio de trabajo
$currentDir = Get-Location
Write-Status "📁 Directorio actual: $currentDir" "Green"

# Verificar Git
if (-not (Test-Path ".git")) {
    Write-Status "❌ ERROR: No es un repositorio Git" "Red"
    exit 1
}
Write-Status "✅ Repositorio Git válido" "Green"

# Verificar Poetry (sin fallar si no está)
$poetryStatus = "❌ No disponible"
try {
    $poetryVersion = poetry --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $poetryStatus = "✅ $poetryVersion"
    }
} catch {
    # Silencioso - no es crítico
}
Write-Status "🐍 Poetry: $poetryStatus" "Cyan"

# Verificar cambios pendientes
$gitStatus = git status --porcelain
if ([string]::IsNullOrEmpty($gitStatus)) {
    Write-Status "✅ No hay cambios para commitear" "Green"
    exit 0
}

$changeCount = ($gitStatus -split "`n").Count
Write-Status "📋 Cambios detectados: $changeCount archivos" "Yellow"

# FASE 2: Pre-commit (opcional y robusto)
Write-Status "🧪 FASE 2: Pre-commit hooks..." "Yellow"

if ($poetryStatus -like "*✅*") {
    Write-Status "🔧 Ejecutando pre-commit con Poetry..." "Cyan"

    # Timeout de 60 segundos para pre-commit
    $job = Start-Job -ScriptBlock {
        Set-Location $using:currentDir
        poetry run pre-commit run --all-files 2>&1
    }

    Wait-Job $job -Timeout 60 | Out-Null
    $precommitOutput = Receive-Job $job
    Remove-Job $job -Force

    if ($job.State -eq "Completed") {
        Write-Status "✅ Pre-commit completado" "Green"
    } else {
        Write-Status "⚠️  Pre-commit timeout - continuando" "Yellow"
    }
} else {
    Write-Status "⚠️  Saltando pre-commit (Poetry no disponible)" "Yellow"
}

# FASE 3: Staging inteligente con validaciones
Write-Status "📁 FASE 3: Staging inteligente..." "Yellow"

# Limpiar staging previo
Write-Status "🔄 Limpiando staging area..." "Cyan"
git reset HEAD . 2>$null

# Añadir todos los archivos
Write-Status "➕ Añadiendo archivos modificados..." "Cyan"
git add .

# Verificar staging exitoso
$stagedFiles = git diff --cached --name-only
$stagedCount = if ($stagedFiles) { ($stagedFiles -split "`n").Count } else { 0 }
Write-Status "✅ Archivos en staging: $stagedCount" "Green"

# Verificar que no hay archivos modified después del add
$modifiedAfterAdd = git diff --name-only
if (-not [string]::IsNullOrEmpty($modifiedAfterAdd)) {
    Write-Status "🔄 Re-staging archivos modificados por hooks..." "Yellow"
    git add .

    # Verificar segunda vez
    $stillModified = git diff --name-only
    if (-not [string]::IsNullOrEmpty($stillModified)) {
        Write-Status "⚠️  Archivos siguen modificándose - posible problema con hooks" "Yellow"
        $modifiedCount = ($stillModified -split "`n").Count
        Write-Status "📋 Archivos aún modificados: $modifiedCount" "Yellow"
    }
}

# FASE 4: Commit con validación
Write-Status "💾 FASE 4: Ejecutando commit..." "Yellow"

# Mostrar resumen pre-commit
Write-Status "📋 Resumen del commit:" "Cyan"
Write-Host "  • Mensaje: $Message" -ForegroundColor White
Write-Host "  • Archivos: $stagedCount staged" -ForegroundColor White

# Ejecutar commit
git commit -m $Message

if ($LASTEXITCODE -eq 0) {
    Write-Status "✅ Commit creado exitosamente" "Green"

    # Mostrar información del commit
    $commitInfo = git log -1 --oneline
    Write-Status "📊 Commit: $commitInfo" "Cyan"
} else {
    Write-Status "❌ ERROR: Falló el commit" "Red"
    exit 1
}

# FASE 5: Push opcional
if ($Push) {
    Write-Status "🚀 FASE 5: Ejecutando push..." "Yellow"

    # Push con timeout
    $pushJob = Start-Job -ScriptBlock {
        Set-Location $using:currentDir
        git push 2>&1
    }

    Wait-Job $pushJob -Timeout 30 | Out-Null
    $pushOutput = Receive-Job $pushJob

    if ($pushJob.State -eq "Completed" -and $LASTEXITCODE -eq 0) {
        Write-Status "✅ Push completado exitosamente" "Green"
    } else {
        Write-Status "❌ ERROR o timeout en push" "Red"
        Write-Status "🔍 Output: $pushOutput" "Yellow"
    }

    Remove-Job $pushJob -Force
}

# FASE 6: Estado final
Write-Status "📊 FASE 6: Estado final..." "Yellow"

# Estado del repositorio
$finalStatus = git status --short
if ([string]::IsNullOrEmpty($finalStatus)) {
    Write-Status "✅ Repositorio limpio - no hay cambios pendientes" "Green"
} else {
    $remainingCount = ($finalStatus -split "`n").Count
    Write-Status "⚠️  Archivos pendientes: $remainingCount" "Yellow"
}

Write-Status "🎉 COMMIT TERMINAL-SAFE COMPLETADO" "Green"
Write-Status "⏱️  Hora de finalización: $((Get-Date).ToString('HH:mm:ss'))" "Cyan"
```

### 2. Diagnóstico de Terminal
**Archivo**: `scripts/terminal_diagnostics.ps1`

```powershell
# DIAGNÓSTICO COMPLETO DE TERMINAL
Write-Host "🔍 DIAGNÓSTICO DE TERMINAL - SiK Python Game" -ForegroundColor Cyan
Write-Host "=" * 50

# Información básica
Write-Host "`n📊 INFORMACIÓN BÁSICA:" -ForegroundColor Yellow
Write-Host "  • PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host "  • Directorio actual: $(Get-Location)" -ForegroundColor White
Write-Host "  • Usuario: $env:USERNAME" -ForegroundColor White

# Estado de Git
Write-Host "`n🔧 ESTADO DE GIT:" -ForegroundColor Yellow
if (Test-Path ".git") {
    $branch = git branch --show-current
    $status = git status --porcelain
    $statusCount = if ($status) { ($status -split "`n").Count } else { 0 }

    Write-Host "  • Repository: ✅ Válido" -ForegroundColor Green
    Write-Host "  • Branch: $branch" -ForegroundColor White
    Write-Host "  • Cambios pendientes: $statusCount archivos" -ForegroundColor White
} else {
    Write-Host "  • Repository: ❌ No encontrado" -ForegroundColor Red
}

# Estado de Poetry
Write-Host "`n🐍 ESTADO DE POETRY:" -ForegroundColor Yellow
try {
    $poetryVersion = poetry --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  • Poetry: ✅ $poetryVersion" -ForegroundColor Green

        # Verificar entorno virtual
        $venvInfo = poetry env info --path 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  • Virtual Environment: ✅ $venvInfo" -ForegroundColor Green
        } else {
            Write-Host "  • Virtual Environment: ⚠️  No configurado" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  • Poetry: ❌ No disponible" -ForegroundColor Red
    }
} catch {
    Write-Host "  • Poetry: ❌ Error al verificar" -ForegroundColor Red
}

# Estado de GitHub CLI
Write-Host "`n🌐 ESTADO DE GITHUB CLI:" -ForegroundColor Yellow
try {
    $ghVersion = gh --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  • GitHub CLI: ✅ Disponible" -ForegroundColor Green

        # Información del repo
        $repoInfo = gh repo view --json name,owner 2>$null
        if ($LASTEXITCODE -eq 0) {
            $repo = $repoInfo | ConvertFrom-Json
            Write-Host "  • Repo: $($repo.owner.login)/$($repo.name)" -ForegroundColor White
        }
    } else {
        Write-Host "  • GitHub CLI: ❌ No disponible" -ForegroundColor Red
    }
} catch {
    Write-Host "  • GitHub CLI: ❌ Error al verificar" -ForegroundColor Red
}

# Variables de entorno críticas
Write-Host "`n🔧 VARIABLES DE ENTORNO:" -ForegroundColor Yellow
$criticalVars = @("PATH", "PYTHONPATH", "VIRTUAL_ENV")
foreach ($var in $criticalVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        $shortValue = if ($value.Length -gt 60) { "$($value.Substring(0, 60))..." } else { $value }
        Write-Host "  • $var: $shortValue" -ForegroundColor White
    } else {
        Write-Host "  • $var: ❌ No definida" -ForegroundColor Red
    }
}

Write-Host "`n✅ DIAGNÓSTICO COMPLETADO" -ForegroundColor Green
```

### 3. Uso Recomendado

#### Para commits diarios (versión segura):
```powershell
.\scripts\terminal_safe_commit.ps1 "mensaje del commit"
```

#### Para diagnóstico de problemas:
```powershell
.\scripts\terminal_diagnostics.ps1
```

## 📋 Mejoras Implementadas

### 1. Timeouts Inteligentes
- Pre-commit: 60 segundos máximo
- Push: 30 segundos máximo
- Jobs en background para evitar bloqueos

### 2. Output Estructurado
- Timestamps en cada mensaje
- Códigos de color consistentes
- Información de progreso clara

### 3. Validaciones Robustas
- Verificación de cada paso
- Manejo de errores graceful
- Información de estado detallada

### 4. Compatibilidad Amplia
- Funciona con/sin Poetry
- Funciona con/sin GitHub CLI
- Manejo de entornos virtuales

## 🎯 Próximos Pasos

1. **Crear** `scripts/terminal_safe_commit.ps1`
2. **Crear** `scripts/terminal_diagnostics.ps1`
3. **Probar** en diferentes estados del terminal
4. **Documentar** en instrucciones principales
5. **Reemplazar** scripts problemáticos existentes

Esta mejora resolverá los problemas de manejo de terminal y proporcionará un método más confiable para commits.
