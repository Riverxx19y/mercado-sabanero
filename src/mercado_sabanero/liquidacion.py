"""Liquidación de la compra."""
from datetime import date

from .carrito import Carrito
from .descuentos import porcentaje_descuento_volumen
from .modelos import Categoria, Liquidacion
from .redondeo import dividir_redondeado


def liquidar(
    carrito: Carrito,
    municipio: str,
    categoria: Categoria = Categoria.ESTANDAR,
    cupon: str | None = None,
    hoy: date | None = None,
) -> Liquidacion:
    subtotal = carrito.subtotal
    porcentaje = porcentaje_descuento_volumen(subtotal)
    descuento = dividir_redondeado(subtotal * porcentaje, 100)
    # El IVA se calcula sobre el valor de cada producto ya con descuento.
    iva = sum(
        dividir_redondeado(i.subtotal * (100 - porcentaje) * i.producto.tarifa_iva, 10_000)
        for i in carrito.items
    )
    total = subtotal - descuento + iva
    return Liquidacion(subtotal, porcentaje, descuento, iva, 0, total, 0)
