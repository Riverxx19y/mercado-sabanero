"""HU-05: costo de envío."""


def costo_envio(municipio: str, base_con_iva: int) -> int:
    if base_con_iva >= 150_000:
        return 0
    if municipio.strip().lower() == "sincelejo":
        return 8_000
    return 15_000
