# define here the models for your scraped items
#
# see documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class MarketWatchItem(scrapy.Item):
    name = scrapy.Field()
    symbol = scrapy.Field()
    country = scrapy.Field()
    exchange = scrapy.Field()
    sector = scrapy.Field()
