from .errores import CantidadInvalidaError, StockInsuficienteError


class Carrito:
    def __init__(self, inventario):
        self._inventario = inventario
        self._cantidades = {}

    def agregar(self, producto, cantidad):
        if not 1 <= cantidad <= 50:
            raise CantidadInvalidaError("La cantidad debe estar entre 1 y 50")
        if self._inventario.obtener_stock(producto.sku) < cantidad:
            raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}")
        self._cantidades[producto.sku] = cantidad

    def cantidad_de(self, sku):
        return self._cantidades.get(sku, 0)