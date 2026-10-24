"""HU-03. Descuento por volumen."""
import pytest

from mercado_sabanero.descuentos import porcentaje_descuento_volumen


@pytest.mark.parametrize(
    "subtotal, porcentaje",
    [
        (0, 0),
        (199_999, 0),
        (200_000, 5),
        (499_999, 5),
        (500_000, 10),
        (1_000_000, 10),
    ],
)
def test_porcentaje_de_descuento_segun_subtotal(subtotal, porcentaje):
    # Arrange: subtotal y porcentaje esperado vienen de la parametrización
    # Act
    resultado = porcentaje_descuento_volumen(subtotal)
    # Assert
    assert resultado == porcentaje