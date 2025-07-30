# Ultra Fast Commit - Optimizado para iteraciones rapidas (5-10s)
# Sin cache cleaning, hooks minimos, ejecucion unica garantizada

param(
    [string]$Message = "",
    [switch]$Force = $false
)

# Configuracion rapida
$ErrorActionPreference = "Continue"
$startTime = Get-Date

Write-Host "Ultra Fast Commit - Iniciando..." -ForegroundColor Cyan

# 1. STAGE RAPIDO (sin verificaciones extensas)
Write-Host "Staging changes..." -ForegroundColor Yellow
git add . 2>$null

# 2. VERIFICAR SI HAY CAMBIOS
$status = git status --porcelain 2>$null
if (-not $status) {
    Write-Host "No hay cambios para commit" -ForegroundColor Green
    exit 0
}

# 3. MENSAJE AUTOMATICO SI NO SE PROPORCIONA
if (-not $Message) {
    $files = (git diff --cached --name-only | Measure-Object).Count
    $Message = "chore(cleanup): optimizacion archivos .github y scripts ($files archivos)"
}

# 4. COMMIT DIRECTO (sin pre-commit extensivo en modo rapido)
Write-Host "Committing: $Message" -ForegroundColor Green
if ($Force) {
    # Bypass hooks para velocidad maxima
    git commit -m "$Message" --no-verify 2>$null
} else {
    # Hooks minimos (solo criticos)
    $env:SKIP = "check-yaml,check-json,check-toml" # Solo formateo critico
    git commit -m "$Message" 2>$null
}

if ($LASTEXITCODE -eq 0) {
    $elapsed = ((Get-Date) - $startTime).TotalSeconds
    Write-Host "Commit exitoso en $([math]::Round($elapsed, 1))s" -ForegroundColor Green

    # Mostrar estado post-commit
    $remainingChanges = git status --porcelain 2>$null
    if ($remainingChanges) {
        Write-Host "Cambios restantes detectados - hooks aplicaron fixes" -ForegroundColor Yellow
        Write-Host "Ejecutar nuevamente para commitear fixes automaticos" -ForegroundColor Cyan
    } else {
        Write-Host "Repositorio limpio - commit completo" -ForegroundColor Green
    }
} else {
    Write-Host "Error en commit" -ForegroundColor Red
    git status --short
    exit 1
}

# 5. PUSH OPCIONAL (solo si esta limpio)
$remainingChanges = git status --porcelain 2>$null
if (-not $remainingChanges) {
    Write-Host "Pushing to remote..." -ForegroundColor Cyan
    git push origin HEAD 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push exitoso" -ForegroundColor Green
    } else {
        Write-Host "Push fallo (no critico)" -ForegroundColor Yellow
    }
}

$totalTime = ((Get-Date) - $startTime).TotalSeconds
Write-Host "Tiempo total: $([math]::Round($totalTime, 1))s" -ForegroundColor Magenta
