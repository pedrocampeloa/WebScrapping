# -*- coding: utf-8 -*-
import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        
        rows = response.xpath("//table/tbody/tr")
        for row in rows:
            name = row.xpath(".//td[1]/a/text()").get()
            link = row.xpath(".//td[1]/a/@href").get()
            national_gdp= row.xpath(".//td[2]/text()").get()
            population = row.xpath(".//td[3]/text()").get()
            
            
            #absolute_url = f"https://www.worldometers.info{link}"
            #absolute_url = response.urljoin(link)
            
            #yield scrapy.Request(url=absolute_url)
            yield response.follow(url=link, 
                                  callback = self.parse_country, 
                                  meta = {'country_name':name, 'national_gdp_ratio_2020': national_gdp, 'country_population':population})
            
            
    def parse_country(self, response):
    
        name = response.request.meta['country_name']
        national_gdp = response.request.meta['national_gdp_ratio_2020']
        population_2020 = response.request.meta['country_population']


        for table in range(2,4):
                     
            html_path = "(//table[@class='datatableStyles__StyledTable-bwtkle-1 hOnuWY table table-striped'])["+str(table)+"]/tbody/tr"
            rows = response.xpath(html_path)
            for row in rows:
                
                year = row.xpath(".//td[1]/text()").get()
                population= row.xpath(".//td[2]/text()").get()
                growth_rate = row.xpath(".//td[3]/span/text()").get()
                density = row.xpath(".//td[4]/text()").get()
                pop_rank = row.xpath(".//td[5]/text()").get()
                density_rank = row.xpath(".//td[6]/text()").get()

                
                yield {
                        'name': name,
                        'national gdp':national_gdp,
                        'population_2020': population_2020,                        
                        'year': year,
                        'population': population,
                        'growth rate':growth_rate,
                        'density':density,
                        'population rank':pop_rank,
                        'density rank':density_rank
                        }        
                
                
                
                