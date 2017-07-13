# -*- coding: utf-8 -*-

import logging

import pymongo

from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)

settings = {
    'MONGODB_SERVER': 'localhost',
    'MONGODB_PORT': 27018,
    'MONGODB_DB': 'portal_transparencia',
    'MONGODB_COLLECTION': 'dados_abertos'
}

class MunicipiosPipelineLinks(object):

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
                logger.info("Item Inválido {0}!".format(data))
        if valid:
            item = dict(item).copy()
            if item.get('municipio') in self.collection.distinct('municipio') \
                and item.get('estado') in self.collection.distinct('estado'):
                logger.info("Item Duplicado: {1} - {0}".format(
                    item['municipio'], item['estado']))
                item = dict(item).copy()
                acoes = item.pop('acoes')
                portal_trans = {
                    'estado': item.get('estado'),
                    'municipio': item.get('municipio'),
                }
                self.collection.update_one(
                    portal_trans,
                    {
                        '$addToSet': {'acoes': {'$each':acoes}},
                        '$set': item
                    },
                    upsert=True
                )
                logger.info("Municipio nao atualizado no banco de dados MongoDB!")
            elif not item.get('municipio') in self.collection.distinct('municipio') \
                or not item.get('estado') in self.collection.distinct('estado'):
                logger.info("Municipio adicionado no banco de dados MongoDB!")
                self.collection.insert_one(item)
        return item

class MunicipiosPipelineInfos(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if (item.get('estado'), item.get('municipio')) \
            in (self.collection.distinct('estado'), self.collection.distinct('municipio')):
            logger.info("Municipio atualizado o banco de dados MongoDB!")
            item = dict(item).copy()
            acoes = item.pop('acoes')
            portal_trans = {
                'estado': item.get('estado'),
                'municipio': item.get('municipio'),
            }
            self.collection.update_one(
                portal_trans,
                {
                    '$addToSet': {'acoes': {'$each':acoes}},
                    '$set': item
                },
                upsert=True
            )
        else:
            logger.info("Municipio nao atualizado no banco de dados MongoDB!")

        return item
