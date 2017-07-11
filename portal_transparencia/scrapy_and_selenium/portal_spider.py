#-*- coding: utf-8 -*-

import os

from scrapy import Spider
from scrapy import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from properties import PropertiesItem

settings = get_project_settings()

DOWNLOADER_MIDDLEWARES = settings.get('DOWNLOADER_MIDDLEWARES').copy()
DOWNLOADER_MIDDLEWARES.update({
    'middleware_hydra.SeleniumMiddleware': 200
})

class PortalTransparenciaSpider(Spider):
    name = "portal-transparencia"
    allowed_domains = ["web"]
    start_urls = ['http://www.portaltransparencia.gov.br/']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES,
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS':1
    }


    def parse(self, response):
        import ipdb; ipdb.set_trace()    
        selenium_response = response.meta['driver'].page_source
        selector = Selector(text=selenium_response)

        loader = ItemLoader(item=PropertiesItem(), selector=selector)
        loader.add_value('url', response.meta['driver'].current_url)

        item = loader.load_item()
        yield item

        return self.render_js

process = CrawlerProcess()
process.crawl(PortalTransparenciaSpider)
process.start()
