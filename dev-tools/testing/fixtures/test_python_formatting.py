# Banco de Pruebas - Sistema de Commits
# Archivo de prueba para testear hooks de pre-commit


def funcion_con_problemas_de_formato():
    x = 1 + 2 + 3  # Formato incorrecto para ruff
    y = 4 + 5  # Espacios incorrectos
    z = x + y
    return z


def funcion_sin_docstring():
    return "Esta funcion no tiene docstring"


def funcion_con_trailing_spaces():
    mensaje = "Esta linea tiene espacios al final"
    return mensaje


# Comentario con problemas de formato
class ClaseConProblemas:
    def __init__(self, nombre, edad):  # Espacios incorrectos
        self.nombre = nombre
        self.edad = edad

    def metodo_sin_type_hints(self, valor):
        return valor * 2


# Variable global sin usar
VARIABLE_NO_USADA = "test"

if __name__ == "__main__":
    print("Archivo de prueba para hooks")
