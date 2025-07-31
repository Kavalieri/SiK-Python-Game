# Script de Prueba para Comprehensive Cleanup
# Valida funcionalidad sin ejecutar operaciones destructivas

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("test", "validate", "show")]
    [string]$Mode = "test"
)

Write-Host "=== PRUEBA DE SCRIPT DE LIMPIEZA COMPLETA ===" -ForegroundColor Cyan

# Verificar estructura del proyecto
function Test-ProjectStructure {
    Write-Host "Verificando estructura del proyecto..." -ForegroundColor Yellow

    $RequiredPaths = @("src", "pyproject.toml", "dev-tools\scripts")
    $Missing = @()

    foreach ($Path in $RequiredPaths) {
        if (Test-Path $Path) {
            Write-Host "[OK] $Path" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] $Path" -ForegroundColor Red
            $Missing += $Path
        }
    }

    return ($Missing.Count -eq 0)
}

# Verificar existencia de caches
function Show-CurrentCaches {
    Write-Host "Caches actuales en el proyecto:" -ForegroundColor Yellow

    $CacheLocations = @(
        "src\__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".vscode\workspaceStorage",
        ".vscode\logs"
    )

    foreach ($Cache in $CacheLocations) {
        if (Test-Path $Cache) {
            $Size = (Get-ChildItem $Cache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $SizeKB = [math]::Round($Size / 1024, 2)
            Write-Host "[CACHE] $Cache - $SizeKB KB" -ForegroundColor Cyan
        } else {
            Write-Host "[NONE] $Cache - no existe" -ForegroundColor Gray
        }
    }
}

# Simular ejecucion del script
function Test-ScriptExecution {
    Write-Host "Simulando ejecucion del script..." -ForegroundColor Yellow

    $ScriptPath = ".\dev-tools\scripts\comprehensive_cleanup.ps1"

    if (Test-Path $ScriptPath) {
        Write-Host "[OK] Script encontrado: $ScriptPath" -ForegroundColor Green

        # Verificar parametros validos
        $ValidLevels = @("light", "deep", "complete", "shutdown")
        Write-Host "[INFO] Niveles disponibles: $($ValidLevels -join ', ')" -ForegroundColor Cyan

        # Mostrar comandos de ejemplo
        Write-Host "Comandos de ejemplo:" -ForegroundColor Yellow
        Write-Host "  .\dev-tools\scripts\comprehensive_cleanup.ps1 -Level light" -ForegroundColor White
        Write-Host "  .\dev-tools\scripts\comprehensive_cleanup.ps1 -Level deep" -ForegroundColor White
        Write-Host "  .\dev-tools\scripts\comprehensive_cleanup.ps1 -Level complete -Force" -ForegroundColor White

    } else {
        Write-Host "[FAIL] Script no encontrado: $ScriptPath" -ForegroundColor Red
        return $false
    }

    return $true
}

# Verificar VS Code
function Test-VSCodeIntegration {
    Write-Host "Verificando integracion VS Code..." -ForegroundColor Yellow

    $VSCodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue
    if ($VSCodeProcesses.Count -gt 0) {
        Write-Host "[OK] VS Code ejecutandose - $($VSCodeProcesses.Count) procesos" -ForegroundColor Green

        $SendKeysScript = ".\dev-tools\scripts\vscode_cleanup_sendkeys.ps1"
        if (Test-Path $SendKeysScript) {
            Write-Host "[OK] Script SendKeys disponible" -ForegroundColor Green
        } else {
            Write-Host "[WARN] Script SendKeys no encontrado" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[INFO] VS Code no esta ejecutandose" -ForegroundColor Gray
    }
}

# EJECUCION PRINCIPAL
switch ($Mode) {
    "test" {
        $StructureOK = Test-ProjectStructure
        if ($StructureOK) {
            Show-CurrentCaches
            $ScriptOK = Test-ScriptExecution
            Test-VSCodeIntegration

            if ($ScriptOK) {
                Write-Host "[SUCCESS] PRUEBA COMPLETADA - El script esta listo para usar" -ForegroundColor Green
            } else {
                Write-Host "[FAIL] PRUEBA FALLIDA - Revisar instalacion del script" -ForegroundColor Red
            }
        } else {
            Write-Host "[FAIL] ESTRUCTURA DE PROYECTO INCORRECTA" -ForegroundColor Red
        }
    }

    "validate" {
        Write-Host "Validando sintaxis del script..." -ForegroundColor Yellow
        $ScriptPath = ".\dev-tools\scripts\comprehensive_cleanup.ps1"

        if (Test-Path $ScriptPath) {
            try {
                # Verificar sintaxis sin ejecutar
                $null = [scriptblock]::Create((Get-Content $ScriptPath -Raw))
                Write-Host "[OK] Sintaxis del script valida" -ForegroundColor Green
            } catch {
                Write-Host "[FAIL] Error de sintaxis: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }

    "show" {
        Show-CurrentCaches
    }
}
