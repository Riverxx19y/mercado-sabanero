from dataclasses import dataclass


@dataclass(frozen=True)
class Producto:
    sku: str
    nombre: str
    precio: int
    tarifa_iva: int = 0