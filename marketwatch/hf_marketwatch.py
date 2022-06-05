import re
from scrapy.loader import ItemLoader
from .items import MarketWatchItem
import logging
from datetime import datetime




def getTime():
    now = datetime.now()
    currentDate = now.strftime("%m_%d_%y")
    return currentDate

def setLocation(self,location):
    subComma = re.sub(r"[\,]",";",location)
    self.location = '-' + subComma + '-'

def setSymbol(self,symbol):
    try:
        symbol = "".join(symbol)
        subParen = re.sub(r"[\(\)]","",symbol)

        if (len(subParen) != 0 and subParen != "None"):
            self.symbol = subParen.lower()
        else:
            self.symbol = "None"

    except Exception as ex:
        print("exception => error setting symbol --- {0}".format(ex))
        self.symbol = "None"

def setName(self,name):
    try:
        self.name = name.lower()

    except Exception as ex:
        print("exception => error setting name --- {0}".format(ex))
        self.name = "None"

def setCountry(self,country):
    try:
        if (country != "None"):
            self.country = country.lower()
        else:
            self.country = "None"

    except Exception as ex:
        print("exception => error setting country --- {0}".format(ex))
        self.country = "None"

def setExchange(self,exchange):
    try:
        if (exchange != "None"):
            self.exchange = exchange.lower()
        else:
            self.exchange = "None"

    except Exception as ex:
        print("exception => error setting exchange --- {0}".format(ex))
        self.exchange = "None"


def setSector(self,sector):
    try:
        if (sector != "None"):
            self.sector = sector.lower()
        else:
            self.sector = "None"

    except Exception as ex:
        print("exception => error setting sector --- {0}".format(ex))
        self.sector = "None"

def setAge(self,age):
    subStr = ""
    if (re.search(r"N/A",age) != None):
        self.age = "None"
    else:
        subStr = re.sub(r"AGE:","",age)
        self.age = subStr.strip()

def setBirthDate(self,birthDate):
    month = ""
    day = ""
    year = ""
    if (re.search(r"N/A",birthDate) != None):
        self.birthDate = "None"
    else:
        splitDash = birthDate.split("-")
        month = splitDash[1]
        day  = splitDash[2]
        year = splitDash[0]

        self.birthDate = month + "/" + day + "/" + year

def setFirstRowFightCard(self,response):
    try:
        # check for meta tag
        hasMeta = checkEmpty(response.xpath("//div[@class='left-module-pad-line']/meta[@itemprop]").get())

        if (hasMeta != "None"):
            fighter1Name = checkEmpty(response.xpath("//div[@class='fighter left_side']/h3/a/span/text()").get())
            if (fighter1Name != "None"):
                self.fighter1Name = fighter1Name.lower()
            else:
                self.fighter1Name = "None"

            fighter1Result = checkEmpty(response.xpath("//div[@class='fighter left_side']/span[contains(@class,'final_result')]/text()").get())
            if (fighter1Result != "None"):
                self.fighter1Result = checkFightResult(self, fighter1Result.lower())
            else:
                self.fighter1Result = "None"

            fighter2Name = checkEmpty(response.xpath("//div[@class='fighter right_side']/h3/a/span/text()").get())
            if (fighter2Name != "None"):
                self.fighter2Name = fighter2Name.lower()
            else:
                self.fighter2Name = "None"

            fighter2Result = checkEmpty(response.xpath("//div[@class='fighter right_side']/span[contains(@class,'final_result')]/text()").get())
            if (fighter2Result != "None"):
                self.fighter2Result = checkFightResult(self, fighter2Result.lower())
            else:
                self.fighter2Result = "None"

            fightMethodResult = checkEmpty(
                response.xpath("//div/table[contains(@class,'fight_card_resume')]/tbody/tr/td[2]/text()").get())
            if (fightMethodResult != "None"):
                self.fightMethodResult = fightMethodResult.strip().lower()
            else:
                self.fightMethodResult = "None"

    except Exception as ex:
        print("exception => error setting first row fight card --- {0}".format(ex))

def checkFightResult(self,fightResult):
    if (fightResult == "win"):
        return "W"
    elif (fightResult == "loss"):
        return "L"

def setFighterName(self,fighterName,type):
    try:
        firstName = fighterName[0]
        lastName = fighterName[1]

        if (type == "f1"):
            self.fighter1Name = firstName.lower() + " " + lastName.lower()
        else:
            self.fighter2Name = firstName.lower() + " " + lastName.lower()


    except Exception as ex:
        print("exception => error setting {0} name --- {1}".format(type,ex))
        if (type == "f1"):
            self.fighter1Name = "None"
        else:
            self.fighter2Name = "None"

def loadMarketWatchItem(self,response):
    self.name = self.name if (self.name != "") else "None"
    self.symbol = self.symbol if (self.symbol != "") else "None"
    self.country = self.country if (self.country != "") else "None"
    self.exchange = self.exchange if (self.exchange != "") else "None"
    self.sector = self.sector if (self.sector != "") else "None"

    loader = ItemLoader(item=MarketWatchItem(),response=response)
    loader.add_value("name",self.name)
    loader.add_value("symbol",self.symbol)
    loader.add_value("country",self.country)
    loader.add_value("exchange",self.exchange)
    loader.add_value("sector",self.sector)
    return loader

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

# def loadNasdaqStockItem(self,response):
#     self.name = self.name if (self.name != "") else "None"
#     self.symbol = self.symbol if (self.symbol != "") else "None"
#     self.high = self.high if (self.high != "") else "None"
#     self.low = self.low if (self.low != "") else "None"
#     self.closePrice = self.closePrice if (self.closePrice != "") else "None"
#     self.volume = self.volume if (self.volume != "") else "None"
#     self.change = self.change if (self.change != "") else "None"
#     self.changePercent = self.changePercent if (self.changePercent != "") else "None"
#
#     loader = ItemLoader(item=NasdaqStockItem(),response=response)
#     loader.add_value("name",self.name)
#     loader.add_value("symbol",self.symbol)
#     loader.add_value("high",self.high)
#     loader.add_value("low",self.low)
#     loader.add_value("closePrice",self.closePrice)
#     loader.add_value("volume",self.volume)
#     loader.add_value("change",self.change)
#     loader.add_value("changePercent",self.changePercent)
#     return loader



def resetNyse(self):
    self.name = ""
    self.symbol = ""
    self.high = ""
    self.low = ""
    self.closePrice = ""
    self.volume = ""
    self.change = ""
    self.changePercent = ""

def resetNasdaq(self):
    self.name = ""
    self.symbol = ""
    self.high = ""
    self.low = ""
    self.closePrice = ""
    self.volume = ""
    self.change = ""
    self.changePercent = ""

def checkEmpty(data):
    if (data == None or len(data) == 0):
        data = "None"
        return data
    else:
        return data