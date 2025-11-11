import re


def validate_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJs, retornando True para válido e False para inválido.

    A função primeiro limpa o CNPJ, removendo qualquer caractere que não
    seja um dígito. Em seguida, verifica se o CNPJ tem 14 dígitos e
    se não é uma sequência de dígitos repetidos. Finalmente, calcula e
    valida os dois dígitos verificadores.
    """
    if not isinstance(cnpj, str):
        return False  # type: ignore[unreachable]

    cnpj_limpo = re.sub(r"\D", "", cnpj)

    if len(cnpj_limpo) != 14:
        return False

    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False

    try:
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma1 = sum(int(cnpj_limpo[i]) * pesos1[i] for i in range(12))
        resto1 = soma1 % 11
        d1 = 0 if resto1 < 2 else 11 - resto1

        if int(cnpj_limpo[12]) != d1:
            return False

        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma2 = sum(int(cnpj_limpo[i]) * pesos2[i] for i in range(13))
        resto2 = soma2 % 11
        d2 = 0 if resto2 < 2 else 11 - resto2

        if int(cnpj_limpo[13]) != d2:
            return False

    except (ValueError, IndexError):
        return False

    return True
