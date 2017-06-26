# -*- coding: utf-8 -*-

from time import sleep
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.python.org")
sleep(120)
driver.close()
