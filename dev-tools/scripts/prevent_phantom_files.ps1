param(
    [switch]$Apply = $false
)

Write-Host "[INFO] Configurando VS Code para prevenir archivos fantasma..." -ForegroundColor Cyan

$VSCodeSettings = @{
    "workbench.editor.restoreViewState" = $false
    "workbench.editor.enablePreview" = $false
    "workbench.startupEditor" = "none"
    "files.hotExit" = "off"
    "workbench.editor.closeOnFileDelete" = $true
    "git.autofetch" = $true
    "git.pruneOnFetch" = $true
}

$SettingsPath = "$env:APPDATA\Code\User\settings.json"

if ($Apply) {
    Write-Host "[APPLY] Aplicando configuración anti-fantasma..." -ForegroundColor Green

    # Leer configuración actual
    $CurrentSettings = @{}
    if (Test-Path $SettingsPath) {
        $CurrentSettings = Get-Content $SettingsPath | ConvertFrom-Json -AsHashtable -ErrorAction SilentlyContinue
        if (-not $CurrentSettings) { $CurrentSettings = @{} }
    }

    # Aplicar nuevas configuraciones
    foreach ($key in $VSCodeSettings.Keys) {
        $CurrentSettings[$key] = $VSCodeSettings[$key]
        Write-Host "[SET] $key = $($VSCodeSettings[$key])" -ForegroundColor Yellow
    }

    # Guardar configuración
    $CurrentSettings | ConvertTo-Json -Depth 10 | Set-Content $SettingsPath
    Write-Host "[SUCCESS] Configuración aplicada en $SettingsPath" -ForegroundColor Green
} else {
    Write-Host "[DRY-RUN] Configuraciones que se aplicarían:" -ForegroundColor Yellow
    $VSCodeSettings.GetEnumerator() | ForEach-Object {
        Write-Host "  $($_.Key): $($_.Value)" -ForegroundColor White
    }
    Write-Host "[INFO] Ejecutar con -Apply para aplicar cambios" -ForegroundColor Cyan
}
