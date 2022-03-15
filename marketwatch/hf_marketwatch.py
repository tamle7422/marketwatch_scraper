import re
from scrapy.loader import ItemLoader
from .items import StockItem
import logging
from datetime import datetime

def getTime():
    now = datetime.now()
    currentDate = now.strftime("%m_%d_%y")
    return currentDate

def setLocation(self,location):
    subComma = re.sub(r"[\,]",";",location)
    self.location = '-' + subComma + '-'

def setHeight(self,height):
    if (re.search(r"N/A",height) == None and re.search(r"0'0",height) == None):
        subDoubleQuote = re.sub(r"[\"]","",height)
        splitSingleQuote = subDoubleQuote.split("'")
        self.height = str((int(splitSingleQuote[0]) * 12) + int(splitSingleQuote[1]))
    else:
        self.height = "None"

def setHighLowCloseVolChg(self,data):
    try:
        self.high = checkEmpty(data[0].strip())

    except Exception as ex:
        print("exception => error setting high --- {0}".format(ex))
        self.high = "None"

    try:
        self.low = checkEmpty(data[1].strip())

    except Exception as ex:
        print("exception => error setting low --- {0}".format(ex))
        self.low = "None"

    try:
        self.closePrice = checkEmpty(data[2].strip())

    except Exception as ex:
        print("exception => error setting close --- {0}".format(ex))
        self.closePrice = "None"

    try:
        volume = checkEmpty(data[3].strip())
        if (volume != "None"):
            self.volume = volume.replace(",","")
        else:
            self.volume = "None"

    except Exception as ex:
        print("exception => error setting volume --- {0}".format(ex))
        self.volume = ""

    try:
        self.change = checkEmpty(data[4].strip())

    except Exception as ex:
        print("exception => error setting change --- {0}".format(ex))
        self.change = "None"

def setChangePercentage(self,data):
    try:
        self.changePercent = checkEmpty(data.strip())

    except Exception as ex:
        print("exception => error setting high --- {0}".format(ex))
        self.changePercent = "None"


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

def setDate(self,sel):
    try:
        monthNumber = ""
        eventDate = checkEmpty(sel.xpath(".//td/div[contains(@class,'calendar-date')]/div/text()").getall())

        if (eventDate != "None"):
            month = eventDate[0].strip()
            day = eventDate[1].strip()
            year = eventDate[2].strip()

            monthNumber = switchMonthThreeLetters(month)

            # if (monthNumber != "None" and len(day) != 0 and len(year) != 0):
            self.date = monthNumber + "/" + day + "/" + year
            # else:
            # self.date = "None"
        else:
            self.date = "None"

    except Exception as ex:
        print("exception => error setting date --- {0}".format(ex))
        self.date = "None"

def loadNyseStockItem(self,response):
    self.name = self.name if (self.name != "") else "None"
    self.symbol = self.symbol if (self.symbol != "") else "None"
    self.high = self.high if (self.high != "") else "None"
    self.low = self.low if (self.low != "") else "None"
    self.closePrice = self.closePrice if (self.closePrice != "") else "None"
    self.volume = self.volume if (self.volume != "") else "None"
    self.change = self.change if (self.change != "") else "None"
    self.changePercent = self.changePercent if (self.changePercent != "") else "None"

    loader = ItemLoader(item=NyseStockItem(),response=response)
    loader.add_value("name",self.name)
    loader.add_value("symbol",self.symbol)
    loader.add_value("high",self.high)
    loader.add_value("low",self.low)
    loader.add_value("closePrice",self.closePrice)
    loader.add_value("volume",self.volume)
    loader.add_value("change",self.change)
    loader.add_value("changePercent",self.changePercent)
    return loader

def loadNasdaqStockItem(self,response):
    self.name = self.name if (self.name != "") else "None"
    self.symbol = self.symbol if (self.symbol != "") else "None"
    self.high = self.high if (self.high != "") else "None"
    self.low = self.low if (self.low != "") else "None"
    self.closePrice = self.closePrice if (self.closePrice != "") else "None"
    self.volume = self.volume if (self.volume != "") else "None"
    self.change = self.change if (self.change != "") else "None"
    self.changePercent = self.changePercent if (self.changePercent != "") else "None"

    loader = ItemLoader(item=NasdaqStockItem(),response=response)
    loader.add_value("name",self.name)
    loader.add_value("symbol",self.symbol)
    loader.add_value("high",self.high)
    loader.add_value("low",self.low)
    loader.add_value("closePrice",self.closePrice)
    loader.add_value("volume",self.volume)
    loader.add_value("change",self.change)
    loader.add_value("changePercent",self.changePercent)
    return loader

def loadSingaporeStockItem(self,response):
    self.name = self.name if (self.name != "") else "None"
    self.symbol = self.symbol if (self.symbol != "") else "None"
    self.high = self.high if (self.high != "") else "None"
    self.low = self.low if (self.low != "") else "None"
    self.closePrice = self.closePrice if (self.closePrice != "") else "None"
    self.volume = self.volume if (self.volume != "") else "None"
    self.change = self.change if (self.change != "") else "None"
    self.changePercent = self.changePercent if (self.changePercent != "") else "None"

    loader = ItemLoader(item=SingaporeStockItem(),response=response)
    loader.add_value("name",self.name)
    loader.add_value("symbol",self.symbol)
    loader.add_value("high",self.high)
    loader.add_value("low",self.low)
    loader.add_value("closePrice",self.closePrice)
    loader.add_value("volume",self.volume)
    loader.add_value("change",self.change)
    loader.add_value("changePercent",self.changePercent)
    return loader

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

def resetSingapore(self):
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