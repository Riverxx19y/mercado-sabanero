"""Modelos de dominio."""
from dataclasses import dataclass
from enum import Enum

from .errores import ProductoInvalidoError

TARIFAS_IVA_VALIDAS = (0, 5, 19)


class Categoria(Enum):
    ESTANDAR = "ESTANDAR"
    ORO = "ORO"


@dataclass(frozen=True)
class Producto:
    sku: str
    nombre: str
    precio: int          # pesos, sin decimales
    tarifa_iva: int = 0  # 0, 5 o 19 (porcentaje)

    def __post_init__(self):
        if self.precio <= 0:
            raise ProductoInvalidoError("El precio debe ser mayor que cero")
        if self.tarifa_iva not in TARIFAS_IVA_VALIDAS:
            raise ProductoInvalidoError(
                f"Tarifa de IVA inválida: {self.tarifa_iva}. Use 0, 5 o 19"
            )


@dataclass(frozen=True)
class ItemCarrito:
    producto: Producto
    cantidad: int

    @property
    def subtotal(self) -> int:
        return self.producto.precio * self.cantidad


@dataclass(frozen=True)
class Liquidacion:
    subtotal: int
    porcentaje_descuento: int
    descuento: int
    iva: int
    envio: int
    total: int
    puntos: int
