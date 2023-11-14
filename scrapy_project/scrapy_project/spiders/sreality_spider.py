import scrapy
from scrapy_project.items import ScrapyProjectItem
from scrapy.crawler import CrawlerProcess


class SrealitySpiderSpider(scrapy.Spider):
    name = "sreality_spider"
    allowed_domains = ['sreality.cz']
    start_urls = [
        f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page={page}'
        for page in range(1, 6)
    ]

    def parse(self, response):
        json_response = response.json()
        for item in json_response["_embedded"]['estates']:
            current_img = next(iter(item["_links"]["images"]), None)
            yield ScrapyProjectItem(name=item['name'], image=current_img)


if __name__ == "__main__":
    settings = {'ITEM_PIPELINES': {'scrapy_project.pipelines.ScrapyProjectPipeline': 300}}
    process = CrawlerProcess(settings)
    process.crawl(SrealitySpiderSpider)
    process.start()