# Terminal Detection Test - ASCII Safe
# Prueba comportamiento de deteccion de output y timeouts

Write-Host "[INFO] Iniciando pruebas de deteccion de terminal..." -ForegroundColor Cyan
Write-Host "[INFO] Fecha: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan

# Test 1: Proceso rapido con output inmediato
Write-Host ""
Write-Host "[TEST 1] Proceso rapido" -ForegroundColor Green
Write-Host "Salida inmediata"

# Test 2: Proceso con delay corto
Write-Host ""
Write-Host "[TEST 2] Proceso con delay 2s" -ForegroundColor Green
Start-Sleep 2
Write-Host "Output despues de 2 segundos"

# Test 3: Proceso incremental que podria ser problematico
Write-Host ""
Write-Host "[TEST 3] Proceso incremental 5s" -ForegroundColor Green
for ($i = 1; $i -le 5; $i++) {
    Write-Host "Progreso: $i/5" -ForegroundColor Yellow
    Start-Sleep 1
}
Write-Host "Proceso incremental completado" -ForegroundColor Green

# Test 4: Comando que podria timeout (simulado)
Write-Host ""
Write-Host "[TEST 4] Simulacion pre-commit" -ForegroundColor Green
Write-Host "Simulando: poetry run pre-commit run --all-files"
Start-Sleep 3
Write-Host "ruff...........................................Passed" -ForegroundColor Green
Start-Sleep 1
Write-Host "ruff-format....................................Passed" -ForegroundColor Green
Start-Sleep 1
Write-Host "trim trailing whitespace.......................Passed" -ForegroundColor Green

# Test 5: Verificar responsividad final
Write-Host ""
Write-Host "[TEST 5] Verificacion final" -ForegroundColor Green
$start = Get-Date
Get-Date | Out-Null
$end = Get-Date
$duration = ($end - $start).TotalMilliseconds

if ($duration -lt 100) {
    Write-Host "[OK] Terminal responsive: ${duration}ms" -ForegroundColor Green
} else {
    Write-Host "[WARN] Terminal lento: ${duration}ms" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[COMPLETADO] Todas las pruebas terminadas" -ForegroundColor Cyan
Write-Host "[INFO] Si este mensaje aparece, la deteccion funciona correctamente" -ForegroundColor Cyan
