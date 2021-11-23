# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CatalogGoodsItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    setting = scrapy.Field()
    url = scrapy.Field()
    url_image = scrapy.Field()
