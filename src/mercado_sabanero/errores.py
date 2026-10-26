class CantidadInvalidaError(Exception):
    """La cantidad no está entre 1 y 50 unidades."""


class StockInsuficienteError(Exception):
    """El inventario no tiene unidades suficientes."""
