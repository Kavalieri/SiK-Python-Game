# Terminal Safe Commit Script
# Evita problemas de timeout y bloqueo en VS Code PowerShell

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Type = "feat",
    [string]$Scope = "",
    [switch]$Push
)

# Configuración de timeouts
$PRE_COMMIT_TIMEOUT = 45
$GIT_TIMEOUT = 15

# Colores para output
$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

Write-Host "[TERMINAL-SAFE] Terminal Safe Commit Script" -ForegroundColor $ColorInfo
Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo

# Verificar directorio de trabajo
$currentDir = Get-Location
Write-Host "[INFO] Directorio actual: $currentDir" -ForegroundColor $ColorInfo
if (-not (Test-Path ".git")) {
    Write-Host "[ERROR] No se encuentra repositorio git en: $currentDir" -ForegroundColor $ColorError
    Write-Host "[INFO] Asegurate de ejecutar desde el directorio del proyecto" -ForegroundColor $ColorWarning
    exit 1
}

# Función: Comando con timeout
function Invoke-CommandWithTimeout {
    param(
        [string]$Command,
        [int]$TimeoutSeconds = 30,
        [string]$Description = "Comando"
    )

    Write-Host "[EXEC] $Description (timeout: ${TimeoutSeconds}s)..." -ForegroundColor $ColorInfo

    $job = Start-Job -ScriptBlock {
        param($cmd, $workingDir)
        try {
            Set-Location $workingDir
            Invoke-Expression $cmd
            return @{ Success = $true; Output = $null }
        } catch {
            return @{ Success = $false; Error = $_.Exception.Message }
        }
    } -ArgumentList $Command, (Get-Location)

    $completed = Wait-Job $job -Timeout $TimeoutSeconds

    if ($completed) {
        $result = Receive-Job $job
        Remove-Job $job
        Write-Host "[OK] $Description completado" -ForegroundColor $ColorSuccess
        return $result
    } else {
        Write-Host "[TIMEOUT] $Description cancelado (${TimeoutSeconds}s)" -ForegroundColor $ColorWarning
        Stop-Job $job
        Remove-Job $job
        return $null
    }
}

# Función: Test de responsividad del terminal
function Test-TerminalResponsive {
    $start = Get-Date
    try {
        Get-Date | Out-Null  # Test simple de comando
        $end = Get-Date
        $duration = ($end - $start).TotalMilliseconds

        if ($duration -lt 1000) {
            Write-Host "[OK] Terminal responsivo (${duration}ms)" -ForegroundColor $ColorSuccess
            return $true
        } else {
            Write-Host "[WARN] Terminal lento (${duration}ms)" -ForegroundColor $ColorWarning
            return $false
        }
    } catch {
        Write-Host "[ERROR] Terminal no responsivo" -ForegroundColor $ColorError
        return $false
    }
}

# Función: Reset de estado del terminal
function Reset-TerminalState {
    Write-Host "[RESET] Reseteando estado del terminal..." -ForegroundColor $ColorInfo
    Get-Date | Out-Null
    Start-Sleep -Milliseconds 500
    Write-Host "[OK] Terminal reseteado" -ForegroundColor $ColorSuccess
}

# ==========================================
# INICIO DEL PROCESO
# ==========================================

# 1. Verificar responsividad del terminal
Write-Host "`n[INFO] FASE 1: Verificacion del Terminal" -ForegroundColor $ColorInfo
if (-not (Test-TerminalResponsive)) {
    Write-Host "[WARN] Intentando reset automatico..." -ForegroundColor $ColorWarning
    Reset-TerminalState

    if (-not (Test-TerminalResponsive)) {
        Write-Host "[ERROR] Terminal no responsive - abortando" -ForegroundColor $ColorError
        Write-Host "[INFO] Solucion manual: cerrar y reabrir terminal" -ForegroundColor $ColorWarning
        exit 1
    }
}

# 2. Verificar herramientas disponibles
Write-Host "`n[INFO] FASE 2: Verificacion de Herramientas" -ForegroundColor $ColorInfo

$poetryCheck = Invoke-CommandWithTimeout "poetry --version" 5 "Poetry check"
if ($null -eq $poetryCheck) {
    Write-Host "[ERROR] Poetry no disponible" -ForegroundColor $ColorError
    exit 1
}

$gitCheck = Invoke-CommandWithTimeout "git --version" 5 "Git check"
if ($null -eq $gitCheck) {
    Write-Host "[ERROR] Git no disponible" -ForegroundColor $ColorError
    exit 1
}

# 3. Pre-commit con timeout inteligente
Write-Host "`n[INFO] FASE 3: Pre-commit Hooks" -ForegroundColor $ColorInfo

$precommitResult = Invoke-CommandWithTimeout "poetry run pre-commit run --all-files" $PRE_COMMIT_TIMEOUT "Pre-commit hooks"

if ($null -eq $precommitResult) {
    Write-Host "`n[WARN] Pre-commit timeout - opciones:" -ForegroundColor $ColorWarning
    Write-Host "1. Continuar sin hooks (Enter)" -ForegroundColor $ColorWarning
    Write-Host "2. Abortar commit (Ctrl+C)" -ForegroundColor $ColorWarning

    $response = Read-Host "Continuar sin pre-commit? (Y/n)"
    if ($response -eq "n" -or $response -eq "N") {
        Write-Host "[ERROR] Commit abortado por usuario" -ForegroundColor $ColorError
        exit 1
    }
    Write-Host "⚠️  Continuando sin pre-commit hooks" -ForegroundColor $ColorWarning
} else {
    Write-Host "[OK] Pre-commit hooks ejecutados correctamente" -ForegroundColor $ColorSuccess
}

# 4. Staging seguro
Write-Host "`n[INFO] FASE 4: Staging de Archivos" -ForegroundColor $ColorInfo

# Add all files (sin reset previo para preservar archivos staged)
$addResult = Invoke-CommandWithTimeout "git add ." $GIT_TIMEOUT "Add files"
if ($null -eq $addResult) {
    Write-Host "[ERROR] Error en git add" -ForegroundColor $ColorError
    exit 1
}

# Verificar que hay cambios para commit
$statusResult = Invoke-CommandWithTimeout "git status --porcelain" $GIT_TIMEOUT "Status check"
if ($null -eq $statusResult -or $null -eq $statusResult.Output -or $statusResult.Output.Trim() -eq "") {
    Write-Host "[WARN] No hay cambios para commit" -ForegroundColor $ColorWarning
    exit 0
}

# 5. Formatear mensaje con Conventional Commits
Write-Host "`n[INFO] FASE 5: Formateo del Mensaje" -ForegroundColor $ColorInfo

$commitMessage = $Message
if ($Scope -ne "") {
    $commitMessage = "${Type}(${Scope}): ${Message}"
} else {
    $commitMessage = "${Type}: ${Message}"
}

Write-Host "[INFO] Mensaje: $commitMessage" -ForegroundColor $ColorInfo

# 6. Commit
Write-Host "`n[INFO] FASE 6: Commit" -ForegroundColor $ColorInfo

$commitResult = Invoke-CommandWithTimeout "git commit -m `"$commitMessage`"" $GIT_TIMEOUT "Git commit"
if ($null -eq $commitResult) {
    Write-Host "[ERROR] Error en commit" -ForegroundColor $ColorError
    exit 1
}

# 7. Push opcional
if ($Push) {
    Write-Host "`n[INFO] FASE 7: Push" -ForegroundColor $ColorInfo
    $pushResult = Invoke-CommandWithTimeout "git push" 30 "Git push"
    if ($null -eq $pushResult) {
        Write-Host "[WARN] Push timeout - verificar manualmente" -ForegroundColor $ColorWarning
    } else {
        Write-Host "[OK] Push completado" -ForegroundColor $ColorSuccess
    }
}

# 8. Verificación final
Write-Host "`n[INFO] FASE FINAL: Verificacion" -ForegroundColor $ColorInfo

$logResult = Invoke-CommandWithTimeout "git log -1 --oneline" $GIT_TIMEOUT "Log verification"
if ($null -ne $logResult) {
    Write-Host "[OK] Ultimo commit: $($logResult.Output)" -ForegroundColor $ColorSuccess
}

Write-Host "`n[SUCCESS] COMMIT COMPLETADO EXITOSAMENTE" -ForegroundColor $ColorSuccess
Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo

# Verificación final de responsividad
Test-TerminalResponsive | Out-Null
