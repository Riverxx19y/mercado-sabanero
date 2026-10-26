"""HU-05: costo de envío."""
import unicodedata

COSTO_SINCELEJO = 8_000
COSTO_OTROS_MUNICIPIOS = 15_000
UMBRAL_ENVIO_GRATIS = 150_000


def _normalizar(texto: str) -> str:
    sin_tildes = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")
    return sin_tildes.strip().lower()


def costo_envio(municipio: str, base_con_iva: int) -> int:
    """base_con_iva: suma de los productos cuya tarifa de IVA es mayor que 0."""
    if base_con_iva >= UMBRAL_ENVIO_GRATIS:
        return 0
    if _normalizar(municipio) == "sincelejo":
        return COSTO_SINCELEJO
    return COSTO_OTROS_MUNICIPIOS
