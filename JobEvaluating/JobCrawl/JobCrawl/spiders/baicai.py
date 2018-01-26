# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import ZpItem
from datacleaning import Datacleaning
import redis

class BaicaiSpider(RedisCrawlSpider):
    name = "baicai"
    redis_key = "baicai:start_urls"
    allowed_domains = ["baicai.com"]
    # start_urls = (
    #     'http://wuhan.baicai.com/jobs/xiaoshouqita/26146505/',
    #     'http://beijing.baicai.com/jobs/xiaoshoujingli/16799463/',
    # )

    rules = (
       Rule(link_extractor=LinkExtractor(allow=('/jobs/[A-Za-z]*/[0-9]*/')), callback='parse_item',follow=True),
    )
    def parse_item(self, response):
        item = ZpItem()
        dc = Datacleaning()
        dc.check_item(item)
        try:
            bsObj = BeautifulSoup(response.body, 'lxml')
            item['url'] = response.url
            item['job'] = bsObj.find('h1', class_='job-title').a.get_text()  # 工作
            job_desc = bsObj.find('ul', class_='JC-headList cfix').findAll('li')  #
            item['job_category'] = job_desc[1].a.get_text()  # 职位类别
            job_desc_detail = job_desc[0].findAll('label')
            item['salary'] = job_desc_detail[2].next_sibling  # 薪水
            item['company'] = bsObj.find('p', class_='JC-company cfix').findAll('a')[0].get_text()  # 公司
            item['working_place'] = job_desc[2].label.next_sibling.replace('\r', '').replace('\n', '').replace('\t', '')  # 工作地点
            item['experience'] = job_desc_detail[0].next_sibling.replace('\r', '').replace('\n', '').replace('\t', '')
            item['educational'] = job_desc_detail[3].next_sibling.replace('\r', '').replace('\n', '').replace('\t', '')
            item['job_description'] = bsObj.find('p', class_='JC-detail').get_text().replace(' ', '')
        except Exception as e:
            self.logger.error("parse url:%s err:%s",response.url,e)
        return item


