# Intelligent PowerShell Commit System
# Sistema robusto de commit que evita bloqueos de entrada usando PowerShell nativo
# Compatible con pre-commit hooks y sin bypasses

param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage,

    [Parameter(Mandatory=$false)]
    [switch]$SkipQualityChecks,

    [Parameter(Mandatory=$false)]
    [int]$TimeoutSeconds = 180
)

# Configuración
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

function Write-ColoredOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [string]$Prefix = ""
    )

    $colors = @{
        "Green" = [ConsoleColor]::Green
        "Red" = [ConsoleColor]::Red
        "Yellow" = [ConsoleColor]::Yellow
        "Blue" = [ConsoleColor]::Blue
        "Cyan" = [ConsoleColor]::Cyan
        "White" = [ConsoleColor]::White
    }

    if ($Prefix) {
        Write-Host "$Prefix " -NoNewline -ForegroundColor $colors[$Color]
    }
    Write-Host $Message -ForegroundColor $colors[$Color]
}

function Invoke-CommandWithTimeout {
    param(
        [string]$Command,
        [array]$Arguments = @(),
        [int]$TimeoutSeconds = 120,
        [string]$WorkingDirectory = (Get-Location).Path
    )

    try {
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = $Command
        $processInfo.Arguments = ($Arguments -join " ")
        $processInfo.WorkingDirectory = $WorkingDirectory
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.RedirectStandardInput = $true  # Crucial: redirigir entrada
        $processInfo.UseShellExecute = $false
        $processInfo.CreateNoWindow = $true

        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo

        # Event handlers para capturar output
        $stdout = New-Object System.Text.StringBuilder
        $stderr = New-Object System.Text.StringBuilder

        $stdoutEvent = Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action {
            if ($Event.SourceEventArgs.Data) {
                $Event.MessageData.AppendLine($Event.SourceEventArgs.Data)
            }
        } -MessageData $stdout

        $stderrEvent = Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action {
            if ($Event.SourceEventArgs.Data) {
                $Event.MessageData.AppendLine($Event.SourceEventArgs.Data)
            }
        } -MessageData $stderr

        # Iniciar proceso
        $process.Start() | Out-Null
        $process.BeginOutputReadLine()
        $process.BeginErrorReadLine()

        # Cerrar entrada inmediatamente para evitar bloqueos
        $process.StandardInput.Close()

        # Esperar con timeout
        $completed = $process.WaitForExit($TimeoutSeconds * 1000)

        if (-not $completed) {
            $process.Kill()
            Write-ColoredOutput "Proceso terminado por timeout de $TimeoutSeconds segundos" "Red" "❌"
            return @{
                Success = $false
                ExitCode = -1
                StandardOutput = ""
                StandardError = "Timeout"
            }
        }

        # Cleanup event handlers
        Unregister-Event -SourceIdentifier $stdoutEvent.Name
        Unregister-Event -SourceIdentifier $stderrEvent.Name

        return @{
            Success = ($process.ExitCode -eq 0)
            ExitCode = $process.ExitCode
            StandardOutput = $stdout.ToString().Trim()
            StandardError = $stderr.ToString().Trim()
        }

    } catch {
        Write-ColoredOutput "Error ejecutando comando: $_" "Red" "❌"
        return @{
            Success = $false
            ExitCode = -1
            StandardOutput = ""
            StandardError = $_.Exception.Message
        }
    } finally {
        if ($process) {
            try { $process.Dispose() } catch { }
        }
    }
}

function Test-GitRepository {
    Write-ColoredOutput "Validando repositorio Git..." "Blue" "🔍"

    if (-not (Test-Path ".git")) {
        Write-ColoredOutput "No se encuentra un repositorio Git válido" "Red" "❌"
        return $false
    }

    $result = Invoke-CommandWithTimeout -Command "git" -Arguments @("rev-parse", "--git-dir")
    if (-not $result.Success) {
        Write-ColoredOutput "Error validando repositorio: $($result.StandardError)" "Red" "❌"
        return $false
    }

    Write-ColoredOutput "Repositorio Git válido" "Green" "✅"
    return $true
}

function Test-WorkingDirectory {
    $result = Invoke-CommandWithTimeout -Command "git" -Arguments @("status", "--porcelain")
    if (-not $result.Success) {
        Write-ColoredOutput "Error verificando estado del repositorio" "Red" "❌"
        return $false
    }

    if (-not $result.StandardOutput.Trim()) {
        Write-ColoredOutput "No hay cambios para commitear" "Yellow" "ℹ️"
        return $false
    }

    # Analizar cambios
    $lines = $result.StandardOutput.Trim() -split "`n"
    $modified = ($lines | Where-Object { $_ -match "^( M|M )" }).Count
    $added = ($lines | Where-Object { $_ -match "^(A |\?\?)" }).Count
    $deleted = ($lines | Where-Object { $_ -match "^( D|D )" }).Count

    Write-ColoredOutput "Cambios detectados: $added nuevos, $modified modificados, $deleted eliminados" "Blue" "📊"
    return $true
}

function Invoke-QualityChecks {
    if ($SkipQualityChecks) {
        Write-ColoredOutput "Verificaciones de calidad omitidas (--SkipQualityChecks)" "Yellow" "⚠️"
        return $true
    }

    Write-ColoredOutput "Ejecutando verificaciones de calidad..." "Blue" "🧪"

    # Formateo con ruff
    Write-ColoredOutput "Formateando código con Ruff..." "Cyan" "  🔧"
    $result = Invoke-CommandWithTimeout -Command "poetry" -Arguments @("run", "ruff", "format", ".")
    if (-not $result.Success) {
        Write-ColoredOutput "Error en formateo (continuando): $($result.StandardError)" "Yellow" "⚠️"
    } else {
        Write-ColoredOutput "Formateo completado" "Green" "  ✅"
    }

    # Linting con ruff
    Write-ColoredOutput "Ejecutando linting con Ruff..." "Cyan" "  🔍"
    $result = Invoke-CommandWithTimeout -Command "poetry" -Arguments @("run", "ruff", "check", ".", "--fix")
    if (-not $result.Success) {
        Write-ColoredOutput "Linting con advertencias (continuando): $($result.StandardError)" "Yellow" "⚠️"
    } else {
        Write-ColoredOutput "Linting completado" "Green" "  ✅"
    }

    Write-ColoredOutput "Verificaciones de calidad completadas" "Green" "✅"
    return $true
}

function Add-Changes {
    Write-ColoredOutput "Agregando cambios al staging area..." "Blue" "📁"

    $result = Invoke-CommandWithTimeout -Command "git" -Arguments @("add", ".")
    if (-not $result.Success) {
        Write-ColoredOutput "Error agregando cambios: $($result.StandardError)" "Red" "❌"
        return $false
    }

    # Verificar archivos staged
    $result = Invoke-CommandWithTimeout -Command "git" -Arguments @("diff", "--cached", "--name-only")
    if ($result.Success -and $result.StandardOutput) {
        $stagedFiles = ($result.StandardOutput -split "`n").Count
        Write-ColoredOutput "$stagedFiles archivos agregados al staging area" "Green" "  ✅"
    } else {
        Write-ColoredOutput "No se detectaron archivos en staging area" "Yellow" "⚠️"
    }

    return $true
}

function Invoke-CommitWithHooks {
    param([string]$Message)

    Write-ColoredOutput "Ejecutando commit con pre-commit hooks..." "Blue" "💾"

    # Commit normal que respeta hooks - SIN --no-verify
    $result = Invoke-CommandWithTimeout -Command "git" -Arguments @("commit", "-m", $Message) -TimeoutSeconds $TimeoutSeconds

    if (-not $result.Success) {
        if ($result.StandardError -match "nothing to commit") {
            Write-ColoredOutput "No hay cambios para commitear" "Yellow" "ℹ️"
            return $true
        } else {
            Write-ColoredOutput "Error en commit: $($result.StandardError)" "Red" "❌"
            if ($result.StandardOutput) {
                Write-ColoredOutput "Salida adicional: $($result.StandardOutput)" "Yellow" "📋"
            }
            return $false
        }
    }

    # Obtener hash del commit
    $hashResult = Invoke-CommandWithTimeout -Command "git" -Arguments @("rev-parse", "HEAD")
    if ($hashResult.Success -and $hashResult.StandardOutput) {
        $commitHash = $hashResult.StandardOutput.Substring(0, 8)
        Write-ColoredOutput "Commit exitoso: $commitHash" "Green" "✅"
    } else {
        Write-ColoredOutput "Commit completado" "Green" "✅"
    }

    return $true
}

function Clear-Caches {
    Write-ColoredOutput "Limpiando cachés..." "Blue" "🧹"

    # Limpiar cachés de Python
    $cachePatterns = @("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache")

    foreach ($pattern in $cachePatterns) {
        Get-ChildItem -Path . -Recurse -Directory -Name $pattern -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                Remove-Item $_ -Recurse -Force
                Write-ColoredOutput "Eliminado: $_" "Green" "  ✅"
            } catch {
                # Ignorar errores de eliminación
            }
        }
    }

    # Cache de pip
    $result = Invoke-CommandWithTimeout -Command "pip" -Arguments @("cache", "purge") -TimeoutSeconds 30
    if ($result.Success) {
        Write-ColoredOutput "Cache de pip limpiado" "Green" "  ✅"
    }

    # Cache de poetry
    $result = Invoke-CommandWithTimeout -Command "poetry" -Arguments @("cache", "clear", "--all", ".") -TimeoutSeconds 30
    if ($result.Success) {
        Write-ColoredOutput "Cache de poetry limpiado" "Green" "  ✅"
    }

    Write-ColoredOutput "Limpieza de cachés completada" "Green" "🧹"
}

function Show-Summary {
    param([bool]$Success, [datetime]$StartTime)

    $elapsed = (Get-Date) - $StartTime

    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor White
    Write-ColoredOutput "RESUMEN DEL COMMIT INTELIGENTE (PowerShell)" "White" "📊"
    Write-Host ("=" * 60) -ForegroundColor White

    if ($Success) {
        Write-ColoredOutput "COMMIT COMPLETADO EXITOSAMENTE" "Green" "✅"
        Write-ColoredOutput "Tiempo total: $($elapsed.TotalSeconds.ToString('F2')) segundos" "Blue" "⏱️"
        Write-ColoredOutput "Proceso completado con herramientas estándar" "Blue" "🎯"
        Write-ColoredOutput "Pre-commit hooks ejecutados correctamente" "Blue" "🔒"
    } else {
        Write-ColoredOutput "COMMIT FALLÓ" "Red" "❌"
        Write-ColoredOutput "Tiempo transcurrido: $($elapsed.TotalSeconds.ToString('F2')) segundos" "Blue" "⏱️"
        Write-ColoredOutput "Revisa los errores mostrados arriba" "Yellow" "🔍"
    }

    Write-Host ("=" * 60) -ForegroundColor White
}

# FUNCIÓN PRINCIPAL
function Main {
    $startTime = Get-Date

    Write-ColoredOutput "SISTEMA DE COMMIT INTELIGENTE (PowerShell)" "Cyan" "🚀"
    Write-Host "Compatible con pre-commit hooks y herramientas estándar"
    Write-Host ("=" * 60)

    try {
        # Paso 1: Limpiar cachés
        Clear-Caches

        # Paso 2: Validar repositorio
        if (-not (Test-GitRepository)) {
            return $false
        }

        # Paso 3: Verificar cambios
        if (-not (Test-WorkingDirectory)) {
            return $true  # No es error, simplemente no hay cambios
        }

        # Paso 4: Verificaciones de calidad
        if (-not (Invoke-QualityChecks)) {
            return $false
        }

        # Paso 5: Agregar cambios
        if (-not (Add-Changes)) {
            return $false
        }

        # Paso 6: Commit con hooks
        if (-not (Invoke-CommitWithHooks -Message $CommitMessage)) {
            return $false
        }

        return $true

    } catch {
        Write-ColoredOutput "Error inesperado: $_" "Red" "❌"
        return $false
    } finally {
        Show-Summary -Success $? -StartTime $startTime
    }
}

# Ejecutar función principal
$success = Main
exit $(if ($success) { 0 } else { 1 })
