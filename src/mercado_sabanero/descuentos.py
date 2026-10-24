"""HU-03: descuento por volumen."""

UMBRAL_DESCUENTO_5 = 200_000
UMBRAL_DESCUENTO_10 = 500_000


def porcentaje_descuento_volumen(subtotal: int) -> int:
    if subtotal >= UMBRAL_DESCUENTO_10:
        return 10
    if subtotal >= UMBRAL_DESCUENTO_5:
        return 5
    return 0