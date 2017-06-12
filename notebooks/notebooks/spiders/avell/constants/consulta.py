# -*- coding: utf-8 -*-

XPATH_C = {
    'links': (
    '//div[contains(@class,"container")][4]'
    '//div[contains(@class,"row")]'
    '//div[contains(@class,"wrap")]'
    '//div[contains(@class,"row")]'
    '//div[contains(@class,"item")]'
    '//div[contains(@class,"actions")]'
    '//div[contains(@class,"row")]'
    '//div/a[contains(@class,"gear")]'
    '//@href'
    ),
    'titles': (
        '//div[contains(@class,"container")][4]'
        '//div[contains(@class,"row")]'
        '//div[contains(@class,"item")]'
        '//div[contains(@class,"informations")]'
        '//h2//a//text()'
    ),
    'actions_products': (
    '//div[contains(@class,"container")][4]'
    '//div[contains(@class,"row")]'
    '//div[contains(@class,"item")]'
    '//div[contains(@class,"informations")]'
    '//div[contains(@class,"short-description")]'
    '//div//text()'
    ),
    'next_page': (
        "//div[@class='pagination-bar wrap']"
        "//li[@class='next']"
        "//a[@title='Próximo']//@href"
    )
}
