import scrapy
import logging
from grap.items import MoviesItem

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ['80s.tw']
    def start_requests(self):
        start = 593
        urls = []
        for i in range(1):
            urls.append('http://www.80s.tw/movie/'+str(start+i))
        for url in urls:
            self.log('正在进行爬虫的url %s' % url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        moviesItem = MoviesItem()
        moviesItem['mlink'] = response.css('input#downid_0::attr(value)').extract_first()
        moviesItem['mname'] = response.css('div.info h1::text').extract_first()
        for span in response.xpath('//span[@class="font_888"]/text()').extract():
            self.logger.info(span)
            if span== "又名：":
                moviesItem['mname2'] = ''# response.xpath('//span[@class="font_888"]/parent::*/text()').extract()
            if span == "演员：":
                actor = ''
                for a in  response.xpath('//span[@class="font_888"]/following-sibling::a/text()').extract():
                    self.logger.info(a)
                    actor =actor+"|"+a
                moviesItem['mactor']=actor
        self.logger.info(moviesItem)
