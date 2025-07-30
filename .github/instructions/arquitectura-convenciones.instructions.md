# Arquitectura y Convenciones

## 🏗️ **Arquitectura Modular**
```
src/core/     # Motor, scene manager
src/entities/ # Jugador, enemigos, proyectiles
src/scenes/   # Menús, gameplay, transiciones
src/ui/       # HUD, componentes UI
src/utils/    # Assets, config, helpers
```

## 🎯 **Convenciones**
- **Variables**: `generacion_enemigos`, `velocidad_movimiento`
- **Clases**: `GestorEnemigos`, `PersonajeJugador` (PascalCase español)
- **Type hints**: Obligatorios en parámetros y retornos
- **Docstrings**: Español completo con Args/Returns/Raises

### Estrategia para Problemas
- **Comentar líneas** problemáticas temporalmente
- **Probar sin conflictos** para identificar impacto real
- **Documentar soluciones** implementadas
