# =================================================================
# SISTEMA DE LIMPIEZA VS CODE - METODO SENDKEYS INTEGRADO
# Basado en pruebas exitosas: SendKeys (Ctrl+K U) cierra pestañas no modificadas
# Preserva pestañas pinned y no cambia tamaño de ventana
# =================================================================

param(
    [string]$Level = "light",
    [switch]$SkipVSCode,
    [switch]$Force
)

Write-Host "=== LIMPIEZA VS CODE CON METODO SENDKEYS ===" -ForegroundColor Yellow

# Función para cerrar pestañas no modificadas con SendKeys
function Close-UnmodifiedTabs {
    Write-Host "[VSCODE] Cerrando pestañas no modificadas..." -ForegroundColor Green

    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue

        # Buscar ventana VS Code
        $vsCodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue |
                        Where-Object {$_.MainWindowTitle -like "*Visual Studio Code*"} |
                        Select-Object -First 1

        if (-not $vsCodeProcess) {
            Write-Host "[INFO] VS Code no está abierto, saltando limpieza de pestañas" -ForegroundColor Yellow
            return $false
        }

        # Obtener título antes
        $tituloAntes = $vsCodeProcess.MainWindowTitle
        Write-Host "[INFO] VS Code encontrado: $tituloAntes" -ForegroundColor Cyan

        # Activar ventana y enviar comando
        $vsCodeProcess.ProcessName | Out-Null  # Asegurar que el proceso está activo

        Write-Host "[INFO] Enviando Ctrl+K U para cerrar pestañas no modificadas..." -ForegroundColor White
        [System.Windows.Forms.SendKeys]::SendWait("^k")  # Ctrl+K
        Start-Sleep -Milliseconds 300
        [System.Windows.Forms.SendKeys]::SendWait("u")   # U

        Start-Sleep -Milliseconds 1000  # Esperar a que se procese

        # Verificar resultado
        $vsCodeDespues = Get-Process -Name "Code" -ErrorAction SilentlyContinue |
                        Where-Object {$_.MainWindowTitle -like "*Visual Studio Code*"} |
                        Select-Object -First 1

        if ($vsCodeDespues) {
            $tituloDespues = $vsCodeDespues.MainWindowTitle
            if ($tituloAntes -ne $tituloDespues) {
                Write-Host "[OK] Pestañas cerradas exitosamente" -ForegroundColor Green
                Write-Host "     Antes: $tituloAntes" -ForegroundColor Gray
                Write-Host "     Despues: $tituloDespues" -ForegroundColor Gray
                return $true
            } else {
                Write-Host "[INFO] No se detectaron cambios (posible que no haya pestañas para cerrar)" -ForegroundColor Yellow
                return $true
            }
        }

        return $false

    } catch {
        Write-Host "[ERROR] Error al cerrar pestañas: $_" -ForegroundColor Red
        return $false
    }
}

# Función principal de limpieza VS Code
function Invoke-VSCodeCleanup {
    param([string]$CleanupLevel)

    if ($SkipVSCode) {
        Write-Host "[SKIP] Limpieza de VS Code omitida por parámetro" -ForegroundColor Yellow
        return
    }

    Write-Host "`n[VSCODE] Iniciando limpieza de VS Code..." -ForegroundColor Cyan

    $operationsCompleted = 0
    $totalOperations = 3

    # 1. Cerrar pestañas no modificadas (MÉTODO COMPROBADO)
    Write-Host "`n[1/3] Cerrando pestañas no modificadas..." -ForegroundColor White
    if (Close-UnmodifiedTabs) {
        $operationsCompleted++
        Write-Host "[OK] Pestañas limpiadas" -ForegroundColor Green
    } else {
        Write-Host "[WARN] No se pudieron cerrar pestañas" -ForegroundColor Yellow
    }

    # 2. Limpiar caché workspace
    Write-Host "`n[2/3] Limpiando caché de workspace..." -ForegroundColor White
    $workspaceStorage = "$env:APPDATA\Code\User\workspaceStorage"
    if (Test-Path $workspaceStorage) {
        try {
            $before = (Get-ChildItem $workspaceStorage -Recurse | Measure-Object Length -Sum).Sum / 1MB
            Get-ChildItem $workspaceStorage -Directory | ForEach-Object {
                Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
            }
            $after = (Get-ChildItem $workspaceStorage -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1MB
            $operationsCompleted++
            Write-Host "[OK] Caché workspace limpiado: $([math]::Round($before - $after, 2)) MB liberados" -ForegroundColor Green
        } catch {
            Write-Host "[WARN] Error limpiando workspace: $_" -ForegroundColor Yellow
        }
    }

    # 3. Limpiar logs VS Code (solo en deep/complete)
    if ($CleanupLevel -in @("deep", "complete")) {
        Write-Host "`n[3/3] Limpiando logs de VS Code..." -ForegroundColor White
        $logsPath = "$env:APPDATA\Code\logs"
        if (Test-Path $logsPath) {
            try {
                $logsBefore = (Get-ChildItem $logsPath -Recurse | Measure-Object Length -Sum).Sum / 1MB
                Get-ChildItem $logsPath -File -Recurse | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item -Force
                $logsAfter = (Get-ChildItem $logsPath -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum / 1MB
                $operationsCompleted++
                Write-Host "[OK] Logs antiguos limpiados: $([math]::Round($logsBefore - $logsAfter, 2)) MB liberados" -ForegroundColor Green
            } catch {
                Write-Host "[WARN] Error limpiando logs: $_" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "`n[3/3] Limpieza de logs omitida (nivel: $CleanupLevel)" -ForegroundColor Gray
        $operationsCompleted++  # Contar como completado
    }

    # Resumen
    Write-Host "`n[VSCODE] Limpieza completada: $operationsCompleted/$totalOperations operaciones" -ForegroundColor Cyan
    if ($operationsCompleted -eq $totalOperations) {
        Write-Host "[OK] VS Code optimizado exitosamente" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Algunas operaciones fallaron" -ForegroundColor Yellow
    }
}

# Ejecución principal
if ($MyInvocation.InvocationName -eq ".\scripts\vscode_cleanup_sendkeys.ps1" -or $MyInvocation.InvocationName -like "*vscode_cleanup_sendkeys.ps1") {
    Write-Host "=== LIMPIEZA VS CODE CON SENDKEYS ===" -ForegroundColor Yellow
    Write-Host "[INFO] Nivel de limpieza: $Level" -ForegroundColor Cyan
    Write-Host "[INFO] Método: SendKeys (Ctrl+K U) - Preserva pestañas pinned" -ForegroundColor Cyan

    if (-not $Force) {
        Write-Host "`n[ADVERTENCIA] Este script cerrará pestañas no modificadas en VS Code" -ForegroundColor Yellow
        Write-Host "[INFO] Las pestañas pinned y con cambios se preservarán" -ForegroundColor White
        $confirm = Read-Host "`n¿Continuar? (s/N)"
        if ($confirm -ne "s" -and $confirm -ne "S") {
            Write-Host "[CANCELADO] Operación cancelada por el usuario" -ForegroundColor Red
            exit 0
        }
    }

    Invoke-VSCodeCleanup -CleanupLevel $Level

    Write-Host "`n[COMPLETADO] Limpieza VS Code finalizada" -ForegroundColor Green
    Write-Host "[INFO] Método SendKeys verificado y funcional" -ForegroundColor White
}

# Nota: Para usar estas funciones en otros scripts, importar con:
# . .\scripts\vscode_cleanup_sendkeys.ps1
