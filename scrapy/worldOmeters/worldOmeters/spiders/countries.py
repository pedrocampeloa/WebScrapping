# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            
            #absolute_url = f"https://www.worldometers.info{link}"
            #absolute_url = response.urljoin(link)
            
            #yield scrapy.Request(url=absolute_url)
            yield response.follow(url=link, callback = self.parse_country, meta = {'country_name':name})
            
    def parse_country(self, response):
    
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])/tbody/tr")
        for row in rows:
            
            year = row.xpath(".//td[1]/text()").get()
            population= row.xpath(".//td[2]/strong/text()").get()
            year_cg_pc = row.xpath(".//td[3]/text()").get()
            year_cg_abs = row.xpath(".//td[4]/text()").get()
            mingrants = row.xpath(".//td[5]/text()").get()
            age_median = row.xpath(".//td[6]/text()").get()
            fert_rate = row.xpath(".//td[7]/text()").get()
            density = row.xpath(".//td[8]/text()").get()
            urban_pop_pc = row.xpath(".//td[9]/text()").get()
            urban_pop_abs = row.xpath(".//td[10]/text()").get()
            pop_world_ratio = row.xpath(".//td[11]/text()").get()
            world_pop  = row.xpath(".//td[12]/text()").get()
            country_global_ranking  = row.xpath(".//td[13]/text()").get()
            
            yield {
                    'name': name,
                    'year': year,
                    'population': population,
                    'year change (%)':year_cg_pc,
                    'year change':year_cg_abs,
                    'mingrants':mingrants,
                    'median age':age_median,
                    'fertility rate':fert_rate,
                    'density':density,
                    'urban population (%)':urban_pop_pc,
                    'urban population ':urban_pop_abs,
                    'population world ration':pop_world_ratio,
                    'world population':world_pop,
                    'country global ranking':country_global_ranking
                    }