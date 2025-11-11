import datetime


def tratar_data(texto: str) -> datetime.datetime | None:
    """
    Converte uma string de data para um objeto datetime.
    Tenta múltiplos formatos.
    """
    if not texto:
        return None
    texto = texto.strip()
    for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(texto, fmt)
        except ValueError:  # noqa: PERF203
            continue
    return None
