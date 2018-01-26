# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from datacleaning import Datacleaning
from ..items import ZpItem

class ZlzpSpider(RedisCrawlSpider):
    name = "zlzp"
    redis_key = "zlzp:start_urls"
    # start_urls = (
    #     'http://jobs.zhaopin.com/000645187251845.htm',
    # )

    #定义爬取规则
    rules = (
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.htm',)),callback='parse_one_job',follow=True),
        Rule(LinkExtractor(allow=('jobs.zhaopin.com/[0-9]*\.htm',),deny=('[a-zA-Z0-9]*/in[0-9]*_','zhaopin.liebiao.com',
                                                    'jobs.zhaopin.com/[a-z]*/[a-z0-9]*/[a-z0-9_]*')),follow=True),
    )
    

    def parse_one_job(self,response):
        try:
            item = ZpItem()
            dc = Datacleaning()
            dc.check_item(item)
            bsObj = BeautifulSoup(response.body, 'html.parser')
            item['url'] = response.url
            item['job'] = bsObj.find('div', class_='inner-left fl').h1.get_text()
            desc = bsObj.find('div', class_='tab-inner-cont').findAll('p')
            self_Job = content  = bsObj.find('ul', class_='terminal-ul clearfix').findAll('strong')
            item['salary'] =  self_Job[0].get_text()
            item['working_place'] = self_Job[1].a.get_text()
            item['experience'] = self_Job[4].get_text()
            item['educational'] = self_Job[5].get_text()
            item['job_category'] = self_Job[7].a.get_text()
            item['company'] = bsObj.find('p', class_='company-name-t').find('a').get_text()
            contents = dc.get_text_content(desc)
            content = dc.get_job_description(contents.decode('utf-8'))
            item['job_description'] = content.replace('\n', '').replace(' ', '')

        except Exception as e:
			#错误日志	
            self.logger.error("parse url:%s err e:%s",response.url,e)
        
        return item