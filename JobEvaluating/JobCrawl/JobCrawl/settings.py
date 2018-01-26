# -*- coding: utf-8 -*-

# Scrapy settings for JobCrawl project

import os
import sys

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath('../../'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'JobEvaluating.settings'
BOT_NAME = 'JobCrawl'

USERDICT_PATH = os.path.dirname(__file__)+'\userdict.txt'

SPIDER_MODULES = ['JobCrawl.spiders']
NEWSPIDER_MODULE = 'JobCrawl.spiders'
COMMANDS_MODULE = 'JobCrawl.commands'

#ROBOTSTXT_OBEY = True
COOKIES_ENABLED = False  #禁止COOKIES
RETRY_ENABLED = False   #禁止重试
DOWNLOAD_TIMEOUT = 15

DOWNLOAD_DELAY = 0.25

DOWNLOADER_MIDDLEWARES = {
    # 'JobCrawl.contrib.google_cache.GoogleCacheMiddleware':50,
      'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
       'JobCrawl.contrib.rotate_useragent.RotateUserAgentMiddleware' : 400,
}

ITEM_PIPELINES = {
    'JobCrawl.pipelines.MySQLPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# MySQL
MYSQL_HOST='127.0.0.1'
MYSQL_DBNAME='test'
MYSQL_USER='root'
MYSQL_PASSWD='chen'


# redis
SCHEDULER = "JobCrawl.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'JobCrawl.scrapy_redis.queue.SpiderPriorityQueue'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIE_URL = None


# 去重队列的信息
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0

