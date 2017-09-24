# -*- coding: utf-8 -*-
import scrapy


class EconoDataSpider(scrapy.Spider):
    name = 'econodata'
    #allowed_domains = ['econodata']
    start_urls = ['http://www.econodata.com.br/lista-empresas/PERNAMBUCO/PAULISTA']
    
    formdata = {
        'j_idt39':'j_idt39',
        'j_idt39:j_idt40:j_idt39':'j_idt40',
        'j_idt39:j_idt40_encodeFeature':'true',
        'j_idt39:j_idt40_first':'20',
        'j_idt39:j_idt40_pagination':'true',
        'j_idt39:j_idt40_rows':'10',
        'javax.faces.ViewState':'',
        'javax.faces.partial.ajax':'true',
        'javax.faces.partial.execute:j_idt39':'j_idt40',
        'javax.faces.partial.render:j_idt39':'j_idt40',
        'javax.faces.source:j_idt39':'j_idt40'
    }

    def parse(self, response):
        nomes = response.xpath("//div[@class='container']/div[@class='row'][3]//div/table//tr/td[1]//span[1]//text()[normalize-space()]").extract()
        endereco = response.xpath("//div[@class='container']/div[@class='row'][3]//div/table//tr/td[2]//span[1]//text()[normalize-space()]").extract()
        capital_social = response.xpath("//div[@class='container']/div[@class='row'][3]//div/table//tr/td[3]//span[1]//text()[normalize-space()]").extract()

        while nomes:
            item = {}
            item['nome'] = nomes.pop()
            item['endereco'] = endereco.pop()
            item['capital_social'] = capital_social.pop()
            yield item
