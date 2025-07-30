# =============================================================================
# AUTO-CLEANUP CONFIGURATION - INTEGRACIÓN CON MÉTODO UNIFICADO
# =============================================================================
# Configura limpieza automática del entorno de trabajo
# Uso: .\scripts\setup_auto_cleanup.ps1 [-Enable] [-Disable] [-Configure]
# =============================================================================

param(
    [switch]$Enable,
    [switch]$Disable,
    [switch]$Configure,
    [ValidateSet("light", "deep", "complete")]
    [string]$DefaultLevel = "light",
    [switch]$CleanAfterCommit,
    [switch]$CleanAfterPhase
)

$ColorInfo = "Cyan"
$ColorSuccess = "Green"
$ColorWarning = "Yellow"

Write-Host "[AUTO-CLEANUP] Configuración de limpieza automática" -ForegroundColor $ColorInfo

# =============================================================================
# CONFIGURACIÓN DE TRIGGERS
# =============================================================================

function Enable-AutoCleanup {
    Write-Host "`n[CONFIG] Habilitando limpieza automática..." -ForegroundColor $ColorInfo

    # Crear archivo de configuración
    $config = @{
        enabled = $true
        defaultLevel = $DefaultLevel
        cleanAfterCommit = $CleanAfterCommit.IsPresent
        cleanAfterPhase = $CleanAfterPhase.IsPresent
        lastCleanup = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }

    $configPath = ".vscode/auto-cleanup.json"
    New-Item -ItemType Directory -Path ".vscode" -Force -ErrorAction SilentlyContinue | Out-Null
    $config | ConvertTo-Json | Set-Content $configPath

    Write-Host "[OK] Configuración guardada en: $configPath" -ForegroundColor $ColorSuccess

    # Configurar VS Code tasks
    Setup-VSCodeTasks

    # Configurar keybindings
    Setup-VSCodeKeybindings

    Write-Host "[SUCCESS] Limpieza automática habilitada" -ForegroundColor $ColorSuccess
}

function Setup-VSCodeTasks {
    Write-Host "`n[TASKS] Configurando tareas de VS Code..." -ForegroundColor $ColorInfo

    $tasksPath = ".vscode/tasks.json"
    $tasks = @{
        version = "2.0.0"
        tasks = @(
            @{
                label = "Cleanup: Light"
                type = "shell"
                command = ".\scripts\workspace_cleanup.ps1"
                args = @("-Level", "light")
                group = "build"
                presentation = @{
                    echo = $true
                    reveal = "silent"
                    focus = $false
                    panel = "shared"
                    showReuseMessage = $false
                }
                problemMatcher = @()
            },
            @{
                label = "Cleanup: Deep"
                type = "shell"
                command = ".\scripts\workspace_cleanup.ps1"
                args = @("-Level", "deep")
                group = "build"
                presentation = @{
                    echo = $true
                    reveal = "always"
                    focus = $false
                }
                problemMatcher = @()
            },
            @{
                label = "Cleanup: Close Tabs"
                type = "shell"
                command = ".\scripts\workspace_cleanup.ps1"
                args = @("-CloseTabs")
                group = "build"
                presentation = @{
                    echo = $false
                    reveal = "silent"
                    focus = $false
                }
                problemMatcher = @()
            }
        )
    }

    New-Item -ItemType Directory -Path ".vscode" -Force -ErrorAction SilentlyContinue | Out-Null
    $tasks | ConvertTo-Json -Depth 10 | Set-Content $tasksPath

    Write-Host "[OK] Tareas configuradas: Cleanup Light/Deep/Close Tabs" -ForegroundColor $ColorSuccess
}

function Setup-VSCodeKeybindings {
    Write-Host "`n[KEYBINDINGS] Configurando atajos de teclado..." -ForegroundColor $ColorInfo

    $keybindingsPath = ".vscode/keybindings.json"
    $keybindings = @(
        @{
            key = "ctrl+k ctrl+l"
            command = "workbench.action.tasks.runTask"
            args = "Cleanup: Light"
        },
        @{
            key = "ctrl+k ctrl+t"
            command = "workbench.action.tasks.runTask"
            args = "Cleanup: Close Tabs"
        },
        @{
            key = "ctrl+k ctrl+d"
            command = "workbench.action.tasks.runTask"
            args = "Cleanup: Deep"
        }
    )

    $keybindings | ConvertTo-Json -Depth 5 | Set-Content $keybindingsPath

    Write-Host "[OK] Atajos configurados:" -ForegroundColor $ColorSuccess
    Write-Host "      Ctrl+K Ctrl+L : Cleanup Light" -ForegroundColor $ColorInfo
    Write-Host "      Ctrl+K Ctrl+T : Close Tabs" -ForegroundColor $ColorInfo
    Write-Host "      Ctrl+K Ctrl+D : Cleanup Deep" -ForegroundColor $ColorInfo
}

function Show-Configuration {
    Write-Host "`n[INFO] Configuración actual:" -ForegroundColor $ColorInfo
    Write-Host "================================" -ForegroundColor $ColorInfo

    $configPath = ".vscode/auto-cleanup.json"
    if (Test-Path $configPath) {
        $config = Get-Content $configPath | ConvertFrom-Json
        Write-Host "Estado: " -NoNewline -ForegroundColor $ColorInfo
        if ($config.enabled) {
            Write-Host "HABILITADO" -ForegroundColor $ColorSuccess
        } else {
            Write-Host "DESHABILITADO" -ForegroundColor $ColorWarning
        }
        Write-Host "Nivel por defecto: $($config.defaultLevel)" -ForegroundColor $ColorInfo
        Write-Host "Limpieza post-commit: $($config.cleanAfterCommit)" -ForegroundColor $ColorInfo
        Write-Host "Limpieza post-fase: $($config.cleanAfterPhase)" -ForegroundColor $ColorInfo
        Write-Host "Última limpieza: $($config.lastCleanup)" -ForegroundColor $ColorInfo
    } else {
        Write-Host "Estado: NO CONFIGURADO" -ForegroundColor $ColorWarning
    }

    # Verificar archivos de configuración
    $files = @(".vscode/tasks.json", ".vscode/keybindings.json")
    foreach ($file in $files) {
        $status = if (Test-Path $file) { "✅" } else { "❌" }
        Write-Host "$status $file" -ForegroundColor $ColorInfo
    }
}

# =============================================================================
# LÓGICA PRINCIPAL
# =============================================================================

if ($Configure -or (-not $Enable -and -not $Disable)) {
    Show-Configuration
}

if ($Enable) {
    Enable-AutoCleanup
}

if ($Disable) {
    Write-Host "`n[CONFIG] Deshabilitando limpieza automática..." -ForegroundColor $ColorWarning
    $configPath = ".vscode/auto-cleanup.json"
    if (Test-Path $configPath) {
        $config = Get-Content $configPath | ConvertFrom-Json
        $config.enabled = $false
        $config | ConvertTo-Json | Set-Content $configPath
        Write-Host "[OK] Limpieza automática deshabilitada" -ForegroundColor $ColorSuccess
    }
}

Write-Host "`n[INFO] Para usar las funciones:" -ForegroundColor $ColorInfo
Write-Host "  - Comandos: Ctrl+Shift+P > 'Tasks: Run Task' > 'Cleanup: ...'" -ForegroundColor $ColorInfo
Write-Host "  - Atajos: Ctrl+K Ctrl+L (light), Ctrl+K Ctrl+T (tabs), Ctrl+K Ctrl+D (deep)" -ForegroundColor $ColorInfo
Write-Host "  - Manual: .\scripts\workspace_cleanup.ps1 -Level light|deep|complete" -ForegroundColor $ColorInfo
