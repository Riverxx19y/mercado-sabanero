"""HU-01. Agregar productos al carrito."""
from unittest.mock import Mock

from mercado_sabanero.carrito import Carrito
from mercado_sabanero.modelos import Producto


def test_agregar_cantidad_valida_deja_producto_en_carrito():
    # Arrange: inventario simulado (mock) con stock suficiente
    inventario = Mock()
    inventario.obtener_stock.return_value = 100
    carrito = Carrito(inventario)
    arroz = Producto("ARR-01", "Arroz", 4_500, 0)
    # Act
    carrito.agregar(arroz, 3)
    # Assert
    assert carrito.cantidad_de(arroz.sku) == 3