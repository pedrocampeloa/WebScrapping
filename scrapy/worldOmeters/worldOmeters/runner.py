#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 16:19:08 2020

@author: pedrocampelo
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from worldometers.spiders.countries import CountriesSpider



process=CrawlerProcess(settings=get_project_settings)
process.crawl(CountriesSpider)
process.start()