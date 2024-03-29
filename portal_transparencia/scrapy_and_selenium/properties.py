from scrapy.item import Item, Field

class PropertiesItem(Item):
    description = Field()
    link = Field()
    url = Field()

class TransparenteItem(Item):
    ano = Field()
    tipo = Field()
    estado = Field()
    municipio = Field()
    acoes = Field()
    url = Field()
