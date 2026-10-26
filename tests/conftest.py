from datetime import date
from unittest.mock import Mock

import pytest

from mercado_sabanero.carrito import Carrito
from mercado_sabanero.modelos import Producto

HOY = date(2026, 10, 24)


@pytest.fixture
def inventario():
    """Doble de prueba (mock) del servicio externo de inventario: stock amplio."""
    mock = Mock()
    mock.obtener_stock.return_value = 100
    return mock


@pytest.fixture
def carrito(inventario):
    return Carrito(inventario)


@pytest.fixture
def licuadora():
    return Producto("LIC-01", "Licuadora", 180_000, 19)


@pytest.fixture
def cafe():
    return Producto("CAF-01", "Café", 15_000, 5)


@pytest.fixture
def arroz():
    return Producto("ARR-01", "Arroz", 4_500, 0)


def producto(precio: int, tarifa: int = 0, sku: str = "X-01") -> Producto:
    return Producto(sku, "Producto de prueba", precio, tarifa)


def carrito_con(inventario, *lineas):
    """Construye un carrito con (producto, cantidad) ya agregados."""
    c = Carrito(inventario)
    for prod, cant in lineas:
        c.agregar(prod, cant)
    return c
