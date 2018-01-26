# -*- coding: utf-8 -*-

import jieba
import jieba.analyse
import jieba.posseg
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import sys
sys.path.append('../')
from items import ZpItem
from spiders.datacleaning import Datacleaning
import logging
from datetime import datetime as dt

class MySQLPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        jieba.load_userdict(settings.get('USERDICT_PATH'))
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass= MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item)
        d.addErrback(self.handle_error)
        return item
    def handle_error(self, e):
        logging.warning(e)

    # 将每行更新或写入数据库中
    def _do_upinsert(self, tx, item):
        dc = Datacleaning()
        if isinstance(item,ZpItem):
            try:
                salary = item['salary']
                if salary is not None:
                    item['salary'] = dc.get_salary(salary)
                sql = "insert into app_zpinfo(url, job, job_category, salary,  company, working_place, experience, educational, job_description, datetime)  values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                params = ([item['url']], [item['job']], [item['job_category']], [item['salary']],[item['company']],[item['working_place']],[item['experience']], [item['educational']],[item['job_description']], [dt.now()])
                tx.execute(sql, params)
                sentence = item['job_description']
                working_place = item['working_place']

                if working_place is not None:
                    list_places = jieba.analyse.extract_tags(working_place,  withWeight=False, allowPOS=('d'))
                    for place in list_places:
                        if place is not None:
                            tx.execute("insert into app_citys(city) values(%s)", [place])

                if sentence is not None:
                    tags = jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=('z'))
                    for tag in tags:
                        if tag is not None:
                            tx.execute("insert into app_asks(ask) values(%s)", [tag])

            except Exception as e:
                print("Execute MySQL error: %s", e)

