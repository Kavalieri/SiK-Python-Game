# Script mejorado para        "unmodified" {
            Write-Host "[INFO] Cerrando pestanas no modificadas..." -ForegroundColor Cyan
            & $VSCodePath --command "workbench.action.closeUnmodifiedEditors" 2>$null
        }
        "others" {
            Write-Host "[INFO] Cerrando otras pestanas..." -ForegroundColor Cyan
            & $VSCodePath --command "workbench.action.closeOtherEditors" 2>$null
        }
        "all" {
            Write-Host "[WARN] Cerrando TODAS las pestanas..." -ForegroundColor Yellow
            & $VSCodePath --command "workbench.action.closeAllEditors" 2>$null
        }pestañas VS Code
# Usa múltiples métodos para garantizar el cierre de pestañas

param(
    [ValidateSet("unmodified", "others", "all")]
    [string]$Mode = "unmodified"
)

Write-Host "[TABS] Gestionando pestanas de VS Code..." -ForegroundColor Cyan

try {
    # Verificar VS Code
    $vscodeProcess = Get-Process "Code" -ErrorAction SilentlyContinue
    if (-not $vscodeProcess) {
        Write-Host "[WARN] VS Code no esta ejecutandose" -ForegroundColor Yellow
        return
    }

    Write-Host "[INFO] VS Code detectado, cerrando pestanas..." -ForegroundColor Green

    # Método 1: Comandos de VS Code CLI
    switch ($Mode) {
        "unmodified" {
            Write-Host "[INFO] Cerrando pestanas no modificadas..." -ForegroundColor Cyan
            & code --command "workbench.action.closeUnmodifiedEditors" 2>$null
        }
        "others" {
            Write-Host "[INFO] Cerrando otras pestanas..." -ForegroundColor Cyan
            & code --command "workbench.action.closeOtherEditors" 2>$null
        }
        "all" {
            Write-Host "[INFO] Cerrando todas las pestanas..." -ForegroundColor Cyan
            & code --command "workbench.action.closeAllEditors" 2>$null
        }
    }

    Start-Sleep -Seconds 2

    # Método 2: Atajos de teclado via SendKeys (fallback)
    if ($Mode -eq "unmodified") {
        try {
            Add-Type -AssemblyName System.Windows.Forms
            # Foco a VS Code
            $vscodeWindows = Get-Process "Code" | Where-Object { $_.MainWindowTitle -ne "" }
            if ($vscodeWindows) {
                $vscodeWindows[0].MainWindowHandle | ForEach-Object {
                    [System.Windows.Forms.SendKeys]::SendWait("^k")
                    Start-Sleep -Milliseconds 500
                    [System.Windows.Forms.SendKeys]::SendWait("u")
                }
                Write-Host "[INFO] Atajo de teclado enviado (Ctrl+K U)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "[DEBUG] SendKeys no disponible: $_" -ForegroundColor DarkYellow
        }
    }

    Write-Host "[OK] Proceso de cierre completado" -ForegroundColor Green

} catch {
    Write-Host "[ERROR] Error gestionando pestanas: $_" -ForegroundColor Red
}
