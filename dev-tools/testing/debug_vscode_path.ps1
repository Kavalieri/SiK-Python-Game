# Debug script para verificar que path de VS Code se esta usando

$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"

Write-Host "[DEBUG] Verificando configuracion de VS Code..." -ForegroundColor Yellow
Write-Host "[DEBUG] Path configurado: $VSCodePath" -ForegroundColor Cyan
Write-Host "[DEBUG] Path existe: $(Test-Path $VSCodePath)" -ForegroundColor Cyan

if (-not (Test-Path $VSCodePath)) {
    Write-Host "[DEBUG] FALLBACK: Usando 'code' del PATH" -ForegroundColor Red
    $VSCodePath = "code"
} else {
    Write-Host "[DEBUG] USANDO PATH ESPECIFICO de VS Code" -ForegroundColor Green
}

Write-Host "[DEBUG] Path final a usar: $VSCodePath" -ForegroundColor Yellow

# Verificar que comando se ejecutara realmente
Write-Host "[DEBUG] Comando que se ejecutara: & `"$VSCodePath`" --version" -ForegroundColor Magenta

# Ejecutar y mostrar version
try {
    Write-Host "[DEBUG] Ejecutando comando..." -ForegroundColor Cyan
    & $VSCodePath --version
    Write-Host "[DEBUG] Comando ejecutado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "[DEBUG] ERROR ejecutando comando: $_" -ForegroundColor Red
}

# Verificar procesos
$processes = Get-Process -Name "*code*", "*cursor*" -ErrorAction SilentlyContinue
Write-Host "[DEBUG] Procesos relacionados encontrados:" -ForegroundColor Yellow
$processes | ForEach-Object {
    Write-Host "  - $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor White
}
