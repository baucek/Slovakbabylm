from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import regex
from urllib.parse import unquote

# odstrani5 jedno slovo oddelene s \n

list_urls=['https://sk.wikipedia.org/wiki/Ob%C4%8Dianska_n%C3%A1uka'] 


# https://sk.wikipedia.org/wiki/Sloven%C4%8Dina https://sk.wikipedia.org/wiki/Matematika



class CrawlingSpider(CrawlSpider): 
    name='wiki_predmety'
    allowed_domains = ['sk.wikipedia.org']
    start_urls = [i for i in list_urls]
    rules=(
        Rule(LinkExtractor(allow=(r'https://sk.wikipedia.org/wiki/.*'),deny=(r'/Kateg%C3%B3ria:.*',r'/%C5%A0peci%C3%A1lne:.*',r'/\S+:\S+',r'/Hlavn%C3%A1_str%C3%A1nka')),callback='parse_item', follow=True),
    )
    custom_settings = {
        'RANDOMIZE_DOWNLOAD_DELAY': False, 
        'DOWNLOAD_DELAY': 0.5,
        'AUTOTHROTTLE_ENABLED': True,
		}
# https://sk.wikipedia.org/wiki/%C5%A0peci%C3%A1lne:.*
#  
    def parse_item(self, response):
        paragraphs = response.xpath('//div//p[not(span) and not(ancestor::table) and not(ancestor::div[@id="Vorlage_BK"])]')
        # paragraphs = response.xpath(
        #     '//div[@class="mw-content-ltr mw-parser-output"]//p['
        #     'not(descendant::img) and '
        #     'not(descendant::span) and '
        #     'not(ancestor::table) and '
        #     'not(ancestor::ul) and '
        #     'not(ancestor::li)'
        #     ']'
        #     '|//div[@class="mw-content-ltr mw-parser-output"]//ol['
        #     'not(descendant::img) and ' 
        #     'not(descendant::span) and ' 
        #     'not(ancestor::table) and ' 
        #     'not(ancestor::li)' 
        #     ']'
        #     '|//div[@class="mw-content-ltr mw-parser-output"]//ul['
        #     'not(descendant::img) and ' 
        #     'not(descendant::span) and ' 
        #     'not(ancestor::table)and ' 
        #     'not(ancestor::ul)'
        #     ']'
            
        # )
        text = paragraphs.xpath('string()').getall()
        url=unquote(response.url)
        yield {
        'url':url,
        'page': text
        }
# response.css('div.mw-content-ltr.mw-parser-output p::text,div.mw-content-ltr.mw-parser-output a::text,div.mw-content-ltr.mw-parser-output span::text, div.mw-content-ltr.mw-parser-output h1::text, div.mw-content-ltr.mw-parser-output:not(tab)').getall()

    #  response.css('div.mw-content-ltr.mw-parser-output p::text,div.mw-content-ltr.mw-parser-output a::text,div.mw-content-ltr.mw-parser-output span::text, div.mw-
    # ...: content-ltr.mw-parser-output h1::text, div.mw-content-ltr.mw-parser-output:not(tab)').getall()