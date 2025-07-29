# Análisis de Bases de Datos para SiK Python Game

## 🎯 Objetivo
Evaluar opciones de bases de datos sencillas, robustas y potentes que soporten SQL para integrar en nuestro videojuego Python.

## 📋 Contexto del Proyecto

### Estado Actual del Sistema de Persistencia
- **Save Manager existente**: Usa archivos binarios cifrados (pickle + zlib + XOR)
- **Configuración**: Archivos JSON modulares
- **Limitaciones actuales**:
  - Sin capacidad de consultas complejas
  - Difícil mantenimiento de estadísticas
  - Sin soporte para rankings o leaderboards
  - Backup y sincronización limitados

### Necesidades Identificadas
1. **Guardado de partidas** con versionado
2. **Estadísticas de jugador** y progreso
3. **Rankings y leaderboards**
4. **Configuraciones** centralizadas
5. **Datos de enemigos** y balancing
6. **Eventos del juego** para analytics
7. **Inventario de items** y mejoras
8. **Achievements/logros** del jugador

## 🔍 Opciones de Bases de Datos Evaluadas

## 1. SQLite (⭐⭐⭐⭐⭐)

### ✅ Ventajas
- **Sin servidor**: Base de datos embebida, archivo único
- **Zero-configuration**: No requiere instalación ni configuración
- **SQL completo**: Soporte para consultas complejas, índices, triggers
- **Transacciones ACID**: Integridad garantizada
- **Multiplataforma**: Funciona en Windows, Linux, macOS
- **Tamaño pequeño**: Menos de 1MB compilado
- **Rendimiento excelente**: Para aplicaciones de escritorio
- **Backup simple**: Solo copiar el archivo .db
- **Python nativo**: Módulo `sqlite3` incluido en stdlib

### ⚠️ Consideraciones
- **Concurrencia limitada**: Un solo escritor a la vez
- **Sin conexiones remotas**: Solo acceso local
- **Tipos limitados**: Solo 5 tipos de datos nativos

### 🎮 Casos de Uso Ideales
- **Guardado de partidas** con queries complejas
- **Estadísticas locales** del jugador
- **Base de datos de items** y configuraciones
- **Historia de partidas** y analytics local

### 💻 Código de Ejemplo
```python
import sqlite3
from typing import Dict, List, Any

class GameDatabase:
    def __init__(self, db_path: str = "game.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS saves (
                id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL,
                level INTEGER,
                score INTEGER,
                save_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS player_stats (
                player_name TEXT PRIMARY KEY,
                total_score INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                best_level INTEGER DEFAULT 1,
                playtime_minutes INTEGER DEFAULT 0
            );
        ''')

    def save_game(self, player_name: str, level: int, score: int, data: str):
        self.conn.execute('''
            INSERT INTO saves (player_name, level, score, save_data)
            VALUES (?, ?, ?, ?)
        ''', (player_name, level, score, data))
        self.conn.commit()

    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        cursor = self.conn.execute('''
            SELECT player_name, MAX(score) as best_score, MAX(level) as best_level
            FROM saves
            GROUP BY player_name
            ORDER BY best_score DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]
```

## 2. DuckDB (⭐⭐⭐⭐)

### ✅ Ventajas
- **Analítica avanzada**: Optimizado para consultas complejas
- **Sin servidor**: Embebido como SQLite
- **SQL moderno**: Soporte para funciones de ventana, CTEs
- **Rendimiento superior**: Para análisis de datos
- **Compatibilidad**: API similar a SQLite
- **Columnar**: Eficiente para agregaciones

### ⚠️ Consideraciones
- **Más pesado**: Mayor overhead que SQLite
- **Menos maduro**: Relativamente nuevo
- **Enfoque analítico**: Sobrekill para saves simples

### 🎮 Casos de Uso Ideales
- **Analytics avanzados** del gameplay
- **Reportes complejos** de estadísticas
- **Data mining** de comportamiento de jugadores

### 💻 Código de Ejemplo
```python
import duckdb

class AnalyticsDatabase:
    def __init__(self, db_path: str = "analytics.duckdb"):
        self.conn = duckdb.connect(db_path)
        self.create_tables()

    def analyze_player_patterns(self):
        return self.conn.execute('''
            SELECT
                DATE_TRUNC('hour', timestamp) as hour,
                COUNT(*) as events,
                AVG(score) as avg_score,
                PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY score) as median_score
            FROM game_events
            WHERE event_type = 'game_over'
            GROUP BY hour
            ORDER BY hour
        ''').fetchall()
```

## 3. TinyDB (⭐⭐⭐)

### ✅ Ventajas
- **100% Python**: No dependencias externas
- **NoSQL**: Documentos JSON flexibles
- **API simple**: Muy fácil de usar
- **Sin SQL**: Para equipos que prefieren evitar SQL

### ⚠️ Consideraciones
- **Sin SQL nativo**: Requiere adaptación
- **Rendimiento limitado**: Para datasets grandes
- **Consultas básicas**: Menos potente que SQL

### 🎮 Casos de Uso Ideales
- **Prototipos rápidos** sin SQL
- **Configuraciones dinámicas** complejas
- **Datos no relacionales** simples

## 4. Peewee ORM + SQLite (⭐⭐⭐⭐)

### ✅ Ventajas
- **ORM Python**: Modelos orientados a objetos
- **SQLite subyacente**: Toda la potencia de SQLite
- **Migraciones**: Sistema de versionado de schema
- **Validación**: Tipos y constraints automáticos

### ⚠️ Consideraciones
- **Dependencia extra**: Requiere instalación
- **Curva de aprendizaje**: ORM vs SQL directo
- **Overhead**: Capa adicional sobre SQLite

### 💻 Código de Ejemplo
```python
from peewee import *
from datetime import datetime

db = SqliteDatabase('game.db')

class BaseModel(Model):
    class Meta:
        database = db

class Player(BaseModel):
    name = CharField(unique=True)
    total_score = IntegerField(default=0)
    games_played = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.now)

class GameSave(BaseModel):
    player = ForeignKeyField(Player, backref='saves')
    level = IntegerField()
    score = IntegerField()
    save_data = TextField()
    created_at = DateTimeField(default=datetime.now)

# Uso
Player.create(name="Kavalieri", total_score=1000)
leaderboard = Player.select().order_by(Player.total_score.desc()).limit(10)
```

## 5. PostgreSQL Embedded (libpq) (⭐⭐)

### ✅ Ventajas
- **SQL completo**: Todas las características de PostgreSQL
- **Escalabilidad**: Puede crecer a servidor completo
- **Extensiones**: PostGIS, funciones avanzadas

### ⚠️ Consideraciones
- **Complejidad**: Requiere proceso separado
- **Overhead**: Demasiado para un videojuego local
- **Distribución**: Complicada para end-users

## 📊 Matriz de Comparación

| Característica | SQLite | DuckDB | TinyDB | Peewee+SQLite | PostgreSQL |
|----------------|--------|---------|---------|---------------|-------------|
| **Facilidad Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Rendimiento** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Capacidades SQL** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Simplicidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Tamaño/Overhead** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Comunidad/Soporte** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Backup/Portabilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 Recomendaciones por Caso de Uso

### 🥇 **RECOMENDACIÓN PRINCIPAL: SQLite**

#### ¿Por qué SQLite?
1. **Perfecta para videojuegos**: Sin overhead de servidor
2. **SQL completo**: Todas las consultas que necesitamos
3. **Zero dependencies**: Ya incluido en Python
4. **Backup trivial**: Solo copiar el archivo .db
5. **Rendimiento excelente**: Para nuestro volumen de datos
6. **Maduro y estable**: 20+ años de desarrollo

#### Estructura Propuesta
```sql
-- Tabla de jugadores
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Guardados de partida
CREATE TABLE game_saves (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    slot_number INTEGER,
    level INTEGER,
    score INTEGER,
    playtime_seconds INTEGER,
    save_data_json TEXT,
    screenshot_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id),
    UNIQUE(player_id, slot_number)
);

-- Estadísticas globales del jugador
CREATE TABLE player_stats (
    player_id INTEGER PRIMARY KEY,
    total_games INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    total_playtime_seconds INTEGER DEFAULT 0,
    best_score INTEGER DEFAULT 0,
    best_level INTEGER DEFAULT 1,
    achievements_unlocked INTEGER DEFAULT 0,
    last_played TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Configuración del juego
CREATE TABLE game_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Items y mejoras del jugador
CREATE TABLE player_inventory (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    item_type TEXT NOT NULL,
    item_id TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Eventos del juego para analytics
CREATE TABLE game_events (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    event_type TEXT NOT NULL,
    event_data_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Leaderboards locales
CREATE TABLE leaderboards (
    id INTEGER PRIMARY KEY,
    player_id INTEGER,
    category TEXT NOT NULL, -- 'high_score', 'best_time', etc.
    value INTEGER NOT NULL,
    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id)
);
```

### 🥈 **ALTERNATIVA: DuckDB para Analytics**

Si necesitamos análisis avanzados de gameplay:
- **SQLite**: Para saves y operaciones CRUD
- **DuckDB**: Para analytics y reportes complejos
- **Sync periódico**: De SQLite a DuckDB para análisis

### 🥉 **OPCIÓN HÍBRIDA: Peewee ORM**

Para desarrollo más rápido con validaciones automáticas:
- **Modelos Python**: Más familiar para el equipo
- **Migraciones**: Evolución controlada del schema
- **SQLite subyacente**: Mantiene todas las ventajas

## 🔧 Plan de Implementación Sugerido

### Fase 1: Migración Básica
1. **Crear DatabaseManager** que coexista con SaveManager actual
2. **Migrar configuraciones** de JSON a SQLite
3. **Implementar sistema de stats** básico

### Fase 2: Saves Híbridos
1. **Mantener saves binarios** para compatibilidad
2. **Agregar metadata** en SQLite para búsquedas
3. **Implementar leaderboards** locales

### Fase 3: Migración Completa
1. **Migrar saves completos** a SQLite
2. **Implementar analytics** de gameplay
3. **Sistema de achievements** completo

## 🛠️ Código de Integración Propuesto

```python
# src/utils/database_manager.py
import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "saves/game.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.init_database()

    def init_database(self):
        # Ejecutar schema completo
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()

    def save_game_metadata(self, player_name: str, slot: int,
                          level: int, score: int, playtime: int) -> int:
        """Guarda metadata del save en DB, retorna save_id"""
        cursor = self.conn.execute('''
            INSERT OR REPLACE INTO game_saves
            (player_id, slot_number, level, score, playtime_seconds)
            VALUES (
                (SELECT id FROM players WHERE name = ? OR
                 INSERT INTO players (name) VALUES (?) RETURNING id),
                ?, ?, ?, ?
            )
        ''', (player_name, player_name, slot, level, score, playtime))
        self.conn.commit()
        return cursor.lastrowid

    def get_leaderboard(self, category: str = "high_score",
                       limit: int = 10) -> List[Dict]:
        """Obtiene leaderboard por categoría"""
        cursor = self.conn.execute('''
            SELECT p.name, l.value, l.achieved_at
            FROM leaderboards l
            JOIN players p ON l.player_id = p.id
            WHERE l.category = ?
            ORDER BY l.value DESC
            LIMIT ?
        ''', (category, limit))
        return [dict(row) for row in cursor.fetchall()]
```

## 🎮 Casos de Uso Específicos

### 1. **Sistema de Guardado Mejorado**
```sql
-- Buscar saves por criterios
SELECT * FROM game_saves
WHERE player_id = ? AND level >= ?
ORDER BY score DESC;

-- Estadísticas de progreso
SELECT
    COUNT(*) as total_saves,
    MAX(level) as best_level,
    AVG(score) as avg_score
FROM game_saves
WHERE player_id = ?;
```

### 2. **Analytics de Gameplay**
```sql
-- Patrones de juego por hora
SELECT
    strftime('%H', timestamp) as hour,
    COUNT(*) as games_played,
    AVG(CAST(json_extract(event_data_json, '$.score') AS INTEGER)) as avg_score
FROM game_events
WHERE event_type = 'game_over'
GROUP BY hour;

-- Progresión de habilidad
SELECT
    DATE(timestamp) as date,
    AVG(CAST(json_extract(event_data_json, '$.survival_time') AS REAL)) as avg_survival
FROM game_events
WHERE event_type = 'player_death'
GROUP BY date
ORDER BY date;
```

### 3. **Sistema de Logros**
```sql
-- Verificar logros
SELECT COUNT(*) FROM game_events
WHERE player_id = ? AND event_type = 'enemy_killed'
AND DATE(timestamp) = DATE('now'); -- Enemigos matados hoy

-- Desbloquear logro
INSERT INTO player_inventory (player_id, item_type, item_id)
VALUES (?, 'achievement', 'zombie_slayer_100');
```

## 📋 Recomendación Final

**SQLite es la opción óptima** para SiK Python Game porque:

1. ✅ **Cumple todos los requisitos**: SQL, robustez, simplicidad
2. ✅ **Zero overhead**: No impacta performance del juego
3. ✅ **Integración perfecta**: Con nuestro stack Python actual
4. ✅ **Escalabilidad**: Puede crecer con el proyecto
5. ✅ **Mantenimiento**: Backup y distribución triviales

¿Procedemos con la implementación de SQLite o prefieres evaluar alguna otra opción en detalle?
