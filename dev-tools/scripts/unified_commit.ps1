#!/bin/bash

# =============================================================================
# SCRIPT UNIFICADO DE COMMIT - SOLUCIÓN DEFINITIVA
# =============================================================================
# Resuelve problemas de pre-commit hooks modificando archivos post-staging
# Uso: .\scripts\unified_commit.ps1 "mensaje" [-Push] [-Type "feat"] [-Scope "assets"]
#
# FLUJO OPTIMIZADO:
# 1. Pre-commit ANTES del staging (evita modificaciones post-add)
# 2. Re-staging automático si hay cambios
# 3. Commit con validación completa
# 4. Push opcional con GitHub CLI + Git
# =============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,

    [Parameter(Mandatory=$false)]
    [string]$Type = "feat",

    [Parameter(Mandatory=$false)]
    [string]$Scope = "",

    [Parameter(Mandatory=$false)]
    [switch]$Push = $false,

    [Parameter(Mandatory=$false)]
    [switch]$Force = $false,

    [Parameter(Mandatory=$false)]
    [switch]$SkipHooks = $false
)

# Colores para output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Cyan = "Cyan"
$Blue = "Blue"

Write-Host "🚀 UNIFIED COMMIT - Flujo optimizado de commits" -ForegroundColor $Cyan
Write-Host "=================================================" -ForegroundColor $Cyan

# =============================================================================
# FASE 1: VALIDACIONES INICIALES
# =============================================================================

Write-Host "`n🔍 FASE 1: Validaciones iniciales..." -ForegroundColor $Blue

# Verificar repositorio Git
if (-not (Test-Path ".git")) {
    Write-Host "❌ ERROR: No estás en un repositorio Git" -ForegroundColor $Red
    exit 1
}

# Verificar Poetry (para pre-commit)
try {
    poetry --version | Out-Null
    $poetryAvailable = $true
} catch {
    Write-Host "⚠️  WARNING: Poetry no disponible, saltando pre-commit" -ForegroundColor $Yellow
    $poetryAvailable = $false
}

# Verificar GitHub CLI (para información del repo)
try {
    gh --version | Out-Null
    $ghAvailable = $true
} catch {
    Write-Host "⚠️  WARNING: GitHub CLI no disponible, usando git tradicional" -ForegroundColor $Yellow
    $ghAvailable = $false
}

# Verificar cambios pendientes
$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Host "✅ No hay cambios para commitear" -ForegroundColor $Green
    exit 0
}

Write-Host "✅ Validaciones iniciales completadas" -ForegroundColor $Green

# =============================================================================
# FASE 2: PRE-COMMIT HOOKS (ANTES DEL STAGING)
# =============================================================================

Write-Host "`n🧪 FASE 2: Ejecutando pre-commit hooks..." -ForegroundColor $Blue

if ($poetryAvailable -and -not $SkipHooks) {
    Write-Host "🔧 Ejecutando ruff format y linting..." -ForegroundColor $Yellow

    # Ejecutar pre-commit en todos los archivos
    poetry run pre-commit run --all-files | Out-Null
    $preCommitExitCode = $LASTEXITCODE

    if ($preCommitExitCode -ne 0) {
        Write-Host "🔄 Pre-commit modificó archivos, verificando cambios..." -ForegroundColor $Yellow

        # Verificar si hay cambios después de pre-commit
        $statusAfterPreCommit = git status --porcelain
        if (-not [string]::IsNullOrEmpty($statusAfterPreCommit)) {
            Write-Host "✅ Archivos formateados y listos para staging" -ForegroundColor $Green
        }

        if (-not $Force) {
            Write-Host "⚠️  Pre-commit hizo cambios. ¿Continuar? (Y/n):" -ForegroundColor $Yellow
            $confirm = Read-Host
            if ($confirm -eq "n" -or $confirm -eq "N") {
                Write-Host "❌ Commit cancelado por el usuario" -ForegroundColor $Red
                exit 0
            }
        }
    } else {
        Write-Host "✅ Pre-commit hooks pasaron sin modificaciones" -ForegroundColor $Green
    }
} else {
    Write-Host "⚠️  Saltando pre-commit hooks" -ForegroundColor $Yellow
}

# =============================================================================
# FASE 3: STAGING INTELIGENTE
# =============================================================================

Write-Host "`n📁 FASE 3: Staging inteligente..." -ForegroundColor $Blue

# Mostrar archivos que se van a añadir
Write-Host "📋 Archivos modificados:" -ForegroundColor $Cyan
git status --short

# Limpiar staging area y añadir todo
Write-Host "🔄 Limpiando staging area..." -ForegroundColor $Yellow
git reset HEAD . 2>$null

Write-Host "➕ Añadiendo todos los archivos..." -ForegroundColor $Yellow
git add .

# Verificar que no hay diferencias entre staged y working
$diffWorking = git diff --name-only

if (-not [string]::IsNullOrEmpty($diffWorking)) {
    Write-Host "⚠️  Detectados archivos modified después del add:" -ForegroundColor $Yellow
    git status --short

    Write-Host "🔄 Re-staging archivos modificados..." -ForegroundColor $Yellow
    git add .

    # Verificar de nuevo
    $diffWorkingAfter = git diff --name-only
    if (-not [string]::IsNullOrEmpty($diffWorkingAfter)) {
        Write-Host "❌ ERROR: Archivos siguen modificándose. Verifique hooks." -ForegroundColor $Red
        exit 1
    }
}

Write-Host "✅ Staging completado correctamente" -ForegroundColor $Green

# =============================================================================
# FASE 4: CONSTRUCCIÓN DEL MENSAJE
# =============================================================================

Write-Host "`n📝 FASE 4: Preparando commit..." -ForegroundColor $Blue

# Construir mensaje conventional commit
$fullMessage = if ($Scope) {
    "${Type}(${Scope}): ${Message}"
} else {
    "${Type}: ${Message}"
}

Write-Host "📋 Mensaje del commit: $fullMessage" -ForegroundColor $Cyan

# Confirmación final
if (-not $Force) {
    Write-Host "🔍 Archivos en staging:" -ForegroundColor $Cyan
    git diff --cached --name-status

    Write-Host "`n❓ ¿Proceder con el commit? (Y/n):" -ForegroundColor $Yellow
    $finalConfirm = Read-Host
    if ($finalConfirm -eq "n" -or $finalConfirm -eq "N") {
        Write-Host "❌ Commit cancelado por el usuario" -ForegroundColor $Red
        exit 0
    }
}

# =============================================================================
# FASE 5: COMMIT
# =============================================================================

Write-Host "`n💾 FASE 5: Ejecutando commit..." -ForegroundColor $Blue

git commit -m $fullMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Falló el commit" -ForegroundColor $Red
    exit 1
}

Write-Host "✅ Commit creado exitosamente" -ForegroundColor $Green

# =============================================================================
# FASE 6: PUSH OPCIONAL
# =============================================================================

if ($Push) {
    Write-Host "`n🚀 FASE 6: Ejecutando push..." -ForegroundColor $Blue

    if ($ghAvailable) {
        # Usar GitHub CLI para información, git para push
        Write-Host "📊 Obteniendo información del repositorio..." -ForegroundColor $Yellow
        $repoInfo = gh repo view --json name,owner,defaultBranch 2>$null

        if ($LASTEXITCODE -eq 0) {
            $repo = $repoInfo | ConvertFrom-Json
            $branch = git branch --show-current
            Write-Host "📊 Repo: $($repo.owner.login)/$($repo.name) | Branch: $branch" -ForegroundColor $Cyan

            git push origin $branch
        } else {
            Write-Host "⚠️  Fallback a git tradicional" -ForegroundColor $Yellow
            git push
        }
    } else {
        git push
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Falló el push" -ForegroundColor $Red
        exit 1
    }

    Write-Host "✅ Push completado exitosamente" -ForegroundColor $Green
}

# =============================================================================
# FASE 7: RESUMEN FINAL
# =============================================================================

Write-Host "`n📊 RESUMEN FINAL" -ForegroundColor $Blue
Write-Host "=================" -ForegroundColor $Blue

Write-Host "✅ Commit: $fullMessage" -ForegroundColor $Green

# Mostrar información del commit
Write-Host "`n📋 Información del commit:" -ForegroundColor $Cyan
git log -1 --oneline --stat

# Estado final del repositorio
Write-Host "`n📊 Estado del repositorio:" -ForegroundColor $Cyan
git status --short

if ($ghAvailable) {
    Write-Host "`n🌐 Estado remoto:" -ForegroundColor $Cyan
    gh status 2>$null
}

Write-Host "`n🎉 ¡UNIFIED COMMIT COMPLETADO EXITOSAMENTE!" -ForegroundColor $Green
