# 🛠️ Dev-Tools - SiK Python Game

## **Herramientas de Desarrollo Centralizadas**

### 📋 **Estructura Actual**

```
🛠️ dev-tools/
├── 📜 scripts/                # Scripts de producción y mantenimiento
│   ├── robust_commit.ps1      # Sistema de commits robusto
│   ├── limpieza_anti_fantasma.ps1  # Limpieza de archivos fantasma
│   └── ...                    # Otros scripts de producción
├── 🧪 testing/                # Framework de testing
│   ├── temp/                  # Tests temporales
│   └── ...                    # Suite de tests automatizados
├── 📦 packaging/               # Empaquetado y distribución
│   └── ...                    # Herramientas de distribución
├── 🔄 migration/               # Scripts de migración
│   └── ...                    # Scripts de refactorización
└── 🐛 debugging/               # Herramientas de depuración
    └── ...                    # Utilidades de debug
```

### 🎯 **Filosofía de dev-tools/**

#### **✅ Herramientas Activas** (mantenidas en dev-tools/)
- **Scripts de producción**: Herramientas necesarias para el desarrollo diario
- **Testing framework**: Tests automatizados y herramientas de verificación
- **Empaquetado**: Herramientas para distribución del juego
- **Migración**: Scripts de refactorización y actualización

#### **📦 Herramientas Archivadas** (movidas a ARCHIVE/)
- Scripts obsoletos → `ARCHIVE/2025/dev-tools/`
- Herramientas experimentales no utilizadas
- Versiones antigas de utilidades

### 🔧 **Herramientas Principales**

#### **📜 Scripts de Producción**
- **`robust_commit.ps1`**: Sistema automatizado de commits con verificaciones
- **`limpieza_anti_fantasma.ps1`**: Limpieza de archivos fantasma de Copilot
- **Comandos principales**:
  ```powershell
  # Commit robusto con verificaciones
  .\dev-tools\scripts\robust_commit.ps1 "mensaje"
  
  # Limpieza anti-fantasma semanal
  .\dev-tools\scripts\limpieza_anti_fantasma.ps1
  ```

#### **🧪 Testing Framework**
- **Suite de tests**: Verificación automatizada del código
- **Tests temporales**: `testing/temp/` para tests experimentales
- **Comandos principales**:
  ```powershell
  # Ejecutar tests específicos
  poetry run python dev-tools\testing\test_*.py
  ```

#### **📦 Packaging y Distribución**
- **Empaquetado**: Herramientas para crear distribuciones del juego
- **Distribución**: Scripts para publicación y releases

### 📊 **Estado Actual**

#### **✅ Reorganización Completada**
- ✅ **Archivados**: Scripts obsoletos movidos a `ARCHIVE/2025/dev-tools/`
- ✅ **Limpieza**: Solo herramientas necesarias mantenidas
- ✅ **Organización**: Estructura clara por categorías

#### **📦 Archivos Movidos a ARCHIVE/2025/dev-tools/**
- `check_db.py`: Script de verificación de DB obsoleto
- `diagnostico*.py`: Scripts de diagnóstico temporales
- `fix_database.py`: Script de reparación DB obsoleto
- `init_database.py`: Script de inicialización DB obsoleto
- `juego_simple_pygame_gui.py`: Versión obsoleta del juego
- `normalize_encoding.ps1`: Script de codificación obsoleto

### 🔄 **Mantenimiento Continuo**

#### **Criterios para Herramientas Activas**
- ✅ **Utilizadas regularmente** en el desarrollo actual
- ✅ **Necesarias para el flujo de trabajo** estándar
- ✅ **Actualizadas y funcionales**
- ✅ **Documentadas y con propósito claro**

#### **Criterios para Archivado**
- ❌ **No utilizadas** en los últimos 30 días
- ❌ **Funcionalidad duplicada** por otras herramientas
- ❌ **Experimentales** que no se adoptaron
- ❌ **Obsoletas** por cambios en la arquitectura

### 📁 **Gestión de Archivos Temporales**

#### **Ubicaciones para Archivos Temporales**
- **Scripts temporales**: `dev-tools/testing/temp/`
- **Tests experimentales**: `dev-tools/testing/temp/`
- **Herramientas en desarrollo**: Desarrollar en temp/ antes de promover

#### **Protocolo de Limpieza**
1. **Revisión semanal**: Evaluar herramientas en temp/
2. **Promover útiles**: Mover a ubicación definitiva
3. **Archivar obsoletas**: Mover a ARCHIVE/
4. **Eliminar temporales**: Borrar archivos sin valor

---

**📍 Ubicación**: `dev-tools/README.md`  
**🔄 Última actualización**: 2025-08-02  
**👤 Mantenido por**: Sistema automatizado GitHub Copilot  
**📋 Estado**: Activo - Herramientas centralizadas y organizadas
