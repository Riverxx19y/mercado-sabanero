"""Aritmética entera con redondeo al peso más cercano (mitad hacia arriba)."""


def dividir_redondeado(numerador: int, denominador: int) -> int:
    """Divide dos enteros no negativos y redondea al entero más cercano.

    Se evita round() de Python porque usa redondeo bancario (0.5 -> 0 y 1.5 -> 2).
    """
    return (2 * numerador + denominador) // (2 * denominador)
