import scrapy
from ..items import IndexItem

count = 0


class IndexScraper(scrapy.Spider):
    name = 'index_scrape'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ["https://en.wikipedia.org/w/index.php?title=Special:AllPages&from=%21"]
    global count
    ending_page = "/w/index.php?title=Special:AllPages&from=Z%C4%83bala+%28R%C3%A2ul+Negru%29"
    base_url = "https://en.wikipedia.org"

    def parse(self, response):
        item = IndexItem()
        page_name = response.css(".mw-allpages-chunk a::text").extract()
        page_url = response.css(".mw-allpages-chunk a").xpath("@href").extract()
        for (name, link) in zip(page_name, page_url):
            item['name'] = name.upper()
            item['link'] = self.base_url + link
            yield item
        global count
        next_page_first = response.css(".mw-allpages-nav a").xpath("@href").get()
        next_page = response.css(".oo-ui-panelLayout-framed+ .mw-allpages-nav a+ a").xpath('@href').get()
        if count != 0:
            if next_page != self.ending_page:
                yield response.follow(next_page, callback=self.parse)
        else:
            count += 1
            yield response.follow(next_page_first, callback=self.parse)
