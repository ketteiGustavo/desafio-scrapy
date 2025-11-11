# trf5_scraper/src/main.py
import os
import subprocess

import questionary

from .styles.styles import custom_style
from .validators.cnpj import validate_cnpj


def exec_spider(processos=None, cnpj=None):
    """
    Executa a aranha do Scrapy com os argumentos fornecidos.

    Args:
        processos (str, optional): Números de processo separados por vírgula.
        cnpj (str, optional): CNPJ para a busca.
    """
    # O diretório do projeto Scrapy é dois níveis acima do diretório deste arquivo
    scrapy_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    command = ["scrapy", "crawl", "trf5_processos"]
    if processos:
        command.extend(["-a", f"processos={processos}"])
    if cnpj:
        command.extend(["-a", f"cnpj={cnpj}"])

    print("Buscando processos. Isso pode levar algum tempo, por favor aguarde...\n")
    try:
        # O cwd deve ser o diretório que contém o scrapy.cfg
        subprocess.run(command, cwd=scrapy_project_dir, check=True)
    except FileNotFoundError:
        print("\nErro: O comando 'scrapy' não foi encontrado.")
        print("Verifique se o Scrapy está instalado e se o ambiente virtual está ativado.")
    except subprocess.CalledProcessError as e:
        print(f"\nA aranha do Scrapy encontrou um erro (código de saída {e.returncode}).")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")


def main():
    """
    Função principal que exibe o menu interativo para o usuário.
    """
    # Dados extraídos do docs/desafio.md
    processos_desafio = [
        "0015648-78.1999.4.05.0000",
        "0012656-90.2012.4.05.0000",
        "0043753-74.2013.4.05.0000",
        "0002098-07.2011.4.05.8500",
        "0460674-33.2019.4.05.0000",
        "0000560-67.2017.4.05.0000",
    ]
    cnpj_desafio = "00.000.000/0001-91"

    while True:
        choice = questionary.select(
            "O que você deseja fazer?",
            choices=[
                "Buscar por número de processo",
                "Buscar por CNPJ",
                "Executar busca completa do desafio",
                "Sair",
            ],
            style=custom_style,
        ).ask()

        if choice is None or choice == "Sair":
            print("Encerrando.")
            break

        if choice == "Buscar por número de processo":
            processos_input = questionary.text("Digite um ou mais números de processo (separados por vírgula):").ask()
            if processos_input:
                exec_spider(processos=processos_input)

        elif choice == "Buscar por CNPJ":
            cnpj_input = questionary.text(
                "Digite o CNPJ:",
                validate=lambda text: True
                if validate_cnpj(text)
                else "CNPJ inválido. Por favor, digite um CNPJ válido.",
            ).ask()
            if cnpj_input:
                exec_spider(cnpj=cnpj_input)

        elif choice == "Executar busca completa do desafio":
            print("Executando a busca com os dados fornecidos no desafio...")
            processos_str = ",".join(processos_desafio)
            exec_spider(processos=processos_str, cnpj=cnpj_desafio)

        another_op = questionary.confirm("Deseja realizar outra operação?").ask()
        if not another_op:
            print("Encerrando.")
            break


if __name__ == "__main__":
    main()
