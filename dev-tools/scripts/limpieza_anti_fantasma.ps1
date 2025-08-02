# LIMPIEZA CACHE COPILOT Y DETECCION ARCHIVOS FANTASMA
# Ejecutar desde PowerShell como administrador

Write-Host "INICIANDO LIMPIEZA ANTI-FANTASMA" -ForegroundColor Red
Write-Host ("=" * 60) -ForegroundColor Yellow

# 1. DETECTAR ARCHIVOS FANTASMA EXISTENTES
Write-Host "`nDETECTANDO ARCHIVOS FANTASMA..." -ForegroundColor Cyan

$fantasmaFiles = Get-ChildItem -Recurse -File | Where-Object { 
    $_.Length -eq 0 -and 
    $_.CreationTime -gt (Get-Date).AddDays(-7) -and
    $_.Name -match "\.(py|md|js|ts|json|txt)$" 
}

if ($fantasmaFiles) {
    Write-Host "ARCHIVOS FANTASMA DETECTADOS:" -ForegroundColor Red
    $fantasmaFiles | Select-Object Name, FullName, CreationTime | Format-Table -AutoSize
    
    # Solicitar confirmación antes de eliminar
    $confirm = Read-Host "Desea eliminar estos archivos fantasma? (s/N)"
    if ($confirm -eq "s" -or $confirm -eq "S") {
        $fantasmaFiles | Remove-Item -Force
        Write-Host "Archivos fantasma eliminados" -ForegroundColor Green
    }
}
else {
    Write-Host "No se detectaron archivos fantasma" -ForegroundColor Green
}

# 2. VERIFICAR TAMANO CACHE COPILOT
Write-Host "`nVERIFICANDO CACHE COPILOT..." -ForegroundColor Cyan

$cachePath = "$env:APPDATA\Code\User\workspaceStorage\*\GitHub.copilot-chat"
$cacheItems = Get-ChildItem $cachePath -Recurse -ErrorAction SilentlyContinue

if ($cacheItems) {
    $cacheSize = ($cacheItems | Measure-Object -Property Length -Sum).Sum
    $cacheSizeMB = ($cacheSize / 1MB).ToString('F2')
    Write-Host "Tamano cache Copilot: $cacheSizeMB MB" -ForegroundColor Yellow
    
    # 3. LIMPIAR CACHE SI ES MAYOR A 50MB
    if ($cacheSize -gt 50MB) {
        Write-Host "Cache excede 50MB, ejecutando limpieza..." -ForegroundColor Red
        
        # Crear backup
        $backupPath = "$env:APPDATA\Code\User\workspaceStorage\backup_copilot_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Write-Host "Creando backup en: $backupPath" -ForegroundColor Yellow
        
        Get-ChildItem "$env:APPDATA\Code\User\workspaceStorage\*\GitHub.copilot-chat" -ErrorAction SilentlyContinue | ForEach-Object {
            New-Item -Path $backupPath -ItemType Directory -Force | Out-Null
            Copy-Item -Path $_.FullName -Destination $backupPath -Recurse -Force
        }
        
        # Limpiar cache
        Get-ChildItem "$env:APPDATA\Code\User\workspaceStorage\*\GitHub.copilot-chat" -ErrorAction SilentlyContinue | ForEach-Object {
            Remove-Item -Path "$($_.FullName)\*" -Recurse -Force
        }
        
        Write-Host "Cache de GitHub Copilot Chat limpiada" -ForegroundColor Green
        Write-Host "Backup guardado en: $backupPath" -ForegroundColor Cyan
    }
    else {
        Write-Host "Tamano de cache dentro de limites normales" -ForegroundColor Green
    }
}
else {
    Write-Host "No se encontro cache de Copilot Chat" -ForegroundColor Blue
}

# 4. VERIFICAR ARCHIVOS TEMPORALES EN PROYECTO
Write-Host "`nVERIFICANDO ARCHIVOS TEMPORALES EN PROYECTO..." -ForegroundColor Cyan

$tempPatterns = @("test_*.py", "demo_*.py", "setup_*.py", "example_*.py", "temp_*", "*.tmp", "*.temp")
$foundTempFiles = @()

foreach ($pattern in $tempPatterns) {
    $tempFiles = Get-ChildItem -Recurse -File -Name $pattern -ErrorAction SilentlyContinue
    $foundTempFiles += $tempFiles
}

if ($foundTempFiles) {
    Write-Host "ARCHIVOS TEMPORALES ENCONTRADOS:" -ForegroundColor Yellow
    $foundTempFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    Write-Host "Estos archivos estan excluidos por .vscode/settings.json" -ForegroundColor Blue
}
else {
    Write-Host "No se encontraron archivos temporales problematicos" -ForegroundColor Green
}

# 5. ESTADISTICAS GIT
Write-Host "`nESTADISTICAS GIT..." -ForegroundColor Cyan

$untracked = git status --porcelain | Where-Object { $_ -match "^\?\?" }
if ($untracked) {
    $untrackedCount = ($untracked | Measure-Object).Count
    Write-Host "Archivos sin seguimiento: $untrackedCount" -ForegroundColor Yellow
    
    # Mostrar solo los primeros 10
    $untracked | Select-Object -First 10 | ForEach-Object {
        Write-Host "  - $($_.Substring(3))" -ForegroundColor Yellow
    }
    if ($untrackedCount -gt 10) {
        Write-Host "  ... y $($untrackedCount - 10) mas" -ForegroundColor Yellow
    }
}
else {
    Write-Host "No hay archivos sin seguimiento" -ForegroundColor Green
}

Write-Host "`nLIMPIEZA ANTI-FANTASMA COMPLETADA" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Yellow

# 6. RECOMENDACIONES
Write-Host "`nRECOMENDACIONES:" -ForegroundColor White
Write-Host "1. Reinicia VS Code para aplicar configuracion anti-fantasma" -ForegroundColor White
Write-Host "2. El historial de Copilot Chat se ha reiniciado" -ForegroundColor White
Write-Host "3. Ejecuta este script semanalmente para mantenimiento" -ForegroundColor White
Write-Host "4. Los archivos temporales ahora estan ocultos en VS Code" -ForegroundColor White

Read-Host "`nPresiona Enter para continuar..."
