"""Excepciones del dominio."""


class MercadoSabaneroError(Exception):
    """Error base del módulo."""


class CantidadInvalidaError(MercadoSabaneroError):
    """La cantidad no está entre 1 y 50 unidades."""


class StockInsuficienteError(MercadoSabaneroError):
    """El inventario no tiene unidades suficientes."""


class CuponInvalidoError(MercadoSabaneroError):
    """El cupón no existe, está vencido o no cumple el mínimo."""


class ProductoInvalidoError(MercadoSabaneroError):
    """Datos de producto inválidos (precio o tarifa de IVA)."""


class CarritoVacioError(MercadoSabaneroError):
    """No se puede liquidar un carrito sin productos."""
