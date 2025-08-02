# Script de Pruebas del Sistema de Commits
# Realiza tests controlados del flujo completo de commits

param(
    [string]$TestType = "all",
    [switch]$Verbose,
    [switch]$SkipCleanup
)

$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"
$ColorError = "Red"

Write-Host "=== BANCO DE PRUEBAS SISTEMA DE COMMITS ===" -ForegroundColor $ColorInfo
Write-Host "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor $ColorInfo
Write-Host "Tipo de test: $TestType" -ForegroundColor $ColorInfo

# Configuracion de prueba
$TestDir = "test_files"
$LogFile = "logs/test_commits_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

# Funcion de logging
function Write-TestLog {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format 'HH:mm:ss'
    $LogMessage = "[$Timestamp] [$Level] $Message"
    Write-Host $LogMessage -ForegroundColor $(
        switch ($Level) {
            "ERROR" { $ColorError }
            "WARN" { $ColorWarning }
            "SUCCESS" { $ColorSuccess }
            default { $ColorInfo }
        }
    )
    Add-Content -Path $LogFile -Value $LogMessage -ErrorAction SilentlyContinue
}

# Crear directorio de logs si no existe
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

Write-TestLog "Iniciando banco de pruebas del sistema de commits"

# Test 1: Verificar herramientas disponibles
if ($TestType -eq "all" -or $TestType -eq "tools") {
    Write-TestLog "=== TEST 1: VERIFICACION DE HERRAMIENTAS ===" "INFO"

    # Poetry
    try {
        $poetryVersion = poetry --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "Poetry: OK - $poetryVersion" "SUCCESS"
        } else {
            Write-TestLog "Poetry: ERROR - No disponible" "ERROR"
            exit 1
        }
    } catch {
        Write-TestLog "Poetry: EXCEPTION - $_" "ERROR"
        exit 1
    }

    # Git
    try {
        $gitVersion = git --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "Git: OK - $gitVersion" "SUCCESS"
        } else {
            Write-TestLog "Git: ERROR - No disponible" "ERROR"
            exit 1
        }
    } catch {
        Write-TestLog "Git: EXCEPTION - $_" "ERROR"
        exit 1
    }

    # Pre-commit
    try {
        $precommitVersion = poetry run pre-commit --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "Pre-commit: OK - $precommitVersion" "SUCCESS"
        } else {
            Write-TestLog "Pre-commit: ERROR - No disponible" "ERROR"
            exit 1
        }
    } catch {
        Write-TestLog "Pre-commit: EXCEPTION - $_" "ERROR"
        exit 1
    }
}

# Test 2: Verificar estado inicial del repositorio
if ($TestType -eq "all" -or $TestType -eq "repo") {
    Write-TestLog "=== TEST 2: ESTADO DEL REPOSITORIO ===" "INFO"

    $gitStatus = git status --porcelain 2>$null
    $changeCount = if ($gitStatus) { ($gitStatus -split "`n").Count } else { 0 }
    Write-TestLog "Cambios detectados: $changeCount archivos" "INFO"

    if ($changeCount -gt 0) {
        Write-TestLog "Archivos modificados:" "INFO"
        git status --porcelain | ForEach-Object {
            Write-TestLog "  $_" "INFO"
        }
    }
}

# Test 3: Ejecutar pre-commit en archivos de prueba
if ($TestType -eq "all" -or $TestType -eq "precommit") {
    Write-TestLog "=== TEST 3: PRE-COMMIT EN ARCHIVOS DE PRUEBA ===" "INFO"

    if (Test-Path $TestDir) {
        $testFiles = Get-ChildItem $TestDir -File
        Write-TestLog "Archivos de prueba encontrados: $($testFiles.Count)" "INFO"

        foreach ($file in $testFiles) {
            Write-TestLog "Procesando: $($file.Name)" "INFO"

            try {
                $precommitResult = poetry run pre-commit run --files "$TestDir/$($file.Name)" 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-TestLog "Pre-commit en $($file.Name): PASSED" "SUCCESS"
                } else {
                    Write-TestLog "Pre-commit en $($file.Name): FAILED/FIXED" "WARN"
                    if ($Verbose) {
                        Write-TestLog "Output: $precommitResult" "INFO"
                    }
                }
            } catch {
                Write-TestLog "Pre-commit en $($file.Name): EXCEPTION - $_" "ERROR"
            }
        }
    } else {
        Write-TestLog "Directorio $TestDir no encontrado" "WARN"
    }
}

# Test 4: Simulacion de add y commit
if ($TestType -eq "all" -or $TestType -eq "commit") {
    Write-TestLog "=== TEST 4: SIMULACION DE COMMIT ===" "INFO"

    # Backup del estado actual
    Write-TestLog "Creando backup del estado actual..." "INFO"
    $backupBranch = "backup-test-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

    try {
        # Crear rama de backup
        git checkout -b $backupBranch 2>$null
        Write-TestLog "Rama de backup creada: $backupBranch" "SUCCESS"

        # Volver a main
        git checkout main 2>$null
        Write-TestLog "Vuelto a rama main" "SUCCESS"

        # Agregar archivos de prueba
        git add "$TestDir/*" 2>$null
        Write-TestLog "Archivos de prueba agregados al staging" "SUCCESS"

        # Verificar staging area
        $stagedFiles = git diff --cached --name-only 2>$null
        $stagedCount = if ($stagedFiles) { ($stagedFiles -split "`n").Count } else { 0 }
        Write-TestLog "Archivos en staging: $stagedCount" "INFO"

        # Commit de prueba
        $commitMessage = "test: banco de pruebas commits $(Get-Date -Format 'HH:mm:ss')"
        git commit -m $commitMessage 2>$null

        if ($LASTEXITCODE -eq 0) {
            Write-TestLog "Commit de prueba exitoso: $commitMessage" "SUCCESS"

            # Mostrar ultimo commit
            $lastCommit = git log -1 --oneline 2>$null
            Write-TestLog "Ultimo commit: $lastCommit" "INFO"
        } else {
            Write-TestLog "Commit de prueba fallo" "ERROR"
        }

    } catch {
        Write-TestLog "Error en simulacion de commit: $_" "ERROR"
    }
}

# Test 5: Ejecutar script terminal-safe
if ($TestType -eq "all" -or $TestType -eq "safe") {
    Write-TestLog "=== TEST 5: SCRIPT TERMINAL-SAFE ===" "INFO"

    if (Test-Path "scripts/terminal_safe_commit.ps1") {
        Write-TestLog "Probando script terminal-safe..." "INFO"

        # Modificar un archivo de prueba para tener cambios
        $testModFile = "$TestDir/test_modification.txt"
        "Archivo modificado en: $(Get-Date)" | Out-File $testModFile

        try {
            # Ejecutar terminal-safe commit
            & "scripts/terminal_safe_commit.ps1" "test: prueba script terminal-safe" -Type "test" -Scope "scripts"

            if ($LASTEXITCODE -eq 0) {
                Write-TestLog "Script terminal-safe: EXITOSO" "SUCCESS"
            } else {
                Write-TestLog "Script terminal-safe: FALLO" "ERROR"
            }
        } catch {
            Write-TestLog "Script terminal-safe: EXCEPTION - $_" "ERROR"
        }
    } else {
        Write-TestLog "Script terminal-safe no encontrado" "WARN"
    }
}

# Cleanup
if (-not $SkipCleanup) {
    Write-TestLog "=== CLEANUP ===" "INFO"

    # Limpiar archivos de prueba del staging si existen
    git reset HEAD "$TestDir/*" 2>$null | Out-Null
    Write-TestLog "Staging area limpiada" "INFO"

    # Nota: No eliminamos los archivos de prueba para poder inspeccionarlos
    Write-TestLog "Archivos de prueba mantenidos para inspeccion" "INFO"
}

# Resumen final
Write-TestLog "=== RESUMEN FINAL ===" "INFO"
Write-TestLog "Banco de pruebas completado" "SUCCESS"
Write-TestLog "Log guardado en: $LogFile" "INFO"
Write-TestLog "Para limpiar archivos de prueba: Remove-Item $TestDir -Recurse -Force" "INFO"

Write-Host ""
Write-Host "=== BANCO DE PRUEBAS COMPLETADO ===" -ForegroundColor $ColorSuccess
