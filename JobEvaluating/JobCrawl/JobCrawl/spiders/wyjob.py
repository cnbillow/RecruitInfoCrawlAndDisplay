# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from datacleaning import Datacleaning
from ..items import ZpItem


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class WyjobSpider(RedisCrawlSpider):
    name = "wyjob"
    redis_key = "wyjob:start_urls"
    # start_urls = (
    #     'http://jobs.51job.com/all/70563395.html',
    # )

    rules = (
        Rule(LinkExtractor(allow=('jobs.51job.com/all/[0-9]*\.html',)),callback='parse_item',follow=True),
        Rule(LinkExtractor(allow=('m.51job.com/jobs/[a-z]{1,10}-[a-z]{1,10}/[0-9]*.html',)),callback='parse_item',follow=True),
        Rule(LinkExtractor(allow=('jobs.51job.com/[a-z]{1,10}-[a-z]{1,10}/[0-9]*.html',)),callback='parse_item',follow=True),
    )

    def parse_item(self,response):
        item = ZpItem()
        dc = Datacleaning()
        dc.check_item(item)
        try:
            bsObj = BeautifulSoup(response.body, 'lxml')
            item['url'] = response.url
            item['job'] = bsObj.find('div', class_='cn').h1.get_text().replace('\r', '').replace('\n', '').replace('\t', '')
            item['working_place'] = bsObj.find('div', class_='cn').span.get_text().replace('\r', '').replace('\n', '').replace('\t', '')
            item['salary'] = bsObj.find('div', class_='cn').strong.get_text().replace('\r', '').replace('\n', '').replace('\t', '')
            item['company'] = bsObj.find('div', class_='cn').find('p', class_='cname').a.get_text().replace('\r', '').replace('\n', '').replace('\t', '')
            item['job_category'] = bsObj.find('div', class_='cn').find('p', class_='msg ltype').get_text().replace('\r', '').replace('\n', '').replace('\t', '')
            desc =  bsObj.find('div', class_='bmsg job_msg inbox').get_text().encode('utf-8')
            item['job_description'] = desc.replace('\r', '').replace('\n', '').replace('\t', '')
            job_desc = bsObj.find('div', class_='t1').findAll('span')
            item['experience'] = job_desc[0].em.next_sibling.encode('utf8')
            item['educational'] = job_desc[1].em.next_sibling

        except Exception as e:
            self.logger.error("parse url:%s err:%s",response.url,e)
        
        return item


