from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import scrapy
import logging
from bs4 import BeautifulSoup
import requests
import json


# url='https://svetrozpravok.sk/rozpravky/#10'
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
# links = soup.find_all('a', class_="stk-block-posts__readmore")
# hrefs = [link.get('href') for link in links]
# print(hrefs)




# https://svetrozpravok.sk/rozpravky/



from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import regex



class CrawlingSpider(CrawlSpider): 
    name='rozp'
    allowed_domains = ['svetrozpravok.sk']
    start_urls = ['https://svetrozpravok.sk/']
    rules=(
        Rule(LinkExtractor(allow=(r'https://svetrozpravok.sk/.*')),callback='parse_item', follow=True),)

                        #    ,deny=(r"/pexeso.*",r"/Rozprávky.*",r"/rozpravky.*",r"/vianocne-.*",r"/Humorné.*",r"/kontakt",r"/o-projekte",r"/zaujimavosti")

# https://sk.wikipedia.org/wiki/%C5%A0peci%C3%A1lne:.*
#  
    def parse_item(self, response):
        text= response.css('div.entry-content.is-layout-flow p::text').getall()
        yield {
            'url':response.url,
            'text':text
        }

