# SiK Auto Workflow - Version Corregida
# =====================================

param(
    [string]$Descripcion = "",
    [switch]$Forzar
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
    Write-Host "  Auto Workflow System" -ForegroundColor Green
    Write-Host ""
}

function Get-GitInfo {
    return @{
        Rama = (git branch --show-current)
        Cambios = @(git status --porcelain)
        EsMain = (git branch --show-current) -eq "main"
        TieneCommitsPendientes = (@(git status --porcelain)).Count -gt 0
    }
}

function Get-ChangeTypeSimple {
    param([array]$Files, [string]$Desc)
    
    $devFiles = $Files | Where-Object { $_ -match "dev-tools|\.github" }
    $srcFiles = $Files | Where-Object { $_ -match "^src/" }
    
    if ($devFiles.Count -gt 0 -and $srcFiles.Count -eq 0) {
        return @{
            Tipo = "dev-tools"
            RequiereNuevaRama = $false
            Razon = "Solo herramientas de desarrollo modificadas"
        }
    }
    
    return @{
        Tipo = "feature" 
        RequiereNuevaRama = $true
        Razon = "Cambios en codigo fuente"
    }
}

# Ejecutar
Write-SiKBanner

# Obtener estado
$git = Get-GitInfo
Write-Host "Estado: Rama=$($git.Rama), Cambios=$($git.Cambios.Count), EsMain=$($git.EsMain)" -ForegroundColor Green

if (-not $git.TieneCommitsPendientes) {
    Write-Host "No hay cambios pendientes." -ForegroundColor Yellow
    exit 0
}

# Si no hay descripcion, pedirla
if (-not $Descripcion) {
    $Descripcion = Read-Host "Descripcion de los cambios"
}

# Analizar cambios
$changedFiles = $git.Cambios | ForEach-Object { $_.Substring(3) }
$changeType = Get-ChangeTypeSimple $changedFiles $Descripcion

Write-Host ""
Write-Host "DECISION: $($changeType.Tipo) - $($changeType.Razon)" -ForegroundColor Cyan

# Decidir acción
if ($git.EsMain -and $git.TieneCommitsPendientes) {
    if ($changeType.RequiereNuevaRama) {
        Write-Host "ACCION: Crear nueva rama" -ForegroundColor Yellow
        # Aquí iría la lógica de crear rama
    } else {
        Write-Host "ACCION: Commit directo en main" -ForegroundColor Yellow
        
        if (-not $Forzar) {
            $confirm = Read-Host "Hacer commit directo en main? (s/N)"
            if ($confirm -ne "s" -and $confirm -ne "S") {
                Write-Host "Operacion cancelada." -ForegroundColor Yellow
                exit 0
            }
        }
        
        # Hacer commit directo
        Write-Host "Ejecutando commit..." -ForegroundColor Green
        git add .
        git commit -m "[$($changeType.Tipo)] $Descripcion"
        git push origin main
        Write-Host "Commit realizado exitosamente." -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "WORKFLOW COMPLETADO" -ForegroundColor Green
