# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from datacleaning import Datacleaning
from ..items import ZpItem
import redis


class ChinahrSpider(RedisCrawlSpider):
    name = "chinahr"
    allowed_domains = ["chinahr.com"]
    redis_key = "chinahr:start_urls"

    # start_urls = (
    #     'http://www.chinahr.com/job/5149152252723715.html',
    # )

    rules = (
        Rule(link_extractor=LinkExtractor(allow=('www.chinahr.com/job/[0-9]*\.html')),callback='parse_item',follow=True),
    )

    def parse_item(self,response):
        item = ZpItem()
        dc = Datacleaning()
        dc.check_item(item)
        try:
            bsObj = BeautifulSoup(response.body ,'lxml')
            item['url'] = response.url
            item['job'] = bsObj.find('div', class_='base_info').h1.span.get_text()  # 工作职位
            company_desc = bsObj.find('div', class_='job-company jrpadding')
            item['job_category'] = company_desc.find('table').findAll('tr')[0].findAll('td')[1].get_text().replace(' ','').replace('\n', '')
            job_require = bsObj.find('div', class_='job_require').findAll('span')
            item['salary'] = job_require[0].get_text()
            item['company'] = company_desc.h4.a.get_text()
            item['working_place'] = job_require[1].get_text()
            item['experience'] = job_require[4].get_text()
            item['educational'] = job_require[3].get_text()
            item['job_description'] = bsObj.find('div', class_='job_intro_info').get_text().replace(' ', '').replace('\n', '').replace('\t', '')
        except Exception as e:
            self.logger.error("parse url:%s err:%s",response.url,e)

        return item




