# PRUEBA 1: Solo metodo URI
Write-Host "=== PRUEBA 1: METODO URI SOLAMENTE ===" -ForegroundColor Yellow

$before = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if (-not $before) {
    Write-Host "[ERROR] VS Code no ejecutandose" -ForegroundColor Red
    exit 1
}

Write-Host "[ANTES] $($before.MainWindowTitle)" -ForegroundColor Cyan
Write-Host "[METODO] URI Scheme vscode://" -ForegroundColor Yellow

Write-Host "[EJECUTANDO] URI method..." -ForegroundColor Green
Start-Process "vscode://command/workbench.action.closeUnmodifiedEditors"

Write-Host "[INFO] Comando URI enviado" -ForegroundColor Green
Write-Host "[INSTRUCCION] Verifica en VS Code:" -ForegroundColor Cyan
Write-Host "  1. ¿Se cerraron pestanas?" -ForegroundColor White
Write-Host "  2. ¿Cambio el tamaño de ventana?" -ForegroundColor White
Write-Host "  3. Espera 3 segundos y presiona ENTER para continuar..." -ForegroundColor Yellow

Read-Host

$after = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1
if ($after) {
    Write-Host "[DESPUES] $($after.MainWindowTitle)" -ForegroundColor Cyan
}
