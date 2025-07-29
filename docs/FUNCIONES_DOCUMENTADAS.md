# Documentación de Funciones

## 🔗 Sistema de Documentación Integrado
**Este archivo debe ACTUALIZARSE con cada función nueva/modificada**

### Referencias Cruzadas del Sistema
- **📋 Documento Central**: [`refactorizacion_progreso.md`](./refactorizacion_progreso.md) - Estado de refactorización (consultar PRIMERO)
- **🗄️ Plan de Migración**: [`PLAN_MIGRACION_SQLITE.md`](./PLAN_MIGRACION_SQLITE.md) - Esquemas SQLite y checklist
- **🔍 Vista Rápida**: [`INDICE_MIGRACION_SQLITE.md`](./INDICE_MIGRACION_SQLITE.md) - Progreso de migración
- **⚙️ Instrucciones**: [`.github/copilot-instructions.md`](../.github/copilot-instructions.md) - Reglas del proyecto

### 🗄️ Funciones de Migración SQLite
**AGREGAR aquí las funciones de DatabaseManager, SchemaManager y módulos divididos durante la refactorización**
- Cuando se cree `DatabaseManager`: documentar `conectar()`, `ejecutar_query()`, `cerrar_conexion()`
- Cuando se divida `SaveManager`: documentar funciones de `save_loader.py`, `save_encryption.py`, etc.
- Cuando se divida `ConfigManager`: documentar funciones de `config_database.py`, `config_loader.py`, etc.

Este archivo contiene la documentación generada automáticamente para todas las funciones del proyecto SiK Python Game.

## Formato de Documentación

Cada función estará documentada con el siguiente formato:

```markdown
### Nombre de la Función
- **Descripción**: Breve descripción de la función.
- **Parámetros**:
  - `nombre_parametro` (tipo): Descripción del parámetro.
- **Retorno**:
  - Tipo: Descripción del valor de retorno.
- **Ejemplo de Uso**:
  ```python
  # Ejemplo de uso
  ```
```

---

## Directorio `config/`

### Archivos de Configuración JSON

Los archivos de configuración contienen parámetros centralizados que son utilizados por múltiples módulos del juego. Durante la refactorización, es importante identificar redundancias entre estos archivos y el código hardcodeado.

#### animations.json
- **Descripción**: Configuración de animaciones de personajes y enemigos.
- **Campos clave**:
  - `characters`: Personajes con sus animaciones disponibles y frames totales
  - `sprite_paths`: Rutas de patrones para cargar sprites
- **Redundancias identificadas**: Comparar con `src/entities/character_data.py` y clases de animación
- **Personajes configurados**: adventureguirl, guerrero, robot, zombieguirl, zombiemale

#### audio.json
- **Descripción**: Configuración de volúmenes, archivos de audio y configuración de reproducción.
- **Campos clave**:
  - `volúmenes`: Niveles de volumen por categoría
  - `archivos_audio`: Rutas de archivos de música y efectos
  - `configuración`: Configuración de reproducción y fade
- **Redundancias identificadas**: Comparar con código hardcodeado de audio en el juego

#### characters.json (190 líneas)
- **Descripción**: Configuración detallada de personajes jugables con estadísticas y ataques.
- **Campos clave**:
  - `characters`: Datos completos de personajes (guerrero, adventureguirl, robot)
  - `stats`: Vida, velocidad, daño, escudo, rango_ataque
  - `ataques`: Configuración detallada de tipos de ataque
  - `habilidades`: Lista de habilidades por personaje
- **Redundancias identificadas**: **CRÍTICA** - Duplicación con `src/entities/character_data.py`

#### enemies.json
- **Descripción**: Configuración de tipos de enemigos con comportamiento y estadísticas.
- **Campos clave**:
  - `tipos_enemigos`: zombie_male, zombie_female
  - `stats`: Vida, velocidad, daño, rangos de detección y ataque
  - `comportamiento`: Patrones de IA
  - `animaciones`: Mapeo de animaciones por tipo
- **Redundancias identificadas**: Comparar con `src/entities/enemy.py` método `_setup_enemy_type`

#### gameplay.json
- **Descripción**: Configuración de mecánicas de juego, niveles, combate y puntuación.
- **Campos clave**:
  - `niveles`: Duración, escalado de dificultad
  - `combate`: Daño, invulnerabilidad, combos
  - `powerups`: Duración, probabilidad, spawn
  - `puntuación`: Multiplicadores y bonificaciones
- **Redundancias identificadas**: Valores hardcodeados en escenas de juego

### Análisis de Redundancias Críticas en Configuración

1. **DUPLICACIÓN CRÍTICA**: `config/characters.json` vs `src/entities/character_data.py`
   - Ambos definen estadísticas de personajes con ligeras diferencias
   - Necesario consolidar en una sola fuente de verdad

2. **INCONSISTENCIAS**: `config/enemies.json` vs `src/entities/enemy.py`
   - Stats definidos en JSON no coinciden con los hardcodeados en Python
   - Método `_setup_enemy_type` ignora la configuración JSON

3. **VALORES HARDCODEADOS**: Múltiples valores en `gameplay.json` están hardcodeados en el código
   - Timers, rangos de detección, cooldowns

---

## Módulo `src/core/`

## Módulo `src/core/`

### Archivo: `game_engine.py`

#### Clase: GameEngine

##### __init__
- **Descripción**: Inicializa el motor del juego con configuración y componentes principales.
- **Parámetros**:
  - `config` (ConfigManager): Gestor de configuración del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  config = ConfigManager()
  engine = GameEngine(config)
  ```

##### _initialize_pygame
- **Descripción**: Inicializa Pygame y configura la pantalla, mixer y reloj del juego.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._initialize_pygame()
  ```

##### _initialize_components
- **Descripción**: Inicializa los componentes principales del juego (estado, guardado, menús, escenas).
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._initialize_components()
  ```

##### _setup_scenes
- **Descripción**: Configura las escenas iniciales del juego y documenta el flujo avanzado de menús y guardado.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._setup_scenes()
  ```

##### _setup_scene_transitions
- **Descripción**: Configura las transiciones entre escenas y documenta la diferenciación de botón Salir y cierre de ventana.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._setup_scene_transitions()
  ```

##### _quit_game
- **Descripción**: Método para salir del juego estableciendo running = False.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._quit_game()
  ```

##### _on_loading_complete
- **Descripción**: Callback cuando termina la carga inicial del juego.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._on_loading_complete()
  ```

##### run
- **Descripción**: Ejecuta el bucle principal del juego con manejo de eventos, actualización y renderizado.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine.run()
  ```

##### _handle_events
- **Descripción**: Procesa todos los eventos de Pygame incluyendo QUIT y delega otros al scene_manager.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._handle_events()
  ```

##### _log_event
- **Descripción**: Registra eventos de Pygame para debug con información detallada.
- **Parámetros**:
  - `event` (pygame.event.Event): Evento de Pygame a registrar.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._log_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN))
  ```

##### _update
- **Descripción**: Actualiza la lógica del juego delegando al scene_manager.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._update()
  ```

##### _render
- **Descripción**: Renderiza el juego en pantalla y actualiza el display.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._render()
  ```

##### _cleanup
- **Descripción**: Limpia recursos y cierra Pygame al finalizar el juego.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._cleanup()
  ```

##### _log_and_quit_menu
- **Descripción**: Diferencia el cierre por botón Salir del menú y el cierre de ventana.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._log_and_quit_menu()
  ```

##### _handle_continue_game
- **Descripción**: Maneja la acción de continuar juego desde el último slot activo.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._handle_continue_game()
  ```

##### _handle_slot_selection
- **Descripción**: Maneja la selección de un slot de guardado y navega a selección de personaje.
- **Parámetros**:
  - `slot` (int): Número del slot seleccionado.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._handle_slot_selection(1)
  ```

##### _handle_clear_slot
- **Descripción**: Maneja el vaciado de un slot de guardado.
- **Parámetros**:
  - `slot` (int): Número del slot a vaciar.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._handle_clear_slot(2)
  ```

##### _handle_character_selection
- **Descripción**: Maneja la selección de personaje tras elegir slot.
- **Parámetros**:
  - `character` (str): Nombre del personaje seleccionado.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._handle_character_selection("guerrero")
  ```

##### _handle_save_game
- **Descripción**: Maneja el guardado manual desde el menú de pausa.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  engine._handle_save_game()
  ```

### Archivo: `game_state.py`

#### Enum: GameStatus
- **Descripción**: Estados posibles del juego (MENU, PLAYING, PAUSED, GAME_OVER, VICTORY).
- **Valores**:
  - `MENU`: "menu"
  - `PLAYING`: "playing"
  - `PAUSED`: "paused"
  - `GAME_OVER`: "game_over"
  - `VICTORY`: "victory"

#### Clase: GameState

##### __init__
- **Descripción**: Inicializa el estado del juego con valores por defecto.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state = GameState()
  ```

##### reset_game
- **Descripción**: Reinicia el estado del juego para una nueva partida.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.reset_game()
  ```

##### add_score
- **Descripción**: Añade puntos al score actual y actualiza el récord si es necesario.
- **Parámetros**:
  - `points` (int): Puntos a añadir.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.add_score(100)
  ```

##### lose_life
- **Descripción**: Reduce una vida del jugador y cambia a GAME_OVER si no quedan vidas.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.lose_life()
  ```

##### next_level
- **Descripción**: Avanza al siguiente nivel incrementando el contador.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.next_level()
  ```

##### set_status
- **Descripción**: Establece el estado del juego.
- **Parámetros**:
  - `status` (GameStatus): Nuevo estado del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.set_status(GameStatus.PLAYING)
  ```

##### get_state_dict
- **Descripción**: Obtiene el estado actual como diccionario para serialización.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `Dict[str, Any]`: Diccionario con el estado actual del juego.
- **Ejemplo de Uso**:
  ```python
  state_dict = game_state.get_state_dict()
  ```

##### set_scene
- **Descripción**: Establece la escena actual del juego usando el scene_manager.
- **Parámetros**:
  - `scene_name` (str): Nombre de la escena.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.set_scene("main_menu")
  ```

##### load_state
- **Descripción**: Carga el estado desde un diccionario.
- **Parámetros**:
  - `state_dict` (Dict[str, Any]): Diccionario con el estado a cargar.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.load_state({"score": 500, "level": 2})
  ```

##### quit_game
- **Descripción**: Marca el juego para salir reseteando al estado MENU.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  game_state.quit_game()
  ```

### Archivo: `scene_manager.py`

#### Clase: Scene (Abstracta)

##### __init__
- **Descripción**: Inicializa la escena base con screen y config.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie de Pygame donde renderizar.
  - `config` (ConfigManager): Configuración del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene = ConcreteScene(screen, config)
  ```

##### handle_event (abstracto)
- **Descripción**: Procesa eventos de Pygame (método abstracto a implementar).
- **Parámetros**:
  - `event` (pygame.event.Event): Evento de Pygame.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene.handle_event(event)
  ```

##### update (abstracto)
- **Descripción**: Actualiza la lógica de la escena (método abstracto a implementar).
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene.update()
  ```

##### render (abstracto)
- **Descripción**: Renderiza la escena (método abstracto a implementar).
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene.render()
  ```

##### enter
- **Descripción**: Se llama cuando se entra en la escena.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene.enter()
  ```

##### exit
- **Descripción**: Se llama cuando se sale de la escena.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene.exit()
  ```

#### Clase: SceneManager

##### __init__
- **Descripción**: Inicializa el gestor de escenas con diccionario vacío de escenas.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie de Pygame donde renderizar.
  - `config` (ConfigManager): Configuración del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager = SceneManager(screen, config)
  ```

##### add_scene
- **Descripción**: Añade una escena al gestor con un nombre identificativo.
- **Parámetros**:
  - `name` (str): Nombre identificativo de la escena.
  - `scene` (Scene): Instancia de la escena.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager.add_scene("main_menu", main_menu_scene)
  ```

##### change_scene
- **Descripción**: Cambia a una escena específica de forma inmediata.
- **Parámetros**:
  - `scene_name` (str): Nombre de la escena a cambiar.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager.change_scene("game")
  ```

##### _switch_scene
- **Descripción**: Realiza el cambio de escena interno (privado).
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager._switch_scene()
  ```

##### handle_event
- **Descripción**: Procesa eventos de Pygame y los delega a la escena actual.
- **Parámetros**:
  - `event` (pygame.event.Event): Evento de Pygame.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager.handle_event(event)
  ```

##### update
- **Descripción**: Actualiza la lógica del gestor de escenas y la escena actual.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager.update()
  ```

##### render
- **Descripción**: Renderiza la escena actual o pantalla de carga si no hay escena.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  scene_manager.render()
  ```

---

## Módulo `src/entities/`

### Archivo: `character_data.py`

#### Constante: CHARACTER_DATA
- **Descripción**: Diccionario centralizado con información de personajes jugables (guerrero, adventureguirl, robot).
- **Tipo**: Dict[str, Dict]
- **Contenido**: Datos de estadísticas, habilidades, imágenes e información de personajes.
- **Ejemplo de Uso**:
  ```python
  personaje = CHARACTER_DATA["guerrero"]
  vida = personaje["stats"]["vida"]
  ```

### Archivo: `enemy.py`

#### Clase: Enemy

##### __init__
- **Descripción**: Inicializa un enemigo con posición, tipo y gestor de animaciones.
- **Parámetros**:
  - `x` (float): Posición X inicial.
  - `y` (float): Posición Y inicial.
  - `enemy_type` (str): Tipo de enemigo ('zombiemale' o 'zombieguirl').
  - `animation_manager`: Gestor de animaciones.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy = Enemy(100, 200, "zombiemale", animation_manager)
  ```

##### _setup_enemy_type
- **Descripción**: Configura propiedades específicas según el tipo de enemigo.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._setup_enemy_type()
  ```

##### update
- **Descripción**: Actualiza el estado del enemigo, animaciones e IA.
- **Parámetros**:
  - `dt` (float): Delta time en segundos.
  - `player_pos` (Optional[Tuple[float, float]]): Posición del jugador (x, y) si está cerca.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy.update(0.016, (100, 200))
  ```

##### _is_player_in_range
- **Descripción**: Verifica si el jugador está en rango de detección (300 píxeles).
- **Parámetros**:
  - `player_pos` (Tuple[float, float]): Posición del jugador.
- **Retorno**:
  - `bool`: True si el jugador está en rango.
- **Ejemplo de Uso**:
  ```python
  en_rango = enemy._is_player_in_range((150, 250))
  ```

##### _chase_player
- **Descripción**: Persigue al jugador calculando dirección y aplicando movimiento.
- **Parámetros**:
  - `player_pos` (Tuple[float, float]): Posición del jugador.
  - `dt` (float): Delta time en segundos.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._chase_player((150, 250), 0.016)
  ```

##### _patrol
- **Descripción**: Patrulla en un área definida usando puntos de patrulla.
- **Parámetros**:
  - `dt` (float): Delta time en segundos.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._patrol(0.016)
  ```

##### _generate_patrol_points
- **Descripción**: Genera puntos de patrulla aleatorios alrededor de la posición inicial.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._generate_patrol_points()
  ```

##### _attack_player
- **Descripción**: Ataca al jugador si el cooldown ha terminado.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._attack_player()
  ```

##### _update_facing_direction
- **Descripción**: Actualiza la dirección a la que mira el enemigo basado en el movimiento.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._update_facing_direction()
  ```

##### _update_dead_animation
- **Descripción**: Actualiza la animación de muerte del enemigo.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy._update_dead_animation()
  ```

##### take_damage
- **Descripción**: Recibe daño y marca como muerto si la salud llega a 0.
- **Parámetros**:
  - `damage` (int): Cantidad de daño a recibir.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy.take_damage(25)
  ```

##### get_current_frame
- **Descripción**: Obtiene el frame actual de la animación con escalado y volteo.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `Optional[pygame.Surface]`: Frame actual de la animación.
- **Ejemplo de Uso**:
  ```python
  frame = enemy.get_current_frame()
  ```

##### get_rect
- **Descripción**: Obtiene el rectángulo de colisión del enemigo.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `pygame.Rect`: Rectángulo de colisión.
- **Ejemplo de Uso**:
  ```python
  rect = enemy.get_rect()
  ```

##### is_attack_ready
- **Descripción**: Verifica si puede atacar según el cooldown.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `bool`: True si puede atacar.
- **Ejemplo de Uso**:
  ```python
  puede_atacar = enemy.is_attack_ready()
  ```

##### reset_attack_state
- **Descripción**: Resetea el estado de ataque del enemigo.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  enemy.reset_attack_state()
  ```

#### Clase: EnemyManager

##### __init__
- **Descripción**: Inicializa el gestor de enemigos con configuración de spawn.
- **Parámetros**:
  - `animation_manager`: Gestor de animaciones.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  manager = EnemyManager(animation_manager)
  ```

##### update
- **Descripción**: Actualiza todos los enemigos y maneja el spawn de nuevos.
- **Parámetros**:
  - `dt` (float): Delta time en segundos.
  - `player_pos` (Optional[Tuple[float, float]]): Posición del jugador.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  manager.update(0.016, (100, 200))
  ```

##### _spawn_enemies
- **Descripción**: Genera nuevos enemigos según el timer y límite máximo.
- **Parámetros**:
  - `dt` (float): Delta time en segundos.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  manager._spawn_enemies(0.016)
  ```

##### _spawn_enemy
- **Descripción**: Genera un enemigo en una posición aleatoria en los bordes del mundo.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  manager._spawn_enemy()
  ```

##### render
- **Descripción**: Renderiza todos los enemigos con offset de cámara.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie donde renderizar.
  - `camera_offset` (Tuple[float, float]): Offset de la cámara.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  manager.render(screen, (50, 100))
  ```

##### get_enemies_in_range
- **Descripción**: Obtiene enemigos en un rango específico desde una posición.
- **Parámetros**:
  - `pos` (Tuple[float, float]): Posición central del rango (x, y).
  - `range` (float): Distancia máxima para incluir enemigos.
- **Retorno**:
  - `List[Enemy]`: Lista de enemigos dentro del rango especificado.
- **Ejemplo de Uso**:
  ```python
  enemigos_cercanos = manager.get_enemies_in_range((100, 200), 50)
  ```

##### clear_all_enemies
- **Descripción**: Elimina todos los enemigos de la lista.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  manager.clear_all_enemies()
  ```

##### get_enemy_count
- **Descripción**: Obtiene el número de enemigos activos.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `int`: Número de enemigos activos.
- **Ejemplo de Uso**:
  ```python
  count = manager.get_enemy_count()
  ```

### Archivo: `enemy_types.py`

#### Enum: EnemyRarity
- **Descripción**: Rareza de los enemigos (NORMAL, RARE, ELITE, LEGENDARY).
- **Valores**: Cuatro niveles de rareza para sistema de loot.

#### Enum: EnemyBehavior
- **Descripción**: Comportamientos de enemigos (CHASE, WANDER, AMBUSH, SWARM, BOSS).
- **Valores**: Cinco tipos de IA diferentes.

#### Dataclass: EnemyConfig
- **Descripción**: Configuración completa de un tipo de enemigo con estadísticas.
- **Campos**: name, rarity, behavior, health, speed, damage, armor, score_value, color, symbol, size, spawn_chance
- **Redundancias identificadas**: **CRÍTICA** - Duplicación con `config/enemies.json`

#### Clase: EnemyTypes
- **Descripción**: Configuraciones estáticas de tipos de enemigos (ZOMBIE_NORMAL, ZOMBIE_RARE, etc.).
- **Redundancias identificadas**: **CRÍTICA** - Stats hardcodeados que deberían estar en JSON
- **Problema**: 231 líneas exceden límite de 150

### Archivo: `entity.py`

#### Enum: EntityType
- **Descripción**: Tipos de entidades (PLAYER, ENEMY, PROJECTILE, POWERUP, TILE).

#### Dataclass: EntityStats
- **Descripción**: Estadísticas base de entidades (health, speed, damage, etc.).

#### Clase: Entity (479 líneas - **CRÍTICO**)
- **Descripción**: Clase base abstracta para todas las entidades del juego.
- **Problema**: 479 líneas exceden extremadamente el límite de 150 líneas.
- **Métodos principales**: move, update, render, take_damage, heal, apply_effect

### Archivo: `player.py`

#### Clase: Player (390 líneas - **CRÍTICO**)
- **Descripción**: Clase principal del jugador que coordina stats, effects y combat.
- **Problema**: 390 líneas exceden extremadamente el límite de 150 líneas.
- **Sistemas integrados**: PlayerStats, PlayerEffects, PlayerCombat

### Archivo: `player_stats.py`

#### Dataclass: PlayerStats (149 líneas - **COMPLIANT**)
- **Descripción**: Estadísticas específicas del jugador (shoot_speed, bullet_speed).
- **Estado**: Dentro del límite de 150 líneas.

### Archivo: `player_effects.py`

#### Clase: PlayerEffects (180 líneas - **EXCEDE**)
- **Descripción**: Gestiona efectos activos y powerups del jugador.
- **Problema**: 180 líneas exceden límite de 150 líneas.

### Archivo: `player_combat.py`

#### Clase: AttackConfig + PlayerCombat (382 líneas - **CRÍTICO**)
- **Descripción**: Sistema de combate del jugador (disparos, daño, ataques).
- **Problema**: 382 líneas exceden extremadamente el límite de 150 líneas.

### Archivo: `projectile.py`

#### Clase: Projectile (125 líneas - **COMPLIANT**)
- **Descripción**: Proyectiles disparados por el jugador.
- **Estado**: Dentro del límite de 150 líneas.

### Archivo: `powerup.py`

#### Enum: PowerupType + Clases (272 líneas - **CRÍTICO**)
- **Descripción**: Sistema de powerups (SPEED, DAMAGE, SHIELD, etc.).
- **Problema**: 272 líneas exceden límite de 150 líneas.

### Archivo: `tile.py`

#### Enum: TileType + Clase (218 líneas - **EXCEDE**)
- **Descripción**: Sistema de tiles del escenario (TREE, ROCK, BUSH, etc.).
- **Problema**: 218 líneas exceden límite de 150 líneas.

---

## Módulo `src/scenes/`

### Archivos de Escenas (Análisis Rápido)

### src/scenes/character_animations.py

#### CharacterAnimations
```python
class CharacterAnimations:
    """
    Gestiona las animaciones de personajes en la selección.
    """
    def __init__(self):
        """Inicializa el gestor de animaciones de personajes."""

    def _load_animation_frames(self):
        """Carga los frames de animación para todos los personajes."""

    def _load_character_frames(self, character_key: str) -> list:
        """
        Carga los frames de animación para un personaje específico.

        Args:
            character_key: Clave del personaje

        Returns:
            list: Lista de frames de animación
        """

    def _get_possible_paths(self, character_key: str) -> list:
        """
        Genera las rutas posibles para buscar frames de un personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            list: Lista de rutas posibles
        """

    def _create_character_placeholder(self, character_key: str) -> pygame.Surface:
        """
        Crea un sprite placeholder para un personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            pygame.Surface: Superficie placeholder
        """

    def update(self, delta_time: float):
        """
        Actualiza las animaciones.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """

    def get_character_image(self, character_key: str) -> Optional[pygame.Surface]:
        """
        Obtiene la imagen actual del personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            Superficie del personaje o None si no existe
        """
```

### src/scenes/character_data.py

#### CharacterData
```python
class CharacterData:
    """
    Gestiona todos los datos de personajes jugables.
    """
    @classmethod
    def get_character_data(cls, character_key: str) -> Dict[str, Any] | None:
        """
        Obtiene los datos de un personaje específico.

        Args:
            character_key: Clave del personaje

        Returns:
            dict: Datos del personaje o None si no existe
        """

    @classmethod
    def is_valid_character(cls, character_key: str) -> bool:
        """
        Verifica si un personaje es válido.

        Args:
            character_key: Clave del personaje

        Returns:
            bool: True si el personaje existe, False en caso contrario
        """

    @classmethod
    def get_character_summary(cls, character_key: str) -> Dict[str, Any]:
        """
        Obtiene un resumen completo de un personaje.

        Args:
            character_key: Clave del personaje

        Returns:
            dict: Resumen del personaje con todos sus datos
        """

    @classmethod
    def validate_character_data(cls):
        """Valida que los datos de los personajes cumplan con el esquema esperado."""
```

### src/scenes/character_select_scene.py

#### CharacterSelectScene
```python
class CharacterSelectScene(Scene):
    """
    Escena de selección de personaje jugable (Refactorizada V2).
    """
    def __init__(self, screen, config, game_state, save_manager):
        """Inicializa la escena de selección de personajes."""

    def update(self):
        """Actualiza la escena."""

    def render(self):
        """Renderiza la escena."""

    def _navigate_character(self, direction: int):
        """
        Navega entre los personajes disponibles.

        Args:
            direction: Dirección de navegación (-1 para anterior, 1 para siguiente)
        """

    def _render_selected_character(self):
        """Renderiza el personaje seleccionado."""

    def handle_event(self, event):
        """
        Maneja eventos de la escena.

        Args:
            event: Evento de Pygame
        """
```

### src/scenes/character_ui.py

#### CharacterUI
```python
class CharacterUI:
    """
    Gestiona la interfaz de usuario para la selección de personajes.
    """
    def __init__(self, screen_width: int, screen_height: int, config_manager):
        """Inicializa la interfaz de usuario de personajes."""

    def render_title(self, screen: pygame.Surface):
        """Renderiza el título de la pantalla."""

    def render_character_card(self, screen: pygame.Surface, character_key: str, x: int, y: int, is_selected: bool = False):
        """
        Renderiza una tarjeta de personaje.

        Args:
            screen: Superficie donde renderizar
            character_key: Clave del personaje
            x: Posición X
            y: Posición Y
            is_selected: Si está seleccionado
        """

    def render_character_stats(self, screen: pygame.Surface, char_data: dict, x: int, y: int):
        """
        Renderiza las estadísticas de un personaje.

        Args:
            screen: Superficie donde renderizar
            char_data: Datos del personaje
            x: Posición X
            y: Posición Y
        """

    def render_buttons(self, screen: pygame.Surface, mouse_pos: Tuple[int, int]):
        """
        Renderiza los botones de la interfaz.

        Args:
            screen: Superficie donde renderizar
            mouse_pos: Posición del mouse
        """

    def get_clicked_button(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Obtiene el botón clickeado.

        Args:
            mouse_pos: Posición del mouse

        Returns:
            Nombre del botón clickeado o None
        """
```

### src/scenes/game_scene.py

#### GameScene (Legacy Wrapper)
```python
# Este archivo es un wrapper temporal sin funciones activas
# Actúa como puente de compatibilidad durante la migración a módulos modularizados
# Archivo candidato para eliminación tras verificar dependencias
```

### src/utils/asset_manager.py

#### AssetManager
```python
class AssetManager:
    """Gestor centralizado de assets del juego."""

    def __init__(self, base_path: str = "assets"):
        """Inicializa el AssetManager."""

    def load_image(self, path: str, scale: float = 1.0) -> Optional[pygame.Surface]:
        """
        Carga una imagen con caché.

        Args:
            path: Ruta de la imagen
            scale: Factor de escala

        Returns:
            Superficie de pygame o None si falla
        """

    def get_character_sprite(self, character_name: str, animation: str, frame: int = 1, scale: float = 1.0) -> Optional[pygame.Surface]:
        """
        Obtiene un sprite de personaje específico.

        Args:
            character_name: Nombre del personaje
            animation: Tipo de animación
            frame: Número de frame
            scale: Factor de escala

        Returns:
            Superficie del sprite o None si falla
        """

    def get_character_animation_frames(self, character_name: str, animation: str, max_frames: Optional[int] = None) -> List[pygame.Surface]:
        """
        Obtiene todos los frames de una animación específica.

        Args:
            character_name: Nombre del personaje
            animation: Tipo de animación
            max_frames: Número máximo de frames a cargar

        Returns:
            Lista de superficies de pygame
        """

    def load_animation_frames(self, ruta: str, max_frames: Optional[int] = None) -> List[pygame.Surface]:
        """
        Carga los frames de animación desde una ruta específica.

        Args:
            ruta: Ruta relativa dentro de la carpeta de assets
            max_frames: Número máximo de frames a cargar

        Returns:
            Lista de superficies de Pygame representando los frames

        Raises:
            FileNotFoundError: Si la ruta no existe o no contiene imágenes
        """

    def get_ui_button(self, button_name: str, state: str = "normal") -> Optional[pygame.Surface]:
        """
        Carga un botón de UI.

        Args:
            button_name: Nombre del botón
            state: Estado del botón ('normal', 'pressed', 'hover')

        Returns:
            Superficie del botón o None si falla
        """

    def clear_cache(self):
        """Limpia la caché de imágenes."""

    def get_cache_info(self) -> Dict[str, Any]:
        """Obtiene información sobre la caché."""
```

### src/utils/camera.py

#### Camera
```python
class Camera:
    """
    Sistema de cámara que sigue al jugador y gestiona la vista del mundo.
    """
    def __init__(self, screen_width: int, screen_height: int, world_width: int, world_height: int):
        """
        Inicializa la cámara.

        Args:
            screen_width: Ancho de la pantalla
            screen_height: Alto de la pantalla
            world_width: Ancho del mundo
            world_height: Alto del mundo
        """

    def follow_target(self, target_x: float, target_y: float):
        """
        Hace que la cámara siga a un objetivo.

        Args:
            target_x: Posición X del objetivo
            target_y: Posición Y del objetivo
        """

    def update(self, delta_time: float):
        """
        Actualiza la posición de la cámara con suavizado.

        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """

    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """
        Convierte coordenadas del mundo a coordenadas de pantalla.

        Args:
            world_x: Coordenada X del mundo
            world_y: Coordenada Y del mundo

        Returns:
            Tupla con coordenadas de pantalla (x, y)
        """

    def screen_to_world(self, screen_x: float, screen_y: float) -> Tuple[float, float]:
        """
        Convierte coordenadas de pantalla a coordenadas del mundo.

        Args:
            screen_x: Coordenada X de pantalla
            screen_y: Coordenada Y de pantalla

        Returns:
            Tupla con coordenadas del mundo (x, y)
        """

    def is_visible(self, world_x: float, world_y: float, width: float = 0, height: float = 0) -> bool:
        """
        Verifica si un objeto está visible en pantalla.

        Args:
            world_x: Posición X del mundo
            world_y: Posición Y del mundo
            width: Ancho del objeto
            height: Alto del objeto

        Returns:
            True si el objeto está visible
        """

    def get_viewport(self) -> Tuple[float, float, float, float]:
        """
        Obtiene el área visible del mundo.

        Returns:
            Tupla con (x, y, width, height) del área visible
        """

    def get_position(self) -> Tuple[float, float]:
        """
        Obtiene la posición actual de la cámara.

        Returns:
            Tupla con posición (x, y) de la cámara
        """
```

### src/utils/config_manager.py

#### ConfigManager
```python
class ConfigManager:
    """
    Gestiona la configuración del juego.
    """
    def __init__(self, config_file: str = "config.json"):
        """Inicializa el gestor de configuración."""

    def _load_default_config(self) -> Dict[str, Any]:
        """Carga la configuración por defecto."""

    def _load_config(self):
        """Carga la configuración principal desde archivo."""

    def _load_specific_configs(self):
        """Carga las configuraciones específicas desde el directorio config/."""

    def _merge_config(self, file_config: Dict[str, Any]):
        """Combina la configuración del archivo con la por defecto."""

    def save_config(self):
        """Guarda la configuración actual en archivo."""

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.

        Args:
            section: Sección de configuración
            key: Clave del valor
            default: Valor por defecto si no existe

        Returns:
            Valor de configuración
        """

    def set(self, section: str, key: str, value: Any):
        """
        Establece un valor de configuración.

        Args:
            section: Sección de configuración
            key: Clave del valor
            value: Valor a establecer
        """

    def get_section(self, section: str) -> Dict[str, Any]:
        """Obtiene una sección completa de configuración."""

    def reload(self):
        """Recarga la configuración desde archivo."""

    def get_music_volume(self) -> float:
        """Obtiene el volumen de música."""

    def get_sfx_volume(self) -> float:
        """Obtiene el volumen de efectos de sonido."""

    def get_master_volume(self) -> float:
        """Obtiene el volumen maestro."""

    def get_audio_enabled(self) -> bool:
        """Obtiene si el audio está habilitado."""

    def get_character_data(self, character_name: str) -> Dict[str, Any]:
        """Devuelve la configuración completa de un personaje."""

    def get_enemy_data(self, enemy_type: str) -> Dict[str, Any]:
        """Obtiene los datos de un enemigo específico."""

    def get_powerup_data(self, powerup_type: str) -> Dict[str, Any]:
        """Obtiene los datos de un powerup específico."""

    def get_ui_dimension(self, key: str, default: int = 0) -> int:
        """Obtiene una dimensión de UI."""

    def get_ui_color(self, key: str, default=(255, 255, 255)) -> tuple:
        """Obtiene un color de UI."""

    def get_ui_font_size(self, key: str, default: int = 24) -> int:
        """Obtiene un tamaño de fuente de UI."""

    def get_resolution(self) -> tuple:
        """Obtiene la resolución actual."""

    def get_fps(self) -> int:
        """Obtiene el FPS configurado."""

    def get_key_binding(self, action: str) -> str:
        """Obtiene la tecla asignada a una acción."""
```

### src/utils/desert_background.py

#### SandParticle
```python
class SandParticle:
    """Partícula de arena para efectos atmosféricos."""

    def __init__(self, x: float, y: float, screen_width: int, screen_height: int):
        """Inicializa una partícula de arena."""

    def update(self, delta_time: float):
        """Actualiza la partícula de arena."""

    def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Renderiza la partícula de arena."""
```

#### Dune
```python
class Dune:
    """Duna de arena para el fondo."""

    def __init__(self, x: float, y: float, width: float, height: float, screen_width: int):
        """Inicializa una duna de arena."""

    def _generate_dune_points(self) -> List[Tuple[float, float]]:
        """Genera puntos para dibujar la duna."""

    def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Renderiza la duna."""
```

#### DesertBackground
```python
class DesertBackground:
    """Sistema de fondo dinámico de desierto con efectos visuales."""

    def __init__(self, screen_width: int, screen_height: int):
        """Inicializa el fondo de desierto."""

    def _create_sand_particles(self, count: int):
        """Crea partículas de arena."""

    def _create_dunes(self):
        """Crea las dunas del desierto."""

    def update(self, delta_time: float):
        """Actualiza el fondo de desierto."""

    def render(self, screen: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Renderiza el fondo de desierto."""

    def _render_sky_gradient(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
        """Renderiza el gradiente del cielo con más profundidad."""

    def _render_dunes(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
        """Renderiza las dunas de arena con efectos de profundidad."""

    def _render_sand_particles(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
        """Renderiza las partículas de arena."""

    def _render_atmospheric_effects(self, screen: pygame.Surface, camera_offset: Tuple[float, float]):
        """Renderiza efectos atmosféricos adicionales."""

    def _interpolate_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Interpola entre dos colores."""

    def get_parallax_offset(self, camera_x: float, camera_y: float, layer: str = "background") -> Tuple[float, float]:
        """
        Obtiene el offset de parallax para diferentes capas.

        Args:
            camera_x: Posición X de la cámara
            camera_y: Posición Y de la cámara
            layer: Capa del parallax

        Returns:
            Offset de parallax (x, y)
        """
```

### src/utils/input_manager.py

#### InputManager
```python
class InputManager:
    """
    Gestiona las entradas del usuario.
    """
    def __init__(self):
        """Inicializa el gestor de entrada."""

    def handle_event(self, event: pygame.event.Event):
        """
        Procesa un evento de Pygame.

        Args:
            event: Evento de Pygame a procesar
        """

    def _handle_key_down(self, key: int):
        """Procesa una tecla presionada."""

    def _handle_key_up(self, key: int):
        """Procesa una tecla liberada."""

    def _handle_mouse_down(self, button: int):
        """Procesa un botón del ratón presionado."""

    def _handle_mouse_up(self, button: int):
        """Procesa un botón del ratón liberado."""

    def _handle_gamepad_down(self, button: int):
        """Procesa un botón del gamepad presionado."""

    def _handle_gamepad_up(self, button: int):
        """Procesa un botón del gamepad liberado."""

    def _handle_gamepad_axis(self, axis: int, value: float):
        """Procesa movimiento de eje del gamepad."""

    def _check_actions(self):
        """Verifica si se han activado acciones."""

    def is_key_pressed(self, key: int) -> bool:
        """
        Verifica si una tecla está presionada.

        Args:
            key: Código de la tecla

        Returns:
            True si la tecla está presionada
        """

    def is_action_pressed(self, action: InputAction) -> bool:
        """
        Verifica si una acción está activa.

        Args:
            action: Acción a verificar

        Returns:
            True si la acción está activa
        """

    def get_mouse_position(self) -> tuple:
        """Obtiene la posición actual del ratón."""

    def is_mouse_button_pressed(self, button: int) -> bool:
        """Verifica si un botón del ratón está presionado."""

    def get_gamepad_axis(self, axis: int) -> float:
        """Obtiene el valor de un eje del gamepad."""

    def add_key_callback(self, key: int, callback: Callable):
        """Añade un callback para una tecla específica."""

    def add_action_callback(self, action: InputAction, callback: Callable):
        """Añade un callback para una acción específica."""

    def set_action_mapping(self, action: InputAction, keys: Set[int]):
        """Establece el mapeo de teclas para una acción."""

    def reset_states(self):
        """Reinicia todos los estados de entrada."""
```

### src/utils/save_manager.py

#### SaveManager
```python
class SaveManager:
    """
    Gestiona el sistema de guardado del juego con cifrado y múltiples archivos.
    """
    def __init__(self, config: ConfigManager):
        """Inicializa el gestor de guardado."""

    def _generate_encryption_key(self) -> str:
        """Genera una clave de cifrado basada en la configuración del juego."""

    def _load_save_files_info(self) -> List[Dict[str, Any]]:
        """Carga la información de los archivos de guardado existentes."""

    def get_save_files_info(self) -> List[Dict[str, Any]]:
        """Obtiene información de todos los archivos de guardado."""

    def create_new_save(self, save_file_number: int) -> bool:
        """
        Crea un nuevo archivo de guardado.

        Args:
            save_file_number: Número del archivo de guardado (1-3)

        Returns:
            True si se creó correctamente
        """

    def load_save(self, save_file_number: int) -> Optional[Dict[str, Any]]:
        """
        Carga un archivo de guardado.

        Args:
            save_file_number: Número del archivo de guardado

        Returns:
            Datos del guardado o None si hay error
        """

    def save_game(self, game_state, additional_data: Dict[str, Any] = None) -> bool:
        """
        Guarda el estado del juego.

        Args:
            game_state: Estado del juego a guardar
            additional_data: Datos adicionales a guardar

        Returns:
            True si se guardó correctamente
        """

    def delete_save(self, save_file_number: int) -> bool:
        """Elimina un archivo de guardado."""

    def _encrypt_data(self, data: bytes) -> bytes:
        """Cifra los datos."""

    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Descifra los datos."""

    def _update_save_info(self, save_info: Dict[str, Any], game_state):
        """Actualiza la información del archivo de guardado."""

    def _validate_save_file(self, save_data: Dict[str, Any]) -> bool:
        """Valida la integridad de un archivo de guardado."""

    def backup_saves(self) -> bool:
        """Crea una copia de seguridad de todos los archivos de guardado."""

    def restore_backup(self, backup_path: str) -> bool:
        """Restaura archivos de guardado desde una copia de seguridad."""
```

### src/utils/world_generator.py

#### WorldGenerator
```python
class WorldGenerator:
    """
    Generador de mundo que crea elementos distribuidos por el escenario.
    """
    def __init__(self, world_width: int, world_height: int, screen_width: int, screen_height: int):
        """Inicializa el generador de mundo."""

    def _load_available_sprites(self) -> List[str]:
        """Carga los sprites disponibles de assets/objects/elementos/."""

    def generate_world(self, element_types: Optional[List[TileType]] = None) -> List[Tile]:
        """Genera el mundo completo con elementos distribuidos."""

    def _is_valid_position(self, x: float, y: float, existing_elements: List[Tile]) -> bool:
        """Verifica si una posición es válida para colocar un elemento."""

    def _create_element_with_sprite(self, x: float, y: float) -> Optional[Tile]:
        """Crea un elemento usando sprites reales de assets/objects/elementos/."""

    def _get_tile_type_from_filename(self, filename: str) -> TileType:
        """Determina el tipo de tile basado en el nombre del archivo."""

    def generate_cluster(self, center_x: float, center_y: float, radius: float, num_elements: int, element_types: List[TileType] = None) -> List[Tile]:
        """
        Genera un cluster de elementos en una zona específica.

        Args:
            center_x: Centro X del cluster
            center_y: Centro Y del cluster
            radius: Radio del cluster
            num_elements: Número de elementos a generar
            element_types: Tipos de elementos permitidos

        Returns:
            Lista de elementos del cluster
        """

    def generate_desert_oasis(self, center_x: float, center_y: float, radius: float) -> List[Tile]:
        """Genera un oasis en el desierto."""

    def generate_rock_formation(self, center_x: float, center_y: float, radius: float) -> List[Tile]:
        """Genera una formación de rocas."""

    def generate_cactus_field(self, center_x: float, center_y: float, radius: float) -> List[Tile]:
        """Genera un campo de cactus."""

    def generate_ruins(self, center_x: float, center_y: float, radius: float) -> List[Tile]:
        """Genera ruinas antiguas."""
```

### add_effect
- **Descripción**: Añade un efecto a la entidad, como invulnerabilidad o aumento de velocidad.
- **Parámetros**:
  - `effect_name` (str): Nombre del efecto.
  - `effect_data` (Dict[str, Any]): Datos del efecto (duración, valor, etc.).
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  entidad.add_effect("invulnerable", {"duration": 5})
  ```

### collides_with
- **Descripción**: Verifica si esta entidad colisiona con otra.
- **Parámetros**:
  - `other` (Entity): Otra entidad.
- **Retorno**:
  - `bool`: True si hay colisión.
- **Ejemplo de Uso**:
  ```python
  if entidad.collides_with(otro):
      print("Colisión detectada")
  ```

### render
- **Descripción**: Renderiza la entidad en pantalla, incluyendo efectos visuales y depuración.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie donde renderizar.
  - `camera_offset` (Tuple[float, float]): Offset de la cámara para coordenadas de pantalla.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  entidad.render(pantalla, (100, 200))
  ```

### get_data
- **Descripción**: Obtiene los datos de la entidad para guardado.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `Dict[str, Any]`: Diccionario con los datos de la entidad.
- **Ejemplo de Uso**:
  ```python
  datos = entidad.get_data()
  ```

### load_data
- **Descripción**: Carga datos en la entidad desde un diccionario.
- **Parámetros**:
  - `data` (Dict[str, Any]): Datos a cargar.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  entidad.load_data(datos)
  ```

### Player
- **Descripción**: Representa al jugador del juego con animaciones y mecánicas de bullet hell.

#### Métodos:

### __init__
- **Descripción**: Inicializa el jugador con estadísticas, animaciones y sistemas modulares.
- **Parámetros**:
  - `x` (float): Posición X inicial.
  - `y` (float): Posición Y inicial.
  - `character_name` (str): Nombre del personaje seleccionado.
  - `config` (ConfigManager): Configuración del juego.
  - `animation_manager` (IntelligentAnimationManager): Gestor de animaciones.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  jugador = Player(100, 200, "guerrero", config, animation_manager)
  ```

### handle_input
- **Descripción**: Maneja la entrada del usuario para mover al jugador y realizar ataques.
- **Parámetros**:
  - `keys` (pygame.key.ScancodeWrapper): Estado de las teclas.
  - `mouse_pos` (Tuple[int, int]): Posición del ratón.
  - `mouse_buttons` (Tuple[bool, bool, bool]): Estado de los botones del ratón.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  jugador.handle_input(teclas, (400, 300), (True, False, False))
  ```

### attack
- **Descripción**: Ejecuta el ataque actual según el tipo (melee, ranged, area).
- **Parámetros**:
  - `target_pos` (Tuple[int, int]): Posición objetivo del ataque.
  - `enemies` (List[Any]): Lista de enemigos en el área.
- **Retorno**: Lista de resultados del ataque.
- **Ejemplo de Uso**:
  ```python
  jugador.attack((500, 500), lista_enemigos)
  ```

### take_damage
- **Descripción**: Aplica daño al jugador.
- **Parámetros**:
  - `damage` (float): Cantidad de daño.
  - `source` (Optional[Any]): Fuente del daño.
- **Retorno**:
  - `bool`: True si el jugador murió, False en caso contrario.
- **Ejemplo de Uso**:
  ```python
  if jugador.take_damage(50):
      print("Jugador muerto")
  ```

### heal
- **Descripción**: Cura al jugador.
- **Parámetros**:
  - `amount` (float): Cantidad de vida a recuperar.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  jugador.heal(20)
  ```

### apply_powerup
- **Descripción**: Aplica un powerup al jugador.
- **Parámetros**:
  - `powerup_effect` (PowerupEffect): Efecto del powerup.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  jugador.apply_powerup(powerup)
  ```

### update
- **Descripción**: Actualiza la posición, efectos y animaciones del jugador.
- **Parámetros**:
  - `delta_time` (float): Tiempo transcurrido desde el último frame.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  jugador.update(0.016)
  ```

### main
- **Descripción**: Función principal que inicializa y ejecuta el juego.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  if __name__ == "__main__":
      main()
  ```

### __init__ (ConfigManager)
- **Descripción**: Inicializa el gestor de configuración.
- **Parámetros**:
  - `config_file` (str): Ruta al archivo de configuración principal.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  config = ConfigManager("config.json")
  ```

### _load_default_config
- **Descripción**: Carga la configuración por defecto.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `Dict[str, Any]`: Configuración por defecto.
- **Ejemplo de Uso**:
  ```python
  default_config = config._load_default_config()
  ```

### _load_config
- **Descripción**: Carga la configuración principal desde archivo.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  config._load_config()
  ```

### _load_specific_configs
- **Descripción**: Carga las configuraciones específicas desde el directorio `config/`.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  config._load_specific_configs()
  ```

### WorldGenerator.__init__
- **Descripción**: Inicializa el generador de mundo.
- **Parámetros**:
  - `world_width` (int): Ancho del mundo (3-4 veces la pantalla).
  - `world_height` (int): Alto del mundo (3-4 veces la pantalla).
  - `screen_width` (int): Ancho de la pantalla.
  - `screen_height` (int): Alto de la pantalla.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  generator = WorldGenerator(4000, 3000, 1280, 720)
  ```

### WorldGenerator._load_available_sprites
- **Descripción**: Carga los sprites disponibles de `assets/objects/elementos/`.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `List[str]`: Lista de nombres de archivos de sprites disponibles.
- **Ejemplo de Uso**:
  ```python
  sprites = generator._load_available_sprites()
  ```

### WorldGenerator.generate_world
- **Descripción**: Genera el mundo completo con elementos distribuidos.
- **Parámetros**:
  - `element_types` (Optional[List[TileType]]): Tipos de elementos a generar.
- **Retorno**:
  - `List[Tile]`: Lista de elementos generados.
- **Ejemplo de Uso**:
  ```python
  world_elements = generator.generate_world()
  ```

### SaveManager.__init__
- **Descripción**: Inicializa el gestor de guardado.
- **Parámetros**:
  - `config` (ConfigManager): Configuración del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  save_manager = SaveManager(config)
  ```

### SaveManager._generate_encryption_key
- **Descripción**: Genera una clave de cifrado basada en la configuración del juego.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `str`: Clave de cifrado.
- **Ejemplo de Uso**:
  ```python
  encryption_key = save_manager._generate_encryption_key()
  ```

### SaveManager._load_save_files_info
- **Descripción**: Carga la información de los archivos de guardado existentes.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `List[Dict[str, Any]]`: Lista con información de archivos de guardado.
- **Ejemplo de Uso**:
  ```python
  save_files_info = save_manager._load_save_files_info()
  ```

### SimpleDesertBackground.__init__
- **Descripción**: Inicializa el fondo simple de desierto.
- **Parámetros**:
  - `screen_width` (int): Ancho de la pantalla.
  - `screen_height` (int): Alto de la pantalla.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  desert_background = SimpleDesertBackground(1280, 720)
  ```

### SimpleDesertBackground.update
- **Descripción**: Actualiza el fondo (no hace nada en esta versión simple).
- **Parámetros**:
  - `delta_time` (float): Tiempo transcurrido desde el último frame.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  desert_background.update(0.016)
  ```

### SimpleDesertBackground.render
- **Descripción**: Renderiza el fondo plano de desierto.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie donde renderizar.
  - `camera_x` (float): Posición X de la cámara (no usado en esta versión).
  - `camera_y` (float): Posición Y de la cámara (no usado en esta versión).
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  desert_background.render(screen)
  ```

### setup_logger
- **Descripción**: Configura el sistema de logging del juego.
- **Parámetros**:
  - `name` (str): Nombre del logger.
  - `log_file` (str): Ruta al archivo de log.
  - `level` (int): Nivel de logging.
  - `max_bytes` (int): Tamaño máximo del archivo de log.
  - `backup_count` (int): Número de archivos de backup.
- **Retorno**:
  - `logging.Logger`: Logger configurado.
- **Ejemplo de Uso**:
  ```python
  logger = setup_logger("SiK_Game", "logs/game.log")
  ```

### AnimationManager.__init__
- **Descripción**: Inicializa el gestor de animaciones.
- **Parámetros**:
  - `asset_manager` (Optional[AssetManager]): Gestor de assets para cargar animaciones.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  animation_manager = AnimationManager()
  ```

### AnimationManager.get_optimal_fps
- **Descripción**: Calcula el FPS óptimo para una animación basado en el número de fotogramas.
- **Parámetros**:
  - `animation_type` (str): Tipo de animación (idle, run, attack, etc.).
  - `frame_count` (int): Número de fotogramas disponibles.
- **Retorno**:
  - `int`: FPS óptimo para la animación.
- **Ejemplo de Uso**:
  ```python
  optimal_fps = animation_manager.get_optimal_fps("run", 10)
  ```

### HUD.__init__
- **Descripción**: Inicializa el sistema de HUD.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie de Pygame donde renderizar.
  - `config` (ConfigManager): Configuración del juego.
  - `game_state` (GameState): Estado del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  hud = HUD(screen, config, game_state)
  ```

### MenuCallbacks.__init__
- **Descripción**: Inicializa los callbacks de menú.
- **Parámetros**:
  - `game_state` (GameState): Estado del juego.
  - `save_manager` (SaveManager): Gestor de guardado.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  callbacks = MenuCallbacks(game_state, save_manager)
  ```

### MenuCallbacks.on_new_game
- **Descripción**: Callback para iniciar un nuevo juego.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  callbacks.on_new_game()
  ```

### MenuFactory.__init__
- **Descripción**: Inicializa la fábrica de menús.
- **Parámetros**:
  - `screen` (pygame.Surface): Superficie de Pygame.
  - `config` (ConfigManager): Configuración del juego.
  - `save_manager` (SaveManager): Gestor de guardado.
  - `callbacks` (MenuCallbacks): Callbacks de menú.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  menu_factory = MenuFactory(screen, config, save_manager, callbacks)
  ```

### MenuFactory._create_theme
- **Descripción**: Crea el tema visual para los menús.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `pygame_menu.themes.Theme`: Tema visual configurado.
- **Ejemplo de Uso**:
  ```python
  theme = menu_factory._create_theme()
  ```

### PlayerCombat.__init__
- **Descripción**: Inicializa el sistema de combate del jugador.
- **Parámetros**:
  - `player_stats` (PlayerStats): Estadísticas del jugador.
  - `player_effects` (PlayerEffects): Efectos activos del jugador.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  combat_system = PlayerCombat(player_stats, player_effects)
  ```

### PlayerEffects.__init__
- **Descripción**: Inicializa el gestor de efectos del jugador.
- **Parámetros**: Ninguno.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  effects_manager = PlayerEffects()
  ```

### PlayerEffects.apply_powerup
- **Descripción**: Aplica un powerup al jugador.
- **Parámetros**:
  - `powerup_effect` (PowerupEffect): Efecto del powerup a aplicar.
  - `current_time` (float): Tiempo actual del juego.
- **Retorno**: Ninguno.
- **Ejemplo de Uso**:
  ```python
  effects_manager.apply_powerup(powerup_effect, current_time)
  ```

### PlayerStats.to_dict
- **Descripción**: Convierte las estadísticas del jugador a un diccionario para guardado.
- **Parámetros**: Ninguno.
- **Retorno**:
  - `Dict[str, Any]`: Diccionario con las estadísticas del jugador.
- **Ejemplo de Uso**:
  ```python
  stats_dict = player_stats.to_dict()
  ```

### PlayerStats.from_dict
- **Descripción**: Crea estadísticas del jugador desde un diccionario.
- **Parámetros**:
  - `data` (Dict[str, Any]): Diccionario con los datos de las estadísticas.
- **Retorno**:
  - `PlayerStats`: Instancia de PlayerStats creada desde el diccionario.
- **Ejemplo de Uso**:
  ```python
  player_stats = PlayerStats.from_dict(data)
  ```

### src/entities/powerup.py

#### Powerup
```python
class Powerup(Entity):
    """
    Powerup que mejora temporalmente al jugador.
    """
    def __init__(self, x: float, y: float, powerup_type: PowerupType):
        """
        Inicializa un powerup.

        Args:
            x: Posición X
            y: Posición Y
            powerup_type: Tipo de powerup
        """

    def _setup_sprite(self):
        """Configura el sprite del powerup."""

    def _add_symbol(self):
        """Añade un símbolo al sprite según el tipo de powerup."""

    def _get_symbol(self) -> str:
        """Obtiene el símbolo para el tipo de powerup."""

    def update(self, delta_time: float):
        """Actualiza el powerup."""

    def _update_logic(self, delta_time: float):
        """Actualiza la lógica específica del powerup."""

    def render(self, screen: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Renderiza el powerup con efecto de flotación."""

    def get_effect(self) -> PowerupEffect:
        """Obtiene el efecto del powerup."""

    @classmethod
    def create_random(cls, x: float, y: float) -> "Powerup":
        """
        Crea un powerup aleatorio.

        Args:
            x: Posición X
            y: Posición Y

        Returns:
            Powerup aleatorio
        """

    @classmethod
    def get_all_types(cls) -> list:
        """Obtiene todos los tipos de powerups disponibles."""
```

### src/entities/projectile.py

#### Projectile
```python
class Projectile(Entity):
    """
    Representa un proyectil disparado por el jugador.
    """
    def __init__(
        self,
        x: float,
        y: float,
        target_x: float,
        target_y: float,
        damage: float,
        speed: float,
        config: ConfigManager,
    ):
        """
        Inicializa un proyectil.

        Args:
            x: Posición X inicial
            y: Posición Y inicial
            target_x: Posición X objetivo (cursor)
            target_y: Posición Y objetivo (cursor)
            damage: Daño del proyectil
            speed: Velocidad del proyectil
            config: Configuración del juego
        """

    def _setup_sprite(self):
        """Configura el sprite del proyectil."""

    def _update_logic(self, delta_time: float):
        """Actualiza la lógica del proyectil."""

    def get_damage(self) -> float:
        """Obtiene el daño del proyectil."""

    def on_hit(self):
        """Se llama cuando el proyectil impacta con algo."""
```

### src/entities/tile.py

#### Tile
```python
class Tile(Entity):
    """
    Tile del escenario que decora el mundo.
    """
    def __init__(
        self,
        x: float,
        y: float,
        tile_type: TileType,
        sprite_name: Optional[str] = None,
    ):
        """
        Inicializa un tile.

        Args:
            x: Posición X
            y: Posición Y
            tile_type: Tipo de tile
        """

    def _setup_sprite(self):
        """Configura el sprite del tile."""

    def _add_symbol(self):
        """Añade un símbolo al sprite según el tipo de tile."""

    def _update_logic(self, delta_time: float):
        """Actualiza la lógica específica del tile."""

    def has_collision(self) -> bool:
        """
        Verifica si el tile tiene colisión.

        Returns:
            True si el tile bloquea el movimiento
        """

    def get_tile_info(self) -> dict:
        """
        Obtiene información del tile.

        Returns:
            Dict con información del tile
        """

    @classmethod
    def create_random(cls, x: float, y: float) -> "Tile":
        """
        Crea un tile aleatorio.

        Args:
            x: Posición X
            y: Posición Y

        Returns:
            Tile aleatorio
        """

    @classmethod
    def get_all_types(cls) -> list:
        """Obtiene todos los tipos de tiles disponibles."""

---

## 🗄️ **MIGRACIÓN SQLITE - NUEVOS MÓDULOS** (Fase 1 Completada + Corregida)
*Referencia: [`PLAN_MIGRACION_SQLITE.md`](./PLAN_MIGRACION_SQLITE.md)*

### Directorio `src/utils/` - Infraestructura SQLite Refactorizada

#### database_manager.py (194 líneas - ⚠️ REQUIERE CORRECCIÓN)
**Descripción**: Gestor centralizado de conexiones SQLite con pooling y transacciones.

##### DatabaseManager.__init__
- **Descripción**: Inicializa el gestor de base de datos con connection pooling.
- **Parámetros**:
  - `db_path` (str): Ruta al archivo de base de datos SQLite (default: "saves/game_database.db")
  - `pool_size` (int): Número máximo de conexiones en el pool (default: 5)
- **Características**:
  - Connection pooling para evitar bloqueos
  - Configuración optimizada de SQLite (WAL mode, foreign keys, timeouts)
  - Logging detallado de operaciones
- **Ejemplo de Uso**:
  ```python
  db_manager = DatabaseManager("saves/game.db", pool_size=5)
  ```

#### schema_manager.py (135 líneas - ✅ CORREGIDO)
**Descripción**: Manager principal refactorizado que delega a módulos especializados.

##### SchemaManager.__init__
- **Descripción**: Inicializa el gestor de esquemas principal con delegación a SchemaCore.
- **Parámetros**:
  - `database_manager` (DatabaseManager): Instancia del gestor de BD
- **Características**:
  - API compatible con versión original
  - Delegación a módulos especializados (SchemaCore)
  - Mantenimiento de límite de 150 líneas
- **Ejemplo de Uso**:
  ```python
  schema_manager = SchemaManager(db_manager)
  ```

#### schema_core.py (131 líneas - ✅ NUEVO MÓDULO)
**Descripción**: Núcleo del sistema de esquemas SQLite con funcionalidad principal.

##### SchemaCore.__init__
- **Descripción**: Inicializa el núcleo del sistema de esquemas con integración a migraciones.
- **Parámetros**:
  - `database_manager` (DatabaseManager): Instancia del gestor de BD
- **Características**:
  - Creación automática de todas las tablas del sistema
  - Integración con sistema de migraciones
  - Validación de esquemas e integridad
  - Backup automático antes de cambios importantes
- **Ejemplo de Uso**:
  ```python
  schema_core = SchemaCore(db_manager)
  success = schema_core.create_all_tables()
  ```

#### schema_tables.py (135 líneas - ✅ NUEVO MÓDULO)
**Descripción**: Definiciones de todas las tablas SQLite del sistema de migración.

##### get_all_table_schemas
- **Descripción**: Obtiene todos los esquemas de tablas definidos para el sistema de migración.
- **Retorno**:
  - `Dict[str, str]`: Diccionario con nombre de tabla y su SQL de creación
- **Tablas incluidas**:
  - `partidas_guardadas`: Reemplaza pickle saves
  - `configuraciones`: Reemplaza JSON distribuido
  - `personajes`: Reemplaza characters.json + character_data.py
  - `enemigos`: Reemplaza enemies.json + enemy_types.py
  - `estadisticas_juego`: Estadísticas por sesión
  - `configuracion_gameplay`: Configuración de mecánicas
- **Ejemplo de Uso**:
  ```python
  schemas = get_all_table_schemas()
  partidas_schema = schemas["partidas_guardadas"]
  ```

#### schema_migrations.py (173 líneas - ⚠️ REQUIERE CORRECCIÓN)
**Descripción**: Sistema de migraciones y validaciones de esquema SQLite.

##### SchemaMigrations.__init__
- **Descripción**: Inicializa el gestor de migraciones con registro de cambios.
- **Características**:
  - Registro de migraciones aplicadas
  - Validación de integridad de esquemas
  - Cálculo de checksums para cambios
  - Rollback de migraciones si es necesario
- **Ejemplo de Uso**:
  ```python
  migrations = SchemaMigrations(db_manager)
  migrations.record_migration("Initial schema", "CREATE_ALL_TABLES")
  ```

### Archivos de Testing SQLite

#### scripts/test_simple_sqlite.py (✅ COMPLETADO)
**Descripción**: Script de pruebas básicas para validar infraestructura SQLite.

##### test_simple
- **Descripción**: Ejecuta pruebas de funcionalidad básica de DatabaseManager y SchemaManager.
- **Pruebas realizadas**:
  - Creación de DatabaseManager y SchemaManager
  - Creación de tablas automática
  - Validación de esquema
  - Inserción y lectura de datos de prueba
  - Limpieza de archivos temporales
- **Resultado**: ✅ Todas las pruebas pasan exitosamente
- **Ejemplo de Uso**:
  ```bash
  python scripts/test_simple_sqlite.py
  ```

## 🎯 **PRÓXIMOS PASOS DE MIGRACIÓN**

### FASE 2: Migración del ConfigManager (PENDIENTE)
**Objetivo**: Dividir ConfigManager (264→3x150 líneas) + migrar JSON a SQLite
**Referencia**: [`PLAN_MIGRACION_SQLITE.md - Fase 2`](./PLAN_MIGRACION_SQLITE.md#fase-2-migración-del-configmanager)

**Módulos a crear**:
- `config_loader.py` (máximo 150 líneas) - Carga desde archivos JSON
- `config_database.py` (máximo 150 líneas) - Operaciones SQLite para configuración
- `config_validator.py` (máximo 150 líneas) - Validación y compatibilidad

**Funciones a documentar** (actualizar al crear):
- ConfigLoader.__init__, load_config, load_all_configs
- ConfigDatabase.__init__, save_config, get_config, migrate_from_json
- ConfigValidator.__init__, validate_config, check_compatibility

### FASE 3: Migración del SaveManager (PENDIENTE)
**Objetivo**: Dividir SaveManager (365→4x150 líneas) + migrar pickle a SQLite
**Referencia**: [`PLAN_MIGRACION_SQLITE.md - Fase 3`](./PLAN_MIGRACION_SQLITE.md#fase-3-migración-del-savemanager)

**Módulos a crear**:
- `save_loader.py` - Carga de partidas y compatibilidad
- `save_encryption.py` - Encriptación XOR mantenida
- `save_database.py` - Operaciones SQLite para partidas
- `save_compatibility.py` - Migración automática pickle→SQLite

---

*📝 Nota: Este documento se actualiza automáticamente con cada nueva función creada durante la refactorización + migración SQLite.*
```
