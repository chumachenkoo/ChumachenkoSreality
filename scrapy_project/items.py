import scrapy

class ScrapyProjectItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()