# Test del Sistema de Cierre de Sesión
# Valida que el sistema de limpieza agresiva funcione correctamente

param(
    [switch]$FullTest,
    [switch]$QuickTest
)

Write-Host "=== TEST SISTEMA CIERRE DE SESION ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date)" -ForegroundColor Gray

# Función para crear archivos de prueba
function New-TestFiles {
    Write-Host "[TEST] Creando archivos de prueba..." -ForegroundColor Yellow

    $testFiles = @(
        "archivo_new.py",
        "archivo_backup.py",
        "archivo_old.py",
        "archivo_optimized.py",
        "archivo_temp.tmp"
    )

    foreach ($file in $testFiles) {
        $content = "# Archivo de prueba creado en $(Get-Date)"
        Set-Content -Path $file -Value $content
        Write-Host "   Creado: $file" -ForegroundColor Gray
    }

    return $testFiles
}

# Función para verificar que los archivos fueron eliminados
function Test-FilesCleanup {
    param([array]$TestFiles)

    Write-Host "[TEST] Verificando limpieza de archivos..." -ForegroundColor Yellow

    $remaining = @()
    foreach ($file in $TestFiles) {
        if (Test-Path $file) {
            $remaining += $file
        }
    }

    if ($remaining.Count -eq 0) {
        Write-Host "   [OK] Todos los archivos de prueba eliminados" -ForegroundColor Green
        return $true
    } else {
        Write-Host "   [ERROR] Archivos restantes: $($remaining -join ', ')" -ForegroundColor Red
        return $false
    }
}

# Función para verificar VS Code
function Test-VSCodeState {
    Write-Host "[TEST] Verificando estado de VS Code..." -ForegroundColor Yellow

    $vsCodeProcesses = Get-Process -Name "Code" -ErrorAction SilentlyContinue

    if ($vsCodeProcesses.Count -eq 0) {
        Write-Host "   [OK] VS Code cerrado completamente" -ForegroundColor Green
        return $true
    } else {
        Write-Host "   [INFO] VS Code aún ejecutándose ($($vsCodeProcesses.Count) procesos)" -ForegroundColor Yellow

        # Mostrar información de procesos
        foreach ($proc in $vsCodeProcesses) {
            $title = if ($proc.MainWindowTitle) { $proc.MainWindowTitle } else { "Sin ventana principal" }
            Write-Host "     Proceso: $($proc.Id) - $title" -ForegroundColor Gray
        }

        return $false
    }
}

# Función para validar scripts
function Test-ScriptAvailability {
    Write-Host "[TEST] Verificando disponibilidad de scripts..." -ForegroundColor Yellow

    $scripts = @(
        ".\dev-tools\scripts\comprehensive_cleanup.ps1",
        ".\dev-tools\scripts\vscode_aggressive_cleanup.ps1"
    )

    $allFound = $true
    foreach ($script in $scripts) {
        if (Test-Path $script) {
            Write-Host "   [OK] Encontrado: $script" -ForegroundColor Green
        } else {
            Write-Host "   [ERROR] No encontrado: $script" -ForegroundColor Red
            $allFound = $false
        }
    }

    return $allFound
}

# Test principal
function Start-SessionCloseTest {
    param([bool]$FullMode = $false)

    Write-Host "`n[INICIO] Iniciando test del sistema..." -ForegroundColor White

    # 1. Verificar disponibilidad de scripts
    $scriptsOk = Test-ScriptAvailability
    if (-not $scriptsOk) {
        Write-Host "[ERROR] Scripts no disponibles, abortando test" -ForegroundColor Red
        return $false
    }

    # 2. Crear archivos de prueba
    $testFiles = New-TestFiles

    # 3. Verificar estado inicial de VS Code
    $initialVSCodeState = Test-VSCodeState
    Write-Host "   Estado inicial VS Code: $(if($initialVSCodeState) {'Cerrado'} else {'Ejecutándose'})" -ForegroundColor Cyan

    # 4. Ejecutar limpieza de shutdown si es test completo
    if ($FullMode) {
        Write-Host "`n[TEST] Ejecutando limpieza de shutdown..." -ForegroundColor Yellow

        try {
            & ".\dev-tools\scripts\comprehensive_cleanup.ps1" -Level "shutdown" -Force
            Write-Host "   [OK] Limpieza ejecutada sin errores" -ForegroundColor Green
        } catch {
            Write-Host "   [ERROR] Error en limpieza: $_" -ForegroundColor Red
            return $false
        }

        # Esperar un momento para que se complete
        Start-Sleep -Seconds 3

        # Verificar estado post-limpieza de VS Code
        $postCleanupVSCode = Test-VSCodeState

        if (-not $initialVSCodeState -and $postCleanupVSCode) {
            Write-Host "   [OK] VS Code cerrado exitosamente por el script" -ForegroundColor Green
        }
    } else {
        Write-Host "`n[TEST] Ejecutando solo limpieza de archivos..." -ForegroundColor Yellow

        try {
            & ".\dev-tools\scripts\comprehensive_cleanup.ps1" -Level "light" -Force
            Write-Host "   [OK] Limpieza light ejecutada sin errores" -ForegroundColor Green
        } catch {
            Write-Host "   [ERROR] Error en limpieza: $_" -ForegroundColor Red
            return $false
        }
    }

    # 5. Verificar limpieza de archivos
    $filesCleanedOk = Test-FilesCleanup -TestFiles $testFiles

    # 6. Resultado final
    if ($filesCleanedOk) {
        Write-Host "`n[SUCCESS] TEST COMPLETADO EXITOSAMENTE" -ForegroundColor Green
        return $true
    } else {
        Write-Host "`n[FAILURE] TEST FALLIDO - Ver errores arriba" -ForegroundColor Red
        return $false
    }
}

# Ejecutar test según parámetros
Write-Host "Directorio de trabajo: $(Get-Location)" -ForegroundColor Gray

if (-not (Test-Path "src") -or -not (Test-Path "pyproject.toml")) {
    Write-Host "[ERROR] No estás en el directorio raíz del proyecto" -ForegroundColor Red
    Write-Host "Navega a la carpeta SiK-Python-Game antes de ejecutar el test" -ForegroundColor Yellow
    exit 1
}

if ($FullTest) {
    Write-Host "[INFO] Modo: Test completo (incluye cierre VS Code)" -ForegroundColor Cyan
    $result = Start-SessionCloseTest -FullMode $true
} else {
    Write-Host "[INFO] Modo: Test rápido (solo limpieza archivos)" -ForegroundColor Cyan
    $result = Start-SessionCloseTest -FullMode $false
}

if ($result) {
    Write-Host "`n[FINAL] Sistema de cierre de sesion VALIDADO" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n[FINAL] Sistema de cierre de sesion REQUIERE REVISION" -ForegroundColor Red
    exit 1
}
