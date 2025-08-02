# PRUEBA 2 CORREGIDA: Solo metodo Send Keys
Write-Host "=== PRUEBA 2: METODO SEND KEYS (CORREGIDO) ===" -ForegroundColor Yellow

$before = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if (-not $before) {
    Write-Host "[ERROR] VS Code no ejecutandose" -ForegroundColor Red
    exit 1
}

Write-Host "[ANTES] $($before.MainWindowTitle)" -ForegroundColor Cyan
Write-Host "[METODO] Send Keys: Ctrl+K U" -ForegroundColor Yellow

Write-Host "[EJECUTANDO] Send Keys method..." -ForegroundColor Green

try {
    Add-Type -AssemblyName System.Windows.Forms

    # Verificar si Win32 ya existe, si no, crearla
    if (-not ("Win32VSCode" -as [type])) {
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class Win32VSCode {
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
        }
"@
    }

    # Activar VS Code
    Write-Host "[INFO] Activando ventana VS Code..." -ForegroundColor Gray
    [Win32VSCode]::SetForegroundWindow($before.MainWindowHandle)
    Start-Sleep -Milliseconds 1000

    # Enviar Ctrl+K
    Write-Host "[INFO] Enviando Ctrl+K..." -ForegroundColor Gray
    [System.Windows.Forms.SendKeys]::SendWait("^k")
    Start-Sleep -Milliseconds 500

    # Enviar U
    Write-Host "[INFO] Enviando U..." -ForegroundColor Gray
    [System.Windows.Forms.SendKeys]::SendWait("u")

    Write-Host "[OK] Ctrl+K U enviado correctamente" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Fallo Send Keys: $($_.Exception.Message)" -ForegroundColor Red
}

Start-Sleep -Seconds 3

$after = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1
if ($after) {
    Write-Host "[DESPUES] $($after.MainWindowTitle)" -ForegroundColor Cyan
    if ($before.MainWindowTitle -ne $after.MainWindowTitle) {
        Write-Host "[CAMBIO DETECTADO] El titulo cambio" -ForegroundColor Green
    } else {
        Write-Host "[SIN CAMBIOS] El titulo no cambio" -ForegroundColor Yellow
    }
}

Write-Host "[INSTRUCCION] Observa VS Code y responde:" -ForegroundColor Cyan
Write-Host "  ¿Se cerraron pestanas? ¿Cambio tamaño ventana?" -ForegroundColor White
