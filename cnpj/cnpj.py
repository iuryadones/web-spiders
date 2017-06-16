# -*- coding: utf-8 -*-

import scrapy
import logging

logger = logging.getLogger('CNPJ')

class CNPJSpider(scrapy.Spider):
    name = 'cnpj-spider'
    searchs = ['votorantim','votorantim cimentos']
    DB = []
    def start_requests(self):
        url = 'http://cnpj.info/'
        self.start_urls = []
        for search in self.searchs: 
            if ' ' in search:
                self.start_urls.append(url+'-'.join((search.upper()).split(' ')))
            else:
                self.start_urls.append(url+search.upper())

        return super(CNPJSpider, self).start_requests()
    
    def parse(self, response):
        titles = response.xpath("//div[@id='content']//li").extract()
        for title in titles:
            self.DB.append(title)
            yield {'title': title}
            
        next_pages = response.xpath(
                "/html/body/div[@id='content']/a[not(contains(.,'suplementar'))]"
        )
        
        logger.info(len(self.DB))

        for next_page in next_pages:
            yield response.follow(next_page, self.parse)
