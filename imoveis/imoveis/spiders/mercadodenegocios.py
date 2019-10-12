import json
import scrapy


class MercadoDeNegociosSpider(scrapy.Spider):

    real_estate = None
    busca_url = None

    def get_payload(self, property_type, skip=None):
        raise NotImplementedError

    def start_requests(self):
        available_types = ["comprar", "alugar"]
        for property_type in available_types:
            payload = self.get_payload(property_type)
            yield scrapy.http.JSONRequest(
                self.busca_url,
                data=payload,
                meta={"skip": 0, "property_type": property_type},
            )

    def parse(self, response):
        results = json.loads(response.body_as_unicode())
        available_properties = results.get("imoveis", [])

        num_results = len(available_properties)
        if num_results == 0:
            return

        for result in available_properties:
            yield result

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
            "skip": 0,
            "limit": "10",
            "modo": False,
        }
