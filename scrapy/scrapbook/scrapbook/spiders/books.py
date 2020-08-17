# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']/article/div/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"))
    )

    def parse_item(self, response):
        yield {
                'title': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
                'price':response.xpath("(//div[@class='col-sm-6 product_main']/p)[1]/text()").get(),
                'availability':response.xpath("normalize-space((//div[@class='col-sm-6 product_main']/p)[2])").get(),
                'url':response.url,
                'description':response.xpath("(//p)[4]/text()") .get()                               
#                'upc':response.xpath("//table/tbody/tr/td[1]/text()").get(),
#                'type':response.xpath("//table/tbody/tr/td[2]/text()").get(),
#                'price_tax':response.xpath("//table/tbody/tr/td[3]/text()").get(),
#                'price_wtax':response.xpath("//table/tbody/tr/td[4]/text()").get(),
#                'tax':response.xpath("//table/tbody/tr/td[5]/text()").get(),
#                'availability':response.xpath("//table/tbody/tr/td[6]/text()").get(),
#                'n_reviews':response.xpath("//table/tbody/tr/td[7]/text()").get()
#                'user-agent':response.request.headers['User-Agent']
                }
        
#        for row in response.xpath("//table/tbody/tr"):
#            yield {
#                    row.xpath(".//td/text()"):row.xpath(".//th/text()")
#                    }

            