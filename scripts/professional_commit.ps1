# PowerShell Professional Commit Script
# Compatible con PowerShell Pro Tools y PowerShell Universal
# Autor: Sistema de Refactorización SiK Python Game
# Fecha: 30 de Julio, 2025

param(
    [Parameter(Mandatory=$true)]
    [string]$CommitMessage
)

# Configuración para compatibilidad con PowerShell Pro Tools
$PSDefaultParameterValues = @{
    'Out-File:Encoding' = 'UTF8'
    'Set-Content:Encoding' = 'UTF8'
}

# Configurar salida para caracteres Unicode
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Write-StatusMessage {
    param([string]$Message, [string]$Type = "Info")

    $timestamp = Get-Date -Format "HH:mm:ss"
    switch ($Type) {
        "Success" { Write-Host "[$timestamp] ✅ $Message" -ForegroundColor Green }
        "Warning" { Write-Host "[$timestamp] ⚠️  $Message" -ForegroundColor Yellow }
        "Error"   { Write-Host "[$timestamp] ❌ $Message" -ForegroundColor Red }
        "Info"    { Write-Host "[$timestamp] 🔍 $Message" -ForegroundColor Cyan }
        default   { Write-Host "[$timestamp] $Message" }
    }
}

function Test-Command {
    param([string]$Command)

    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

function Invoke-SafeCommand {
    param(
        [string[]]$Command,
        [string]$Description,
        [int]$TimeoutSeconds = 60
    )

    Write-StatusMessage "Ejecutando: $Description" "Info"

    try {
        $job = Start-Job -ScriptBlock {
            param($cmd, $cmdArgs)
            & $cmd @cmdArgs
        } -ArgumentList $Command[0], $Command[1..($Command.Length-1)]

        $completed = Wait-Job $job -Timeout $TimeoutSeconds
        $result = Receive-Job $job
        Remove-Job $job -Force

        if ($completed) {
            if ($job.State -eq "Completed") {
                Write-StatusMessage "$Description completado exitosamente" "Success"
                return @{ Success = $true; Output = $result }
            } else {
                Write-StatusMessage "$Description falló" "Error"
                return @{ Success = $false; Output = $result }
            }
        } else {
            Write-StatusMessage "$Description excedió el timeout de $TimeoutSeconds segundos" "Error"
            return @{ Success = $false; Output = "Timeout" }
        }
    }
    catch {
        Write-StatusMessage "Error ejecutando $Description`: $($_.Exception.Message)" "Error"
        return @{ Success = $false; Output = $_.Exception.Message }
    }
}

function Test-GitRepository {
    Write-StatusMessage "Validando repositorio Git..." "Info"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "No se encuentra directorio .git" "Error"
        return $false
    }

    $gitStatus = Invoke-SafeCommand @("git", "status", "--porcelain") "Verificar estado Git"
    if (-not $gitStatus.Success) {
        Write-StatusMessage "Error verificando estado de Git" "Error"
        return $false
    }

    Write-StatusMessage "Repositorio Git válido" "Success"
    return $true
}

function Invoke-PreCommitValidations {
    Write-StatusMessage "Iniciando validaciones pre-commit..." "Info"

    # 1. Verificar Poetry
    if (-not (Test-Command "poetry")) {
        Write-StatusMessage "Poetry no encontrado" "Error"
        return $false
    }

    # 2. Formatear código con Ruff
    $ruffFormat = Invoke-SafeCommand @("poetry", "run", "ruff", "format", "src/", "scripts/", "tests/") "Formateo Ruff"
    if (-not $ruffFormat.Success) {
        Write-StatusMessage "Error en formateo Ruff" "Error"
        return $false
    }

    # 3. Linting con Ruff
    $ruffCheck = Invoke-SafeCommand @("poetry", "run", "ruff", "check", "src/", "scripts/", "tests/") "Linting Ruff"
    if (-not $ruffCheck.Success) {
        Write-StatusMessage "Advertencias en linting (continuando)" "Warning"
    }

    # 4. Verificar sintaxis Python en archivos críticos
    $criticalFiles = @(
        "src/entities/entity.py",
        "src/entities/entity_core.py",
        "src/entities/entity_types.py",
        "src/entities/entity_effects.py",
        "src/entities/entity_rendering.py"
    )

    foreach ($file in $criticalFiles) {
        if (Test-Path $file) {
            $pyCompile = Invoke-SafeCommand @("python", "-m", "py_compile", $file) "Verificar sintaxis $file"
            if (-not $pyCompile.Success) {
                Write-StatusMessage "Error de sintaxis en $file" "Error"
                return $false
            }
        }
    }

    Write-StatusMessage "Todas las validaciones pre-commit completadas" "Success"
    return $true
}

function Invoke-GitCommit {
    param([string]$Message)

    Write-StatusMessage "Iniciando proceso de commit..." "Info"

    # 1. Agregar cambios
    $gitAdd = Invoke-SafeCommand @("git", "add", ".") "Agregar cambios"
    if (-not $gitAdd.Success) {
        Write-StatusMessage "Error agregando cambios" "Error"
        return $false
    }

    # 2. Verificar que hay cambios para commitear
    $gitDiff = Invoke-SafeCommand @("git", "diff", "--cached", "--name-only") "Verificar cambios staged"
    if ($gitDiff.Success -and $gitDiff.Output) {
        $stagedFiles = ($gitDiff.Output -split "`n") | Where-Object { $_.Trim() -ne "" }
        Write-StatusMessage "Archivos staged: $($stagedFiles.Count)" "Info"
    } else {
        Write-StatusMessage "No hay cambios para commitear" "Warning"
        return $true
    }

    # 3. Ejecutar commit
    $gitCommit = Invoke-SafeCommand @("git", "commit", "-m", $Message) "Commit"
    if (-not $gitCommit.Success) {
        Write-StatusMessage "Error en commit" "Error"
        return $false
    }

    # 4. Obtener hash del commit
    $gitHash = Invoke-SafeCommand @("git", "rev-parse", "HEAD") "Obtener hash commit"
    if ($gitHash.Success) {
        $hash = $gitHash.Output.Substring(0, 8)
        Write-StatusMessage "Commit exitoso: $hash" "Success"
    }

    return $true
}

function Update-Documentation {
    Write-StatusMessage "Actualizando documentación..." "Info"

    # Ejecutar file_analyzer.py si existe
    if (Test-Path "scripts/file_analyzer.py") {
        $analysis = Invoke-SafeCommand @("python", "scripts/file_analyzer.py") "Análisis de archivos"
        if ($analysis.Success) {
            Write-StatusMessage "Análisis de archivos completado" "Success"
        } else {
            Write-StatusMessage "Error en análisis de archivos" "Warning"
        }
    }

    return $true
}

# SCRIPT PRINCIPAL
function Main {
    param([string]$CommitMessage)

    Write-Host ""
    Write-Host "🚀 COMMIT PROFESIONAL POWERSHELL" -ForegroundColor Magenta
    Write-Host "Compatible con PowerShell Pro Tools" -ForegroundColor Gray
    Write-Host "="*50 -ForegroundColor Gray

    $startTime = Get-Date

    try {
        # Paso 1: Validar repositorio
        if (-not (Test-GitRepository)) {
            Write-StatusMessage "Validación de repositorio falló" "Error"
            exit 1
        }

        # Paso 2: Ejecutar validaciones pre-commit
        if (-not (Invoke-PreCommitValidations)) {
            Write-StatusMessage "Validaciones pre-commit fallaron" "Error"
            exit 1
        }

        # Paso 3: Ejecutar commit
        if (-not (Invoke-GitCommit $CommitMessage)) {
            Write-StatusMessage "Commit falló" "Error"
            exit 1
        }

        # Paso 4: Actualizar documentación
        Update-Documentation | Out-Null

        # Resumen final
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds

        Write-Host ""
        Write-Host "="*50 -ForegroundColor Green
        Write-Host "✅ COMMIT COMPLETADO EXITOSAMENTE" -ForegroundColor Green
        Write-Host "⏱️  Tiempo total: $([math]::Round($duration, 2)) segundos" -ForegroundColor Gray
        Write-Host "="*50 -ForegroundColor Green

        exit 0
    }
    catch {
        Write-StatusMessage "Error inesperado: $($_.Exception.Message)" "Error"
        exit 1
    }
}

# Ejecutar script principal
Main -CommitMessage $CommitMessage
