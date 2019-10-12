import json
import scrapy


class VillaImoveisCampinasSpider(scrapy.Spider):
    name = "villaimoveiscampinas"
    allowed_domains = ["villaimoveiscampinas.com.br"]

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

    def start_requests(self):
        available_types = ["comprar", "alugar"]
        for property_type in available_types:
            payload = self.get_payload(property_type)
            yield scrapy.http.JSONRequest(
                "https://villaimoveiscampinas.com.br/busca/Imoveis",
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
            "https://villaimoveiscampinas.com.br/busca/Imoveis",
            data=payload,
            meta={"skip": offset, "property_type": property_type},
        )
