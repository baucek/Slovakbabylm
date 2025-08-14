from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re


class CrawlingSpider(CrawlSpider): 
    name='zones_lit'
    allowed_domains = ['zones.sk']
    start_urls = ['https://zones.sk/']
    rules=(
        Rule(LinkExtractor(allow=(r'/studentske-prace/slohove-prace')),callback='parse_item', follow=True),)
    def parse_item(self, response):
        text=response.css('div.referaty_tahaky.a_inarticle.clanok  p::text,div.referaty_tahaky.a_inarticle.clanok  em::text,div.referaty_tahaky.a_inarticle.clanok  strong::text,div.referaty_tahaky.a_inarticle.clanok  h1::text,div.referaty_tahaky.a_inarticle.clanok h2::text,div.referaty_tahaky.a_inarticle.clanok  h3::text,div.referaty_tahaky.a_inarticle.clanok  h4::text').getall()
        text=' '.join(text)
        text= text.replace('\xa0',' ')
        text=re.sub(r'(\n\s*\n)+', ' ', text)

        # text=
        yield {
        'url':response.url,
        'page': text
        }


        # https://www.zones.sk/studentske-prace/slohove-prace/4399-prejav-k-zivotnemu-jubileu/