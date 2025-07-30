#!/bin/bash

# Script para workflow profesional de commits
# Uso: ./scripts/commit_profesional.ps1 "mensaje del commit"
#
# Implementa estrategia híbrida GitHub CLI + Git tradicional
# Ver matriz de decisión: docs/MATRIZ_DECISIÓN_GH_VS_GIT.md
# - Git: para staging y commits (operaciones locales)
# - GitHub CLI: para información del repo y estado

param(
    [Parameter(Mandatory=$true)]
    [string]$Mensaje,

    [Parameter(Mandatory=$false)]
    [string]$Tipo = "feat",

    [Parameter(Mandatory=$false)]
    [string]$Ambito = "",

    [Parameter(Mandatory=$false)]
    [switch]$Push = $false,

    [Parameter(Mandatory=$false)]
    [switch]$Force = $false
)

Write-Host "🔄 Iniciando workflow profesional de commit..." -ForegroundColor Cyan

# 1. Verificar que estamos en un repositorio Git
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: No estás en un repositorio Git" -ForegroundColor Red
    exit 1
}

# 2. Verificar estado del repositorio
Write-Host "📊 Verificando estado del repositorio..." -ForegroundColor Yellow
$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Host "✅ No hay cambios para commitear" -ForegroundColor Green
    exit 0
}

# 3. Ejecutar pre-commit hooks
Write-Host "🧪 Ejecutando validaciones pre-commit..." -ForegroundColor Yellow
try {
    poetry run pre-commit run --all-files
    if ($LASTEXITCODE -ne 0) {
        if (-not $Force) {
            Write-Host "❌ Pre-commit hooks fallaron. Usa -Force para ignorar" -ForegroundColor Red
            exit 1
        } else {
            Write-Host "⚠️  Pre-commit hooks fallaron pero continuando con -Force" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "⚠️  Pre-commit no disponible, continuando..." -ForegroundColor Yellow
}

# 4. Construir mensaje de commit
$mensajeCompleto = if ($Ambito) {
    "$Tipo($Ambito): $Mensaje"
} else {
    "$Tipo: $Mensaje"
}

# 5. Mostrar archivos que se van a añadir
Write-Host "📁 Archivos a incluir en el commit:" -ForegroundColor Cyan
git status --short

# 6. Confirmar con el usuario
if (-not $Force) {
    $confirmar = Read-Host "¿Continuar con el commit? (y/N)"
    if ($confirmar -ne "y" -and $confirmar -ne "Y") {
        Write-Host "❌ Commit cancelado por el usuario" -ForegroundColor Red
        exit 0
    }
}

# 7. Añadir archivos y hacer commit
Write-Host "📝 Creando commit..." -ForegroundColor Green
git add .
git commit -m $mensajeCompleto

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al crear el commit" -ForegroundColor Red
    exit 1
}

# 8. Push opcional con GitHub CLI
if ($Push) {
    Write-Host "🚀 Verificando estado del repositorio..." -ForegroundColor Green

    # Usar GitHub CLI para obtener información del repo
    $repoInfo = gh repo view --json name,owner,defaultBranch 2>$null
    if ($LASTEXITCODE -eq 0) {
        $repo = $repoInfo | ConvertFrom-Json
        $branch = $repo.defaultBranch
        Write-Host "📊 Repositorio: $($repo.owner.login)/$($repo.name)" -ForegroundColor Cyan
        Write-Host "🌿 Branch principal: $branch" -ForegroundColor Cyan

        # Push usando git tradicional (local a remoto)
        Write-Host "📤 Haciendo push a $branch..." -ForegroundColor Green
        git push origin $branch
    } else {
        # Fallback a git tradicional
        Write-Host "📤 Haciendo push al repositorio remoto..." -ForegroundColor Green
        git push origin main
    }

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al hacer push" -ForegroundColor Red
        exit 1
    }

    Write-Host "✅ Push completado exitosamente" -ForegroundColor Green

    # Mostrar estado con GitHub CLI si está disponible
    Write-Host "`n📊 Estado del repositorio:" -ForegroundColor Cyan
    gh status 2>$null
    if ($LASTEXITCODE -ne 0) {
        git status --short
    }
}

Write-Host "✅ Commit creado exitosamente: $mensajeCompleto" -ForegroundColor Green

# 9. Mostrar información del último commit
Write-Host "`n📊 Información del commit:" -ForegroundColor Cyan
git log -1 --oneline
git log -1 --stat
