import json
from urllib.parse import urlparse

import scrapy

from imoveis.items import PropertyItem


class MercadoDeNegociosSpider(scrapy.Spider):

    real_estate = None
    busca_url = None
    available_types = ()

    def get_payload(self, property_type, skip=None):
        raise NotImplementedError

    def result_to_item(self, result):
        item = PropertyItem()

        property_code = result["sigla"]
        parsed_url = urlparse(self.busca_url)
        property_url = (
            f"{parsed_url.scheme}://{parsed_url.netloc}/imovel/{property_code}"
        )
        item["url"] = property_url
        item["code"] = property_code
        item["property_type"] = result["tipo"]

        local = result.get("local", {})
        item["city"] = local.get("cidade")
        item["neighborhood"] = local.get("bairro")

        coordinates = local.get("coordenadas", [])
        if len(coordinates) == 2:
            item["latitude"] = local["coordenadas"][0]
            item["longitude"] = local["coordenadas"][1]

        rent_info = result["comercializacao"].get("locacao", {})
        item["for_rent"] = rent_info.get("ativa", False)
        item["rent_price"] = rent_info.get("preco")

        sale_info = result["comercializacao"].get("venda", {})
        item["for_sale"] = sale_info.get("ativa", False)
        item["sale_price"] = sale_info.get("preco")

        numbers = result["numeros"]
        item["built_area"] = numbers["areas"].get("construida")
        item["total_area"] = numbers["areas"].get("total")

        item["real_estate"] = self.real_estate

        return item

    def start_requests(self):
        for property_type in self.available_types:
            payload = self.get_payload(property_type)
            yield scrapy.http.JSONRequest(
                self.busca_url,
                data=payload,
                meta={"skip": 0, "property_type": property_type},
            )

    def parse(self, response):
        results = json.loads(response.body_as_unicode())

        if isinstance(results, list):
            available_properties = results
        else:
            available_properties = results.get("imoveis", [])

        num_results = len(available_properties)
        if num_results == 0:
            return

        for result in available_properties:
            yield self.result_to_item(result)

        # Pagination
        skip = response.meta.get("skip", 0)
        property_type = response.meta.get("property_type")

        offset = skip + num_results
        payload = self.get_payload(property_type=property_type, skip=offset)
        yield scrapy.http.JSONRequest(
            self.busca_url,
            data=payload,
            meta={"skip": offset, "property_type": property_type},
        )


class VillaImoveisCampinasSpider(MercadoDeNegociosSpider):
    name = "villaimoveiscampinas"
    allowed_domains = ["villaimoveiscampinas.com.br"]
    real_estate = "villaimoveiscampinas"
    busca_url = "https://villaimoveiscampinas.com.br/busca/Imoveis"
    available_types = ["comprar", "alugar"]

    def get_payload(self, property_type, skip=0):
        return {
            "busca": {
                "comercializacao": property_type,
                "categoria": "",
                "condominio": [],
                "tipo": [],
                "bairro": [],
                "cidade": [],
                "finalidade": "",
                "vagas": 0,
                "dorms": 0,
                "banheiros": 0,
                "preco": 0,
                "emCondominio": False,
                "corretor": False,
            },
            "ordem": "crescente",
            "skip": skip,
            "limit": 8,
            "modo": "imoveis",
        }


class GalanteImoveisSpider(MercadoDeNegociosSpider):
    name = "galanteimoveis"
    allowed_domains = ["galanteimoveis.com.br"]
    real_estate = "galanteimoveis"
    busca_url = "https://galanteimoveis.com.br/busca/Imoveis"
    available_types = ["comprar", "alugar"]

    def get_payload(self, property_type, skip=0):
        return {
            "busca": {
                "comercializacao": property_type,
                "tipo": "",
                "numeros": [],
                "bairro": [],
                "venda": {"min": 0, "max": 0},
                "area": {"min": 0, "max": 0},
                "codigos": [],
                "aluguel": {"min": 0, "max": 0},
                "emcondominio": False,
            },
            "ordem": "recente",
            "skip": skip,
            "limit": "10",
            "modo": False,
        }


class StartImoveisSpider(MercadoDeNegociosSpider):
    name = "startimoveis"
    allowed_domains = ["startimoveis.com.br"]
    real_estate = "startimoveis"
    busca_url = "https://startimoveis.com.br/busca/Imoveis"
    available_types = ["venda", "alugar"]

    def get_payload(self, property_type, skip=0):
        return {
            "busca": {
                "comercializacao": property_type,
                "categoria": "",
                "tipo": "",
                "bairro": [],
                "condominio": [],
                "cidade": [],
                "codigos": [],
                "numeros": [None, "", "", ""],
                "emcondominio": False,
                "empermuta": False,
                "valor": {"venda": {}, "alugar": {}},
                "area": {},
            },
            "ordem": "recente",
            "skip": skip,
            "categoria": "",
            "limit": 12,
            "modo": False,
        }


class RumoImobiliariaSpider(MercadoDeNegociosSpider):
    name = "rumoimobiliaria"
    allowed_domains = ["rumoimobiliaria.com.br"]
    real_estate = "rumoimobiliaria"
    busca_url = "https://rumoimobiliaria.com.br/busca/Imoveis"
    available_types = ["comprar", "alugar"]

    def get_payload(self, property_type, skip=0):
        return {
            "busca": {
                "comercializacao": property_type,
                "categoria": "",
                "condominio": [],
                "tipo": [],
                "bairro": [],
                "cidade": [],
                "finalidade": "",
                "vagas": 0,
                "dorms": 0,
                "banheiros": 0,
                "preco": 0,
                "emCondominio": False,
                "corretor": False,
            },
            "ordem": "crescente",
            "skip": skip,
            "limit": 8,
            "modo": "imoveis",
        }


class PradoGoncalvesSpider(MercadoDeNegociosSpider):
    name = "pradogoncalves"
    allowed_domains = ["pradogoncalves.com.br"]
    real_estate = "pradogoncalves"
    busca_url = "https://pradogoncalves.com.br/busca/Imoveis"
    available_types = ("comprar", "alugar")

    def get_payload(self, property_type, skip=0):
        return {
            "busca": {
                "comercializacao": property_type,
                "categoria": "",
                "condominio": [],
                "tipo": [],
                "bairro": [],
                "cidade": [],
                "finalidade": "",
                "vagas": 0,
                "dorms": 0,
                "banheiros": 0,
                "preco": "",
                "emCondominio": False,
                "corretor": False,
            },
            "ordem": "crescente",
            "skip": skip,
            "limit": 8,
            "modo": "imoveis",
        }


class ProvectumImoveisSpider(MercadoDeNegociosSpider):
    name = "provectumimoveis"
    allowed_domains = ["provectumimoveis.com.br"]
    real_estate = "provectumimoveis"
    busca_url = "https://provectumimoveis.com.br/busca/Imoveis"
    available_types = ("locacao", "venda")

    def get_payload(self, property_type, skip=0):
        return {
            "busca": f'{{"comercializacao.{property_type}.ativa":true}}',
            "modo": False,
            "ordem": {
                f"comercializacao.{property_type}.ativa": -1,
                f"comercializacao.{property_type}.preco": -1,
            },
            "skip": skip,
            "limit": 12,
            "exclusivo": False,
        }
