def porcentaje_descuento_volumen(subtotal: int) -> int:
    if subtotal >= 500_000:
        return 10
    if subtotal >= 200_000:
        return 5
    return 0