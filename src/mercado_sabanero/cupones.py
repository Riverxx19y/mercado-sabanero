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


CATALOGO = {
    "SABANERO10": Cupon("SABANERO10", date(2027, 12, 31), porcentaje=10, subtotal_minimo=50_000),
    "ENVIOGRATIS": Cupon("ENVIOGRATIS", date(2027, 12, 31), envio_gratis=True),
    "NAVIDAD2025": Cupon("NAVIDAD2025", date(2025, 12, 31), porcentaje=15),  # vencido
}


def validar_cupon(codigo: str, subtotal: int, hoy: date) -> Cupon:
    """Devuelve el cupón si es aplicable; si no, lanza CuponInvalidoError."""
    cupon = CATALOGO.get((codigo or "").strip().upper())
    if cupon is None:
        raise CuponInvalidoError(f"El cupón {codigo!r} no existe")
    if hoy > cupon.vence:
        raise CuponInvalidoError(f"El cupón {cupon.codigo} está vencido")
    if subtotal < cupon.subtotal_minimo:
        raise CuponInvalidoError(
            f"El cupón {cupon.codigo} requiere un subtotal mínimo de ${cupon.subtotal_minimo:,}"
        )
    return cupon
