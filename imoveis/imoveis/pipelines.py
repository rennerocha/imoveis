import datetime
from urllib.parse import urlparse
from scrapy.exceptions import DropItem


class ImoveisPipeline(object):
    def process_item(self, item, spider):
        item["date"] = datetime.date.today()
        return item
