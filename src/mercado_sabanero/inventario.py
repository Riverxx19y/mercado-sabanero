"""Contrato del servicio externo de inventario (se reemplaza por un mock en pruebas)."""
from typing import Protocol


class Inventario(Protocol):
    def obtener_stock(self, sku: str) -> int:
        """Devuelve las unidades disponibles del producto."""
        ...
