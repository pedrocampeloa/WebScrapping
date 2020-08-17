#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 17:26:19 2020

@author: pedrocampelo
"""

# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import json


class QuotesSpider(scrapy.Spider):
    name = 'ebooks'
    
    
    incremented_by = 12
    offset=0
    
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org.subjects/picture_books.json?limit=12']

    def parse(self, response):
        
        if response.status == 500:
            raise CloseSpider("Ultima pagina")
            
        resp = json.loads(response.body)
        ebooks = resp.get('works')
        for ebooks in ebooks:
            yield{
                  'title':ebooks.get('title'),
                  'subject':ebooks.get('subject')
                    }
        self.offset += self.incremented_by
        yield scrapy.Request(
                url = f"http://openlibrary.org.subjects/picture_books.json?limit=12&offset={self.offset}",
                callback=self.parse
                )
                    