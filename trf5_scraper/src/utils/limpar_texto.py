import re


def limpar_texto(value):
    if not value:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()
