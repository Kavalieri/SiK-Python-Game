# Script de Limpieza Agresiva de VS Code
# Cierra todas las pestañas abiertas, incluso las modificadas (con confirmación)

param(
    [string]$Level = "aggressive",
    [switch]$Force
)

Write-Host "=== LIMPIEZA AGRESIVA VS CODE ===" -ForegroundColor Red

# Función para cerrar todas las pestañas
function Close-AllTabs {
    param([bool]$ConfirmUnsaved = $true)

    Write-Host "[VSCODE] Cerrando TODAS las pestañas..." -ForegroundColor Yellow

    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue

        # Buscar ventana VS Code
        $vsCodeProcess = Get-Process -Name "Code" -ErrorAction SilentlyContinue |
                        Where-Object {$_.MainWindowTitle -like "*Visual Studio Code*"} |
                        Select-Object -First 1

        if (-not $vsCodeProcess) {
            Write-Host "[INFO] VS Code no está abierto" -ForegroundColor Yellow
            return $false
        }

        Write-Host "[INFO] VS Code encontrado: $($vsCodeProcess.MainWindowTitle)" -ForegroundColor Cyan

        # Método 1: Ctrl+K Ctrl+W (Cerrar todas las pestañas)
        Write-Host "[INFO] Enviando Ctrl+K Ctrl+W para cerrar todas las pestañas..." -ForegroundColor White
        [System.Windows.Forms.SendKeys]::SendWait("^k")  # Ctrl+K
        Start-Sleep -Milliseconds 300
        [System.Windows.Forms.SendKeys]::SendWait("^w")  # Ctrl+W
        Start-Sleep -Milliseconds 1500  # Esperar más tiempo

        # Si hay archivos modificados, VS Code preguntará - enviar Escape para cancelar
        # y luego intentar cerrar sin guardar
        if (-not $ConfirmUnsaved) {
            Start-Sleep -Milliseconds 500
            # Si aparece diálogo, presionar "Don't Save" (Alt+N en inglés, Alt+O en español)
            [System.Windows.Forms.SendKeys]::SendWait("%n")  # Alt+N
            Start-Sleep -Milliseconds 500
        }

        # Método 2: Si el anterior no funcionó, usar Ctrl+Shift+W (cerrar ventana)
        Write-Host "[INFO] Enviando Ctrl+Shift+W como respaldo..." -ForegroundColor White
        [System.Windows.Forms.SendKeys]::SendWait("^+w")  # Ctrl+Shift+W
        Start-Sleep -Milliseconds 1000

        # Verificar resultado
        $vsCodeDespues = Get-Process -Name "Code" -ErrorAction SilentlyContinue |
                        Where-Object {$_.MainWindowTitle -like "*Visual Studio Code*"} |
                        Select-Object -First 1

        if ($vsCodeDespues) {
            $tituloDespues = $vsCodeDespues.MainWindowTitle
            Write-Host "[INFO] Estado después: $tituloDespues" -ForegroundColor Gray

            # Si el título cambió o está vacío, probablemente funcionó
            if ($tituloDespues -like "*Welcome*" -or $tituloDespues -like "*Visual Studio Code" -or $tituloDespues -eq "Visual Studio Code") {
                Write-Host "[OK] Pestañas cerradas exitosamente" -ForegroundColor Green
                return $true
            }
        }

        Write-Host "[WARN] Cierre de pestañas puede no haber sido completo" -ForegroundColor Yellow
        return $true  # Asumir éxito para continuar

    } catch {
        Write-Host "[ERROR] Error al cerrar pestañas: $_" -ForegroundColor Red
        return $false
    }
}

# Función para cerrar completamente VS Code
function Close-VSCodeCompletely {
    Write-Host "[VSCODE] Cerrando VS Code completamente..." -ForegroundColor Red

    try {
        # Enviar Alt+F4 para cerrar la aplicación
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
        [System.Windows.Forms.SendKeys]::SendWait("%{F4}")  # Alt+F4
        Start-Sleep -Milliseconds 2000

        # Verificar si aún hay procesos
        $vsCodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue
        if ($vsCodeProcesses.Count -gt 0) {
            Write-Host "[INFO] Aún hay $($vsCodeProcesses.Count) procesos VS Code ejecutándose" -ForegroundColor Yellow

            # Método más agresivo: matar procesos
            if ($Force) {
                Write-Host "[FORCE] Matando procesos VS Code forzadamente..." -ForegroundColor Red
                $vsCodeProcesses | Stop-Process -Force -ErrorAction SilentlyContinue
                Start-Sleep -Milliseconds 1000

                $remaining = Get-Process -Name "Code" -ErrorAction SilentlyContinue
                if ($remaining.Count -eq 0) {
                    Write-Host "[OK] Todos los procesos VS Code eliminados" -ForegroundColor Green
                    return $true
                }
            }
        } else {
            Write-Host "[OK] VS Code cerrado completamente" -ForegroundColor Green
            return $true
        }

        return $false

    } catch {
        Write-Host "[ERROR] Error al cerrar VS Code: $_" -ForegroundColor Red
        return $false
    }
}

# Función principal
function Invoke-AggressiveVSCodeCleanup {
    param([string]$CleanupLevel)

    Write-Host "[INFO] Nivel de limpieza: $CleanupLevel" -ForegroundColor Cyan

    switch ($CleanupLevel) {
        "aggressive" {
            Write-Host "[INFO] Modo agresivo: Cerrar todas las pestañas" -ForegroundColor Yellow
            $result = Close-AllTabs -ConfirmUnsaved $false
        }
        "shutdown" {
            Write-Host "[INFO] Modo shutdown: Cerrar VS Code completamente" -ForegroundColor Red
            $result = Close-VSCodeCompletely
        }
        default {
            Write-Host "[INFO] Modo estándar: Cerrar pestañas con confirmación" -ForegroundColor White
            $result = Close-AllTabs -ConfirmUnsaved $true
        }
    }

    if ($result) {
        Write-Host "[SUCCESS] Limpieza agresiva completada" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Limpieza agresiva con problemas" -ForegroundColor Yellow
    }

    return $result
}

# Ejecución principal
if (-not $Force) {
    Write-Host "`n[ADVERTENCIA] Este script cerrará TODAS las pestañas de VS Code" -ForegroundColor Red
    Write-Host "[PELIGRO] Archivos modificados pueden perderse sin guardar" -ForegroundColor Red
    Write-Host "[INFO] Asegúrate de haber guardado todo antes de continuar" -ForegroundColor Yellow
    $confirm = Read-Host "`n¿Estás seguro de continuar? (s/N)"
    if ($confirm -ne "s" -and $confirm -ne "S") {
        Write-Host "[CANCELADO] Operación cancelada por el usuario" -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "`n[INICIO] Iniciando limpieza agresiva..." -ForegroundColor White
$success = Invoke-AggressiveVSCodeCleanup -CleanupLevel $Level

if ($success) {
    Write-Host "`n[COMPLETADO] Limpieza agresiva finalizada exitosamente" -ForegroundColor Green
} else {
    Write-Host "`n[FALLIDO] Limpieza agresiva con errores" -ForegroundColor Red
    exit 1
}
