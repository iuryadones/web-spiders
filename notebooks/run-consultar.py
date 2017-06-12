# -*- coding: utf-8 -*-

import os

nome = 'notebooks'

os.system('scrapy crawl notebooks-avell-consultar -a nome="{nome}"'.format(nome=nome))
