# 📖 Guia de Boas Práticas – Uso de `__init__.py` em Projetos Python

Este documento define como estruturar e utilizar os arquivos `__init__.py` no projeto **TRF5 Scraper**, servindo como referência para todos os desenvolvedores.

---

## 🔎 O que é o `__init__.py`?

- Arquivo especial que indica ao Python que um diretório é um **pacote importável**.
- Desde o Python 3.3, pacotes **implícitos** existem, mas ainda é boa prática manter o `__init__.py` para clareza e consistência.
- Pode ser **vazio**, mas também pode **centralizar imports**, definir a **API pública** do pacote (`__all__`) ou executar **inicializações leves**.

---

## ✅ Boas práticas no nosso projeto

### 1. Pacotes de alto nível (`spiders`, `utils`, `validators`, etc.)

- Devem **expor a API pública principal** do pacote, facilitando o acesso aos seus componentes mais importantes.
- Exemplo:

  ```python
  # trf5_scraper/src/spiders/__init__.py
  from .trf5_processos import Trf5ProcessosSpider

  __all__ = ["Trf5ProcessosSpider"]
  ```

- Uso:

  ```python
  from src.spiders import Trf5ProcessosSpider
  ```

---

### 2. Centralizar imports úteis

- Pacotes como `utils` e `validators` devem funcionar como **pontos de entrada** simples para suas funções.
- Exemplo:

  ```python
  # trf5_scraper/src/utils/__init__.py
  from .limpar_texto import limpar_texto
  from .tratar_data import tratar_data

  __all__ = ["limpar_texto", "tratar_data"]
  ```

  Agora, em vez de `from src.utils.limpar_texto import limpar_texto`, podemos usar:

  ```python
  from src.utils import limpar_texto
  ```

---

### 3. Evitar lógica pesada no `__init__.py`

- Pode conter **configurações leves** (ex.: inicialização de logging), mas isso não é comum em nosso projeto.
- **Nunca** coloque código demorado, como chamadas de rede, I/O de arquivo pesado ou lógica de negócio complexa, dentro de um `__init__.py`. Isso pode causar lentidão na inicialização e dificultar os testes.

---

### 4. Controle com `__all__`

- Use `__all__` para definir explicitamente quais nomes (classes, funções, variáveis) são exportados quando um pacote é importado com `from pacote import *`.
- Isso documenta a **API estável** do seu pacote e evita a exposição acidental de módulos ou variáveis internas.

---

## 📂 Exemplo de Estrutura Organizada

Abaixo, um exemplo de como os `__init__.py` podem organizar a estrutura do nosso projeto `trf5_scraper`:

```bash
trf5_scraper/
└── src/
    ├── __init__.py     # Pode ficar vazio ou expor componentes principais de 'src'
    ├── spiders/
    │   ├── __init__.py # Expondo Trf5ProcessosSpider
    │   └── trf5_processos.py
    ├── utils/
    │   ├── __init__.py # Expondo limpar_texto, tratar_data
    │   ├── limpar_texto.py
    │   └── tratar_data.py
    ├── validators/
    │   ├── __init__.py # Expondo a função de validação de CNPJ
    │   └── cnpj.py
    ├── items.py
    ├── main.py
    └── pipelines.py
```

---

## 🚀 Conclusão

- Use `__init__.py` para **organizar a API pública** dos seus pacotes.
- **Pacotes de alto nível** (`spiders`, `utils`) devem expor seus componentes principais para facilitar o uso em outras partes do projeto.
- **Subpacotes internos** (se existissem) poderiam ter `__init__.py` vazios para evitar expor detalhes de implementação.

---
