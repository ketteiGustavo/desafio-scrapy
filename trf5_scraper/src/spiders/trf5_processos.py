# trf5_scraper/src/spiders/trf5_processos.py
import re
from typing import ClassVar

import scrapy
from src.items import ProcessoItem
from src.utils.limpar_texto import limpar_texto
from src.utils.tratar_data import tratar_data


class Trf5ProcessosSpider(scrapy.Spider):
    """
    Aranha para extrair dados de processos do TRF5.
    Permite a busca por número de processo ou por CNPJ.
    """

    name = "trf5_processos"
    allowed_domains: ClassVar[list[str]] = ["trf5.jus.br", "cp.trf5.jus.br"]
    base_url = "https://www5.trf5.jus.br"
    form_url = "https://cp.trf5.jus.br/cp/"

    def __init__(self, processos=None, cnpj=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processos = []
        if processos:
            self.processos = [p.strip() for p in processos.split(",") if p.strip()]
        self.cnpj = cnpj

    async def start(self):
        """
        Gera as requisições iniciais de forma assíncrona.
        """
        for numero in self.processos:
            url = f"{self.base_url}/processo/{numero}"
            self.logger.info(f"📄 Buscando processo informado: {numero}")
            yield scrapy.Request(
                url,
                callback=self.parse_processo,
                cb_kwargs={"numero_informado": numero},
            )

        if self.cnpj:
            self.logger.info(f"🔎 Iniciando busca por CNPJ: {self.cnpj}")
            yield scrapy.Request(
                url=self.form_url,
                callback=self.parse_cnpj_form,
            )

    def parse_cnpj_form(self, response):
        """
        Preenche e submete o formulário de busca por CNPJ.
        """
        cnpj_limpo = re.sub(r"\D", "", self.cnpj)
        if not cnpj_limpo or len(cnpj_limpo) != 14:
            self.logger.warning("CNPJ vazio após limpeza, abortando busca por CNPJ.")
            return

        form_url = "https://cp.trf5.jus.br/cp/cp.do"
        formdata = {
            "navigation": "Netscape",
            "filtroCpfRequest": cnpj_limpo,
            "tipo": "xmlcpf",
            "filtro": "",
            "filtroCPF2": cnpj_limpo,
            "tipoproc": "T",
            "filtroRPV_Precatorios": "",
            "uf_rpv": "PE",
            "numOriginario": "",
            "numRequisitorio": "",
            "numProcessExec": "",
            "uf_rpv_OAB": "PE",
            "filtro_processo_OAB": "",
            "filtro_CPFCNPJ": "",
            "campo_data_de": "",
            "campo_data_ate": "",
            "vinculados": "true",
            "ordenacao": "D",
            "ordenacao cpf": "D",
        }

        self.logger.info(f"Enviando formulário de CPF/CNPJ para {form_url} com {cnpj_limpo}")
        yield scrapy.FormRequest(
            url=form_url,
            formdata=formdata,
            callback=self.parse_cnpj_resultados,
            cb_kwargs={"cnpj_limpo": cnpj_limpo},
        )

    def parse_cnpj_resultados(self, response, cnpj_limpo):
        """
        Extrai os processos da primeira página de resultados do CNPJ
        e agenda as demais páginas para extração.
        """
        self.logger.info("Processando página de resultados da busca por CNPJ.")
        numeros_processo = re.findall(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", response.text)

        if not numeros_processo:
            self.logger.warning("Nenhum processo encontrado para o CNPJ na página %s", response.url)
            return

        self.logger.info("Encontrados %d processos na página %s", len(set(numeros_processo)), response.url)

        for numero in set(numeros_processo):
            url = f"{self.base_url}/processo/{numero}"
            yield scrapy.Request(
                url,
                callback=self.parse_processo,
                cb_kwargs={"numero_informado": numero},
            )

        if response.request.method == "POST":
            total_match = re.search(r"Total:\s*(\d+)", response.text)
            if total_match:
                total_results = int(total_match.group(1))
                num_pages = (total_results + 9) // 10
                self.logger.info(f"Total de {total_results} processos encontrados em {num_pages} páginas.")

                if num_pages > 1:
                    for page_num in range(2, num_pages + 1):
                        next_page_url = f"https://cp.trf5.jus.br/processo/cpf/porData/ativos/{cnpj_limpo}/{page_num}"
                        self.logger.info(f"Agendando busca na página {page_num}: {next_page_url}")
                        yield scrapy.Request(url=next_page_url, callback=self.parse_cnpj_pagination_page)

    def parse_cnpj_pagination_page(self, response):
        """
        Extrai os processos de uma página de paginação da busca por CNPJ.
        """
        self.logger.info("Processando página de paginação: %s", response.url)
        numeros_processo = re.findall(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", response.text)

        if not numeros_processo:
            self.logger.warning("Nenhum processo encontrado na página de paginação %s", response.url)
            return

        self.logger.info("Encontrados %d processos na página %s", len(set(numeros_processo)), response.url)

        for numero in set(numeros_processo):
            url = f"{self.base_url}/processo/{numero}"
            yield scrapy.Request(
                url,
                callback=self.parse_processo,
                cb_kwargs={"numero_informado": numero},
            )

    def parse_processo(self, response, numero_informado):
        """
        Extrai todos os campos da página de detalhes do processo.
        Versão final que processa os nós de texto para máxima robustez.
        """
        item = ProcessoItem()
        item["fonte"] = response.url

        text_nodes = [node.strip() for node in response.xpath("//body//text()").getall() if node.strip()]
        full_text = "\n".join(text_nodes)

        num_proc_match = re.search(r"PROCESSO Nº\s+([\d.-]+)", full_text)
        item["numero_processo"] = limpar_texto(num_proc_match.group(1)) if num_proc_match else numero_informado

        num_legado_match = re.search(r"PROCESSO Nº\s+[\d.-]+\s+\(([\d.-]+)\)", full_text)
        item["numero_legado"] = limpar_texto(num_legado_match.group(1)) if num_legado_match else ""

        data_autuacao_match = re.search(r"AUTUADO EM\s+([\d/]+)", full_text)
        item["data_autuacao"] = tratar_data(data_autuacao_match.group(1)) if data_autuacao_match else None

        relator_match = re.search(r"RELATOR\s*:\s*(.*?)\n", full_text, re.IGNORECASE)
        relator = limpar_texto(relator_match.group(1)) if relator_match else ""

        envolvidos = []
        movimentacoes = []

        i = 0
        while i < len(text_nodes):
            node = text_nodes[i]
            if i + 2 < len(text_nodes) and text_nodes[i + 1] == ":":
                papel = node
                nome = text_nodes[i + 2]

                ignore_list = [
                    "RELATOR",
                    "ASSUNTO",
                    "VARA",
                    "ORGÃO",
                    "FASE ATUAL",
                    "COMPLEMENTO",
                    "ÚLTIMA LOCALIZAÇÃO",
                    "CRÉDITO",
                ]
                if not any(keyword in papel.upper() for keyword in ignore_list):
                    envolvidos.append({"papel": limpar_texto(papel), "nome": limpar_texto(nome)})
                i += 3
                continue

            if node.startswith("Em ") and tratar_data(node.replace("Em ", "")):
                mov_date_str = node.replace("Em ", "")
                mov_text_parts = []
                i += 1
                while i < len(text_nodes) and not text_nodes[i].startswith("Em "):
                    mov_text_parts.append(text_nodes[i])
                    i += 1

                movimentacoes.append(
                    {"data": tratar_data(mov_date_str), "texto": limpar_texto(" ".join(mov_text_parts))}
                )
                continue

            i += 1

        item["relator"] = relator
        item["envolvidos"] = envolvidos
        item["movimentacoes"] = movimentacoes

        log_msg = (
            f"Processo {item['numero_processo']}: "
            f"{len(item['envolvidos'])} envolvidos, "
            f"{len(item['movimentacoes'])} movimentações"
        )
        self.logger.info(log_msg)
        yield item
