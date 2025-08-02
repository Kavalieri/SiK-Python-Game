# SiK Release Integration System
# =============================
# Autor: SiK Team
# Descripcion: Integra el build automatico con el sistema de releases de GitHub

param(
    [string]$Version = "",
    [switch]$UploadToRelease,
    [switch]$CreateDraftRelease
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

function Write-ReleaseHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Magenta
    Write-Host " SiK RELEASE SYSTEM: $Title" -ForegroundColor Yellow
    Write-Host "====================================================" -ForegroundColor Magenta
}

function Invoke-ProfessionalBuild {
    param([string]$Version)
    
    Write-ReleaseHeader "EJECUTANDO BUILD PROFESIONAL"
    
    $buildScript = Join-Path $ProjectRoot "dev-tools\scripts\build_professional.ps1"
    
    try {
        & $buildScript -Version $Version -Release -Clean
        
        # Verificar que el build fue exitoso
        $expectedZip = "dist\SiK-Python-Game-$Version-windows.zip"
        if (Test-Path $expectedZip) {
            Write-Host "Build profesional completado: $expectedZip" -ForegroundColor Green
            return $expectedZip
        } else {
            Write-Error "Build fallido: archivo esperado no encontrado"
            return $null
        }
    } catch {
        Write-Error "Error durante el build: $($_.Exception.Message)"
        return $null
    }
}

function Get-ReleaseAssets {
    param([string]$Version)
    
    $assets = @()
    
    # Buscar el ZIP del build
    $buildZip = "dist\SiK-Python-Game-$Version-windows.zip"
    if (Test-Path $buildZip) {
        $assets += @{
            Path = $buildZip
            Name = "SiK-Python-Game-v$Version-Windows-x64.zip"
            Description = "Ejecutable para Windows (64-bit)"
        }
    }
    
    # Buscar codigo fuente (automatico en GitHub)
    # Agregar changelog si existe
    $changelogPath = "docs\changelogs\$Version.md"
    if (Test-Path $changelogPath) {
        $assets += @{
            Path = $changelogPath
            Name = "CHANGELOG-v$Version.md"
            Description = "Notas de la version $Version"
        }
    }
    
    return $assets
}

function Update-WorkflowForBuilds {
    Write-ReleaseHeader "ACTUALIZANDO WORKFLOW AUTOMATION"
    
    # Leer el workflow actual
    $workflowPath = Join-Path $ProjectRoot "dev-tools\scripts\workflow_automation.ps1"
    $workflowContent = Get-Content $workflowPath -Raw
    
    # Verificar si ya tiene integracion de build
    if ($workflowContent -match "build_professional\.ps1") {
        Write-Host "Workflow ya tiene integracion de build" -ForegroundColor Green
        return
    }
    
    Write-Host "Integrando build profesional en workflow..." -ForegroundColor Yellow
    
    # Buscar la funcion New-Release y agregar build
    $buildIntegration = @'

    # Ejecutar build profesional antes de crear release
    Write-Info "Ejecutando build profesional..."
    try {
        $buildScript = Join-Path $ProjectRoot "dev-tools\scripts\build_release.ps1"
        & $buildScript -Version $NewVersion -UploadToRelease
        Write-Success "Build profesional completado"
    } catch {
        Write-Info "Error en build profesional: $($_.Exception.Message)"
        Write-Info "Continuando con release sin ejecutable..."
    }

'@
    
    # Insertar integracion de build en el workflow
    # (Esto requeriria modificacion manual del workflow_automation.ps1)
    
    Write-Host "NOTA: Integrar manualmente en workflow_automation.ps1" -ForegroundColor Yellow
    Write-Host "Agregar llamada a build_professional.ps1 en funcion New-Release" -ForegroundColor Yellow
}

function Show-ReleaseInstructions {
    param([string]$Version, [array]$Assets)
    
    Write-ReleaseHeader "INSTRUCCIONES DE RELEASE"
    
    Write-Host "Version: $Version" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Assets generados:" -ForegroundColor Cyan
    foreach ($asset in $Assets) {
        if (Test-Path $asset.Path) {
            $size = (Get-Item $asset.Path).Length / 1MB
            Write-Host "  ✓ $($asset.Name) ($([math]::Round($size, 2)) MB)" -ForegroundColor Green
            Write-Host "    Descripcion: $($asset.Description)" -ForegroundColor Gray
            Write-Host "    Archivo: $($asset.Path)" -ForegroundColor Gray
        } else {
            Write-Host "  ✗ $($asset.Name) (NO ENCONTRADO)" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "Para crear release manualmente:" -ForegroundColor Yellow
    Write-Host "1. Ir a: https://github.com/Kavalieri/SiK-Python-Game/releases/new" -ForegroundColor Cyan
    Write-Host "2. Tag: v$Version" -ForegroundColor Cyan
    Write-Host "3. Titulo: SiK Python Game v$Version" -ForegroundColor Cyan
    Write-Host "4. Subir assets encontrados arriba" -ForegroundColor Cyan
    Write-Host "5. Usar changelog como descripcion" -ForegroundColor Cyan
    
    Write-Host ""
    Write-Host "Para integracion automatica:" -ForegroundColor Yellow
    Write-Host "  .\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release" -ForegroundColor Cyan
}

# EJECUCION PRINCIPAL
# ==================

Write-ReleaseHeader "SISTEMA DE RELEASE PROFESIONAL"

# Obtener version
if (-not $Version) {
    $versionFile = Join-Path $ProjectRoot "VERSION.txt"
    if (Test-Path $versionFile) {
        $Version = (Get-Content $versionFile).Trim()
    } else {
        $Version = "0.1.0"
    }
}

Write-Host "Preparando release para version: $Version" -ForegroundColor Cyan

# Ejecutar build profesional
$buildResult = Invoke-ProfessionalBuild $Version
if (-not $buildResult) {
    Write-Error "No se pudo completar el build profesional"
    exit 1
}

# Obtener assets de release
$assets = Get-ReleaseAssets $Version

# Actualizar workflow (preparacion)
Update-WorkflowForBuilds

# Mostrar instrucciones
Show-ReleaseInstructions $Version $assets

Write-Host ""
Write-Host "SISTEMA DE RELEASE PROFESIONAL PREPARADO" -ForegroundColor Green
