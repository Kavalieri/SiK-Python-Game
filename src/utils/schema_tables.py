"""
SchemaTable Definitions - Definiciones de tablas SQLite
=======================================================

Módulo que contiene todas las definiciones de esquemas de tablas para el sistema
de migración SQLite. Separado de SchemaManager para mantener límite de 150 líneas.

Fase 1 de migración SQLite - Definiciones de esquemas
"""


def get_all_table_schemas() -> dict[str, str]:
    """
    Obtiene todos los esquemas de tablas definidos para el sistema de migración.

    Returns:
        Diccionario con nombre de tabla y su SQL de creación
    """
    return {
        "partidas_guardadas": _get_partidas_guardadas_schema(),
        "configuraciones": _get_configuraciones_schema(),
        "personajes": _get_personajes_schema(),
        "enemigos": _get_enemigos_schema(),
        "estadisticas_juego": _get_estadisticas_juego_schema(),
        "configuracion_gameplay": _get_configuracion_gameplay_schema(),
    }


def _get_partidas_guardadas_schema() -> str:
    """Schema para la tabla de partidas guardadas (reemplaza pickle saves)."""
    return """
        CREATE TABLE IF NOT EXISTS partidas_guardadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot INTEGER NOT NULL CHECK(slot IN (1, 2, 3)),
            nombre_jugador TEXT NOT NULL,
            descripcion TEXT,
            nivel_actual INTEGER DEFAULT 1,
            puntuacion INTEGER DEFAULT 0,
            vidas INTEGER DEFAULT 3,
            tiempo_jugado INTEGER DEFAULT 0,
            personaje TEXT NOT NULL,
            estado_juego TEXT,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(slot)
        )
    """


def _get_configuraciones_schema() -> str:
    """Schema para configuraciones centralizadas (reemplaza JSON distribuido)."""
    return """
        CREATE TABLE IF NOT EXISTS configuraciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            clave TEXT NOT NULL,
            valor TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('string', 'number', 'boolean', 'object')),
            descripcion TEXT,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(categoria, clave)
        )
    """


def _get_personajes_schema() -> str:
    """Schema para datos de personajes (reemplaza characters.json + character_data.py)."""
    return """
        CREATE TABLE IF NOT EXISTS personajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            nombre_mostrar TEXT NOT NULL,
            tipo TEXT NOT NULL,
            descripcion TEXT,
            stats TEXT NOT NULL,
            ataques TEXT NOT NULL,
            sprite_config TEXT,
            activo BOOLEAN DEFAULT 1,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """


def _get_enemigos_schema() -> str:
    """Schema para tipos de enemigos (reemplaza enemies.json + enemy_types.py)."""
    return """
        CREATE TABLE IF NOT EXISTS enemigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT UNIQUE NOT NULL,
            nombre_mostrar TEXT NOT NULL,
            stats TEXT NOT NULL,
            comportamiento TEXT NOT NULL,
            animaciones TEXT NOT NULL,
            variantes TEXT,
            activo BOOLEAN DEFAULT 1,
            creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """


def _get_estadisticas_juego_schema() -> str:
    """Schema para estadísticas de juego por sesión."""
    return """
        CREATE TABLE IF NOT EXISTS estadisticas_juego (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_partida INTEGER NOT NULL,
            tipo_estadistica TEXT NOT NULL,
            valor INTEGER NOT NULL,
            sesion_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (slot_partida) REFERENCES partidas_guardadas(slot)
        )
    """


def _get_configuracion_gameplay_schema() -> str:
    """Schema para configuración de mecánicas de juego."""
    return """
        CREATE TABLE IF NOT EXISTS configuracion_gameplay (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            configuracion TEXT NOT NULL,
            version INTEGER DEFAULT 1,
            activo BOOLEAN DEFAULT 1,
            actualizado_en DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """


def get_table_list() -> list:
    """
    Lista de todas las tablas definidas en el sistema.

    Returns:
        Lista con nombres de todas las tablas
    """
    return [
        "partidas_guardadas",
        "configuraciones",
        "personajes",
        "enemigos",
        "estadisticas_juego",
        "configuracion_gameplay",
    ]


def validate_table_exists(table_name: str) -> bool:
    """
    Valida si una tabla está definida en el esquema.

    Args:
        table_name: Nombre de la tabla a validar

    Returns:
        True si la tabla está definida
    """
    return table_name in get_table_list()
