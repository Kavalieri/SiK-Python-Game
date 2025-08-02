# SiK Auto Workflow - Script de Migracion
# =======================================
# Descripcion: Instala el sistema de workflow automatico en un nuevo proyecto

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,
    [string]$ProjectName = "",
    [string]$MainBranch = "main"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $ProjectPath)) {
    Write-Error "La ruta del proyecto no existe: $ProjectPath"
    exit 1
}

Write-Host "Instalando SiK Auto Workflow en: $ProjectPath" -ForegroundColor Green

# Crear estructura de directorios
$dirs = @(
    "dev-tools/scripts",
    "config",
    "docs/registro",
    "docs/changelogs"
)

foreach ($dir in $dirs) {
    $fullPath = Join-Path $ProjectPath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "Creado directorio: $dir" -ForegroundColor Blue
    }
}

# Crear archivo de configuracion
$configContent = @"
{
    "workflow": {
        "version_strategy": "semantic",
        "default_version_bump": "patch",
        "branch_prefix": "feature/",
        "commit_format": "conventional",
        "auto_changelog": true,
        "auto_release": false,
        "auto_detect_change_type": true,
        "smart_branching": true
    },
    "activation_rules": {
        "hotfix_keywords": ["hotfix", "urgente", "critico", "security", "seguridad"],
        "bugfix_keywords": ["fix", "bug", "error", "corrige", "arregla", "soluciona"],
        "feature_keywords": ["feature", "caracteristica", "nueva", "implementa", "añade", "agrega"],
        "docs_only_branch": false,
        "config_only_branch": true,
        "dev_tools_only_branch": false
    },
    "branch_strategy": {
        "feature_prefix": "feature/",
        "bugfix_prefix": "bugfix/",
        "hotfix_prefix": "hotfix/",
        "docs_prefix": "docs/",
        "config_prefix": "config/",
        "dev_prefix": "dev/",
        "max_branch_name_length": 30
    },
    "git": {
        "main_branch": "$MainBranch",
        "remote": "origin",
        "require_pr": true,
        "auto_delete_branch": true,
        "squash_merge": true,
        "direct_commit_types": ["docs", "dev-tools"]
    },
    "release": {
        "auto_tag": true,
        "tag_prefix": "v",
        "include_assets": false,
        "changelog_archive": "docs/changelogs",
        "auto_release_on_merge": true
    },
    "quality": {
        "run_tests": true,
        "check_linting": true,
        "verify_build": false
    }
}
"@

$configPath = Join-Path $ProjectPath "config/workflow.json"
Set-Content -Path $configPath -Value $configContent -Encoding UTF8
Write-Host "Creado: config/workflow.json" -ForegroundColor Green

# Crear VERSION.txt inicial
$versionPath = Join-Path $ProjectPath "VERSION.txt"
if (-not (Test-Path $versionPath)) {
    Set-Content -Path $versionPath -Value "0.1.0" -Encoding UTF8
    Write-Host "Creado: VERSION.txt (v0.1.0)" -ForegroundColor Green
}

Write-Host ""
Write-Host "INSTALACION COMPLETADA" -ForegroundColor Green
Write-Host ""
Write-Host "Archivos requeridos en tu proyecto SiK:" -ForegroundColor Yellow
Write-Host "  1. Copia auto_workflow.ps1 a dev-tools/scripts/" -ForegroundColor Cyan
Write-Host "  2. Copia workflow_automation.ps1 a dev-tools/scripts/" -ForegroundColor Cyan  
Write-Host "  3. Copia sik.ps1 a dev-tools/scripts/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Uso del sistema:" -ForegroundColor Yellow
Write-Host "  .\dev-tools\scripts\sik.ps1               # Auto workflow" -ForegroundColor Cyan
Write-Host "  .\dev-tools\scripts\sik.ps1 -Status       # Ver estado" -ForegroundColor Cyan
Write-Host "  .\dev-tools\scripts\sik.ps1 -Mensaje '...' # Con descripcion" -ForegroundColor Cyan
Write-Host ""
