# -*- coding: utf-8 -*-

# Debug
import logging

# Pymongo - DB
import pymongo

# Spider
from scrapy import Spider
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.conf import settings

# Itens
from notebooks.items import NotebooksAvellLinks
from notebooks.items import NotebooksAvellInfos

# Constantes
from notebooks.spiders.avell.constants.consulta import XPATH_C
from notebooks.spiders.avell.constants.extracao import XPATH_E

# Utils
from notebooks.spiders.avell.utils import limpar_polos

logger = logging.getLogger('Target-Avell')

class AvellConsultar(Spider):
    name = "notebooks-avell-consultar"
    allowed_domains = ["avell.com.br"]
    start_urls = ['http://avell.com.br']
    optional_args = ['nome']

    def parse(self, response):
        """
            Entrar na URL, Pesquisar sobre notebooks e
            Enviar o resposta da pesquisa para a função obter_links.
        """

        formid = 'frm-search'
        formdata = {
            'q': self.nome
        }
        callback = self.obter_links

        yield FormRequest.from_response(
            response=response,
            formid=formid,
            formdata=formdata,
            callback=callback
        )

    def obter_links(self, response):
        """
            Obter os links dos itens pesquisados, fazer a paginação
            e Repetir o processo de obter links até não existir
            a próxima página.
        """

        links = response.xpath(XPATH_C['links']).extract()
        titles = response.xpath(XPATH_C['titles']).extract()
        actions_products = response.xpath(XPATH_C['actions_products']).extract()

        if (len(links) == len(titles) == len(actions_products)):
            links_titles_actions = list(zip(links, titles, actions_products))
            for url, title, action in links_titles_actions:
                url = url.split('#')[0]
                item = NotebooksAvellLinks()
                item['title'] = title
                item['action_product'] = action
                item['url'] = url
                yield item

        next_page = response.xpath(XPATH_C['next_page']).extract_first()
        if next_page:
            callback = self.obter_links
            yield Request(
                url=next_page,
                callback=callback
            )


class AvellExtrair(Spider):
    name = "notebooks-avell-extrair"
    allowed_domains = ["avell.com.br"]
    handle_httpstatus_list = [404, 502, 504]

    def __init__(self):
        super(AvellExtrair, self).__init__()

        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        collection = db[settings['MONGODB_COLLECTION']]
        list_urls = list(collection.distinct('url'))
        self.start_urls = list_urls

    def parse(self, response):
        """
            Falta Extrair o máximo das informações contida na URL
        """

        especification = response.xpath('//a[contains(@id,"espec")]//@href')
        link = "".join(
            [response.url.split('#')[0], especification.extract_first()]
        )
        callback = self.especifications
        yield Request(
            url=link,
            method='GET',
            callback=callback)

    def especifications(self, response):
        title = response.xpath(
            "//h1[@class='prod-title']/text()").extract_first()
        labels = response.xpath(
            "//div[@class='produtos-abas-conteudo']"
            "//div[@id='aba-especificacoes']"
            "//table//tr[*[not(contains(.,'1'))]]//td[1]//text()").extract()
        labels = limpar_polos(labels)

        especifications = []
        for i,label in enumerate(labels):
            descriptions = response.xpath(
                "//table//tr[{n}]//td[2]//text()".format(n=i+2)).extract()
            description = limpar_polos(descriptions)
            especification = {
                'label': label,
                'description': description
            }
            especifications.append(especification)

        prices = {}
        value_bol = response.xpath(
            "//div[@class='config-option']"
            "//div[@class='config-option-header grey-scale']"
            "//span[@class='boleto-price']//text()").extract_first()
        discount = response.xpath(
            "//div[@class='config-option']"
            "//div[@class='config-option-header grey-scale']"
            "//span[@class='discount']//text()").extract_first()
        prices.update({
            "boleto":{
                'valor': value_bol,
                'desconto': discount}
            }
        )

        quantity = response.xpath(
            "//div[@class='config-option']"
            "//div[@class='config-option-header grey-scale']"
            "//span[@class='installments-quantity']//text()").extract_first()
        value_cart = response.xpath(
            "//div[@class='config-option']"
            "//div[@class='config-option-header grey-scale']"
            "//strong//text()").extract_first()
        value_final = response.xpath(
            "//div[@class='config-option']"
            "//div[@class='config-option-header grey-scale']"
            "//span[@class='final-price']//text()").extract_first()
        prices.update({
            "cartao_credito":{
                'valor': value_cart,
                'quantidade': quantity,
                'valor_total': value_final}
            }
        )

        content = response.xpath(
            "//div[@id='main']/form[@id='product_addtocart_form']"
            "/div[@class='container']/div[@class='row']"
            "/div[@class='col-md-12'][4]/div[@class='wrap']"
            "/div[@id='product-options-wrapper']"
            "/div[@class='row'][3]//div[@class='col-md-8']"
            "//div[contains(@class,'box-configurar-item')]"
        )
        settings_notebook = []
        for item_conf in content:
            setting_notebook = {}
            label_notebook = item_conf.xpath('.//h2/text()').extract_first()
            items_notebook_x = item_conf.xpath('.//li')
            items_notebook = []
            for items_note in items_notebook_x:
                label_item = items_note.xpath('.//span[contains(@class, "label")]/label/text()').extract_first()
                signal_item = items_note.xpath('.//span[@class="price-notice"]/text()').extract_first()
                value_item = items_note.xpath('.//span[@class="price"]/text()').extract_first()
                items_notebook.append({
                    'label':label_item,
                    'signal': signal_item,
                    'value': value_item
                })

            setting_notebook.update({
                'label': label_notebook,
                'choice': items_notebook
            })
            settings_notebook.append(setting_notebook)


        item = NotebooksAvellInfos()
        item['title'] = title
        item['especifications'] = especifications
        item['prices'] = prices
        item['settings'] = settings_notebook
        yield item
