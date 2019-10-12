import json
import scrapy


class ProvectumSpider(scrapy.Spider):
    name = "provectum"
    allowed_domains = ["provectumimoveis.com.br"]

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

    def start_requests(self):
        available_types = ["locacao", "venda"]
        for property_type in available_types:
            payload = self.get_payload(property_type)
            yield scrapy.http.JSONRequest(
                "https://provectumimoveis.com.br/busca/Imoveis",
                data=payload,
                meta={"skip": 0, "property_type": property_type},
            )

    def parse(self, response):
        results = json.loads(response.body_as_unicode())
        num_results = len(results)
        if num_results == 0:
            return

        for result in results:
            yield result

        # Pagination
        skip = response.meta.get("skip", 0)
        property_type = response.meta.get("property_type")

        offset = skip + num_results
        payload = self.get_payload(property_type=property_type, skip=offset)
        yield scrapy.http.JSONRequest(
            "https://provectumimoveis.com.br/busca/Imoveis",
            data=payload,
            meta={"skip": offset, "property_type": property_type},
        )
