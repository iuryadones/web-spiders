from scrapy.item import Item, Field

class PropertiesItem(Item):
    description = Field()
    link = Field()
    url = Field()
