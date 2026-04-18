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
