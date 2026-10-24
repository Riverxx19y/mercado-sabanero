class Carrito:
    def __init__(self, inventario):
        self._cantidades = {}

    def agregar(self, producto, cantidad):
        self._cantidades[producto.sku] = cantidad

    def cantidad_de(self, sku):
        return self._cantidades.get(sku, 0)