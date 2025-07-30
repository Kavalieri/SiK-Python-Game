# Verificacion FINAL - Todos los scripts usan VS Code path correcto

Write-Host "=== VERIFICACION FINAL DE PATHS VS CODE ===" -ForegroundColor Yellow
Write-Host ""

# Verificar que NINGUN script use 'code' directamente
$problemScripts = @()

$scripts = Get-ChildItem -Path "scripts" -Filter "*.ps1" | Where-Object { $_.Name -like "*cleanup*" -or $_.Name -like "*tab*" -or $_.Name -like "*vscode*" }

foreach ($script in $scripts) {
    $content = Get-Content $script.FullName -Raw

    # Buscar uso directo de 'code' (sin VSCodePath)
    if ($content -match '& code (?!Path)' -or $content -match 'code --command' -and $content -notmatch '\$VSCodePath') {
        $problemScripts += $script.Name
        Write-Host "[ERROR] $($script.Name) usa 'code' directamente" -ForegroundColor Red
    } else {
        Write-Host "[OK] $($script.Name) usa VSCodePath correctamente" -ForegroundColor Green
    }
}

Write-Host ""
if ($problemScripts.Count -eq 0) {
    Write-Host "[SUCCESS] TODOS los scripts usan el path correcto de VS Code" -ForegroundColor Green
    Write-Host "[INFO] NO se abrira Cursor IDE" -ForegroundColor Cyan
} else {
    Write-Host "[ERROR] Scripts con problemas: $($problemScripts -join ', ')" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== PRUEBA REAL ===" -ForegroundColor Yellow

# Probar script principal
Write-Host "[TEST] Ejecutando smart_tab_manager.ps1..." -ForegroundColor Cyan
& "scripts\smart_tab_manager.ps1" -Mode "smart"

Write-Host ""
Write-Host "[INFO] Si se abrio Cursor, hay que investigar mas..." -ForegroundColor Yellow
