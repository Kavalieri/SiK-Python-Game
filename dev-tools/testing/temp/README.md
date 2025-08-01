# Directorio temporal para pruebas y scripts de desarrollo

Este directorio está destinado para:

## ✅ **USAR PARA:**
- Scripts temporales de prueba
- Archivos de diagnóstico
- Scripts de inicialización/corrección
- Pruebas de funcionalidad específica
- Experimentos de desarrollo

## ❌ **NO INCLUIR:**
- Código de producción
- Configuración definitiva del proyecto
- Archivos que deban persistir en el repositorio

## 🗂️ **ORGANIZACIÓN:**
```
temp/
├── database/          # Scripts relacionados con BD
├── ui/               # Pruebas de interfaz
├── gameplay/         # Tests de mecánicas de juego
└── utils/           # Utilidades de desarrollo
```

## 🧹 **LIMPIEZA:**
Este directorio debe limpiarse regularmente. Los archivos aquí son temporales y pueden eliminarse sin afectar el proyecto principal.

**IMPORTANTE**: Mantener la raíz del proyecto limpia. Siempre usar este directorio para pruebas y desarrollo temporal.
