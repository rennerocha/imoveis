from urllib.parse import urlparse
from scrapy.exceptions import DropItem


class ImoveisPipeline(object):
    def process_item(self, item, spider):
        if not item["comercializacao"]["locacao"]["ativa"]:
            raise DropItem("Not for rent")

        property_code = item["sigla"]
        parsed_url = urlparse(spider.busca_url)
        property_url = (
            f"{parsed_url.scheme}://{parsed_url.netloc}/imovel/{property_code}"
        )

        return {
            "bairro": item["local"]["bairro"],
            "latitude": item["local"]["coordenadas"][0],
            "longitude": item["local"]["coordenadas"][1],
            "preco": item["comercializacao"]["locacao"]["preco"],
            "preco_total": item["comercializacao"]["locacao"]["total"],
            "area_construida": item["numeros"]["areas"]["construida"],
            "url": property_url,
            "imobiliaria": spider.real_estate,
            "codigo": item["sigla"],
        }
