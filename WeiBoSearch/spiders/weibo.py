# -*- coding: utf-8 -*-
import re
import scrapy
from bs4 import BeautifulSoup
from ..items import WeiboItem
class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = ['https://weibo.cn/search/mblog?hideSearchFrame=&keyword=000001&page=2']
    cookies={
    'cookie':'your cookies'
    }
    keyword='美食'

    def start_requests(self):
        url='https://weibo.cn/search/mblog'
        for page in range(100):
            data = {
                'hideSearchFrame': '',
                'keyword': self.keyword,
                'page': str(page),
                'vt':''
            }
            yield scrapy.FormRequest(url=url, cookies=self.cookies, callback=self.parse_test, formdata=data,method='GET')

    def parse_test(self, response):
        item=WeiboItem()
        soup=BeautifulSoup(response.text,'lxml')
        DIVS=soup.find_all('div',id=re.compile(r'M_'))
        for DIV in DIVS:
            if bool(DIV.find('span',class_='cmt')):
                #转发的微博 不做处理
                pass
            else:
                #原创的微博
                item['name']= DIV.find('a', class_='nk').get_text()
                item['contents'] = DIV.find('span', class_='ctt').get_text()
                item['argu']=DIV.find('a',class_='cc').get_text().split(' ')[-1]
                item['forward']=DIV.find('a',class_='cc').find_previous_sibling('a').get_text()
                item['yes'] =DIV.find('a',class_='cc').find_previous_sibling('a').find_previous_sibling('a').get_text()
                item['From']=DIV.find('span',class_='ct').get_text()
                yield item


