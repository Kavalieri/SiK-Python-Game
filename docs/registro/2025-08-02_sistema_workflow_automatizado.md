# 🚀 Sistema de Workflow Automatizado - SiK Python Game

## **Descripción**
Sistema completo de workflow automatizado para gestión de desarrollo, changelog automático y releases del proyecto SiK Python Game.

## 🎯 **Componentes del Sistema**

### 📜 **Scripts Principales**

#### **1. workflow_automation.ps1** (Completo)
```powershell
# Crear nueva rama de desarrollo
.\dev-tools\scripts\workflow_automation.ps1 -Accion nueva-rama -RamaNombre "feature/sistema-powerups" -Mensaje "Implementar sistema de powerups"

# Completar desarrollo y crear PR
.\dev-tools\scripts\workflow_automation.ps1 -Accion completar -Mensaje "Sistema powerups implementado y probado"

# Mergear PR a main y crear versión
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release -TipoVersion minor -Mensaje "Nueva funcionalidad: sistema powerups"

# Crear release manual
.\dev-tools\scripts\workflow_automation.ps1 -Accion release -TipoVersion patch -Mensaje "Correcciones menores"

# Ver estado
.\dev-tools\scripts\workflow_automation.ps1 -Accion status
```

#### **2. dev_helper.ps1** (Simplificado)
```powershell
# Iniciar nueva característica
.\dev-tools\scripts\dev_helper.ps1 start

# Guardar progreso
.\dev-tools\scripts\dev_helper.ps1 save

# Finalizar y crear PR
.\dev-tools\scripts\dev_helper.ps1 finish

# Ver estado
.\dev-tools\scripts\dev_helper.ps1 status
```

### ⚙️ **Configuración**
- **Archivo**: `config/workflow.json`
- **Parámetros**: Versionado, estrategia de merge, formato de commits
- **Personalizable**: Adaptable a diferentes necesidades

## 🔄 **Flujo de Trabajo Recomendado**

### **Opción A: Desarrollo Rápido (dev_helper.ps1)**
```powershell
# 1. Iniciar nueva característica
.\dev-tools\scripts\dev_helper.ps1 start
# → Ingresa: nombre rama y descripción

# 2. Desarrollar (repetir según necesidad)
# ... hacer cambios en código ...
.\dev-tools\scripts\dev_helper.ps1 save
# → Ingresa: descripción de cambios

# 3. Finalizar
.\dev-tools\scripts\dev_helper.ps1 finish
# → Ingresa: descripción final

# 4. Completar merge y release
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release -Mensaje "Descripción final"
```

### **Opción B: Desarrollo Completo (workflow_automation.ps1)**
```powershell
# 1. Nueva rama
.\dev-tools\scripts\workflow_automation.ps1 -Accion nueva-rama -RamaNombre "feature/mi-caracteristica" -Mensaje "Descripción"

# 2. Desarrollar normalmente con git
git add .
git commit -m "Progreso en característica"
git push

# 3. Completar y crear PR
.\dev-tools\scripts\workflow_automation.ps1 -Accion completar -Mensaje "Característica completada"

# 4. Mergear y release
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -Release -TipoVersion minor -Mensaje "Nueva característica"
```

## 📋 **Changelog Automático**

### **Características**
- ✅ **Generación automática**: Se actualiza en cada release
- ✅ **Archivado**: Versiones individuales en `docs/changelogs/`
- ✅ **Formato consistente**: Estructura estandarizada
- ✅ **Integración Git**: Tags y releases automáticos

### **Estructura del Changelog**
```markdown
## [version] - fecha

### 🔄 Descripción

#### ✅ Cambios Implementados
- Lista de cambios

#### 📊 Estado del Proyecto
- Estado actual del proyecto
```

### **Archivos Generados**
- **CHANGELOG.md**: Archivo principal actualizado
- **docs/changelogs/X.Y.Z.md**: Archivo individual por versión
- **GitHub Release**: Release automático con notas

## 🎯 **Versionado Semántico**

### **Tipos de Versión**
- **patch** (0.1.0 → 0.1.1): Correcciones menores
- **minor** (0.1.0 → 0.2.0): Nuevas características
- **major** (0.1.0 → 1.0.0): Cambios que rompen compatibilidad

### **Uso**
```powershell
# Versión patch por defecto
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge

# Versión minor
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -TipoVersion minor

# Versión major
.\dev-tools\scripts\workflow_automation.ps1 -Accion merge -TipoVersion major
```

## 🔧 **Configuración Inicial**

### **Requisitos**
- **GitHub CLI**: `gh` instalado y configurado
- **Git**: Repositorio configurado con origin
- **PowerShell**: 5.1 o superior
- **Permisos**: Acceso para crear PRs y releases

### **Configuración**
```powershell
# Verificar GitHub CLI
gh auth status

# Verificar configuración Git
git remote -v
git branch -a

# Ejecutar primer test
.\dev-tools\scripts\workflow_automation.ps1 -Accion status
```

## 📊 **Beneficios del Sistema**

### **Para el Desarrollo**
- 🚀 **Velocidad**: Flujo automatizado reduce tiempo manual
- 🔄 **Consistencia**: Proceso estandarizado para todos
- 📋 **Trazabilidad**: Historial completo de cambios
- 🛡️ **Calidad**: Verificaciones automáticas

### **Para la Documentación**
- 📚 **Changelog automático**: Sin intervención manual
- 🗂️ **Archivado organizado**: Versiones individuales preservadas
- 🔗 **Integración GitHub**: Releases profesionales
- 📈 **Seguimiento**: Progreso visible del proyecto

### **Para la Colaboración**
- 🤝 **PRs consistentes**: Templates automáticos
- 🔍 **Revisión estructurada**: Formato estandarizado
- 📢 **Comunicación clara**: Descripciones automáticas
- 🎯 **Releases organizados**: Publicación automática

## 🚨 **Consideraciones Importantes**

### **Flujo Obligatorio**
- ❌ **No hacer commits directos a main**
- ✅ **Siempre usar ramas feature/**
- ✅ **Crear PRs para todos los cambios**
- ✅ **Usar scripts para merge y release**

### **Gestión de Ramas**
- **Automática**: Ramas se eliminan tras merge
- **Convención**: Prefijo `feature/` obligatorio
- **Limpieza**: Sistema mantiene repositorio organizado

### **Compatibilidad**
- **GitHub**: Integración completa con GitHub CLI
- **Local**: Funciona sin conexión (limitado)
- **Multi-usuario**: Cada desarrollador usa su configuración

---

**📍 Ubicación**: `docs/registro/2025-08-02_sistema_workflow_automatizado.md`  
**🔄 Última actualización**: 2025-08-02  
**👤 Autor**: Sistema automatizado GitHub Copilot  
**📋 Estado**: Documentación activa del sistema de workflow
