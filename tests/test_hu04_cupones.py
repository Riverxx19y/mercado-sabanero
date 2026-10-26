"""HU-04. Usar cupones."""
from datetime import date

import pytest

from conftest import HOY, carrito_con, producto
from mercado_sabanero.errores import CuponInvalidoError
from mercado_sabanero.liquidacion import liquidar


# CA1 ---------------------------------------------------------------
def test_sabanero10_con_subtotal_minimo_aplica_10_por_ciento(inventario):
    # Arrange
    carrito = carrito_con(inventario, (producto(50_000), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", cupon="SABANERO10", hoy=HOY)
    # Assert
    assert resultado.descuento == 5_000


def test_sabanero10_con_subtotal_bajo_el_minimo_es_rechazado(inventario):
    # Arrange: $49.999 < $50.000
    carrito = carrito_con(inventario, (producto(49_999), 1))
    # Act / Assert
    with pytest.raises(CuponInvalidoError):
        liquidar(carrito, "Sincelejo", cupon="SABANERO10", hoy=HOY)


def test_codigo_de_cupon_no_distingue_mayusculas_ni_espacios(inventario):
    # Arrange
    carrito = carrito_con(inventario, (producto(100_000), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", cupon="  sabanero10 ", hoy=HOY)
    # Assert
    assert resultado.descuento == 10_000


# CA2 ---------------------------------------------------------------
def test_enviogratis_deja_el_envio_en_cero(inventario):
    # Arrange: compra pequeña a otro municipio (sin el cupón costaría $15.000)
    carrito = carrito_con(inventario, (producto(10_000), 1))
    # Act
    resultado = liquidar(carrito, "Sampués", cupon="ENVIOGRATIS", hoy=HOY)
    # Assert
    assert resultado.envio == 0


# CA3 ---------------------------------------------------------------
@pytest.mark.parametrize("codigo", ["NOEXISTE", "", "SABANERO11"])
def test_cupon_inexistente_lanza_error_de_cupon_invalido(inventario, codigo):
    # Arrange: con código vacío no se intenta aplicar cupón, por eso se usa " "
    carrito = carrito_con(inventario, (producto(100_000), 1))
    codigo = codigo or " "
    # Act / Assert
    with pytest.raises(CuponInvalidoError):
        liquidar(carrito, "Sincelejo", cupon=codigo, hoy=HOY)


def test_cupon_vencido_lanza_error_de_cupon_invalido(inventario):
    # Arrange: NAVIDAD2025 venció el 31/12/2025
    carrito = carrito_con(inventario, (producto(100_000), 1))
    # Act / Assert
    with pytest.raises(CuponInvalidoError, match="vencido"):
        liquidar(carrito, "Sincelejo", cupon="NAVIDAD2025", hoy=HOY)


def test_cupon_vigente_el_ultimo_dia_de_vigencia_es_valido(inventario):
    # Arrange: SABANERO10 vence el 31/12/2027
    carrito = carrito_con(inventario, (producto(100_000), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", cupon="SABANERO10", hoy=date(2027, 12, 31))
    # Assert
    assert resultado.descuento == 10_000


# CA4 ---------------------------------------------------------------
def test_con_descuento_por_volumen_mayor_se_conserva_solo_el_mayor(inventario):
    # Arrange: subtotal 600.000 => volumen 10 %; cupón 10 % => NO se suman (60.000)
    carrito = carrito_con(inventario, (producto(600_000), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", cupon="SABANERO10", hoy=HOY)
    # Assert
    assert resultado.porcentaje_descuento == 10
    assert resultado.descuento == 60_000


def test_cupon_de_10_supera_al_descuento_por_volumen_de_5(inventario):
    # Arrange: subtotal 300.000 => volumen 5 %; cupón 10 % => se aplica el 10 %
    carrito = carrito_con(inventario, (producto(300_000), 1))
    # Act
    resultado = liquidar(carrito, "Sincelejo", cupon="SABANERO10", hoy=HOY)
    # Assert
    assert resultado.porcentaje_descuento == 10
    assert resultado.descuento == 30_000
