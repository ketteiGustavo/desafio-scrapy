import json
import os
import re
from datetime import datetime

from itemadapter import ItemAdapter


class SalvarJson:
    """
    Pipeline que processa um item e o salva em um arquivo JSON.

    O arquivo será salvo em '../data/processos/{numero_processo}.json'.
    O diretório será criado se não existir.
    Datas são convertidas para o formato ISO 8601.
    """

    def open_spider(self, spider):
        """Cria o diretório de dados na inicialização"""
        self.output_dir = "../data/processos"
        os.makedirs(self.output_dir, exist_ok=True)

    def process_item(self, item, spider):
        """
        Processa e salva o item em um arquivo JSON.
        """
        adapter = ItemAdapter(item)
        numero_processo = adapter.get("numero_processo")

        if not numero_processo:
            spider.logger.warning(f"Item sem número de processo, não será salvo: {adapter.asdict()}")
            return item

        filename = re.sub(r"[^a-zA-Z0-9.-]", "_", numero_processo) + ".json"
        filepath = os.path.join(self.output_dir, filename)

        item_dict = adapter.asdict()
        for key, value in item_dict.items():
            if isinstance(value, datetime):
                item_dict[key] = value.isoformat()
            elif isinstance(value, list):
                new_list = []
                for i in value:
                    if isinstance(i, dict):
                        new_dict = {}
                        for k, v in i.items():
                            if isinstance(v, datetime):
                                new_dict[k] = v.isoformat()
                            else:
                                new_dict[k] = v
                        new_list.append(new_dict)
                    else:
                        new_list.append(i)
                item_dict[key] = new_list

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(item_dict, f, ensure_ascii=False, indent=4)

        spider.logger.info(f"Processo salvo em {filepath}")
        return item
