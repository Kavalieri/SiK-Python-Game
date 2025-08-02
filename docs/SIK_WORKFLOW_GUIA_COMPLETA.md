# SiK Simple Workflow System - Guía Completa
# ==========================================
# Sistema robusto, simple y eficaz para gestión de desarrollo

## COMANDOS DISPONIBLES

### `status` - Ver estado del repositorio
```powershell
.\sik-flow.ps1 status
```
**Función**: Muestra rama actual, archivos modificados y versión actual.
**Cuándo usar**: Antes de cualquier operación para conocer el estado.

### `new` - Crear nueva rama
```powershell
.\sik-flow.ps1 new -Rama "feature/login" -Mensaje "Implementar sistema de login"
.\sik-flow.ps1 new -Rama "bugfix/fix-crash" -Mensaje "Corregir crash en menú"
.\sik-flow.ps1 new -Rama "hotfix/security" -Mensaje "Parche de seguridad urgente"
```
**Función**: Crea nueva rama desde main actualizado.
**Requisitos**: Estar en main con repositorio limpio.
**Resultado**: Nueva rama creada y activada.

### `save` - Guardar cambios
```powershell
.\sik-flow.ps1 save -Mensaje "Añadir validación de usuarios"
.\sik-flow.ps1 save -Mensaje "Implementar login básico" -Push
```
**Función**: Commitea cambios en la rama actual.
**Opciones**: `-Push` para subir automáticamente a origin.
**Resultado**: Commit creado, opcionalmente subido.

### `pr` - Crear Pull Request
```powershell
.\sik-flow.ps1 pr -Mensaje "Sistema de login completo"
.\sik-flow.ps1 pr -Mensaje "Corregir bug de login" -Issue 123
```
**Función**: Crea PR desde rama actual hacia main.
**Opciones**: `-Issue` para vincular con issue específica.
**Resultado**: PR creado en GitHub, issue vinculada si se especifica.

### `merge` - Mergear Pull Request
```powershell
.\sik-flow.ps1 merge -Mensaje "Merge sistema de login"
```
**Función**: Mergea PR actual, elimina rama de feature, vuelve a main.
**Requisitos**: Debe haber PR abierto para la rama actual.
**Resultado**: PR mergeado, rama eliminada, posicionado en main actualizado.

### `release` - Crear release con build
```powershell
.\sik-flow.ps1 release -Version "1.2.0" -Mensaje "Nueva funcionalidad de login"
```
**Función**: Crea tag, build profesional y release de GitHub.
**Requisitos**: Estar en main con repositorio limpio.
**Resultado**: Tag creado, ejecutable generado, release publicado.

### `switch` - Cambiar de rama
```powershell
.\sik-flow.ps1 switch -Rama main
.\sik-flow.ps1 switch -Rama feature/otra-funcionalidad
```
**Función**: Cambia a otra rama.
**Opciones**: `-Force` para descartar cambios locales.
**Resultado**: Cambio de rama exitoso.

## FLUJOS DE TRABAJO TÍPICOS

### Flujo Feature Completo
```powershell
# 1. Verificar estado
.\sik-flow.ps1 status

# 2. Crear nueva rama
.\sik-flow.ps1 new -Rama "feature/sistema-puntuacion" -Mensaje "Implementar sistema de puntuación"

# 3. [Desarrollar código]

# 4. Guardar progreso (múltiples veces si es necesario)
.\sik-flow.ps1 save -Mensaje "Añadir estructura básica de puntuación" -Push
.\sik-flow.ps1 save -Mensaje "Implementar cálculo de puntos" -Push
.\sik-flow.ps1 save -Mensaje "Añadir persistencia de puntuación" -Push

# 5. Crear PR vinculado a issue
.\sik-flow.ps1 pr -Mensaje "Sistema de puntuación completo" -Issue 45

# 6. [Review y aprobación en GitHub]

# 7. Mergear una vez aprobado
.\sik-flow.ps1 merge -Mensaje "Merge sistema de puntuación"

# 8. Crear release si es una funcionalidad importante
.\sik-flow.ps1 release -Version "1.3.0" -Mensaje "Nueva funcionalidad: Sistema de puntuación"
```

### Flujo Bugfix Rápido
```powershell
# 1. Crear rama de bugfix
.\sik-flow.ps1 new -Rama "bugfix/fix-menu-crash" -Mensaje "Corregir crash en menú principal"

# 2. Corregir el bug
.\sik-flow.ps1 save -Mensaje "Corregir null reference en menú" -Push

# 3. PR inmediato
.\sik-flow.ps1 pr -Mensaje "Fix: Corregir crash en menú principal" -Issue 67

# 4. Merge después de review
.\sik-flow.ps1 merge -Mensaje "Fix crash en menú principal"

# 5. Release patch si es crítico
.\sik-flow.ps1 release -Version "1.2.1" -Mensaje "Hotfix: Corregir crash en menú"
```

### Flujo Hotfix Urgente
```powershell
# 1. Hotfix inmediato
.\sik-flow.ps1 new -Rama "hotfix/security-patch" -Mensaje "Parche de seguridad crítico"

# 2. Implementar fix
.\sik-flow.ps1 save -Mensaje "Aplicar parche de seguridad" -Push

# 3. PR urgente
.\sik-flow.ps1 pr -Mensaje "URGENT: Parche de seguridad crítico"

# 4. Merge inmediato (después de review rápido)
.\sik-flow.ps1 merge -Mensaje "Aplicar parche de seguridad urgente"

# 5. Release inmediato
.\sik-flow.ps1 release -Version "1.2.2" -Mensaje "URGENT: Parche de seguridad"
```

## CONVENCIONES DE NOMENCLATURA

### Nombres de Ramas
- **feature/**: Nuevas funcionalidades (`feature/login`, `feature/multiplayer`)
- **bugfix/**: Correcciones de bugs (`bugfix/fix-crash`, `bugfix/menu-error`)
- **hotfix/**: Correcciones urgentes (`hotfix/security`, `hotfix/critical-bug`)
- **docs/**: Cambios de documentación (`docs/update-readme`, `docs/api-docs`)
- **refactor/**: Refactorización (`refactor/clean-code`, `refactor/optimize`)

### Mensajes de Commit
- **feat**: Nueva funcionalidad (`feat: añadir sistema de login`)
- **fix**: Corrección de bug (`fix: corregir crash en menú`)
- **docs**: Documentación (`docs: actualizar README`)
- **refactor**: Refactorización (`refactor: optimizar renderizado`)
- **test**: Tests (`test: añadir tests de login`)
- **chore**: Mantenimiento (`chore: actualizar dependencias`)

### Versionado Semántico
- **Major (X.0.0)**: Cambios incompatibles, nuevas funcionalidades grandes
- **Minor (1.X.0)**: Nuevas funcionalidades compatibles
- **Patch (1.1.X)**: Correcciones de bugs, hotfixes

## INTEGRACIÓN CON ISSUES

### Vincular PR con Issues
```powershell
# PR que cierra una issue automáticamente
.\sik-flow.ps1 pr -Mensaje "Implementar autenticación de usuarios" -Issue 123

# El PR incluirá automáticamente "Closes #123" en la descripción
```

### Keywords que Cierran Issues
El sistema automáticamente usa "Closes #123" que cierra la issue al mergear el PR.

Otras opciones que puedes usar manualmente en mensajes:
- `Fixes #123`
- `Resolves #123`
- `Closes #123`

## CARACTERÍSTICAS TÉCNICAS

### Validaciones de Seguridad
- ✅ **Nunca permite commits directos a main**
- ✅ **Verifica estado limpio antes de crear ramas**
- ✅ **Confirma existencia de PR antes de merge**
- ✅ **Actualiza main antes de operaciones críticas**

### Build Automático
- ✅ **Genera ejecutable Windows x64 en cada release**
- ✅ **Incluye assets automáticamente en GitHub release**
- ✅ **Maneja errores de build gracefully**
- ✅ **Continúa con release aunque falle el build**

### Gestión de Ramas
- ✅ **Elimina ramas de feature automáticamente después del merge**
- ✅ **Actualiza main después de operaciones**
- ✅ **Preserva historial completo de cambios**

## EXPORTACIÓN A OTROS PROYECTOS

### Archivos Necesarios
1. **dev-tools/scripts/sik-flow.ps1** - Script principal
2. **dev-tools/scripts/build_professional.ps1** - Sistema de build (opcional)
3. **VERSION.txt** - Archivo de versión

### Configuración Mínima
```powershell
# En el nuevo proyecto
mkdir dev-tools\scripts
copy sik-flow.ps1 dev-tools\scripts\
echo "0.1.0" > VERSION.txt

# Configurar Git y GitHub CLI
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
gh auth login
```

### Adaptación
- Cambiar `$MainBranch` si tu rama principal no es "main"
- Modificar rutas de build si usas otra herramienta de empaquetado
- Adaptar mensajes y estructura según las convenciones del proyecto

## SOLUCIÓN DE PROBLEMAS

### Error: "No se reconoce el comando gh"
```powershell
winget install GitHub.cli
# o
choco install gh
```

### Error: "Execution Policy"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "No hay PR abierto"
- Crear PR primero con `.\sik-flow.ps1 pr`
- Verificar que estás en la rama correcta

### Error: "Cambios sin commitear"
- Commitear cambios con `.\sik-flow.ps1 save`
- O usar `-Force` para descartar cambios (¡cuidado!)

## BENEFICIOS DEL SISTEMA

### Para Desarrollo Individual
- ✅ **Workflow consistente y predecible**
- ✅ **Eliminación de errores manuales**
- ✅ **Builds automáticos en releases**
- ✅ **Trazabilidad completa de cambios**

### Para Colaboración en Equipo
- ✅ **Estándar unificado de trabajo**
- ✅ **Review obligatorio vía PR**
- ✅ **Releases profesionales con ejecutables**
- ✅ **Historial limpio y organizado**

### Para Distribución
- ✅ **Releases automáticos con ejecutables**
- ✅ **Versionado semántico consistente**
- ✅ **Changelogs automáticos**
- ✅ **Assets organizados por versión**

---

**Este sistema garantiza un flujo de desarrollo profesional, seguro y eficiente que escala desde desarrollo individual hasta equipos grandes.**
