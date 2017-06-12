# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NotebooksAvellLinks(scrapy.Item):
    title = scrapy.Field()
    action_product = scrapy.Field()
    url = scrapy.Field()

class NotebooksAvellInfos(scrapy.Item):
    title = scrapy.Field()
    especifications = scrapy.Field()
    prices = scrapy.Field()
    settings = scrapy.Field()
