"""HU-04: cupones de descuento."""
from dataclasses import dataclass
from datetime import date

from .errores import CuponInvalidoError


@dataclass(frozen=True)
class Cupon:
    codigo: str
    vence: date
    porcentaje: int = 0
    subtotal_minimo: int = 0
    envio_gratis: bool = False


def validar_cupon(codigo: str, subtotal: int, hoy: date) -> Cupon:
    codigo = (codigo or "").strip().upper()
    if codigo == "SABANERO10":
        cupon = Cupon(codigo, date(2027, 12, 31), porcentaje=10, subtotal_minimo=50_000)
    elif codigo == "ENVIOGRATIS":
        cupon = Cupon(codigo, date(2027, 12, 31), envio_gratis=True)
    elif codigo == "NAVIDAD2025":
        cupon = Cupon(codigo, date(2025, 12, 31), porcentaje=15)
    else:
        raise CuponInvalidoError(f"El cupón {codigo!r} no existe")
    if hoy > cupon.vence:
        raise CuponInvalidoError(f"El cupón {cupon.codigo} está vencido")
    if subtotal < cupon.subtotal_minimo:
        raise CuponInvalidoError(f"El cupón {cupon.codigo} requiere un subtotal mínimo")
    return cupon
