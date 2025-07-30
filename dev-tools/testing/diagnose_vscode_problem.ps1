# Script de diagnostico - NO ejecuta comandos VS Code, solo analiza
# Valida el estado actual sin abrir nuevas instancias

Write-Host "=== DIAGNOSTICO DEL PROBLEMA ===" -ForegroundColor Yellow
Write-Host ""

# 1. Verificar que comando 'code' se esta usando
Write-Host "[ANALISIS] Verificando mapeo del comando 'code'..." -ForegroundColor Cyan
$codeCommands = where.exe code 2>$null
Write-Host "Comandos 'code' encontrados en orden de prioridad:" -ForegroundColor White
$codeCommands | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }

if ($codeCommands[0] -like "*cursor*") {
    Write-Host "[PROBLEMA] El primer 'code' apunta a CURSOR!" -ForegroundColor Red
} else {
    Write-Host "[OK] El primer 'code' apunta a VS Code" -ForegroundColor Green
}

Write-Host ""

# 2. Verificar procesos actuales de VS Code
Write-Host "[ANALISIS] Procesos VS Code actuales..." -ForegroundColor Cyan
$vscodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue
if ($vscodeProcesses) {
    Write-Host "Procesos VS Code encontrados: $($vscodeProcesses.Count)" -ForegroundColor Green
    $vscodeProcesses | ForEach-Object {
        Write-Host "  - PID: $($_.Id), Ventana: '$($_.MainWindowTitle)'" -ForegroundColor Gray
    }
} else {
    Write-Host "[INFO] No hay procesos VS Code ejecutandose" -ForegroundColor Yellow
}

Write-Host ""

# 3. Verificar que path especifico funciona
Write-Host "[ANALISIS] Verificando path especifico de VS Code..." -ForegroundColor Cyan
$VSCodePath = "${env:LOCALAPPDATA}\Programs\Microsoft VS Code\bin\code.cmd"
Write-Host "Path configurado: $VSCodePath" -ForegroundColor White
Write-Host "Existe: $(Test-Path $VSCodePath)" -ForegroundColor White

Write-Host ""

# 4. Simular que haria cada comando (SIN ejecutar)
Write-Host "[SIMULACION] Comandos que se ejecutarian:" -ForegroundColor Cyan
Write-Host "1. Para cerrar pestanas sin cambios:" -ForegroundColor White
Write-Host "   Comando: & `"$VSCodePath`" --command `"workbench.action.closeUnmodifiedEditors`"" -ForegroundColor Gray

Write-Host "2. Para reorganizar editores:" -ForegroundColor White
Write-Host "   Comando: & `"$VSCodePath`" --command `"workbench.action.evenEditorWidths`"" -ForegroundColor Gray

Write-Host ""

# 5. Problema potencial identificado
Write-Host "[HIPOTESIS] Posibles causas del problema:" -ForegroundColor Magenta
Write-Host "1. El comando 'code --command' puede abrir nueva instancia en lugar de usar la existente" -ForegroundColor Yellow
Write-Host "2. VS Code puede no estar configurado para 'reuse window'" -ForegroundColor Yellow
Write-Host "3. El comando puede necesitar parametros adicionales para usar instancia existente" -ForegroundColor Yellow

Write-Host ""
Write-Host "[RECOMENDACION] Probar comando alternativo:" -ForegroundColor Green
Write-Host "code --reuse-window --command workbench.action.closeUnmodifiedEditors" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== FIN DEL DIAGNOSTICO ===" -ForegroundColor Yellow
