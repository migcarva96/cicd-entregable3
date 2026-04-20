# app/calculadora.py

AUTORES = "oalzatev@eafit.edu.co , maurreac@eafit.edu.co , jmgarzonv@eafit.edu.co , dvillamizm@eafit.edu.co"  # IMPORTANTE: Reemplaza con los usuarios de correo de EAFIT de los estudiantes que participaron en la entrega, separados por comas.


def sumar(a, b):
    return a + b


def restar(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b

def potencia(base, exponente):
    """Eleva base al exponente dado."""
    return base ** exponente
 
 
def modulo(a, b):
    """Retorna el residuo de dividir a entre b."""
    if b == 0:
        raise ValueError("No se puede calcular el módulo con divisor 0")
    return a % b
