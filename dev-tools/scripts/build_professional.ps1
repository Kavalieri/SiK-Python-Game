# SiK Professional Build System
# ============================
# Autor: SiK Team
# Descripcion: Sistema profesional de empaquetado con Nuitka para releases

param(
    [string]$Version = "",
    [string]$Platform = "windows",
    [switch]$Release,
    [switch]$Debug,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PWD

# Configuracion
$BuildConfig = @{
    ProjectName = "SiK-Python-Game"
    EntryPoint = "src\main.py"
    OutputDir = "dist"
    BuildDir = "build"
    AssetsDir = "assets"
    ConfigDir = "config"
    IconFile = "assets\icon.ico"
    RequiredPython = "3.11"
}

function Write-BuildHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host " SiK BUILD SYSTEM: $Title" -ForegroundColor Yellow
    Write-Host "====================================================" -ForegroundColor Cyan
}

function Test-BuildEnvironment {
    Write-BuildHeader "VERIFICANDO ENTORNO"
    
    # Verificar Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "Python: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Error "Python no encontrado. Instalar Python $($BuildConfig.RequiredPython)+"
        return $false
    }
    
    # Verificar Nuitka
    try {
        $nuitkaVersion = python -m nuitka --version 2>&1
        Write-Host "Nuitka: $nuitkaVersion" -ForegroundColor Green
    } catch {
        Write-Host "Nuitka no encontrado. Instalando..." -ForegroundColor Yellow
        python -m pip install nuitka
    }
    
    # Verificar archivos requeridos
    $requiredFiles = @(
        $BuildConfig.EntryPoint,
        "pyproject.toml",
        "config\packaging.json"
    )
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            Write-Error "Archivo requerido no encontrado: $file"
            return $false
        }
    }
    
    Write-Host "Entorno de build verificado exitosamente" -ForegroundColor Green
    return $true
}

function Get-ProjectVersion {
    if ($Version) {
        return $Version
    }
    
    $versionFile = Join-Path $ProjectRoot "VERSION.txt"
    if (Test-Path $versionFile) {
        return (Get-Content $versionFile).Trim()
    }
    
    return "0.1.0"
}

function New-BuildDirectory {
    param([string]$Dir)
    
    if (Test-Path $Dir) {
        if ($Clean) {
            Write-Host "Limpiando directorio: $Dir" -ForegroundColor Yellow
            Remove-Item $Dir -Recurse -Force
        }
    }
    
    New-Item -ItemType Directory -Path $Dir -Force | Out-Null
    Write-Host "Directorio de build creado: $Dir" -ForegroundColor Green
}

function Copy-BuildAssets {
    param([string]$OutputDir)
    
    Write-Host "Copiando assets de juego..." -ForegroundColor Blue
    
    # Copiar assets
    if (Test-Path $BuildConfig.AssetsDir) {
        $assetsTarget = Join-Path $OutputDir $BuildConfig.AssetsDir
        Copy-Item $BuildConfig.AssetsDir $assetsTarget -Recurse -Force
        Write-Host "Assets copiados a $assetsTarget" -ForegroundColor Green
    }
    
    # Copiar configuracion
    if (Test-Path $BuildConfig.ConfigDir) {
        $configTarget = Join-Path $OutputDir $BuildConfig.ConfigDir
        Copy-Item $BuildConfig.ConfigDir $configTarget -Recurse -Force
        Write-Host "Configuracion copiada a $configTarget" -ForegroundColor Green
    }
    
    # Copiar archivos adicionales
    $additionalFiles = @("README.md", "LICENSE", "VERSION.txt")
    foreach ($file in $additionalFiles) {
        if (Test-Path $file) {
            Copy-Item $file $OutputDir -Force
            Write-Host "Copiado: $file" -ForegroundColor Green
        }
    }
}

function Invoke-NuitkaBuild {
    param([string]$Version, [string]$OutputDir)
    
    Write-BuildHeader "COMPILANDO CON NUITKA"
    
    $outputName = "$($BuildConfig.ProjectName)-$Version-$Platform"
    $outputPath = Join-Path $OutputDir "$outputName.exe"
    
    # Argumentos base de Nuitka
    $nuitkaArgs = @(
        "-m", "nuitka",
        "--onefile",
        "--standalone",
        "--output-filename=$outputName.exe",
        "--output-dir=$OutputDir",
        "--remove-output"
    )
    
    # Argumentos de optimizacion
    if ($Release) {
        $nuitkaArgs += @(
            "--optimize-for=speed",
            "--no-debug-mode",
            "--strip",
            "--assume-yes-for-downloads"
        )
    } else {
        $nuitkaArgs += @(
            "--debug",
            "--enable-console"
        )
    }
    
    # Incluir dependencias
    $nuitkaArgs += @(
        "--include-package=pygame",
        "--include-package=pygame_menu", 
        "--include-package=pygame_gui",
        "--include-package=numpy",
        "--include-package=PIL"
    )
    
    # Incluir assets
    $nuitkaArgs += @(
        "--include-data-dir=$($BuildConfig.AssetsDir)=$($BuildConfig.AssetsDir)",
        "--include-data-dir=$($BuildConfig.ConfigDir)=$($BuildConfig.ConfigDir)"
    )
    
    # Archivo de entrada
    $nuitkaArgs += $BuildConfig.EntryPoint
    
    Write-Host "Ejecutando Nuitka..." -ForegroundColor Yellow
    Write-Host "Comando: python $($nuitkaArgs -join ' ')" -ForegroundColor Gray
    
    try {
        & python @nuitkaArgs
        
        if (Test-Path $outputPath) {
            Write-Host "Build exitoso: $outputPath" -ForegroundColor Green
            
            # Verificar tamaño del archivo
            $fileSize = (Get-Item $outputPath).Length / 1MB
            Write-Host "Tamaño del ejecutable: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
            
            return $outputPath
        } else {
            Write-Error "Build fallido: archivo de salida no encontrado"
            return $null
        }
    } catch {
        Write-Error "Error durante el build: $($_.Exception.Message)"
        return $null
    }
}

function New-ReleasePackage {
    param([string]$Version, [string]$OutputDir, [string]$ExePath)
    
    Write-BuildHeader "CREANDO PAQUETE DE RELEASE"
    
    $packageName = "$($BuildConfig.ProjectName)-$Version-$Platform"
    $packageDir = Join-Path $OutputDir $packageName
    
    # Crear directorio de paquete
    New-Item -ItemType Directory -Path $packageDir -Force | Out-Null
    
    # Copiar ejecutable
    Copy-Item $ExePath $packageDir -Force
    
    # Copiar assets y configuracion
    Copy-BuildAssets $packageDir
    
    # Crear archivo de informacion de version
    $versionInfo = @"
SiK Python Game - Version $Version
==================================

Build Information:
- Version: $Version
- Platform: $Platform
- Build Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
- Build Type: $(if ($Release) { 'Release' } else { 'Debug' })
- Python Version: $(python --version)
- Nuitka Version: $(python -m nuitka --version)

Installation:
1. Extract all files to a folder
2. Run $($BuildConfig.ProjectName).exe
3. Enjoy the game!

System Requirements:
- Windows 10/11 (64-bit)
- DirectX 11 compatible graphics
- 2GB RAM minimum
- 1GB free disk space

For support, visit: https://github.com/Kavalieri/SiK-Python-Game
"@
    
    Set-Content -Path (Join-Path $packageDir "VERSION_INFO.txt") -Value $versionInfo -Encoding UTF8
    
    # Crear archivo ZIP
    $zipPath = "$packageDir.zip"
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }
    
    Compress-Archive -Path $packageDir -DestinationPath $zipPath -CompressionLevel Optimal
    Write-Host "Paquete de release creado: $zipPath" -ForegroundColor Green
    
    # Mostrar contenido del paquete
    Write-Host ""
    Write-Host "Contenido del paquete:" -ForegroundColor Cyan
    Get-ChildItem $packageDir -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Replace($packageDir, "").TrimStart("\")
        Write-Host "  $relativePath" -ForegroundColor Gray
    }
    
    return $zipPath
}

function Show-BuildSummary {
    param([string]$Version, [string]$ExePath, [string]$ZipPath)
    
    Write-BuildHeader "RESUMEN DEL BUILD"
    
    Write-Host "Version: $Version" -ForegroundColor Green
    Write-Host "Platform: $Platform" -ForegroundColor Green
    Write-Host "Build Type: $(if ($Release) { 'Release' } else { 'Debug' })" -ForegroundColor Green
    
    if ($ExePath -and (Test-Path $ExePath)) {
        $exeSize = (Get-Item $ExePath).Length / 1MB
        Write-Host "Ejecutable: $ExePath ($([math]::Round($exeSize, 2)) MB)" -ForegroundColor Green
    }
    
    if ($ZipPath -and (Test-Path $ZipPath)) {
        $zipSize = (Get-Item $ZipPath).Length / 1MB
        Write-Host "Paquete: $ZipPath ($([math]::Round($zipSize, 2)) MB)" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "BUILD COMPLETADO EXITOSAMENTE" -ForegroundColor Green
}

# EJECUCION PRINCIPAL
# ==================

Write-BuildHeader "INICIANDO BUILD"

# Verificar entorno
if (-not (Test-BuildEnvironment)) {
    exit 1
}

# Obtener version
$projectVersion = Get-ProjectVersion
Write-Host "Version del proyecto: $projectVersion" -ForegroundColor Cyan

# Preparar directorios
New-BuildDirectory $BuildConfig.OutputDir

# Ejecutar build
$builtExe = Invoke-NuitkaBuild $projectVersion $BuildConfig.OutputDir
if (-not $builtExe) {
    Write-Error "Build fallido"
    exit 1
}

# Crear paquete de release
$releasePackage = New-ReleasePackage $projectVersion $BuildConfig.OutputDir $builtExe

# Mostrar resumen
Show-BuildSummary $projectVersion $builtExe $releasePackage

Write-Host ""
Write-Host "Para probar el ejecutable:" -ForegroundColor Yellow
Write-Host "  $builtExe" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para distribuir:" -ForegroundColor Yellow
Write-Host "  $releasePackage" -ForegroundColor Cyan
