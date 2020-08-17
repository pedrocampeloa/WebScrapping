# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestmoviesSpider(CrawlSpider):
    name = 'bestmovies'
    allowed_domains = ['imdb.com']
#    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    start_urls = ['https://www.imdb.com/list/ls006266261']
    
#    user_agente = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'

#    def start_request(self):
#        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating',
#                             headers = {'User-Agent': self.user_agente
#                                        })
        
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='flat-button lister-page-next next-page']"))
    )

#    def set_user_agent(self,request):
#        request.headers['User-Agent'] = self.user_agente
#        return request

    def parse_item(self, response):
        yield {
                'title': response.xpath("//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/h1/text()[1]").get(),
                'url':response.url,
                'original_title':response.xpath("//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/div[@class='originalTitle']/text()").get(),
                'year':response.xpath("//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/h1/span/a/text()").get(),
                'duration':response.xpath("normalize-space(//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/div[@class='subtext']/time/text())").get(),
                'type':response.xpath("//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/div[@class='subtext']/a[1]/text()").get(),
                'classification':response.xpath("normalize-space((//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/div[@class='subtext']/text())[1])").get(),
                'launch':response.xpath("//div[@class='title_bar_wrapper']/div[@class='titleBar']/div/div[@class='subtext']/a[2]/text()").get(),
                'rating':response.xpath("//div[@class='title_bar_wrapper']/div[@class='ratings_wrapper']/div/div/strong/@title").get(),
                'raters':response.xpath("//div[@class='title_bar_wrapper']/div[@class='ratings_wrapper']/div/a/span/text()").get(),
                'description':response.xpath("normalize-space(//div[@class='plot_summary ']/div[1]/text())").get(),
                'directors':response.xpath("//div[@class='plot_summary ']/div[2]/a/text()").get(),
                'writers':response.xpath("//div[@class='plot_summary ']/div[3]/a/text()").get(),
                'stars':response.xpath("//div[@class='plot_summary ']/div[4]/a/text()").get()
#                'user-agent':response.request.headers['User-Agent']
                }
        
