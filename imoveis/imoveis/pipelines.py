import datetime
from urllib.parse import urlparse
from scrapy.exceptions import DropItem


class ImoveisPipeline:
    def process_item(self, item, spider):
        item["date"] = datetime.date.today()
        return item


class FilterDuplicatedPropertiesPipeline:
    def __init__(self):
        self.visited_codes = set()

    def process_item(self, item, spider):
        item_code = item["code"]
        if item_code in self.visited_codes:
            raise DropItem(f"Already collected {item_code}")
        else:
            self.visited_codes.add(item["code"])
            return item
