"""HU-03. Descuento por volumen."""
from mercado_sabanero.descuentos import porcentaje_descuento_volumen


def test_subtotal_menor_a_200000_no_aplica_descuento():
    # Arrange
    subtotal = 199_999
    # Act
    resultado = porcentaje_descuento_volumen(subtotal)
    # Assert
    assert resultado == 0