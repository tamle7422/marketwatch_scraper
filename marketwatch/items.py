# define here the models for your scraped items
#
# see documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class StockItem(scrapy.Item):
    name = scrapy.Field()
    birthDate = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    association = scrapy.Field()
    fighterClass = scrapy.Field()
    win = scrapy.Field()
    loss = scrapy.Field()
    nationality = scrapy.Field()
    locality = scrapy.Field()
    url = scrapy.Field()