"""HU-05. Calcular el envío y el total."""
import pytest

from conftest import HOY, carrito_con, producto
from mercado_sabanero.envio import costo_envio
from mercado_sabanero.errores import CarritoVacioError
from mercado_sabanero.liquidacion import liquidar


# CA1 ---------------------------------------------------------------
@pytest.mark.parametrize(
    "municipio, costo",
    [
        ("Sincelejo", 8_000),
        ("sincelejo", 8_000),
        ("SINCELEJO", 8_000),
        ("Sampués", 15_000),
        ("Corozal", 15_000),
        ("Tolú", 15_000),
    ],
)
def test_costo_de_envio_segun_municipio(municipio, costo):
    # Act
    resultado = costo_envio(municipio, base_con_iva=0)
    # Assert
    assert resultado == costo


# CA2: valores límite $149.999 / $150.000 ----------------------------
def test_productos_con_iva_por_149999_pagan_envio(inventario):
    # Arrange
    carrito = carrito_con(inventario, (producto(149_999, 19), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.envio == 8_000


def test_productos_con_iva_por_150000_tienen_envio_gratis(inventario):
    # Arrange
    carrito = carrito_con(inventario, (producto(150_000, 19), 1))
    # Act
    resultado = liquidar(carrito, "Sampués", hoy=HOY)
    # Assert
    assert resultado.envio == 0


def test_productos_sin_iva_no_cuentan_para_el_envio_gratis(inventario):
    # Arrange: 150.000 en productos con IVA 0 % => no califica
    carrito = carrito_con(inventario, (producto(150_000, 0), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.envio == 8_000


def test_la_suma_de_productos_con_iva_distintos_alcanza_el_umbral(inventario):
    # Arrange: 100.000 (19 %) + 50.000 (5 %) = 150.000
    carrito = carrito_con(
        inventario, (producto(100_000, 19, "A"), 1), (producto(50_000, 5, "B"), 1)
    )
    # Act
    resultado = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert resultado.envio == 0


# CA3 ---------------------------------------------------------------
def test_total_es_subtotal_menos_descuento_mas_iva_mas_envio(inventario):
    # Arrange: 100.000 al 19 % en Sincelejo => 100.000 - 0 + 19.000 + 8.000
    carrito = carrito_con(inventario, (producto(100_000, 19), 1))
    # Act
    r = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert r.total == r.subtotal - r.descuento + r.iva + r.envio == 127_000


def test_liquidar_carrito_vacio_lanza_error(carrito):
    with pytest.raises(CarritoVacioError):
        liquidar(carrito, "Sincelejo", hoy=HOY)
