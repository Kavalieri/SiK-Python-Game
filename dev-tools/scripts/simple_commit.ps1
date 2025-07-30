# =============================================================================
# SCRIPT SIMPLIFICADO DE COMMIT - SOLUCION DIRECTA
# =============================================================================
# Resuelve problemas de pre-commit hooks
# Uso: .\scripts\simple_commit.ps1 "mensaje"
# =============================================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [switch]$Push = $false
)

Write-Host "🚀 COMMIT SIMPLIFICADO - Resolviendo problemas de staging" -ForegroundColor Cyan

# Validar repositorio
if (-not (Test-Path ".git")) {
    Write-Host "❌ ERROR: No es un repositorio Git" -ForegroundColor Red
    exit 1
}

# Verificar cambios
$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Host "✅ No hay cambios para commitear" -ForegroundColor Green
    exit 0
}

Write-Host "🔧 PASO 1: Ejecutando pre-commit hooks..." -ForegroundColor Yellow
try {
    poetry run pre-commit run --all-files
} catch {
    Write-Host "⚠️  Pre-commit no disponible, continuando..." -ForegroundColor Yellow
}

Write-Host "📁 PASO 2: Limpiando y re-staging archivos..." -ForegroundColor Yellow
git reset HEAD . 2>$null
git add .

# Verificar que no hay archivos modified después del add
$diffWorking = git diff --name-only
if (-not [string]::IsNullOrEmpty($diffWorking)) {
    Write-Host "🔄 Re-staging archivos modificados por hooks..." -ForegroundColor Yellow
    git add .
}

Write-Host "💾 PASO 3: Creando commit..." -ForegroundColor Green
git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Falló el commit" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Commit creado exitosamente" -ForegroundColor Green

if ($Push) {
    Write-Host "🚀 PASO 4: Haciendo push..." -ForegroundColor Green
    git push

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Push completado" -ForegroundColor Green
    } else {
        Write-Host "❌ ERROR: Falló el push" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🎉 ¡PROCESO COMPLETADO!" -ForegroundColor Green
git log -1 --oneline
