from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import logging

class CrawlingSpider(CrawlSpider):
    name='rozpravkozem'
    allowed_domains=['www.rozpravkozem.sk']
    start_urls=['https://www.rozpravkozem.sk/']

    rules=(
        Rule(LinkExtractor(deny=[r"https://www.rozpravkozem.sk/page/\d+", r'https://www.rozpravkozem.sk/tag/\w+']), callback='parse', follow=True),
    )

    def parse(self,response):
        text=response.css('div.entry-content p::text').getall()
        text=' '.join(text)

        yield {
        'url':response.url,
        'page': text
        }




