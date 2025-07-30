# METODO DEFINITIVO FUNCIONAL: Cerrar pestanas VS Code
param(
    [ValidateSet("uri", "keys", "palette")]
    [string]$Method = "uri",
    [switch]$TestOnly
)

Write-Host "=== METODO DEFINITIVO FUNCIONAL ===" -ForegroundColor Yellow
Write-Host "Metodo seleccionado: $Method" -ForegroundColor Cyan
Write-Host ""

# Verificar VS Code esta ejecutandose
$vscodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if (-not $vscodeProcess) {
    Write-Host "[ERROR] VS Code no esta ejecutandose" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] VS Code detectado: $($vscodeProcess.MainWindowTitle)" -ForegroundColor Green
$beforeTitle = $vscodeProcess.MainWindowTitle

if ($TestOnly) {
    Write-Host "[TEST MODE] Se ejecutaria metodo: $Method" -ForegroundColor Yellow
    switch ($Method) {
        "uri" { Write-Host "  - Start-Process 'vscode://command/workbench.action.closeUnmodifiedEditors'" -ForegroundColor White }
        "keys" { Write-Host "  - Send Keys: Ctrl+K U" -ForegroundColor White }
        "palette" { Write-Host "  - Command Palette: Ctrl+Shift+P + 'Close Unmodified Editors'" -ForegroundColor White }
    }
    exit 0
}

Write-Host "[EJECUTANDO] Cerrando pestanas no modificadas..." -ForegroundColor Yellow

switch ($Method) {
    "uri" {
        Write-Host "  [URI] Enviando comando via vscode://" -ForegroundColor Cyan
        try {
            Start-Process "vscode://command/workbench.action.closeUnmodifiedEditors"
            Write-Host "  [OK] URI enviado correctamente" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Fallo URI: $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }

    "keys" {
        Write-Host "  [KEYS] Enviando Ctrl+K U" -ForegroundColor Cyan
        try {
            Add-Type -AssemblyName System.Windows.Forms

            # Win32 API para activar ventana
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Win32 {
                [DllImport("user32.dll")]
                public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
                [DllImport("user32.dll")]
                public static extern bool SetForegroundWindow(IntPtr hWnd);
            }
"@

            # Activar VS Code
            [Win32]::SetForegroundWindow($vscodeProcess.MainWindowHandle)
            Start-Sleep -Milliseconds 500

            # Enviar Ctrl+K U
            [System.Windows.Forms.SendKeys]::SendWait("^k")
            Start-Sleep -Milliseconds 200
            [System.Windows.Forms.SendKeys]::SendWait("u")

            Write-Host "  [OK] Ctrl+K U enviado correctamente" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Fallo Send Keys: $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }

    "palette" {
        Write-Host "  [PALETTE] Usando Command Palette" -ForegroundColor Cyan
        try {
            Add-Type -AssemblyName System.Windows.Forms

            # Activar VS Code
            [Win32]::SetForegroundWindow($vscodeProcess.MainWindowHandle)
            Start-Sleep -Milliseconds 500

            # Ctrl+Shift+P para Command Palette
            [System.Windows.Forms.SendKeys]::SendWait("^+p")
            Start-Sleep -Milliseconds 500

            # Escribir comando
            [System.Windows.Forms.SendKeys]::SendWait("Close Unmodified Editors")
            Start-Sleep -Milliseconds 300

            # Enter para ejecutar
            [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

            Write-Host "  [OK] Command Palette usado correctamente" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Fallo Command Palette: $($_.Exception.Message)" -ForegroundColor Red
            exit 1
        }
    }
}

# Esperar a que VS Code procese
Start-Sleep -Seconds 3

# Verificar resultado
$afterProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if ($afterProcess) {
    $afterTitle = $afterProcess.MainWindowTitle
    Write-Host ""
    Write-Host "[RESULTADO]" -ForegroundColor Yellow
    Write-Host "  ANTES: $beforeTitle" -ForegroundColor Gray
    Write-Host "  DESPUES: $afterTitle" -ForegroundColor Gray

    if ($beforeTitle -ne $afterTitle) {
        Write-Host "  [SUCCESS] ✓ Pestanas cerradas - titulo cambio detectado" -ForegroundColor Green
    } else {
        Write-Host "  [INFO] Sin cambios de titulo - verificar manualmente" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] VS Code ya no esta ejecutandose" -ForegroundColor Red
}

Write-Host ""
Write-Host "[VALIDACION] Verificar en VS Code:" -ForegroundColor Cyan
Write-Host "  ✓ Pestanas sin modificar y sin pin: CERRADAS" -ForegroundColor White
Write-Host "  ✓ Pestanas fijadas (pin): ABIERTAS" -ForegroundColor White
Write-Host "  ✓ Pestanas modificadas: ABIERTAS" -ForegroundColor White
