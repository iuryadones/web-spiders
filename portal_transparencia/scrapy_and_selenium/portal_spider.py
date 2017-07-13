#-*- coding: utf-8 -*-

import os

from scrapy import Spider
from scrapy import Selector
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from constants import URL, XPATH
from properties import TransparenteItem

def _limpar(listagem):
    lista = []
    for l in listagem:
        l = l.strip().replace('\n','')
        if l:
            lista.append(l)
    return lista

settings = get_project_settings()

DOWNLOADER_MIDDLEWARES = settings.get('DOWNLOADER_MIDDLEWARES').copy()
DOWNLOADER_MIDDLEWARES.update({
    'middleware_hydra.SeleniumMiddleware': 200
})

class PortalTransparenciaSpider(Spider):
    name = "portal-transparencia"
    allowed_domains = ["portaltransparencia.gov.br"]
    domain = 'http://www.portaltransparencia.gov.br/'
    start_urls = [URL['recursos'](2017)]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': DOWNLOADER_MIDDLEWARES,
        'CONCURRENT_REQUESTS': 200,
        'DOWNLOAD_DELAY': 0,
    }

    def parse(self, response):
        estados = _limpar(response.xpath(XPATH['estado_text']).extract())
        links = _limpar(response.xpath(XPATH['estado_link']).extract())

        requests = []
        if len(estados) == len(links):
            for i, estado in enumerate(estados):
                # loader = ItemLoader(item=TransparenteItem(), response=response)
                # loader.add_value('estado', estado)
                # loader.add_value('url', self.domain+links[i])
                # item = loader.load_item()
                # yield item

                requests.append(
                    Request(
                        url=self.domain+links[i],
                        method='GET',
                        callback=self.consultar_municipios,
                        meta={'estado': estado}
                    )
                )

            for request in requests:
                yield request

        else:
            print("\n\n Error url: {}\n\n".format(response.url))

        paginacao = response.xpath(XPATH['paginacao']).extract_first()
        if paginacao:
            fim_page = int(paginacao.split('/')[1])
            limit_page = '&Pagina={}'.format(fim_page)
            if not limit_page in response.url:
                for j in range(fim_page+1):
                    if j > 1:
                        if not '&Pagina=' in response.url:
                            next_page = response.url+'&Pagina={}'.format(j)
                        else:
                            next_page = response.url.split('&Pagina=')[0]
                            next_page = next_page + '&Pagina={}'.format(j)
                        yield response.follow(next_page, self.parse)

    def consultar_municipios(self, response):
        meta = response.meta.copy()
        municipios = _limpar(response.xpath(XPATH['municipio_text']).extract())
        links = _limpar(response.xpath(XPATH['municipio_link']).extract())

        requests = []
        if len(municipios) == len(links):
            for i, municipio in enumerate(municipios):
                # loader = ItemLoader(item=TransparenteItem(), response=response)
                # loader.add_value('municipio', municipio)
                # loader.add_value('url', self.domain+links[i])
                # item = loader.load_item()
                # yield item

                meta['municipio'] = municipio
                requests.append(
                    Request(
                        url=self.domain+links[i],
                        method='GET',
                        callback=self.extrair_municipio,
                        meta=meta
                    )
                )

            for request in requests:
                yield request

        else:
            print("\n\n Error url: {}\n\n".format(response.url))

        paginacao = response.xpath(XPATH['paginacao']).extract_first()
        if paginacao:
            fim_page = int(paginacao.split('/')[1])
            limit_page = '&Pagina={}'.format(fim_page)
            if not limit_page in response.url:
                for j in range(fim_page+1):
                    if j > 1:
                        if not '&Pagina=' in response.url:
                            next_page = response.url+'&Pagina={}'.format(j)
                        else:
                            next_page = response.url.split('&Pagina=')[0]
                            next_page = next_page + '&Pagina={}'.format(j)

                        yield response.follow(
                            next_page, self.consultar_municipios, meta=meta
                        )

    def extrair_municipio(self, response):
        meta = response.meta.copy()
        funcoes = _limpar(response.xpath(XPATH['funcao']).extract())
        acoes_governamentais = _limpar(
            response.xpath(XPATH['acao_governamental']).extract())
        # linguagens_cidadaos = response.xpath(XPATH['linguagem_cidada']).extract()
        totais_no_ano = _limpar(response.xpath(XPATH['total_no_ano']).extract())

        if len(funcoes) == len(acoes_governamentais):
            loader = ItemLoader(item=TransparenteItem(), response=response)
            item = loader.load_item()
            item['estado'] = meta.get('estado','')
            item['municipio'] = meta.get('municipio','')
            acoes = []
            for i in range(len(funcoes)):
                acoes.append(
                    {
                        'funcoes': funcoes[i],
                        'acao_governamental': acoes_governamentais[i],
                        'total_no_ano': float(
                            totais_no_ano[i].replace('.','').replace(',','.'))
                    }
                )
            item['acoes'] = acoes
            yield item

        else:
            print("\n\n Error url: {}\n\n".format(response.url))

        paginacao = response.xpath(XPATH['paginacao']).extract_first()
        if paginacao:
            fim_page = int(paginacao.split('/')[1])
            limit_page = '&Pagina={}'.format(fim_page)
            if not limit_page in response.url:
                for j in range(fim_page+1):
                    if j > 1:
                        if not '&Pagina=' in response.url:
                            next_page = response.url+'&Pagina={}'.format(j)
                        else:
                            next_page = response.url.split('&Pagina=')[0]
                            next_page = next_page + '&Pagina={}'.format(j)
                        yield response.follow(
                            next_page, self.extrair_municipio, meta=meta
                        )

process = CrawlerProcess()
process.crawl(PortalTransparenciaSpider)
process.start()
