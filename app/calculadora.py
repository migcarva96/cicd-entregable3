"""Calculator module with basic arithmetic operations."""

AUTORES = (
    "oalzatev@eafit.edu.co , maurreac@eafit.edu.co ,"
    " jmgarzonv@eafit.edu.co , dvillamizm@eafit.edu.co"
)


def sumar(a, b):
    """Retorna la suma de a y b"""
    return a + b


def restar(a, b):
    """Retorna la resta de a y b"""
    return a - b


def multiplicar(a, b):
    """Retorna la multiplicación de a y b"."""
    return a * b


def dividir(a, b):
    """Retorna la división de a y b. Tira error si divisor es 0"""
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def potencia(base, exponente):
    """Eleva base al exponente dado."""
    return base**exponente


def modulo(a, b):
    """Retorna el residuo de dividir a entre b."""
    if b == 0:
        raise ValueError("No se puede calcular el módulo con divisor 0")
    return a % b
