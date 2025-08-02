# SiK Development Command - Punto de Entrada Unico
# =================================================
# Autor: SiK Team
# Descripcion: Comando simple que evalua contexto y ejecuta workflow automatico

param(
    [string]$Mensaje = "",
    [switch]$Status,
    [switch]$Forzar,
    [switch]$Debug
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

function Write-SiKBanner {
    Write-Host ""
    Write-Host "  ███████ ██ ██   ██" -ForegroundColor Magenta
    Write-Host "  ██      ██ ██  ██ " -ForegroundColor Magenta  
    Write-Host "  ███████ ██ █████  " -ForegroundColor Cyan
    Write-Host "       ██ ██ ██  ██ " -ForegroundColor Cyan
    Write-Host "  ███████ ██ ██   ██" -ForegroundColor Blue
    Write-Host ""
    Write-Host "  Python Game Development" -ForegroundColor Yellow
    Write-Host "  Auto Workflow System" -ForegroundColor Green
    Write-Host ""
}

# Mostrar estado si se solicita
if ($Status) {
    Write-SiKBanner
    Write-Host "ESTADO DEL REPOSITORIO:" -ForegroundColor Cyan
    Write-Host ""
    
    $currentBranch = git branch --show-current
    $changes = @(git status --porcelain)
    $isMain = $currentBranch -eq "main"
    
    Write-Host "  Rama actual: $currentBranch" -ForegroundColor Green
    Write-Host "  Archivos modificados: $($changes.Count)" -ForegroundColor Green
    Write-Host "  Es rama main: $isMain" -ForegroundColor Green
    
    if ($changes.Count -gt 0) {
        Write-Host ""
        Write-Host "  Archivos pendientes:" -ForegroundColor Yellow
        $changes | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    }
    
    Write-Host ""
    Write-Host "Para procesar cambios, ejecuta:" -ForegroundColor Cyan
    Write-Host "  .\dev-tools\scripts\sik.ps1" -ForegroundColor Yellow
    Write-Host ""
    exit 0
}

# Ejecutar workflow automatico
Write-SiKBanner

$autoScript = Join-Path $ProjectRoot "dev-tools/scripts/auto_workflow.ps1"
$params = @()

if ($Mensaje) { $params += "-Descripcion"; $params += $Mensaje }
if ($Forzar) { $params += "-Forzar" }
if ($Debug) { $params += "-Debug" }

& $autoScript @params
