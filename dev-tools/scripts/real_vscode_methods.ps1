# SOLUCION REAL: Metodos alternativos para cerrar pestanas VS Code
param([switch]$TestOnly)

Write-Host "=== INVESTIGACION: METODOS REALES VS CODE ===" -ForegroundColor Yellow
Write-Host ""

# OPCION 1: vscode:// URI scheme
Write-Host "[OPCION 1] URI Scheme vscode://" -ForegroundColor Cyan
if ($TestOnly) {
    Write-Host "  [TEST] Start-Process 'vscode://command/workbench.action.closeUnmodifiedEditors'" -ForegroundColor White
} else {
    try {
        Start-Process "vscode://command/workbench.action.closeUnmodifiedEditors"
        Write-Host "  [OK] URI enviado" -ForegroundColor Green
    } catch {
        Write-Host "  [ERROR] $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# OPCION 2: Extension Custom
Write-Host "[OPCION 2] Extension con CLI" -ForegroundColor Cyan
$extensionsList = & "C:\Users\Kava\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd" --list-extensions 2>$null | Where-Object { $_ -like "*command*" -or $_ -like "*cli*" }
if ($extensionsList) {
    Write-Host "  [INFO] Extensions CLI disponibles:" -ForegroundColor Green
    $extensionsList | ForEach-Object { Write-Host "    - $_" -ForegroundColor Gray }
} else {
    Write-Host "  [INFO] No hay extensions CLI instaladas" -ForegroundColor Yellow
}

Write-Host ""

# OPCION 3: Send Keys (Windows API)
Write-Host "[OPCION 3] Send Keys API" -ForegroundColor Cyan
if ($TestOnly) {
    Write-Host "  [TEST] Enviar Ctrl+K U (Close Unmodified Editors)" -ForegroundColor White
} else {
    # Buscar ventana de VS Code
    Add-Type -AssemblyName System.Windows.Forms
    $vscodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

    if ($vscodeProcess) {
        Write-Host "  [INFO] VS Code encontrado: $($vscodeProcess.MainWindowTitle)" -ForegroundColor Green

        # Activar ventana de VS Code
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

        [Win32]::ShowWindow($vscodeProcess.MainWindowHandle, 9) # SW_RESTORE
        [Win32]::SetForegroundWindow($vscodeProcess.MainWindowHandle)
        Start-Sleep -Milliseconds 500

        # Enviar comando teclado: Ctrl+K U
        [System.Windows.Forms.SendKeys]::SendWait("^k")
        Start-Sleep -Milliseconds 200
        [System.Windows.Forms.SendKeys]::SendWait("u")

        Write-Host "  [OK] Comando teclado enviado: Ctrl+K U" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] VS Code no encontrado" -ForegroundColor Red
    }
}

Write-Host ""

# OPCION 4: Command Palette automation
Write-Host "[OPCION 4] Command Palette automation" -ForegroundColor Cyan
if ($TestOnly) {
    Write-Host "  [TEST] Ctrl+Shift+P + buscar 'Close Unmodified Editors'" -ForegroundColor White
} else {
    $vscodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

    if ($vscodeProcess) {
        # Activar VS Code
        [Win32]::SetForegroundWindow($vscodeProcess.MainWindowHandle)
        Start-Sleep -Milliseconds 500

        # Abrir Command Palette
        [System.Windows.Forms.SendKeys]::SendWait("^+p")  # Ctrl+Shift+P
        Start-Sleep -Milliseconds 500

        # Escribir comando
        [System.Windows.Forms.SendKeys]::SendWait("Close Unmodified Editors")
        Start-Sleep -Milliseconds 300

        # Presionar Enter
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

        Write-Host "  [OK] Command Palette usado" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] VS Code no encontrado" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "[CONCLUSION] Metodos reales disponibles:" -ForegroundColor Yellow
Write-Host "  1. URI scheme (mas compatible)" -ForegroundColor White
Write-Host "  2. Send Keys API (directo)" -ForegroundColor White
Write-Host "  3. Command Palette automation (universal)" -ForegroundColor White
Write-Host "  4. Extension customizada (requiere instalacion)" -ForegroundColor White
