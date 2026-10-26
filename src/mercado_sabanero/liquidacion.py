"""Liquidación de la compra: integra HU-01 a HU-06."""
from datetime import date

from .carrito import Carrito
from .cupones import validar_cupon
from .descuentos import porcentaje_descuento_volumen
from .envio import costo_envio
from .errores import CarritoVacioError
from .modelos import Categoria, Liquidacion
from .puntos import calcular_puntos
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

    hoy = hoy or date.today()
    subtotal = carrito.subtotal

    # Descuento: se aplica el mayor entre volumen y cupón (no se suman).
    porcentaje = porcentaje_descuento_volumen(subtotal)
    envio_gratis_cupon = False
    if cupon:
        c = validar_cupon(cupon, subtotal, hoy)
        porcentaje = max(porcentaje, c.porcentaje)
        envio_gratis_cupon = c.envio_gratis

    descuento = dividir_redondeado(subtotal * porcentaje, 100)

    # IVA sobre el valor de cada producto ya con descuento.
    iva = sum(
        dividir_redondeado(
            item.subtotal * (100 - porcentaje) * item.producto.tarifa_iva, 10_000
        )
        for item in carrito.items
    )

    base_con_iva = sum(i.subtotal for i in carrito.items if i.producto.tarifa_iva > 0)
    envio = costo_envio(municipio, base_con_iva, envio_gratis_cupon)

    total = subtotal - descuento + iva + envio
    puntos = calcular_puntos(total - envio, categoria)

    return Liquidacion(subtotal, porcentaje, descuento, iva, envio, total, puntos)
