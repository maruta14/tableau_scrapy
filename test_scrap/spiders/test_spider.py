# -*- coding: utf-8 -*-
import os, scrapy, urllib, time
from test_scrap.items import TestScrapItem
from scrapy_splash import SplashRequest
import zipfile
import xml.etree.ElementTree as ET
import re

class TestSpiderSpider(scrapy.Spider):

    name = 'test_spider'
    allowed_domains = ['localhost']
    start_urls = []
    urls = []
    # with open("/Users/maruta/graduation/bunseki/dict.txt") as search_words:
    #     for word in search_words:
    #         for i in range(1):
    #             start_urls.append('http://localhost:8050/render.html?url=https://public.tableau.com/ja-jp/search/all/'+word.split()[0]+'?page='+str(i+123)+'&timout=10&wait=5')

    start_urls = ['http://localhost:8050/render.html?url=https://public.tableau.com/ja-jp/search/all/action?page='+str(i+123)+'&timout=10&wait=5' for i in range(3)]

    dest_dir = '/Users/maruta/graduation/twb_files'

    def parse(self, response):
        for quote in response.css('#search-page-container > div > div > div.search-page-lower > section.search-results-container > div > ol'):
            item = TestScrapItem()
            a = quote.css('li > div > h3 > a::attr(href)').extract()
            for url_mini in a:
                file_id = url_mini.split("/")[6]
                url = 'https://public.tableau.com/workbooks/'+file_id+'.twb'
                try:
                    urllib.request.urlretrieve(url, os.path.join(self.dest_dir, file_id))
                    file_name = '/Users/maruta/graduation/twb_files/'+file_id
                    
                    with zipfile.ZipFile(file_name, 'r') as post:
                        fname = post.namelist()[-1]
                        root = ET.fromstring(post.read(fname))
                        print("---", fname, "---")
                        titles = []
                        for name in root.iter('worksheet'):
                            worksheet_name = ""
                            dashboard_name = ""
                            worksheet_title  = ""
                            a = name.attrib["name"]
                            # ワークシート名縛り
                            if not re.match("Sheet [0-9]", a):
                                worksheet_name = " "+name.attrib["name"]
                            #ダッシュボード名取得
                            for a in root.iter("dashboard"):
                                if "Dashboard" not in a.attrib["name"]:
                                    dashboard_name = a.attrib["name"]
                            #ワークシート表示タイトル取得
                            for title in name.iter("title"):
                                t = title.find('formatted-text').find("run")
                                try:
                                    t.text
                                    if "<Sheet Name>" not in t.text and not "<" in t.text:
                                        worksheet_title = " "+t.text

                                except:
                                    worksheet_title = ""
                            title = dashboard_name + worksheet_name + worksheet_title
                            #グラフ種類取得
                            for mark in name.iter("mark"):
                                mark_type = mark.attrib["class"]
                            #タイトル長さ縛り
                            if len(title.split()) > 3 and mark_type != "Automatic":
                                titles.append(title+mark_type)
                                print("title: {}   marktype: {}".format(title, mark_type))

                        if len(titles) == 0:
                            os.remove(file_name)
                            print("remove : ", file_name)
                    time.sleep(3)
                except urllib.error.HTTPError:
                    continue
                