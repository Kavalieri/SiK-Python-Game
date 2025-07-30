# Test final: Metodo directo usando VS Code CLI correctamente
param(
    [switch]$TestOnly,
    [switch]$Verbose
)

Write-Host "=== TEST FINAL: METODO DIRECTO VS CODE ===" -ForegroundColor Yellow
Write-Host ""

# Configuracion
$VSCodePath = "C:\Users\Kava\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd"

# Verificar VS Code existe
if (-not (Test-Path $VSCodePath)) {
    Write-Host "[ERROR] VS Code no encontrado en: $VSCodePath" -ForegroundColor Red
    exit 1
}

# 1. Detectar instancias antes
$beforeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
$beforeCount = $beforeProcesses.Count
Write-Host "[BEFORE] VS Code instances: $beforeCount" -ForegroundColor Cyan

if ($beforeCount -eq 0) {
    Write-Host "[ERROR] No hay VS Code ejecutandose. Abrir VS Code primero." -ForegroundColor Red
    exit 1
}

# Mostrar PIDs de instancias existentes
Write-Host "[INFO] PIDs existentes:" -ForegroundColor Green
$beforeProcesses | ForEach-Object { Write-Host "  - PID: $($_.Id), Titulo: $($_.MainWindowTitle)" -ForegroundColor Gray }

Write-Host ""

if ($TestOnly) {
    Write-Host "[TEST MODE] Comando que se ejecutaria:" -ForegroundColor Yellow
    Write-Host "& `"$VSCodePath`" --command workbench.action.closeUnmodifiedEditors" -ForegroundColor White
    Write-Host ""
    Write-Host "[INFO] Este metodo NO usa --reuse-window" -ForegroundColor Cyan
    Write-Host "[INFO] Usa el parametro --command que es especifico para instancias existentes" -ForegroundColor Cyan
    exit 0
}

# Ejecutar comando real
Write-Host "[EXECUTING] Cerrando pestanas no modificadas..." -ForegroundColor Yellow

# El parametro --command es especifico para enviar comandos a VS Code existente
try {
    & "$VSCodePath" --command workbench.action.closeUnmodifiedEditors
    Start-Sleep -Seconds 2  # Dar tiempo a VS Code para procesar
    Write-Host "[SUCCESS] Comando enviado a VS Code" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Fallo al ejecutar comando: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. Verificar instancias despues
Start-Sleep -Seconds 1
$afterProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
$afterCount = $afterProcesses.Count

Write-Host ""
Write-Host "[AFTER] VS Code instances: $afterCount" -ForegroundColor Cyan

# Analizar resultados
if ($afterCount -eq $beforeCount) {
    Write-Host "[RESULTADO] ✓ No se abrieron nuevas instancias" -ForegroundColor Green
} elseif ($afterCount -gt $beforeCount) {
    Write-Host "[RESULTADO] ✗ Se abrieron $($afterCount - $beforeCount) nuevas instancias" -ForegroundColor Red
} else {
    Write-Host "[RESULTADO] ? Se cerraron $($beforeCount - $afterCount) instancias" -ForegroundColor Yellow
}

# Mostrar PIDs finales
Write-Host "[INFO] PIDs finales:" -ForegroundColor Green
$afterProcesses | ForEach-Object { Write-Host "  - PID: $($_.Id), Titulo: $($_.MainWindowTitle)" -ForegroundColor Gray }

Write-Host ""
Write-Host "[CONCLUSION] Resultado del test:" -ForegroundColor Yellow

if ($afterCount -eq $beforeCount) {
    Write-Host "✓ Metodo --command funciona correctamente" -ForegroundColor Green
    Write-Host "✓ No se abren nuevas instancias de VS Code" -ForegroundColor Green
    Write-Host ""
    Write-Host "[NEXT] Verificar manualmente si las pestanas se cerraron:" -ForegroundColor Cyan
    Write-Host "  1. Revisar VS Code para ver si se cerraron pestanas no modificadas" -ForegroundColor White
    Write-Host "  2. Las pestanas fijadas y modificadas deben permanecer abiertas" -ForegroundColor White
    Write-Host "  3. Solo las pestanas sin cambios ni pin deben cerrarse" -ForegroundColor White
} else {
    Write-Host "✗ El metodo aun abre nuevas instancias" -ForegroundColor Red
    Write-Host "  Necesario investigar otros parametros" -ForegroundColor White
}

Write-Host ""
