# Configuración de GitHub CLI - SiK Python Game

## 🎯 Objetivo
Configurar GitHub CLI de manera segura para mejorar la experiencia de gestión del repositorio.

## � Documentación Oficial
- **Manual completo**: https://cli.github.com/manual/
- **Comandos disponibles**: https://cli.github.com/manual/gh
- **Ejemplos de uso**: https://cli.github.com/manual/examples
- **Extensiones community**: https://github.com/topics/gh-extension

## �🔧 Configuración Inicial

### 1. Verificar Instalación
```powershell
gh --version
# Debe mostrar: gh version 2.76.1 (o superior)
```

### 2. Configuración Segura con Token Personal

#### Crear Token en GitHub (Recomendado)
1. **Ir a GitHub.com** → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generar nuevo token** con permisos:
   - `repo` (acceso completo a repositorios)
   - `workflow` (para GitHub Actions)
   - `write:packages` (para releases)
3. **Copiar el token** (solo se muestra una vez)

#### Configurar con Token
```powershell
# Opción 1: Configuración interactiva
gh auth login
# Seleccionar:
# - GitHub.com
# - HTTPS (más compatible)
# - Paste an authentication token
# - Pegar el token

# Opción 2: Variable de entorno (para scripts)
$env:GH_TOKEN = "tu_token_aquí"
gh auth status  # Verificar que funciona
```

### 3. Configuración Avanzada

#### Configurar Git con GitHub CLI
```powershell
# Configurar Git para usar GitHub CLI automáticamente
gh auth setup-git

# Verificar configuración
git config --list | Select-String "credential"
```

#### Configurar Preferencias
```powershell
# Editor predeterminado (VS Code)
gh config set editor "code --wait"

# Navegador predeterminado
gh config set browser "default"

# Protocolo Git
gh config set git_protocol https
```

## 🚀 Comandos Útiles Configurados

### Información del Repositorio
```powershell
# Vista general del repositorio
gh repo view

# Información detallada en JSON
gh repo view --json name,description,stargazerCount,issuesCount,pullRequestsCount
```

### Gestión de Issues
```powershell
# Listar issues abiertos
gh issue list --state open

# Crear issue desde terminal
gh issue create --title "Bug: Error en carga de assets" --body "Descripción detallada del problema encontrado"

# Ver issue específico
gh issue view 123
```

### Pull Requests Automatizados
```powershell
# Crear PR después de push
gh pr create --title "feat: nueva funcionalidad" --body "Descripción de cambios"

# Listar PRs
gh pr list --state open

# Hacer checkout de PR para revisión
gh pr checkout 456
```

### Releases Automáticos
```powershell
# Crear release con archivos
gh release create v0.2.0 --title "Nueva versión estable" --notes-file CHANGELOG.md

# Subir archivos al release
gh release upload v0.2.0 "builds/sik-game-v0.2.0.exe"

# Listar releases
gh release list
```

## 🔧 Integración con Scripts del Proyecto

### Actualización del Script de Commits
El script `commit_profesional.ps1` puede usar GitHub CLI:

```powershell
# Ejemplo de uso avanzado
.\scripts\commit_profesional.ps1 -Mensaje "añade sistema de IA" -Tipo "feat" -Ambito "entities" -Push

# Crear issue automático para seguimiento
gh issue create --title "feat: Sistema de IA para enemigos" --body "Implementación completada en commit anterior"
```

### Comandos PowerShell Específicos

#### Búsqueda y Filtrado (Sin grep)
```powershell
# Buscar en archivos (equivalente a grep)
Get-Content "archivo.txt" | Select-String "patrón"

# Buscar en múltiples archivos
Get-ChildItem -Recurse -Include "*.py" | Select-String "función_específica"

# Filtrar salida de comandos
gh issue list | Select-String "bug"
git log --oneline | Select-String "feat"
```

#### Configuración Git con PowerShell
```powershell
# Ver configuración Git filtrada
git config --list | Select-String "(user\.|commit\.|push\.)"

# Configurar usando variables
$usuario = "Tu Nombre"
$email = "tu@email.com"
git config user.name $usuario
git config user.email $email
```

## ✅ Verificación de Configuración

### Comandos de Prueba
```powershell
# 1. Verificar autenticación
gh auth status

# 2. Probar acceso al repositorio
gh repo view SiK-Python-Game

# 3. Verificar integración Git
gh auth setup-git
git credential-helper

# 4. Probar comando de información
gh api user --jq .login
```

### Solución de Problemas Comunes

#### Error de Autenticación
```powershell
# Limpiar credenciales y reconfigurar
gh auth logout
gh auth login
```

#### Error de Permisos SSH
```powershell
# Usar HTTPS en lugar de SSH
gh config set git_protocol https
```

#### Token Expirado
```powershell
# Regenerar token en GitHub.com y volver a configurar
gh auth refresh
```

## 🎯 Flujo de Trabajo Mejorado

### Para Desarrollo Diario (FLUJO PRINCIPAL)
```powershell
# 1. Verificar estado general (PREFERIR sobre git status)
gh repo view
gh issue list --assignee @me

# 2. Hacer cambios y commit
.\scripts\commit_profesional.ps1 -Mensaje "implementa nueva funcionalidad" -Push

# 3. Gestión post-commit
gh issue create --title "feat: Nueva funcionalidad" --body "Implementada en último commit"
gh browse  # Abrir repo si necesario
```

### Para Releases
```powershell
# 1. Preparar release
.\scripts\commit_profesional.ps1 -Tipo "chore" -Mensaje "prepara release v0.2.0"

# 2. Crear release
gh release create v0.2.0 --title "Versión Estable 0.2.0" --notes-file CHANGELOG.md

# 3. Notificar en issues relevantes
gh issue comment 123 --body "Resuelto en release v0.2.0"
```

## 🔒 Seguridad y Mejores Prácticas

### Gestión de Tokens
- ✅ **Usar tokens de acceso limitado** (no classic tokens completos)
- ✅ **Establecer fecha de expiración** en los tokens
- ✅ **Revocar tokens** no utilizados regularmente
- ✅ **No compartir tokens** en código o documentación

### Variables de Entorno Seguras
```powershell
# Para scripts automatizados, usar variables de entorno
[Environment]::SetEnvironmentVariable("GH_TOKEN", "tu_token", "User")

# Verificar que está configurado
$env:GH_TOKEN  # No debe mostrar el token completo en logs
```

---

**Configuración completada. GitHub CLI está ahora optimizado para el proyecto SiK Python Game.**
