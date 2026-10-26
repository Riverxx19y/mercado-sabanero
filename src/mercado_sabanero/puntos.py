"""HU-06: puntos de fidelización."""
from .modelos import Categoria

PESOS_POR_PUNTO = 1_000


def calcular_puntos(total_sin_envio: int, categoria: Categoria) -> int:
    puntos = total_sin_envio // PESOS_POR_PUNTO
    return puntos * 2 if categoria is Categoria.ORO else puntos
