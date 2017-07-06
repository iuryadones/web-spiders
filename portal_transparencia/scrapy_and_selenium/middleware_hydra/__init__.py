#-*- coding: utf-8 -*-

import logging

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from selenium import webdriver

logger = logging.getLogger('MIDDLEWARE_HYDRA')

class SeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        request.meta['driver'] = self.driver
        self.driver.get(request.url)
        body = to_bytes(self.driver.page_source)

        return HtmlResponse(
            url=self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_opened(self, spider):
        logger.info('OPEN webdriver')
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)

    def spider_closed(self, spider):
        logger.info('CLOSE webdriver')
        self.driver.close()
