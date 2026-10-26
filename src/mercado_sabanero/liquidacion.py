"""Liquidación de la compra."""
from datetime import date

from .carrito import Carrito
from .descuentos import porcentaje_descuento_volumen
from .modelos import Categoria, Liquidacion


def _redondear(numerador: int, denominador: int) -> int:
    return (2 * numerador + denominador) // (2 * denominador)


def liquidar(
    carrito: Carrito,
    municipio: str,
    categoria: Categoria = Categoria.ESTANDAR,
    cupon: str | None = None,
    hoy: date | None = None,
) -> Liquidacion:
    subtotal = carrito.subtotal
    porcentaje = porcentaje_descuento_volumen(subtotal)
    descuento = _redondear(subtotal * porcentaje, 100)
    iva = sum(
        _redondear(i.subtotal * (100 - porcentaje) * i.producto.tarifa_iva, 10_000)
        for i in carrito.items
    )
    total = subtotal - descuento + iva
    return Liquidacion(subtotal, porcentaje, descuento, iva, 0, total, 0)
