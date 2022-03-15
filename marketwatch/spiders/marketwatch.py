import scrapy
import os,re,sys
import random
import logging
from selenium.webdriver.firefox.options import Options
from scrapy.utils.log import configure_logging
from ..hf_marketwatch import checkEmpty,setHighLowCloseVolChg,setChangePercentage,loadNyseStockItem,resetNyse,loadNasdaqStockItem, \
    resetNasdaq,loadSingaporeStockItem,resetSingapore
from scrapy_splash import SplashRequest,SplashFormRequest
from ..settings import USER_AGENT_LIST

class MarketwatchSpider(scrapy.Spider):
    name = "marketwatch"
    # allowed_domains = ["eoddata.com"]
    # start_urls =  [""]

    custom_settings = {
        "ITEM_PIPELINES": {
            "marketwatch.pipelines.MarketwatchPipeline": 196,
        },
        "CLOSESPIDER_ITEMCOUNT": 20
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO, filemode="w+"
    # )

    def __init__(self, *args, **kwargs):
        super(MarketwatchSpider,self).__init__(*args,**kwargs)
        self.name = ""
        self.symbol = ""
        self.high = ""
        self.low = ""
        # cannot use self.close
        self.closePrice = ""
        self.volume = ""
        self.change = ""
        self.changePercent = ""

        # self.url = ""
        self.parseScript = """
                              function main(splash)
                                  splash:init_cookies(splash.args.cookies)
                                  assert(splash:go(splash.args.url))
                                  splash:set_viewport_full()
                                  assert(splash:wait(0.65))

                                  return {
                                      cookies = splash:get_cookies(),
                                      html = splash:html()
                                 }
                             end
                          """

        self.script = """
                         function main(splash,args)
                             local cookies = splash:get_cookies()
                             splash:init_cookies(cookies)
                             assert(splash:go(splash.args.url))
                             assert(splash:wait(1.5))

                             return {
                                 cookies,
                                 html = splash:html(),
                                 -- png = splash:png(),
                                 -- har = splash:har()
                             }
                         end
                     """

    def start_requests(self):
        urls = [
            "http://www.marketwatch.com/tools/markets/stocks/a-z/0-9", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/B", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/C", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/D", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/E", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/F", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/G", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/H", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/I", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/J", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/K", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/L", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/M", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/N", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/O", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/P", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/Q", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/R", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/S", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/T", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/U", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/V", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/W", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/X", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/Y", \
            "http://www.marketwatch.com/tools/markets/stocks/a-z/Z"]

        for url in urls:
            # yield SplashRequest(url=url,callback=self.parse,endpoint="execute", args={"lua_source": self.script}, \
            #     cache_args=['lua_source'],session_id="session1",headers={"User-Agent": random.choice(USER_AGENT_LIST)})
            yield scrapy.Request(url=url,callback=self.parseUrl,headers={"User-Agent": random.choice(USER_AGENT_LIST)})


    def parseUrl(self,response):
        try:
            splitIndex = ""
            indexes = checkEmpty(response.xpath(".//div[contains(@id,'marketsindex')]/ul[@class='pagination']/li/a/text()").getall())

            lastIndex = indexes[-2]
            if (re.search(r"[\-]",lastIndex) != None):
                lastIndex = lastIndex.split("-")[1]

            # create pagination links
            for i in range(1,int(lastIndex)):
                url = response.url + "/" + str(i)
                yield scrapy.Request(url=url,callback=self.parse, \
                    headers={"User-Agent": random.choice(USER_AGENT_LIST)})



        except Exception as ex:
            print("exception => error occurred in parse url method --- {0}".format(ex))

    def parse(self,response):
        try:
            print("")

            # self.driver.execute_script("arguments[0].click();",yesterdayButton)
            # page = response.url.split("/")[-2]
            # splitNyse = response.url.split("NYSE/")
            # splitPeriod = splitNyse[1].split(".")[0]
            #
            # trTags = response.xpath("//table[@class='quotes']/tbody/tr[contains(@class,'ro')]")
            #
            # for sel in trTags:
            #     resetNyse(self)
            #     name = checkEmpty(sel.xpath(".//td[not(@align)]/text()").get())
            #     if (name != "None"):
            #         self.name = name
            #     else:
            #         self.name = "None"
            #
            #     symbol = checkEmpty(sel.xpath(".//td[not(@align)]/a/text()").get())
            #     if (symbol != "None"):
            #         self.symbol = symbol
            #     else:
            #         self.symbol = "None"
            #
            #     tdAlignRight = sel.xpath(".//td[@align='right']/text()").getall()
            #     setHighLowCloseVolChg(self,tdAlignRight)
            #
            #     tdAlignLeft = sel.xpath(".//td[@align='left']/text()").get()
            #     setChangePercentage(self,tdAlignLeft)
            #
            #     loader = loadNyseStockItem(self,response)
            #     yield loader.load_item()

        except Exception as ex:
            print("exception => error occurred in parse method --- {0}".format(ex))