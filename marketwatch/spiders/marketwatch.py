import scrapy
import os,re,sys
import random
import logging
from scrapy.utils.log import configure_logging
from ..hf_marketwatch import checkEmpty,setHighLowCloseVolChg,setChangePercentage,loadNyseStockItem,resetNyse,loadNasdaqStockItem, \
    resetNasdaq,loadSingaporeStockItem,resetSingapore
from scrapy_splash import SplashRequest,SplashFormRequest
from ..settings import USER_AGENT_LIST

class EoddataNyseSpider(scrapy.Spider):
    name = "eoddata_nyse"
    # allowed_domains = ["eoddata.com"]
    # start_urls =  [""]

    custom_settings = {
        "ITEM_PIPELINES": {
            'eoddata.pipelines.EoddataNysePipeline': 198,
        },
        "CLOSESPIDER_ITEMCOUNT": 10001
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO, filemode="w+"
    # )

    def __init__(self, *args, **kwargs):
        super(EoddataNyseSpider,self).__init__(*args,**kwargs)
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
            "http://www.eoddata.com/stocklist/NYSE/A.htm", \
            "http://www.eoddata.com/stocklist/NYSE/B.htm", \
            "http://www.eoddata.com/stocklist/NYSE/C.htm", \
            "http://www.eoddata.com/stocklist/NYSE/D.htm", \
            "http://www.eoddata.com/stocklist/NYSE/E.htm", \
            "http://www.eoddata.com/stocklist/NYSE/F.htm", \
            "http://www.eoddata.com/stocklist/NYSE/G.htm", \
            "http://www.eoddata.com/stocklist/NYSE/H.htm", \
            "http://www.eoddata.com/stocklist/NYSE/I.htm", \
            "http://www.eoddata.com/stocklist/NYSE/J.htm", \
            "http://www.eoddata.com/stocklist/NYSE/K.htm", \
            "http://www.eoddata.com/stocklist/NYSE/L.htm", \
            "http://www.eoddata.com/stocklist/NYSE/M.htm", \
            "http://www.eoddata.com/stocklist/NYSE/N.htm", \
            "http://www.eoddata.com/stocklist/NYSE/O.htm", \
            "http://www.eoddata.com/stocklist/NYSE/P.htm", \
            "http://www.eoddata.com/stocklist/NYSE/Q.htm", \
            "http://www.eoddata.com/stocklist/NYSE/R.htm", \
            "http://www.eoddata.com/stocklist/NYSE/S.htm", \
            "http://www.eoddata.com/stocklist/NYSE/T.htm", \
            "http://www.eoddata.com/stocklist/NYSE/U.htm", \
            "http://www.eoddata.com/stocklist/NYSE/V.htm", \
            "http://www.eoddata.com/stocklist/NYSE/W.htm", \
            "http://www.eoddata.com/stocklist/NYSE/X.htm", \
            "http://www.eoddata.com/stocklist/NYSE/Y.htm", \
            "http://www.eoddata.com/stocklist/NYSE/Z.htm"]

        for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(url=url,callback=self.parse,endpoint="execute", args={"lua_source": self.script}, \
                cache_args=['lua_source'],session_id="session1",headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    def parse(self,response):
        try:
            page = response.url.split("/")[-2]
            splitNyse = response.url.split("NYSE/")
            splitPeriod = splitNyse[1].split(".")[0]

            trTags = response.xpath("//table[@class='quotes']/tbody/tr[contains(@class,'ro')]")

            for sel in trTags:
                resetNyse(self)
                name = checkEmpty(sel.xpath(".//td[not(@align)]/text()").get())
                if (name != "None"):
                    self.name = name
                else:
                    self.name = "None"

                symbol = checkEmpty(sel.xpath(".//td[not(@align)]/a/text()").get())
                if (symbol != "None"):
                    self.symbol = symbol
                else:
                    self.symbol = "None"

                tdAlignRight = sel.xpath(".//td[@align='right']/text()").getall()
                setHighLowCloseVolChg(self,tdAlignRight)

                tdAlignLeft = sel.xpath(".//td[@align='left']/text()").get()
                setChangePercentage(self,tdAlignLeft)

                loader = loadNyseStockItem(self,response)
                yield loader.load_item()

        except Exception as ex:
            print("exception => error occurred in parse method --- {0}".format(ex))

class EoddataNasdaqSpider(scrapy.Spider):
    name = "eoddata_nasdaq"
    # allowed_domains = ["eoddata.com"]
    # start_urls =  [""]

    custom_settings = {
        "ITEM_PIPELINES": {
            'eoddata.pipelines.EoddataNasdaqPipeline': 198,
        },
        "CLOSESPIDER_ITEMCOUNT": 9999
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO, filemode="w+"
    # )

    def __init__(self,*args,**kwargs):
        super(EoddataNasdaqSpider,self).__init__(*args,**kwargs)
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
            "http://www.eoddata.com/stocklist/NASDAQ/A.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/B.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/C.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/D.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/E.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/F.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/G.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/H.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/I.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/J.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/K.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/L.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/M.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/N.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/O.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/P.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/Q.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/R.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/S.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/T.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/U.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/V.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/W.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/X.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/Y.htm", \
            "http://www.eoddata.com/stocklist/NASDAQ/Z.htm"]

        for url in urls:
            # yield scrapy.Request(url=url,callback=self.parse)
            yield SplashRequest(url=url,callback=self.parse,endpoint="execute", args={"lua_source": self.script}, \
                cache_args=['lua_source'],session_id="session1",headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    def parse(self,response):
        try:
            page = response.url.split("/")[-2]
            splitNasdaq = response.url.split("NASDAQ/")
            splitPeriod = splitNasdaq[1].split(".")[0]

            trTags = response.xpath("//table[@class='quotes']/tbody/tr[contains(@class,'ro')]")

            for sel in trTags:
                resetNasdaq(self)
                name = checkEmpty(sel.xpath(".//td[not(@align)]/text()").get())
                if (name != "None"):
                    self.name = name
                else:
                    self.name = "None"

                symbol = checkEmpty(sel.xpath(".//td[not(@align)]/a/text()").get())
                if (symbol != "None"):
                    self.symbol = symbol
                else:
                    self.symbol = "None"

                tdAlignRight = sel.xpath(".//td[@align='right']/text()").getall()
                setHighLowCloseVolChg(self,tdAlignRight)

                tdAlignLeft = sel.xpath(".//td[@align='left']/text()").get()
                setChangePercentage(self,tdAlignLeft)

                loader = loadNasdaqStockItem(self,response)
                yield loader.load_item()

        except Exception as ex:
            print("exception => error occurred in parse method --- {0}".format(ex))

# singapore exchange
class EoddataSingaporeSpider(scrapy.Spider):
    name = "eoddata_singapore"
    # allowed_domains = ["eoddata.com"]
    # start_urls =  [""]

    custom_settings = {
        "ITEM_PIPELINES": {
            'eoddata.pipelines.EoddataSingaporePipeline': 198,
        },
        "CLOSESPIDER_ITEMCOUNT": 10555
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO, filemode="w+"
    # )

    def __init__(self,*args,**kwargs):
        super(EoddataSingaporeSpider,self).__init__(*args,**kwargs)
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
            "http://www.eoddata.com/stocklist/SGX/1.htm", \
            "http://www.eoddata.com/stocklist/SGX/2.htm", \
            "http://www.eoddata.com/stocklist/SGX/3.htm", \
            "http://www.eoddata.com/stocklist/SGX/4.htm", \
            "http://www.eoddata.com/stocklist/SGX/5.htm", \
            "http://www.eoddata.com/stocklist/SGX/6.htm", \
            "http://www.eoddata.com/stocklist/SGX/7.htm", \
            "http://www.eoddata.com/stocklist/SGX/8.htm", \
            "http://www.eoddata.com/stocklist/SGX/9.htm", \
            "http://www.eoddata.com/stocklist/SGX/A.htm", \
            "http://www.eoddata.com/stocklist/SGX/B.htm", \
            "http://www.eoddata.com/stocklist/SGX/C.htm", \
            "http://www.eoddata.com/stocklist/SGX/D.htm", \
            "http://www.eoddata.com/stocklist/SGX/E.htm", \
            "http://www.eoddata.com/stocklist/SGX/F.htm", \
            "http://www.eoddata.com/stocklist/SGX/G.htm", \
            "http://www.eoddata.com/stocklist/SGX/H.htm", \
            "http://www.eoddata.com/stocklist/SGX/I.htm", \
            "http://www.eoddata.com/stocklist/SGX/J.htm", \
            "http://www.eoddata.com/stocklist/SGX/K.htm", \
            "http://www.eoddata.com/stocklist/SGX/L.htm", \
            "http://www.eoddata.com/stocklist/SGX/M.htm", \
            "http://www.eoddata.com/stocklist/SGX/N.htm", \
            "http://www.eoddata.com/stocklist/SGX/O.htm", \
            "http://www.eoddata.com/stocklist/SGX/P.htm", \
            "http://www.eoddata.com/stocklist/SGX/Q.htm", \
            "http://www.eoddata.com/stocklist/SGX/R.htm", \
            "http://www.eoddata.com/stocklist/SGX/S.htm", \
            "http://www.eoddata.com/stocklist/SGX/T.htm", \
            "http://www.eoddata.com/stocklist/SGX/U.htm", \
            "http://www.eoddata.com/stocklist/SGX/V.htm", \
            "http://www.eoddata.com/stocklist/SGX/W.htm", \
            "http://www.eoddata.com/stocklist/SGX/X.htm", \
            "http://www.eoddata.com/stocklist/SGX/Y.htm", \
            "http://www.eoddata.com/stocklist/SGX/Z.htm"]

        for url in urls:
            # yield scrapy.Request(url=url,callback=self.parse)
            yield SplashRequest(url=url,callback=self.parse,endpoint="execute", args={"lua_source": self.script}, \
                cache_args=['lua_source'],session_id="session1",headers={"User-Agent": random.choice(USER_AGENT_LIST)})

    def parse(self,response):
        try:
            page = response.url.split("/")[-2]
            splitSingapore = response.url.split("SGX/")
            splitPeriod = splitSingapore[1].split(".")[0]

            trTags = response.xpath("//table[@class='quotes']/tbody/tr[contains(@class,'ro')]")

            for sel in trTags:
                resetSingapore(self)
                name = checkEmpty(sel.xpath(".//td[not(@align)]/text()").get())
                if (name != "None"):
                    self.name = name
                else:
                    self.name = "None"

                symbol = checkEmpty(sel.xpath(".//td[not(@align)]/a/text()").get())
                if (symbol != "None"):
                    self.symbol = symbol
                else:
                    self.symbol = "None"

                tdAlignRight = sel.xpath(".//td[@align='right']/text()").getall()
                setHighLowCloseVolChg(self,tdAlignRight)

                tdAlignLeft = sel.xpath(".//td[@align='left']/text()").get()
                setChangePercentage(self,tdAlignLeft)

                loader = loadSingaporeStockItem(self,response)
                yield loader.load_item()

        except Exception as ex:
            print("exception => error occurred in parse method --- {0}".format(ex))
