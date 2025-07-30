# Script de Limpieza de Archivos Obsoletos - SiK Python Game
# Fecha: 30 de Julio, 2025
# Propósito: Mover archivos obsoletos de src/ a dev-tools/deprecated/

Write-Host "=== LIMPIEZA DE ARCHIVOS OBSOLETOS - SiK Python Game ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "src") -or -not (Test-Path "dev-tools")) {
	Write-Host "[ERROR] No se encuentra en el directorio raíz del proyecto" -ForegroundColor Red
	Write-Host "Ejecute este script desde: e:\GitHub\SiK-Python-Game\" -ForegroundColor Yellow
	exit 1
}

# Crear estructura de directorios si no existe
$deprecatedDirs = @(
	"dev-tools\deprecated\backup-original-files\utils",
	"dev-tools\deprecated\backup-original-files\entities",
	"dev-tools\deprecated\backup-original-files\scenes",
	"dev-tools\deprecated\backup-original-files\ui",
	"dev-tools\deprecated\backup-original-files\core",
	"dev-tools\deprecated\old-versions\utils",
	"dev-tools\deprecated\old-versions\entities",
	"dev-tools\deprecated\old-versions\scenes",
	"dev-tools\deprecated\old-versions\ui",
	"dev-tools\deprecated\old-versions\core",
	"dev-tools\deprecated\duplicate-versions\utils",
	"dev-tools\deprecated\duplicate-versions\entities",
	"dev-tools\deprecated\duplicate-versions\scenes",
	"dev-tools\deprecated\duplicate-versions\ui",
	"dev-tools\deprecated\duplicate-versions\core",
	"dev-tools\testing\moved-from-src"
)

foreach ($dir in $deprecatedDirs) {
	if (-not (Test-Path $dir)) {
		New-Item -ItemType Directory -Path $dir -Force | Out-Null
		Write-Host "[CREATED] Directorio: $dir" -ForegroundColor Green
	}
}

Write-Host ""
Write-Host "=== FASE 1: ARCHIVOS BACKUP/ORIGINAL ===" -ForegroundColor Yellow

# Lista de archivos backup/original a mover
$backupFiles = @(
	# utils
	"src\utils\asset_manager_original_backup.py",
	"src\utils\character_assets_original_backup.py",
	"src\utils\atmospheric_effects_original.py",
	"src\utils\desert_background_original.py",
	"src\utils\world_generator_original.py",
	"src\utils\schema_manager_original.py",
	"src\utils\save_manager_original.py",
	"src\utils\save_compatibility_original.py",
	"src\utils\config_manager_original.py",
	"src\utils\database_manager_original.py",
	"src\utils\database_manager_backup.py",
	"src\utils\schema_migrations_backup.py",

	# entities
	"src\entities\player_original.py",
	"src\entities\player_combat_original.py",
	"src\entities\powerup_original.py",
	"src\entities\entity_core_backup.py",
	"src\entities\enemy_types_backup.py",

	# scenes
	"src\scenes\character_ui_original.py",
	"src\scenes\loading_scene_original.py",

	# ui
	"src\ui\hud_original_backup.py"
)

$moved = 0
foreach ($file in $backupFiles) {
	if (Test-Path $file) {
		$fileName = Split-Path $file -Leaf
		$sourceDir = Split-Path (Split-Path $file -Parent) -Leaf
		$destPath = "dev-tools\deprecated\backup-original-files\$sourceDir\$fileName"

		Move-Item $file $destPath -Force
		Write-Host "[MOVED] $file → $destPath" -ForegroundColor Green
		$moved++
	} else {
		Write-Host "[SKIP] No encontrado: $file" -ForegroundColor Gray
	}
}
Write-Host "Archivos backup movidos: $moved" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== FASE 2: ARCHIVOS OLD ===" -ForegroundColor Yellow

# Lista de archivos _old a mover
$oldFiles = @(
	"src\core\game_engine_old.py",
	"src\entities\enemy_old.py",
	"src\ui\menu_callbacks_old.py"
)

$moved = 0
foreach ($file in $oldFiles) {
	if (Test-Path $file) {
		$fileName = Split-Path $file -Leaf
		$sourceDir = Split-Path (Split-Path $file -Parent) -Leaf
		$destPath = "dev-tools\deprecated\old-versions\$sourceDir\$fileName"

		Move-Item $file $destPath -Force
		Write-Host "[MOVED] $file → $destPath" -ForegroundColor Green
		$moved++
	} else {
		Write-Host "[SKIP] No encontrado: $file" -ForegroundColor Gray
	}
}
Write-Host "Archivos old movidos: $moved" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== FASE 3: ARCHIVOS DUPLICATE/NEW ===" -ForegroundColor Yellow

# Lista de archivos _new y duplicados
$duplicateFiles = @(
	"src\utils\world_generator_new.py",
	"src\utils\asset_manager_new.py",
	"src\utils\atmospheric_effects_new.py",
	"src\core\game_engine_new.py",
	"src\ui\menu_callbacks_new.py",
	"src\ui\hud_new.py"
)

$moved = 0
foreach ($file in $duplicateFiles) {
	if (Test-Path $file) {
		$fileName = Split-Path $file -Leaf
		$sourceDir = Split-Path (Split-Path $file -Parent) -Leaf
		$destPath = "dev-tools\deprecated\duplicate-versions\$sourceDir\$fileName"

		Move-Item $file $destPath -Force
		Write-Host "[MOVED] $file → $destPath" -ForegroundColor Green
		$moved++
	} else {
		Write-Host "[SKIP] No encontrado: $file" -ForegroundColor Gray
	}
}
Write-Host "Archivos duplicados movidos: $moved" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== FASE 4: TESTS EN RAÍZ ===" -ForegroundColor Yellow

# Lista de archivos de test en la raíz
$rootTestFiles = @(
	"debug_game_engine.py",
	"test_game_engine_simple.py",
	"test_menu_flow.py",
	"test_simple_game.py"
)

$moved = 0
foreach ($file in $rootTestFiles) {
	if (Test-Path $file) {
		$fileName = Split-Path $file -Leaf
		$destPath = "dev-tools\testing\moved-from-src\$fileName"

		Move-Item $file $destPath -Force
		Write-Host "[MOVED] $file → $destPath" -ForegroundColor Green
		$moved++
	} else {
		Write-Host "[SKIP] No encontrado: $file" -ForegroundColor Gray
	}
}
Write-Host "Tests de raíz movidos: $moved" -ForegroundColor Cyan

Write-Host ""
Write-Host "=== FASE 5: LIMPIEZA HTMLCOV ===" -ForegroundColor Yellow

if (Test-Path "htmlcov") {
	Remove-Item "htmlcov" -Recurse -Force
	Write-Host "[DELETED] Directorio htmlcov/ (reportes de cobertura)" -ForegroundColor Green

	# Verificar si htmlcov está en .gitignore
	if (Test-Path ".gitignore") {
		$gitignoreContent = Get-Content ".gitignore" -Raw
		if ($gitignoreContent -notmatch "htmlcov/") {
			Add-Content ".gitignore" "`nhtmlcov/"
			Write-Host "[ADDED] htmlcov/ a .gitignore" -ForegroundColor Green
		}
	}
} else {
	Write-Host "[SKIP] htmlcov/ ya no existe" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== VERIFICACIÓN FINAL ===" -ForegroundColor Yellow

# Contar archivos en src/
$srcFiles = Get-ChildItem -Path "src" -Recurse -File -Name "*.py"
$srcCount = $srcFiles.Count

Write-Host "Archivos Python en src/: $srcCount" -ForegroundColor Cyan

# Mostrar estructura de deprecated
Write-Host ""
Write-Host "Estructura dev-tools/deprecated/:" -ForegroundColor Cyan
Get-ChildItem -Path "dev-tools\deprecated" -Recurse -File | ForEach-Object {
	$relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
	Write-Host "  $relativePath" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== LIMPIEZA COMPLETADA ===" -ForegroundColor Green
Write-Host "✅ Archivos obsoletos movidos a dev-tools/deprecated/" -ForegroundColor Green
Write-Host "✅ Estructura src/ limpia y organizada" -ForegroundColor Green
Write-Host "✅ htmlcov/ eliminado (se regenera automáticamente)" -ForegroundColor Green
Write-Host ""
Write-Host "📋 PRÓXIMO PASO: Revisar INVENTARIO_ARCHIVOS_OBSOLETOS.md para detalles" -ForegroundColor Yellow
Write-Host "📂 Ubicación: dev-tools/deprecated/INVENTARIO_ARCHIVOS_OBSOLETOS.md" -ForegroundColor Yellow
