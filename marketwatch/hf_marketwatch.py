import re
from scrapy.loader import ItemLoader
from .items import MarketWatchItem
import logging
from datetime import datetime

def getTime():
    try:
        now = datetime.now()
        currentDate = now.strftime("%m_%d_%y")
        return currentDate

    except Exception as ex:
        print("exception --- error in get time => {0}".format(ex))

def setName1(self,sel):
    try:
        name = checkEmpty(sel.xpath(".//td[@class='name']/a/text()").get())
        if (name != "None"):
            self.name = name
        else:
            self.name = "None"

    except Exception as ex:
        print("exception --- error in set name => {0}".format(ex))

def setLocation(self,location):
    subComma = re.sub(r"[\,]",";",location)
    self.location = '-' + subComma + '-'


def setSymbol(self,sel):
    try:
        symbol = checkEmpty(sel.xpath(".//td[@class='name']/a/small/text()").extract())
        symbol = "".join(symbol)
        subParen = re.sub(r"[\(\)]+","",symbol)

        if (len(subParen) != 0 and subParen != "None"):
            self.symbol = subParen.lower()
        else:
            self.symbol = "None"

    except Exception as ex:
        print("exception --- error in set symbol => {0}".format(ex))
        self.symbol = "None"

def setName(self,name):
    try:
        self.name = name.lower()

    except Exception as ex:
        print("exception => error setting name --- {0}".format(ex))
        self.name = "None"

def setCountry(self,sel):
    try:
        country = checkEmpty(sel.xpath(".//td[2]/text()").get())
        if (country != "None"):
            self.country = country.lower()
        else:
            self.country = "None"

    except Exception as ex:
        print("exception --- error in set country => {0}".format(ex))
        self.country = "None"

def setExchange(self,sel):
    try:
        exchange = checkEmpty(sel.xpath(".//td[3]/text()").get())
        if (exchange != "None"):
            self.exchange = exchange.lower()
        else:
            self.exchange = "None"

    except Exception as ex:
        print("exception --- error in set exchange => {0}".format(ex))
        self.exchange = "None"

def setSector(self,sel):
    try:
        sector = checkEmpty(sel.xpath(".//td[4]/text()").get())
        if (sector != "None"):
            self.sector = sector.lower()
        else:
            self.sector = "None"

    except Exception as ex:
        print("exception --- error in set sector => {0}".format(ex))
        self.sector = "None"

def loadMarketWatchItem(self,response):
    try:
        self.name = self.name if (self.name != "") else "None"
        self.symbol = self.symbol if (self.symbol != "") else "None"
        self.country = self.country if (self.country != "") else "None"
        self.exchange = self.exchange if (self.exchange != "") else "None"
        self.sector = self.sector if (self.sector != "") else "None"

        loader = ItemLoader(item=MarketWatchItem(), response=response)
        loader.add_value("name", self.name)
        loader.add_value("symbol", self.symbol)
        loader.add_value("country", self.country)
        loader.add_value("exchange", self.exchange)
        loader.add_value("sector", self.sector)
        return loader

    except Exception as ex:
        print("exception --- error in load marketwatch item => {0}".format(ex))

def loadMarketWatchItemSelector(self,response,sel):
    self.name = self.name if (len(self.name) != 0) else "None"
    self.symbol = self.symbol if (len(self.symbol) != 0) else "None"
    self.country = self.country if (len(self.country) != 0) else "None"
    self.exchange = self.exchange if (len(self.exchange) != 0) else "None"
    self.sector = self.sector if (len(self.sector) != 0) else "None"

    loader = ItemLoader(item=MarketWatchItem(),response=response)
    loader.add_value("name",self.name)
    loader.add_value("symbol",self.symbol)
    loader.add_value("country",self.country)
    loader.add_value("exchange",self.exchange)
    loader.add_value("sector",self.sector)
    return loader

def checkEmpty(data):
    if (data == None or len(data) == 0):
        data = "None"
        return data
    else:
        return data