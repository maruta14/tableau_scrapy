# -*- coding: utf-8 -*-
import os, scrapy, urllib, time
from test_scrap.items import TestScrapItem
from scrapy_splash import SplashRequest

class TestSpiderSpider(scrapy.Spider):

    # name = 'test_spider'
    # allowed_domains = ['public.tableau.com']

    # start_urls = ['https://public.tableau.com/ja-jp/search/all/COVID?page=300']
    # dest_dir = '/Users/maruta/graduation/twb_files'


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url,
    #                         callback=self.parse, 
    #                         endpoint='render.html',
    #                         args={'wait': 1.0})

    # def parse(self, response):
    #     for quote in response.css('#search-page-container > div > div > div.search-page-lower > section.search-results-container > div > ol'):
    #         item = TestScrapItem()
    #         a = quote.css('li > div > h3 > a::attr(href)').extract()
    #         print(a)
    #         for url_mini in a:
    #             file_id = url_mini.split("/")[6]
    #             url = 'https://public.tableau.com/workbooks/'+file_id+'.twd'
    #             print(url)
    #             urllib.request.urlretrieve(url, os.path.join(self.dest_dir, file_id))

    #             time.sleep(3)


    name = 'test_spider'
    allowed_domains = ['localhost']

    # start_urls = ['http://localhost:8050/render.html?url=https://public.tableau.com/ja-jp/search/all/COVID?page='+str(i+200) for i in range(5)]
    start_urls = ['http://localhost:8050/render.html?url=https://public.tableau.com/ja-jp/search/all/COVID?page=200']

    dest_dir = '/Users/maruta/graduation/twb_files'

    def parse(self, response):
        for quote in response.css('#search-page-container > div > div > div.search-page-lower > section.search-results-container > div > ol'):
            item = TestScrapItem()
            a = quote.css('li > div > h3 > a::attr(href)').extract()
            print(a)
            for url_mini in a:
                file_id = url_mini.split("/")[6]
                url = 'https://public.tableau.com/workbooks/'+file_id+'.twd'
                print(url)
                urllib.request.urlretrieve(url, os.path.join(self.dest_dir, file_id))

                time.sleep(3)

