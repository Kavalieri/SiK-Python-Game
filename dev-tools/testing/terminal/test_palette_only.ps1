# PRUEBA 3: Solo metodo Command Palette
Write-Host "=== PRUEBA 3: METODO COMMAND PALETTE SOLAMENTE ===" -ForegroundColor Yellow

$before = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if (-not $before) {
    Write-Host "[ERROR] VS Code no ejecutandose" -ForegroundColor Red
    exit 1
}

Write-Host "[ANTES] $($before.MainWindowTitle)" -ForegroundColor Cyan
Write-Host "[METODO] Command Palette: Ctrl+Shift+P" -ForegroundColor Yellow

Write-Host "[EJECUTANDO] Command Palette method..." -ForegroundColor Green

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
    Write-Host "[INFO] Activando ventana VS Code..." -ForegroundColor Gray
    [Win32]::SetForegroundWindow($before.MainWindowHandle)
    Start-Sleep -Milliseconds 1000

    # Abrir Command Palette
    Write-Host "[INFO] Abriendo Command Palette (Ctrl+Shift+P)..." -ForegroundColor Gray
    [System.Windows.Forms.SendKeys]::SendWait("^+p")
    Start-Sleep -Milliseconds 1000

    # Escribir comando
    Write-Host "[INFO] Escribiendo 'Close Unmodified Editors'..." -ForegroundColor Gray
    [System.Windows.Forms.SendKeys]::SendWait("Close Unmodified Editors")
    Start-Sleep -Milliseconds 500

    # Presionar Enter
    Write-Host "[INFO] Presionando Enter..." -ForegroundColor Gray
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

    Write-Host "[OK] Command Palette usado correctamente" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Fallo Command Palette: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "[INSTRUCCION] Verifica en VS Code:" -ForegroundColor Cyan
Write-Host "  1. ¿Se cerraron pestanas?" -ForegroundColor White
Write-Host "  2. ¿Cambio el tamaño de ventana?" -ForegroundColor White
Write-Host "  3. ¿Se quedo abierto Command Palette?" -ForegroundColor White
Write-Host "  4. Espera 3 segundos y presiona ENTER para continuar..." -ForegroundColor Yellow

Read-Host

$after = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1
if ($after) {
    Write-Host "[DESPUES] $($after.MainWindowTitle)" -ForegroundColor Cyan
}
