#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 00:08:04 2020

@author: pedrocampelo
"""

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en']
    
    def __init__(self):
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")         #to no open chrome
        
        #chrome_path = which("chromedriver")
        driver = webdriver.Chrome(executable_path="/Users/pedrocampelo/Projects/selenium/chromedriver", options = chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.livecoin.net/en")
        
#        usd_tab = driver.find_element_by_class_name("filterPanelItem___2z5Gb")
#        usd_tab[2].click()
        
        usd_tab = driver.find_element_by_xpath("//div[@class='filterPanelItem___2z5Gb '][3]").click()
        
        self.html = driver.page_source
        driver.close() 

    def parse(self, response):
        
        resp = Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume': currency.xpath(".//div[2]/span/text()").get(),
                'last_price': currency.xpath(".//div[3]/span/text()").get(),
                'variation': currency.xpath(".//div[4]/span/span/text()").get(),
                'high': currency.xpath(".//div[5]/span/text()").get(),
                'low': currency.xpath(".//div[6]/span/text()").get()
                    }
