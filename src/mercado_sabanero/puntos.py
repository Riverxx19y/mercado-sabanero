"""HU-06: puntos de fidelización."""
from .modelos import Categoria


def calcular_puntos(total_sin_envio: int, categoria: Categoria) -> int:
    puntos = total_sin_envio // 1_000
    if categoria is Categoria.ORO:
        return puntos * 2
    return puntos
