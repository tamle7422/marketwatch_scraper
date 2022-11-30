import scrapy
import os,re,sys
import random
import logging
from selenium.webdriver.firefox.options import Options
from scrapy.utils.log import configure_logging
from ..hf_marketwatch import checkEmpty,setName,setSymbol,setCountry,setExchange,loadMarketWatchItem,resetNyse, \
    resetNasdaq,setSector,loadMarketWatchItemSelector
from scrapy_splash import SplashRequest,SplashFormRequest
from ..settings import USER_AGENT_LIST

class MarketwatchSpider(scrapy.Spider):
    name = "marketwatch"
    allowed_domains = ["marketwatch.com"]
    # start_urls =  [""]

    custom_settings = {
        "ITEM_PIPELINES": {
            "marketwatch.pipelines.MarketwatchPipeline": 196,
        },
        "CLOSESPIDER_ITEMCOUNT": 22
    }

    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='marketwatch_log.txt',format='%(levelname)s: %(message)s',level=logging.INFO, filemode="w+"
    )

    def __init__(self, *args, **kwargs):
        super(MarketwatchSpider,self).__init__(*args,**kwargs)
        self.name = ""
        self.symbol = ""
        self.country = ""
        self.exchange = ""
        self.sector = ""

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
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/0-9",
            "http://www.marketwatch.com/tools/markets/stocks/a-z/A"]
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/B",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/C",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/D",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/E",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/F",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/G",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/H",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/I",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/J",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/K",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/L",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/M",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/N",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/O",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/P",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/Q",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/R",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/S",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/T",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/U",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/V",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/W",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/X",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/Y",
            # "http://www.marketwatch.com/tools/markets/stocks/a-z/Z",

        for url in urls:
            # yield SplashRequest(url=url,callback=self.parse,endpoint="execute",args={"lua_source": self.script}, \
            #     cache_args=['lua_source'],session_id="session1",headers={"User-Agent": random.choice(USER_AGENT_LIST)})
            yield scrapy.Request(url=url,callback=self.start,headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    # from list of urls, get pagination links associated with it
    def start(self,response):
        try:
            indexes = checkEmpty(response.xpath(".//div[contains(@id,'marketsindex')]/ul[@class='pagination']/li/a/text()").getall())

            lastIndex = indexes[-2:-1]
            if (re.search(r"[\-]",str(lastIndex)) != None):
                lastIndex = str(lastIndex).split("-")[1]
                lastIndex = re.sub(r"[\'\(\)\]]","",lastIndex)
            else:
                lastIndex = "".join(lastIndex)

            # create pagination links
            for i in range(1,int(lastIndex)):
                url = response.url + "/" + str(i)
                yield scrapy.Request(url=url,callback=self.constructUrl, \
                    headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception --- error in start method => {0}".format(ex))

    def constructUrl(self,response):
        try:
            paginationLinks = checkEmpty(response.xpath(".//div[contains(@id,'marketsindex')]/ul[@class='pagination']/li[not(@class)]/a/@href").getall())
            linksSet = set(paginationLinks)

            trSelectors = checkEmpty(response.xpath(".//table[contains(@class,'table-condensed')]/tbody/tr"))
            for sel in trSelectors:
                loader = self.processFirstPage(response,sel)
                yield loader.load_item()

            if (linksSet != None):
                for i in linksSet:
                    url = "https://www.marketwatch.com" + i
                    url1 = response.urljoin(i)

                    if (len(i) != 0):
                        # yield response.follow(url=url1,callback=self.extractData1)
                        yield scrapy.Request(url=url,callback=self.extractData1, \
                            headers={"User-Agent": random.choice(USER_AGENT_LIST)})

        except Exception as ex:
            print("exception --- error in construct url => {0}".format(ex))

    def processFirstPage(self,response,sel):
        name = checkEmpty(sel.xpath(".//td[@class='name']/a/text()").get())
        if (name != "None"):
            self.name = name
        else:
            self.name = "None"

        symbol = checkEmpty(sel.xpath(".//td[@class='name']/a/small/text()").extract())
        setSymbol(self,symbol)

        country = checkEmpty(sel.xpath(".//td[2]/text()").get())
        setCountry(self, country)

        exchange = checkEmpty(sel.xpath(".//td[3]/text()").get())
        setExchange(self, exchange)

        sector = checkEmpty(sel.xpath(".//td[4]/text()").get())
        setSector(self, sector)

        loader = loadMarketWatchItemSelector(self,response,sel)
        return loader

    def extractData1(self,response):
        try:
            trSelectors = checkEmpty(response.xpath(".//table[contains(@class,'table-condensed')]/tbody/tr"))

            for sel in trSelectors:
                name = checkEmpty(sel.xpath(".//td[@class='name']/a/text()").get())
                if (name != "None"):
                    self.name = name
                else:
                    self.name = "None"

                symbol = checkEmpty(sel.xpath(".//td[@class='name']/a/small/text()").extract())
                setSymbol(self, symbol)

                country = checkEmpty(sel.xpath(".//td[2]/text()").get())
                setCountry(self, country)

                exchange = checkEmpty(sel.xpath(".//td[3]/text()").get())
                setExchange(self, exchange)

                sector = checkEmpty(sel.xpath(".//td[4]/text()").get())
                setSector(self, sector)

                loader = loadMarketWatchItemSelector(self,response,sel)
                yield loader.load_item()

        except Exception as ex:
            print("exception --- error in extract data1 => {0}".format(ex))