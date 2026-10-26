"""HU-06. Acumular puntos y caso de verificación del enunciado."""
import pytest

from conftest import HOY, carrito_con, producto
from mercado_sabanero.liquidacion import liquidar
from mercado_sabanero.modelos import Categoria
from mercado_sabanero.puntos import calcular_puntos


# CA1 ---------------------------------------------------------------
@pytest.mark.parametrize(
    "total, puntos",
    [(0, 0), (999, 0), (1_000, 1), (1_999, 1), (2_000, 2), (250_515, 250)],
)
def test_cliente_estandar_recibe_un_punto_por_cada_mil_completos(total, puntos):
    # Act
    resultado = calcular_puntos(total, Categoria.ESTANDAR)
    # Assert
    assert resultado == puntos


# CA2 ---------------------------------------------------------------
@pytest.mark.parametrize("total, puntos", [(999, 0), (1_000, 2), (250_515, 500)])
def test_cliente_oro_recibe_el_doble_de_puntos(total, puntos):
    # Act
    resultado = calcular_puntos(total, Categoria.ORO)
    # Assert
    assert resultado == puntos


def test_los_puntos_se_calculan_sin_incluir_el_envio(inventario):
    # Arrange: 10.000 sin IVA a Sincelejo => total 18.000, pero puntos sobre 10.000
    carrito = carrito_con(inventario, (producto(10_000), 1))
    # Act
    r = liquidar(carrito, "Sincelejo", hoy=HOY)
    # Assert
    assert r.total == 18_000
    assert r.puntos == 10


# Ejemplo del enunciado ----------------------------------------------
def test_ejemplo_del_enunciado_cliente_estandar_en_sincelejo(
    inventario, licuadora, cafe, arroz
):
    # Arrange: 1 licuadora, 2 cafés, 4 arroces
    carrito = carrito_con(inventario, (licuadora, 1), (cafe, 2), (arroz, 4))
    # Act
    r = liquidar(carrito, "Sincelejo", Categoria.ESTANDAR, hoy=HOY)
    # Assert
    assert r.subtotal == 228_000
    assert r.descuento == 11_400
    assert r.iva == 33_915
    assert r.envio == 0
    assert r.total == 250_515
    assert r.puntos == 250


def test_mismo_ejemplo_con_cliente_oro_duplica_los_puntos(
    inventario, licuadora, cafe, arroz
):
    # Arrange
    carrito = carrito_con(inventario, (licuadora, 1), (cafe, 2), (arroz, 4))
    # Act
    r = liquidar(carrito, "Sincelejo", Categoria.ORO, hoy=HOY)
    # Assert
    assert r.total == 250_515
    assert r.puntos == 500
