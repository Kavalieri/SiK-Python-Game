param(
    [switch]$CleanCache = $false,
    [switch]$Force = $false
)

Write-Host "[INFO] Detectando archivos fantasma en VS Code..." -ForegroundColor Cyan

# Verificar archivos que deberían estar eliminados según nuestros commits recientes
$RecentlyMovedFiles = @(
    "scripts/*",
    "tests/*",
    "tools/*",
    "htmlcov/*",
    "backups__DISABLED/*",
    "commit_message.txt",
    ".github/OJO.instructions.md",
    ".github/SEGUNDA_OPTIMIZACION.md",
    ".github/OPTIMIZACION_INSTRUCCIONES.md",
    ".github/copilot-instructions-optimized.md",
    ".github/copilot-instructions-nueva.md"
)

Write-Host "[INFO] Verificando archivos que deberían estar eliminados..." -ForegroundColor Yellow

$PhantomFiles = @()
foreach ($pattern in $RecentlyMovedFiles) {
    $files = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
    if ($files) {
        $PhantomFiles += $files
        Write-Host "[PHANTOM] Encontrado: $pattern" -ForegroundColor Red
    }
}

# Verificar estado de git para archivos no rastreados
Write-Host "[INFO] Verificando archivos no rastreados en git..." -ForegroundColor Yellow
$UntrackedFiles = & git ls-files --others --exclude-standard
if ($UntrackedFiles) {
    Write-Host "[UNTRACKED] Archivos no rastreados encontrados:" -ForegroundColor Yellow
    $UntrackedFiles | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
}

# Limpiar caché de VS Code si se solicita
if ($CleanCache) {
    Write-Host "[INFO] Limpiando caché de VS Code..." -ForegroundColor Cyan

    $VSCodePaths = @(
        "$env:APPDATA\Code\User\workspaceStorage",
        "$env:APPDATA\Code\User\History",
        "$env:APPDATA\Code\CachedExtensions"
    )

    foreach ($path in $VSCodePaths) {
        if (Test-Path $path) {
            Write-Host "[CLEAN] Limpiando $path..." -ForegroundColor Green
            if ($Force) {
                Remove-Item -Path "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
            } else {
                Write-Host "[DRY-RUN] Sería limpiado: $path" -ForegroundColor Yellow
            }
        }
    }
}

# Comando para cerrar todas las pestañas en VS Code
Write-Host "[SOLUTION] Para cerrar todas las pestañas fantasma en VS Code:" -ForegroundColor Green
Write-Host "  1. Ctrl+K U (cerrar no guardadas)" -ForegroundColor White
Write-Host "  2. Ctrl+K W (cerrar todas)" -ForegroundColor White
Write-Host "  3. O ejecutar: .\dev-tools\scripts\vscode_cleanup_sendkeys.ps1 -Level complete" -ForegroundColor White

Write-Host "[INFO] Análisis completado." -ForegroundColor Cyan
