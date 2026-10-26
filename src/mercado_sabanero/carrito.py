"""HU-01: carrito de compras."""
from .errores import CantidadInvalidaError, StockInsuficienteError
from .inventario import Inventario
from .modelos import ItemCarrito, Producto

CANTIDAD_MINIMA = 1
CANTIDAD_MAXIMA = 50


class Carrito:
    def __init__(self, inventario: Inventario):
        self._inventario = inventario
        self._cantidades: dict[str, int] = {}
        self._productos: dict[str, Producto] = {}

    def agregar(self, producto: Producto, cantidad: int) -> None:
        if not CANTIDAD_MINIMA <= cantidad <= CANTIDAD_MAXIMA:
            raise CantidadInvalidaError(
                f"La cantidad debe estar entre {CANTIDAD_MINIMA} y {CANTIDAD_MAXIMA}"
            )
        nueva_cantidad = self._cantidades.get(producto.sku, 0) + cantidad
        if self._inventario.obtener_stock(producto.sku) < nueva_cantidad:
            raise StockInsuficienteError(
                f"Stock insuficiente para {producto.nombre}"
            )
        self._cantidades[producto.sku] = nueva_cantidad
        self._productos[producto.sku] = producto

    @property
    def items(self) -> list[ItemCarrito]:
        return [
            ItemCarrito(self._productos[sku], cant)
            for sku, cant in self._cantidades.items()
        ]

    def cantidad_de(self, sku: str) -> int:
        return self._cantidades.get(sku, 0)

    @property
    def subtotal(self) -> int:
        return sum(item.subtotal for item in self.items)

    def esta_vacio(self) -> bool:
        return not self._cantidades
