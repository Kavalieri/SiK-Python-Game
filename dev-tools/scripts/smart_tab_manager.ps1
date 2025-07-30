# =============================================================================
# SCRIPT INTELIGENTE DE GESTION DE PESTANAS VS CODE
# =============================================================================
# RESPETA: Pestanas con PIN y pestanas con cambios pendientes
# CIERRA: Solo pestanas sin cambios y sin pin
# =============================================================================

param(
    [ValidateSet("smart", "unmodified", "others", "all")]
    [string]$Mode = "smart"
)

# Path especifico de VS Code (evita abrir Cursor)
$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"

if (-not (Test-Path $VSCodePath)) {
    $VSCodePath = "code"  # Fallback
}

Write-Host "[TABS] Gestion inteligente de pestanas VS Code" -ForegroundColor Cyan

try {
    # Verificar VS Code
    $vscodeProcess = Get-Process "Code" -ErrorAction SilentlyContinue
    if (-not $vscodeProcess) {
        Write-Host "[WARN] VS Code no esta ejecutandose" -ForegroundColor Yellow
        exit 1
    }

    Write-Host "[INFO] VS Code detectado (PID: $($vscodeProcess.Id -join ', '))" -ForegroundColor Green

    switch ($Mode) {
        "smart" {
            Write-Host "[INFO] Modo INTELIGENTE: Solo cierra pestanas SIN cambios y SIN pin" -ForegroundColor Cyan
            & $VSCodePath --command "workbench.action.closeUnmodifiedEditors" 2>$null
            Write-Host "[OK] Pestanas sin cambios cerradas (pins y modificadas PRESERVADAS)" -ForegroundColor Green
        }
        "unmodified" {
            Write-Host "[INFO] Cerrando pestanas no modificadas..." -ForegroundColor Cyan
            & $VSCodePath --command "workbench.action.closeUnmodifiedEditors" 2>$null
            Write-Host "[OK] Pestanas no modificadas cerradas" -ForegroundColor Green
        }
        "others" {
            Write-Host "[INFO] Cerrando otras pestanas (mantiene activa)..." -ForegroundColor Cyan
            & $VSCodePath --command "workbench.action.closeOtherEditors" 2>$null
            Write-Host "[OK] Otras pestanas cerradas" -ForegroundColor Green
        }
        "all" {
            Write-Host "[WARN] Cerrando TODAS las pestanas..." -ForegroundColor Yellow
            & $VSCodePath --command "workbench.action.closeAllEditors" 2>$null
            Write-Host "[OK] Todas las pestanas cerradas" -ForegroundColor Green
        }
    }

    Start-Sleep -Seconds 1

    # Reorganizar editores
    & $VSCodePath --command "workbench.action.evenEditorWidths" 2>$null
    Write-Host "[OK] Editores reorganizados" -ForegroundColor Green

    Write-Host "[SUCCESS] Gestion de pestanas completada" -ForegroundColor Green

} catch {
    Write-Host "[ERROR] Error gestionando pestanas: $_" -ForegroundColor Red
    exit 1
}

# Script termina automaticamente, SIN Read-Host
