from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def crawl_all():
    process = CrawlerProcess(get_project_settings())
    spiders = process.spider_loader.list()
    for spider in spiders:
        process.crawl(spider)
    process.start()


if __name__ == "__main__":
    crawl_all()
