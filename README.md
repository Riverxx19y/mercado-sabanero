# Mercado Sabanero - Módulo de liquidación de compras

Lógica de negocio (sin interfaz ni base de datos) para liquidar una compra: carrito, IVA,
descuento por volumen, cupones, envío y puntos. Desarrollado con TDD.

## Requisitos
- Python 3.10 o superior

## Instalación y ejecución
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

pytest                             # ejecuta todas las pruebas
pytest --cov --cov-report=term-missing   # con reporte de cobertura
pytest --cov --cov-report=html     # reporte HTML en htmlcov/index.html
```

## Estructura
| Módulo | Historia |
|---|---|
| `carrito.py`, `inventario.py` | HU-01 Agregar productos |
| `liquidacion.py`, `redondeo.py` | HU-02 IVA y total (HU-05 CA3) |
| `descuentos.py` | HU-03 Descuento por volumen |
| `cupones.py` | HU-04 Cupones |
| `envio.py` | HU-05 Envío |
| `puntos.py` | HU-06 Puntos |

## Ejemplo de uso
```python
from mercado_sabanero.carrito import Carrito
from mercado_sabanero.liquidacion import liquidar
# `inventario` es cualquier objeto con obtener_stock(sku) -> int
carrito = Carrito(inventario)
carrito.agregar(licuadora, 1)
resultado = liquidar(carrito, "Sincelejo")
```

## Decisiones y supuestos
- Valores enteros en pesos; redondeo al peso más cercano, mitad hacia arriba (no se usa `round()`).
- El descuento aplicado (volumen o cupón) es el mayor; no se suman. `ENVIOGRATIS` es independiente.
- Envío gratis: suma de productos con tarifa de IVA > 0 (antes de descuento) >= $150.000.
- `SABANERO10` con subtotal < $50.000 se rechaza con `CuponInvalidoError`.
- El stock se valida contra la cantidad acumulada del carrito.
- Cualquier municipio distinto de Sincelejo paga $15.000.
