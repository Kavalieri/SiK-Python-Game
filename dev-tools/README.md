# SiK Development Tools
## Herramientas de Desarrollo Limpias y Organizadas

### Estructura:

#### scripts/
Scripts principales de desarrollo:
- sik.ps1 - Comando principal de workflow
- workflow_automation.ps1 - Sistema de workflow completo
- build_professional.ps1 - Sistema de build profesional
- build_release.ps1 - Integracion de releases

#### testing/
- active/ - Tests activos y mantenidos
- fixtures/ - Datos de prueba reutilizables

#### packaging/
Scripts y configuracion de empaquetado

#### migration/
Scripts de migracion de base de datos

#### docs/
Documentacion tecnica de desarrollo

### Archivos Obsoletos
Los archivos obsoletos han sido archivados en ARCHIVE/2025/dev-tools/

### Uso
- Para desarrollo normal: .\dev-tools\scripts\sik.ps1
- Para builds: .\dev-tools\scripts\build_professional.ps1
- Para tests: archivos en testing/active/
