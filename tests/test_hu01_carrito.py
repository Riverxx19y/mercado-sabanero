"""HU-01. Agregar productos al carrito."""
import pytest

from mercado_sabanero.carrito import Carrito
from mercado_sabanero.errores import CantidadInvalidaError, StockInsuficienteError


# CA1 ---------------------------------------------------------------
@pytest.mark.parametrize("cantidad", [1, 2, 49, 50])
def test_agregar_cantidad_dentro_del_rango_deja_producto_en_carrito(carrito, arroz, cantidad):
    # Arrange: carrito vacío y producto con stock suficiente (fixture)
    # Act
    carrito.agregar(arroz, cantidad)
    # Assert
    assert carrito.cantidad_de(arroz.sku) == cantidad


def test_agregar_producto_consulta_el_stock_del_inventario(carrito, inventario, arroz):
    # Arrange / Act
    carrito.agregar(arroz, 3)
    # Assert: se usó el doble de prueba del inventario con el SKU correcto
    inventario.obtener_stock.assert_called_once_with(arroz.sku)


def test_agregar_cantidad_igual_al_stock_es_permitido(inventario, arroz):
    # Arrange
    inventario.obtener_stock.return_value = 5
    carrito = Carrito(inventario)
    # Act
    carrito.agregar(arroz, 5)
    # Assert
    assert carrito.cantidad_de(arroz.sku) == 5


# CA2 ---------------------------------------------------------------
@pytest.mark.parametrize("cantidad", [0, -1, 51, 100])
def test_agregar_cantidad_fuera_de_rango_lanza_error(carrito, arroz, cantidad):
    # Arrange: carrito vacío
    # Act / Assert
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar(arroz, cantidad)


def test_cantidad_invalida_no_consulta_inventario_ni_modifica_carrito(carrito, inventario, arroz):
    # Act
    with pytest.raises(CantidadInvalidaError):
        carrito.agregar(arroz, 0)
    # Assert
    inventario.obtener_stock.assert_not_called()
    assert carrito.esta_vacio()


# CA3 ---------------------------------------------------------------
def test_agregar_mas_que_el_stock_lanza_stock_insuficiente(inventario, arroz):
    # Arrange: inventario simulado con solo 2 unidades
    inventario.obtener_stock.return_value = 2
    carrito = Carrito(inventario)
    # Act / Assert
    with pytest.raises(StockInsuficienteError):
        carrito.agregar(arroz, 3)
    assert carrito.esta_vacio()


# CA4 ---------------------------------------------------------------
def test_agregar_producto_existente_suma_las_cantidades(carrito, arroz):
    # Arrange
    carrito.agregar(arroz, 2)
    # Act
    carrito.agregar(arroz, 3)
    # Assert
    assert carrito.cantidad_de(arroz.sku) == 5
    assert len(carrito.items) == 1


def test_suma_de_cantidades_que_supera_el_stock_lanza_error(inventario, arroz):
    # Arrange: stock 5, ya hay 4 en el carrito
    inventario.obtener_stock.return_value = 5
    carrito = Carrito(inventario)
    carrito.agregar(arroz, 4)
    # Act / Assert
    with pytest.raises(StockInsuficienteError):
        carrito.agregar(arroz, 2)
    assert carrito.cantidad_de(arroz.sku) == 4
