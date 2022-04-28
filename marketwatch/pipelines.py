# define your item pipelines here
# don't forget to add your pipeline to the ITEM_PIPELINES setting
# see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os,re
from sys import platform
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from .items import MarketWatchItem
from datetime import datetime

class MarketwatchPipeline:
    def __init__(self):
        self.outputMarketWatchDir = "csv_files"
        self.marketWatchList = ["name","symbol","country","exchange","sector"]

        self.marketWatchWriter = ""
        self.marketWatchFileName = ""
        self.marketWatchExporter = ""

    @classmethod
    def from_crawler(cls,crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened,signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed,signals.spider_closed)
        return pipeline

    def spider_opened(self,spider):
        # check system; change if on windows
        if (platform != "linux"):
            self.outputMarketWatchDir = "csv_files"

        today = datetime.today()
        dt = datetime(today.year,today.month,today.day)
        self.marketWatchFileName = "marketwatch_" + self.checkMonthDay(dt.month) + "_" + self.checkMonthDay(dt.day) + "_"\
            + str(dt.year) + ".csv"

        absolutePathMarketWatch = os.path.join(os.getcwd(),self.outputMarketWatchDir)

        self.marketWatchWriter = open(os.path.join(absolutePathMarketWatch,self.marketWatchFileName),'wb+')
        self.marketWatchExporter = CsvItemExporter(self.marketWatchWriter)
        self.marketWatchExporter.fields_to_export = self.marketWatchList
        self.marketWatchExporter.start_exporting()

    def spider_closed(self,spider):
        self.marketWatchExporter.finish_exporting()
        self.marketWatchWriter.close()

    def process_item(self,item,spider):
        if (isinstance(item,MarketWatchItem)):
            if (len(item) == 0):
                return item
            else:
                self.marketWatchExporter.export_item(item)
                return item

    def checkMonthDay(self,dayOrMonth):
        if (int(dayOrMonth) <= 9):
            concatStr = "0" + str(dayOrMonth)
            return concatStr
        else:
            return str(dayOrMonth)