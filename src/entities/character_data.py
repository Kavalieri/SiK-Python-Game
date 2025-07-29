"""
Datos de personajes jugables
===========================

Autor: SiK Team
Fecha: 2024
Descripción: Diccionario centralizado con la información de los personajes jugables.
"""

CHARACTER_DATA = {
    "guerrero": {
        "nombre": "Kava",
        "descripcion": "Guerrero cuerpo a cuerpo especializado en combate cercano. Utiliza ataques de espada y escudo para derrotar enemigos. Su estilo de juego requiere acercarse a los enemigos para causar daño máximo.",
        "imagen": "assets/characters/guerrero/idle/Idle_1_.png",
        "tipo": "Melee",
        "stats": {
            "vida": 200,
            "velocidad": 180,
            "daño": 50,
            "escudo": 20,
            "disparo": 0.0,
            "rango_ataque": 80,
        },
        "habilidades": [
            "Ataque de espada cuerpo a cuerpo",
            "Escudo protector",
            "Mayor resistencia al daño",
            "Combo de ataques rápidos",
        ],
    },
    "adventureguirl": {
        "nombre": "Sara",
        "descripcion": "Aventurera ágil especializada en combate a distancia. Dispara flechas mágicas con precisión y velocidad. Su estilo de juego se basa en mantener distancia y usar la movilidad para evadir enemigos.",
        "imagen": "assets/characters/adventureguirl/Idle_1_.png",
        "tipo": "Ranged",
        "stats": {
            "vida": 120,
            "velocidad": 220,
            "daño": 25,
            "escudo": 5,
            "disparo": 1.5,
            "rango_ataque": 300,
        },
        "habilidades": [
            "Flechas mágicas de fuego",
            "Disparo rápido y preciso",
            "Alta movilidad",
            "Evasión mejorada",
        ],
    },
    "robot": {
        "nombre": "Guiral",
        "descripcion": "Robot de combate con tecnología avanzada. Lanza proyectiles de energía y misiles explosivos. Su estilo de juego combina potencia de fuego con proyectiles especiales que causan daño en área.",
        "imagen": "assets/characters/robot/Idle_1_.png",
        "tipo": "Tech",
        "stats": {
            "vida": 150,
            "velocidad": 160,
            "daño": 35,
            "escudo": 15,
            "disparo": 1.2,
            "rango_ataque": 250,
        },
        "habilidades": [
            "Proyectiles de energía",
            "Misiles explosivos",
            "Daño en área",
            "Blindaje mejorado",
        ],
    },
}

# Para añadir un nuevo personaje, basta con añadir una nueva entrada siguiendo el formato anterior.
