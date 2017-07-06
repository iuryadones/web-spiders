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
    # start_urls = ['http://www.portaltransparencia.gov.br/']
    start_urls = ['http://www.iens.nl']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES,
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS':10
    }


    def parse(self, response):
        text_box = response.meta['driver'].find_element_by_xpath('//*[@id="searchText"]')
        text_box.send_keys("Amsterdam")

        submit_button = response.meta['driver'].find_element_by_xpath('//*[@id="button_search"]')
        submit_button.click()

        selenium_response = response.meta['driver'].page_source
        selector = Selector(text=selenium_response)

        loader = ItemLoader(item=PropertiesItem(), selector=selector)
        loader.add_xpath('description', '//*[@id="results"]/ul/li[1]/div[2]/h3/a/text()')
        loader.add_xpath('link', '//*[@id="results"]/ul/li[1]/div[2]/h3/a/@href')
        loader.add_value('url', response.meta['driver'].current_url)

        item = loader.load_item()
        yield item

        return self.render_js

    def render_js(self, response):
        response.meta['driver'].get(response.url)
        body = to_bytes(response.meta['driver'].page_source)

        return HtmlResponse(
            url=response.meta['driver'].current_url,
            body=body,
            encoding='utf-8'
        )

process = CrawlerProcess()
process.crawl(PortalTransparenciaSpider)
process.start()
