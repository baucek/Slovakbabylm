from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import re

class CrawlingSpider(CrawlSpider):
    name='zones_rozpravky'
    allowed_domains=['www.zones.sk']
    start_urls=['https://www.zones.sk/studentske-prace/rozpravky/']


    rules=(
        Rule(LinkExtractor(allow=('www.zones.sk/studentske-prace/rozpravky/'), deny=(r'www.zones.sk/studentske-prace/rozpravky/.*/?(ulozit=1|vytlacit=1|diskusia=1|referaty=1)')), callback='parse', follow=True),
    )

    def parse(self,response):

        text=response.css('div.referaty_tahaky.a_inarticle.clanok p::text, div.referaty_tahaky.a_inarticle.clanok::text, div.referaty_tahaky.a_inarticle.clanok ul::text, div.referaty_tahaky.a_inarticle.clanok strong u::text').getall()
        text=' '.join(text)
        text= text.replace('\xa0',' ')
        text=re.sub(r'(\n\s*\n)+', ' ', text)
        
        yield {
        'url':response.url,
        'page': text
        }
# , deny=(r'www.zones.sk/studentske-prace/rozpravky/[^?]*\?vytlacit=1',r'www.zones.sk/studentske-prace/rozpravky/[^?]*\?ulozit=1'))

