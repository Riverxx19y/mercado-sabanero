"""HU-02. Calcular el IVA."""
import pytest

from conftest import HOY, carrito_con, producto
from mercado_sabanero.errores import ProductoInvalidoError
from mercado_sabanero.liquidacion import liquidar


# CA1 ---------------------------------------------------------------
@pytest.mark.parametrize(
    "tarifa, iva_esperado",
    [(0, 0), (5, 5_000), (19, 19_000)],
)
def test_iva_del_producto_corresponde_a_su_tarifa(inventario, tarifa, iva_esperado):
    # Arrange: un producto de $100.000 (sin descuento por volumen)
    carrito = carrito_con(inventario, (producto(100_000, tarifa), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.iva == iva_esperado


def test_iva_se_calcula_por_producto_con_tarifas_distintas(inventario):
    # Arrange: 80.000 al 19 % + 80.000 al 5 % = 15.200 + 4.000 (subtotal 160.000, sin descuento)
    carrito = carrito_con(
        inventario,
        (producto(80_000, 19, "A"), 1),
        (producto(80_000, 5, "B"), 1),
    )
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.iva == 19_200


@pytest.mark.parametrize("tarifa_invalida", [3, 10, 16, -5])
def test_producto_con_tarifa_de_iva_invalida_lanza_error(tarifa_invalida):
    with pytest.raises(ProductoInvalidoError):
        producto(10_000, tarifa_invalida)


# CA2 ---------------------------------------------------------------
def test_iva_se_calcula_sobre_el_valor_con_descuento(inventario):
    # Arrange: 200.000 al 19 % => descuento 5 % = 10.000; base 190.000; IVA 36.100
    carrito = carrito_con(inventario, (producto(200_000, 19), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.descuento == 10_000
    assert resultado.iva == 36_100


def test_iva_se_redondea_al_peso_mas_cercano(inventario):
    # Arrange: 1.050 * 5 % = 52,5 -> 53 (mitad hacia arriba)
    carrito = carrito_con(inventario, (producto(1_050, 5), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.iva == 53


@pytest.mark.parametrize("precio_invalido", [0, -1_000])
def test_producto_con_precio_no_positivo_lanza_error(precio_invalido):
    with pytest.raises(ProductoInvalidoError):
        producto(precio_invalido)
