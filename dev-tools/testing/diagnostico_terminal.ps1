# =============================================================================
# DIAGNÓSTICO AVANZADO DE TERMINAL - SiK Python Game
# =============================================================================
# Identifica problemas específicos que causan timeouts y bloqueos
# =============================================================================

Write-Host "🔍 DIAGNÓSTICO AVANZADO DE TERMINAL" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# =============================================================================
# FUNCIÓN DE PRUEBA CON TIMEOUT
# =============================================================================
function Test-CommandWithTimeout {
    param(
        [string]$Command,
        [string]$Description,
        [int]$TimeoutSeconds = 10
    )

    Write-Host "🧪 Probando: $Description" -ForegroundColor Yellow
    Write-Host "   Comando: $Command" -ForegroundColor Gray

    $startTime = Get-Date

    try {
        # Ejecutar comando con timeout
        $job = Start-Job -ScriptBlock {
            param($cmd)
            Invoke-Expression $cmd
        } -ArgumentList $Command

        # Esperar con timeout
        $completed = Wait-Job $job -Timeout $TimeoutSeconds

        if ($completed) {
            $output = Receive-Job $job
            $endTime = Get-Date
            $duration = ($endTime - $startTime).TotalSeconds

            Write-Host "   ✅ Completado en $([math]::Round($duration, 2))s" -ForegroundColor Green
            if ($output) {
                Write-Host "   📋 Output: $($output | Select-Object -First 3 | Out-String)" -ForegroundColor Gray
            }
        } else {
            Write-Host "   ⏰ TIMEOUT después de ${TimeoutSeconds}s" -ForegroundColor Red
            Stop-Job $job
        }

        Remove-Job $job -Force

    } catch {
        Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }

    Write-Host ""
}

# =============================================================================
# PRUEBAS SISTEMÁTICAS
# =============================================================================

Write-Host "📊 INFORMACIÓN DEL SISTEMA" -ForegroundColor Blue
Write-Host "PowerShell Version: $($PSVersionTable.PSVersion)"
Write-Host "OS: $($PSVersionTable.OS)"
Write-Host "Directorio: $(Get-Location)"
Write-Host ""

Write-Host "🔧 PRUEBAS BÁSICAS" -ForegroundColor Blue
Test-CommandWithTimeout "echo 'test simple'" "Echo básico" 5
Test-CommandWithTimeout "Get-Date" "Get-Date" 5
Test-CommandWithTimeout "Get-Location" "Get-Location" 5

Write-Host "🐍 PRUEBAS DE POETRY" -ForegroundColor Blue
Test-CommandWithTimeout "poetry --version" "Poetry version" 10
Test-CommandWithTimeout "poetry env info" "Poetry env info" 15
Test-CommandWithTimeout "poetry show --tree | Select-Object -First 5" "Poetry dependencies (limitado)" 15

Write-Host "🔧 PRUEBAS DE PRE-COMMIT" -ForegroundColor Blue
Test-CommandWithTimeout "poetry run pre-commit --version" "Pre-commit version" 10

# Test más agresivo de pre-commit
Write-Host "🧪 PRUEBA CRÍTICA: Pre-commit check" -ForegroundColor Yellow
Test-CommandWithTimeout "poetry run pre-commit run --help" "Pre-commit help" 15

Write-Host "🌐 PRUEBAS DE GIT" -ForegroundColor Blue
Test-CommandWithTimeout "git --version" "Git version" 5
Test-CommandWithTimeout "git status --porcelain" "Git status porcelain" 10
Test-CommandWithTimeout "git branch --show-current" "Git current branch" 5

Write-Host "🌍 PRUEBAS DE GITHUB CLI" -ForegroundColor Blue
Test-CommandWithTimeout "gh --version" "GitHub CLI version" 10
Test-CommandWithTimeout "gh status" "GitHub CLI status" 15

# =============================================================================
# PRUEBAS DE PROCESOS PROBLEMÁTICOS
# =============================================================================

Write-Host "⚠️  PRUEBAS DE COMANDOS PROBLEMÁTICOS" -ForegroundColor Red

# Test de comando que puede bloquear
Write-Host "🔥 Probando comando que históricamente causa problemas..." -ForegroundColor Yellow
Test-CommandWithTimeout "poetry run pre-commit run --all-files --verbose" "Pre-commit run completo" 30

# =============================================================================
# ANÁLISIS DE VARIABLES DE ENTORNO
# =============================================================================

Write-Host "🔧 ANÁLISIS DE VARIABLES DE ENTORNO" -ForegroundColor Blue

$criticalVars = @(
    "PATH",
    "PYTHONPATH",
    "VIRTUAL_ENV",
    "POETRY_CACHE_DIR",
    "PRE_COMMIT_HOME",
    "GIT_DIR"
)

foreach ($var in $criticalVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        $shortValue = if ($value.Length -gt 100) {
            "$($value.Substring(0, 100))..."
        } else {
            $value
        }
        Write-Host "  $var = $shortValue" -ForegroundColor Gray
    } else {
        Write-Host "  $var = (no definida)" -ForegroundColor Yellow
    }
}

# =============================================================================
# PRUEBAS DE MEMORIA Y PROCESOS
# =============================================================================

Write-Host "`n💾 ESTADO DE MEMORIA Y PROCESOS" -ForegroundColor Blue

# Memoria disponible
$memory = Get-CimInstance -ClassName Win32_OperatingSystem
$freeMemory = [math]::Round($memory.FreePhysicalMemory / 1MB, 2)
$totalMemory = [math]::Round($memory.TotalVisibleMemorySize / 1MB, 2)
Write-Host "  Memoria libre: ${freeMemory}GB de ${totalMemory}GB" -ForegroundColor Gray

# Procesos relacionados con desarrollo
$devProcesses = @("poetry", "pre-commit", "git", "gh", "python", "powershell")
foreach ($processName in $devProcesses) {
    $processes = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if ($processes) {
        $count = $processes.Count
        Write-Host "  Procesos ${processName}: $count activos" -ForegroundColor Gray
    }
}

# =============================================================================
# RECOMENDACIONES
# =============================================================================

Write-Host "`n💡 RECOMENDACIONES BASADAS EN DIAGNÓSTICO" -ForegroundColor Green
Write-Host "1. Verificar si alguna prueba tuvo TIMEOUT" -ForegroundColor White
Write-Host "2. Comprobar procesos que consumen memoria excesiva" -ForegroundColor White
Write-Host "3. Revisar variables de entorno problemáticas" -ForegroundColor White
Write-Host "4. Identificar comandos específicos que causan bloqueos" -ForegroundColor White

Write-Host "`n✅ DIAGNÓSTICO COMPLETADO" -ForegroundColor Green
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray
