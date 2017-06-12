# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem

import logging
logger = logging.getLogger(__name__)

class NotebooksPipelineLinks(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Item Inválido {0}!".format(data))
        if valid:
            if item.get('title') in self.collection.distinct('title') \
                and item.get('especifications','') in self.collection.distinct('especifications'):
                raise DropItem("Item Duplicado {0}".format(item['title']))
            elif item.get('especifications','') in self.collection.distinct('especifications'):
                logger.info("Notebook adicionado no banco de dados MongoDB!")
                self.collection.insert(dict(item))
            elif not item.get('title') in self.collection.distinct('title'):
                logger.info("Notebook adicionado no banco de dados MongoDB!")
                self.collection.insert(dict(item))
        return item

class NotebooksPipelineInfos(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item.get('title') in self.collection.distinct('title'):
            if item.get('especifications',''):
                notebook = {'title': item.pop('title')}
                logger.info("Notebook atualizado o banco de dados MongoDB!")
                self.collection.update_one(notebook, {'$set': item})
            else:
                logger.info("Notebook adicionado no banco de dados MongoDB!")
        return item
