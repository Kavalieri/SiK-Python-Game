# Metodo alternativo - Usar extension de VS Code para comunicacion interna
# En lugar de comandos externos, usar mecanismos internos

Write-Host "=== METODO ALTERNATIVO - COMUNICACION INTERNA ===" -ForegroundColor Yellow
Write-Host ""

# Verificar si hay una instancia de VS Code activa
$vscodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" }
if (-not $vscodeProcesses) {
    Write-Host "[ERROR] No hay VS Code ejecutandose" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] VS Code detectado: PID $($vscodeProcesses[0].Id)" -ForegroundColor Green

# Metodo 1: Usar VS Code con workspace especifico
$workspaceFolder = Get-Location
Write-Host "[INFO] Workspace actual: $workspaceFolder" -ForegroundColor Cyan

# Crear archivo temporal con comando
$tempCommand = @"
{
  "command": "workbench.action.closeUnmodifiedEditors"
}
"@

$tempFile = "$env:TEMP\vscode_command.json"
$tempCommand | Out-File -FilePath $tempFile -Encoding UTF8

Write-Host "[METODO 1] Archivo temporal creado: $tempFile" -ForegroundColor Cyan

# Metodo 2: Intentar comunicacion directa via socket/pipe
Write-Host "[METODO 2] Buscando pipes de comunicacion de VS Code..." -ForegroundColor Cyan

# Los pipes de VS Code suelen estar en formato: \\.\pipe\vscode-{id}
$pipes = Get-ChildItem "\\.\pipe\" -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "vscode*" }
if ($pipes) {
    Write-Host "[INFO] Pipes de VS Code encontrados:" -ForegroundColor Green
    $pipes | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
} else {
    Write-Host "[INFO] No se encontraron pipes de VS Code" -ForegroundColor Yellow
}

# Metodo 3: Usar API de VS Code via HTTP (si esta habilitada)
Write-Host "[METODO 3] Verificando API HTTP de VS Code..." -ForegroundColor Cyan

# VS Code puede tener un servidor interno en puerto 23579 o similar
$ports = @(23579, 23580, 23581)
foreach ($port in $ports) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/status" -TimeoutSec 2 -ErrorAction Stop
        Write-Host "[INFO] API encontrada en puerto $port" -ForegroundColor Green
        break
    } catch {
        # Silenciosamente continuar
    }
}

Write-Host ""
Write-Host "[CONCLUSION] Metodos de comunicacion disponibles:" -ForegroundColor Yellow
Write-Host "1. Comando directo con --reuse-window (puede abrir nueva instancia)" -ForegroundColor White
Write-Host "2. Archivo temporal + inotify (VS Code debe detectar cambios)" -ForegroundColor White
Write-Host "3. Pipes nombrados (requiere acceso de bajo nivel)" -ForegroundColor White
Write-Host "4. API HTTP (si esta habilitada)" -ForegroundColor White

Write-Host ""
Write-Host "[RECOMENDACION] Probar metodo mas simple primero:" -ForegroundColor Green
Write-Host "VS Code CLI con parametros especificos para instancia existente" -ForegroundColor Cyan

# Limpiar archivo temporal
Remove-Item $tempFile -ErrorAction SilentlyContinue
