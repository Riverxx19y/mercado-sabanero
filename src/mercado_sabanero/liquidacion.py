"""Liquidación de la compra."""
from datetime import date

from .carrito import Carrito
from .descuentos import porcentaje_descuento_volumen
from .envio import costo_envio
from .errores import CarritoVacioError
from .modelos import Categoria, Liquidacion
from .redondeo import dividir_redondeado


def liquidar(
    carrito: Carrito,
    municipio: str,
    categoria: Categoria = Categoria.ESTANDAR,
    cupon: str | None = None,
    hoy: date | None = None,
) -> Liquidacion:
    if carrito.esta_vacio():
        raise CarritoVacioError("No se puede liquidar un carrito vacío")
    subtotal = carrito.subtotal
    porcentaje = porcentaje_descuento_volumen(subtotal)
    descuento = dividir_redondeado(subtotal * porcentaje, 100)
    iva = sum(
        dividir_redondeado(i.subtotal * (100 - porcentaje) * i.producto.tarifa_iva, 10_000)
        for i in carrito.items
    )
    base_con_iva = sum(i.subtotal for i in carrito.items if i.producto.tarifa_iva > 0)
    envio = costo_envio(municipio, base_con_iva)
    total = subtotal - descuento + iva + envio
    return Liquidacion(subtotal, porcentaje, descuento, iva, envio, total, 0)
