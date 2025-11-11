<h1 align="center">
  TRF5 Scraper
</h1>

<div align="center">

# 🕷️ Desafio TRF5 Scraper

**Um scraper robusto em Python para extrair, padronizar e salvar dados de processos judiciais do portal de consulta pública do Tribunal Regional Federal da 5ª Região (TRF5).**

[![Mantido](https://img.shields.io/badge/Mantido%3F-sim-green.svg)](https://github.com/ketteiGustavo/desafio-scrapy)
[![Maintainer](https://img.shields.io/badge/mantenedor-luizgustavo-blue)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-bem--vindas-brightgreen.svg?style=flat-square)](https://github.com/ketteiGustavo/desafio-scrapy/pulls)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

</div>
<div align="center">
  <a href="https://github.com/ketteiGustavo/desafio-scrapy/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D+">Reportar Bug</a>
  ·
  <a href="https://github.com/ketteiGustavo/desafio-scrapy/issues/new?assignees=&labels=enhancement&template=solicitar_recurso.md&title=%5BFEATURE%5D+">Solicitar Recurso</a>
</div>

---
## 🛠️ Principais Ferramentas

![Python](https://img.shields.io/badge/python-3.13-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Scrapy](https://img.shields.io/badge/Scrapy-772A00?style=for-the-badge&logo=scrapy&logoColor=white)
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-222?style=for-the-badge&logo=ruff&logoColor=white)
![isort](https://img.shields.io/badge/isort-161B22?style=for-the-badge&logo=isort&logoColor=white)
![MyPy](https://img.shields.io/badge/MyPy-13679A?style=for-the-badge&logo=mypy&logoColor=white)

---

## 📖 Sobre o Projeto

O **TRF5 Scraper** é uma ferramenta de automação construída com o framework **Scrapy** para realizar a coleta de dados de processos judiciais diretamente do portal do TRF5. A interação é facilitada por uma CLI (Interface de Linha de Comando) amigável e interativa, que guia o usuário através das diferentes opções de busca.

O projeto foi desenhado para ser eficiente, lidando com a busca por múltiplos critérios e a paginação dos resultados, garantindo a extração completa dos dados.

### ✨ Funcionalidades

- **Busca por Número de Processo:** Extrai dados de um ou mais processos específicos.
- **Busca por CNPJ:** Realiza uma busca completa por CNPJ, navegando através de todas as páginas de resultados para coletar todos os processos associados.
- **Execução Completa do Desafio:** Um modo que executa um conjunto pré-definido de buscas por processos e CNPJ.
- **CLI Interativa:** Uma interface de linha de comando construída com `questionary` que torna a execução simples e intuitiva.
- **Armazenamento Estruturado:** Salva os dados de cada processo em arquivos `JSON` individuais no diretório `data/processos/`.
    *Observação: A integração com MongoDB foi considerada, mas não foi possível implementar a tempo. Será uma melhoria futura.*

---

## 🗂️ Índice

<details>

<summary>Ver mais</summary>

- [🕷️ Desafio TRF5 Scraper](#️-desafio-trf5-scraper)
  - [🛠️ Principais Ferramentas](#️-principais-ferramentas)
  - [📖 Sobre o Projeto](#-sobre-o-projeto)
    - [✨ Funcionalidades](#-funcionalidades)
  - [🗂️ Índice](#️-índice)
  - [🚀 Começando](#-começando)
    - [📋 Pré-requisitos](#-pré-requisitos)
    - [📋 Instruções de Instalação](#-instruções-de-instalação)
  - [🏃‍♀️ Executando a Aplicação](#️-executando-a-aplicação)
    - [✅ Via CLI Interativa](#-via-cli-interativa)
    - [✅ Via Scrapy CLI](#-via-scrapy-cli)
  - [🧑‍💻 Desenvolvimento](#-desenvolvimento)
    - [✏️ Formatação e Linting](#️-formatação-e-linting)
  - [📂 Estrutura do Projeto](#-estrutura-do-projeto)
    - [Descrição dos Arquivos de Configuração](#descrição-dos-arquivos-de-configuração)
  - [📚 Documentação Adicional](#-documentação-adicional)
  - [🤝 Contribuindo](#-contribuindo)
  - [🤝 CONTRIBUIÇÕES E CONTRIBUIDORES ✒️](#-contribuições-e-contribuidores-️)
  - [🚫 .gitignore (Recomendado)](#-gitignore-recomendado)

</details>

---

## 🚀 Começando

Siga estes passos para configurar e executar o projeto em seu ambiente de desenvolvimento local.

### 📋 Pré-requisitos

- **Python 3.8+**
- **Git** para controle de versão.
- Um ambiente virtual (venv, conda, etc.) é altamente recomendado.

### 📋 Instruções de Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/ketteiGustavo/desafio-scrapy.git
    cd desafio-scrapy
    ```

2. **Crie e ative um ambiente virtual (Exemplo com `venv`):**

    ```bash
    # Linux / macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

---

## 🏃‍♀️ Executando a Aplicação

### ✅ Via CLI Interativa

A forma principal de executar o projeto é através do script `main.py`, que inicia a interface interativa.

1. **Ative o ambiente virtual** (se ainda não estiver ativo).

2. **Execute o script principal:**

    ```bash
    python -m trf5_scraper.src.main
    ```

    *No Linux/macOS, pode ser necessário usar `python3`.*

3. **Siga as instruções do menu interativo** para escolher o tipo de busca. Os resultados serão salvos na pasta `data/processos/`.

### ✅ Via Scrapy CLI

Você também pode executar o scraper diretamente com o Scrapy, o que é útil para testes e automação.

1. **Ative o ambiente virtual** e navegue até a raiz do projeto.

2. **Execute os comandos `scrapy crawl`:**

    - **Para buscar por número de processo:**

        ```bash
        scrapy crawl trf5_processos -a processos="0000560-67.2017.4.05.0000"
        ```

    - **Para buscar por CNPJ:**

        ```bash
        scrapy crawl trf5_processos -a cnpj="00.000.000/0001-91"
        ```

---

## 🧑‍💻 Desenvolvimento


### ✏️ Formatação e Linting

O projeto utiliza um conjunto de ferramentas para garantir a qualidade e a consistência do código, gerenciadas através do `pre-commit`.

- **Ruff:** Usado para linting e formatação de código (substituto do `black` e `flake8`).
- **isort:** Organiza automaticamente os imports.
- **mypy:** Realiza a checagem estática de tipos.

Ao fazer um `git commit`, os hooks do `pre-commit` serão executados automaticamente para formatar e validar os arquivos modificados. Para instalar os hooks no seu ambiente local, execute:

```bash
pre-commit install
```

---

## 📂 Estrutura do Projeto

A estrutura de pastas foi pensada para ser modular e escalável. Abaixo está uma visão geral dos principais arquivos e diretórios:

```bash
.
├── .editorconfig
├── .git/
├── .github/
├── .venv/
├── .vscode/
├── data/
│   └── processos/
├── docs/
├── trf5_scraper/
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
└── requirements.txt
```

### Descrição dos Arquivos de Configuração

- **`.github/`**: Contém templates para Issues e Pull Requests, além de workflows de automação (CI/CD) com GitHub Actions. Ajuda a padronizar as contribuições e a manter a qualidade do projeto.
- **`.vscode/`**: Armazena configurações específicas do Visual Studio Code, como configurações de depuração (`launch.json`) e tarefas (`tasks.json`), facilitando o desenvolvimento no editor.
- **`.editorconfig`**: Ajuda a manter estilos de codificação consistentes (como indentação e fim de linha) entre diferentes editores e IDEs.
- **`.gitattributes`**: Define atributos específicos para caminhos no Git. É útil para gerenciar como o Git trata finais de linha (`eol`) e para configurar o Git LFS.
- **`.pre-commit-config.yaml`**: Arquivo de configuração para os hooks do `pre-commit`. Define quais ferramentas de linting e formatação são executadas antes de cada commit.
- **`pyproject.toml`**: Arquivo de configuração padrão para projetos Python. Neste projeto, é usado principalmente para configurar ferramentas como `ruff`, `isort` e `mypy`.
- **`requirements.txt`**: Lista as dependências Python necessárias para executar o projeto.

---

## 📚 Documentação Adicional

Para mais detalhes sobre as convenções e guias utilizados no desenvolvimento deste projeto, consulte os seguintes documentos na pasta `docs/`:

- **[Descrição do Desafio](./docs/desafio.md):** O documento original que descreve o problema e os requisitos do projeto.
- **[Guia de Boas Práticas para `__init__.py`](./docs/boas-praticas-init.md):** Padrões para a estruturação de pacotes Python no projeto.
- **[Guia Rápido de Git](./docs/guia-git.md):** Comandos essenciais do Git para contribuir com o repositório.
- **[Guia Básico de Markdown](./docs/guia-markdown.md):** Como formatar textos para a documentação.

---

## 🤝 Contribuindo

Contribuições são o que tornam a comunidade de código aberto um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

Para contribuir, por favor, siga estes passos:

1. **Crie uma Issue:** Antes de começar a trabalhar, abra uma issue descrevendo o bug que você encontrou ou a funcionalidade que deseja adicionar. Isso ajuda a alinhar as ideias com os mantenedores do projeto.
    - Use o template [**Reportar Bug**](https://github.com/ketteiGustavo/desafio-scrapy/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D+) para problemas.
    - Use o template [**Solicitar Recurso**](https://github.com/ketteiGustavo/desafio-scrapy/issues/new?assignees=&labels=enhancement&template=solicitar_recurso.md&title=%5BFEATURE%5D+) para novas ideias.

2. **Faça um Fork e crie uma Branch:**

    ```bash
    # Crie um fork do projeto
    # Clone o seu fork e crie uma branch para sua feature
    git checkout -b feature/AmazingFeature
    ```

3. **Desenvolva e Faça o Commit:**
    - Escreva seu código seguindo os padrões do projeto.
    - Faça commits atômicos e utilize o padrão [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

    ```bash
    git commit -m "feat: Add some AmazingFeature"
    ```

4. **Abra um Pull Request:**
    - Faça o push das suas alterações para o seu fork.
    - Abra um Pull Request para a branch `main` do repositório original.
    - Preencha o template do Pull Request com os detalhes da sua contribuição.

---

## 🤝 CONTRIBUIÇÕES E CONTRIBUIDORES ✒️
<!---
Mencione todos as pessoas que contribuiram com código nesse projeto
-->
Consulte os maiores [contribuidores](https://github.com/ketteiGustavo/desafio-scrapy/graphs/contributors) do projeto.

<!--- Sinta se livre para adicionar sua foto de contribuidor, mas siga o modelo abaixo-->
Agradecimento especial a todas as pessoas que participaram deste projeto:

<table>
  <tr>
    <td align="center">
        <div style="text-align: center;">
          <a href="https://github.com/ketteiGustavo" target="_blank">
            <img src="https://avatars.githubusercontent.com/u/140563277?v=4" width="80px" style="border-radius: 50%;" alt="Luiz Gustavo Profile Picture"/>
            <div style="color: #fac864"><b>Luiz Gustavo</b></div>
            <div style="color: #006effff">Desenvolvedor</div>
          </a>
        </div>
    </td>
  </tr>
</table>

---

## 🚫 .gitignore (Recomendado)

> foi utilizado o .gitignore padronizado fornecido pela [toptal](https://www.toptal.com/developers/gitignore).

> os demais arquivos que não tem necessidade de serem commitados adicione ao .gitignore e o atualize separadamente.
