from __future__ import absolute_import

import subprocess
from celery import task
import os

from django.db import connection,transaction
from .handlesql import BaseOnSqlHelper

sqlHelper = BaseOnSqlHelper()

def executeSql(sql):
    with transaction.atomic():
        cursor = connection.cursor()
        cursor.execute(sql)
        raw = cursor.fetchall()
        return raw

@task()
def crawl():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'JobCrawl.settings')
    return subprocess.call(['python', 'JobCrawl\crawlall.py'])

@task()
def update_sql():
    salary = sqlHelper.getSalary()
    lan = sqlHelper.getLan()
    ask = sqlHelper.getKeyWords()
    citys = sqlHelper.getCity()
    education = sqlHelper.getEducation()
    length_s = len(salary)
    length_l = len(lan)
    length_a = len(ask)
    length_c = len(citys)
    length_e = len(education)

    for i in range(length_s):
        sql = "update app_middleware set salary  = '%s' where id = '%d' " % (salary[i], i+1)
        executeSql(sql)
    for i in range(length_l):
        sql = "update app_middleware set Lan  = '%s' where id = '%s' " % (lan[i]['value'], i+1)
        executeSql(sql)
    for i in range(length_a):
        sql = "update app_middleware set KeyWords  = '%s' where id = '%s'" % (ask[i]['value'], i+1)
        executeSql(sql)
    for i in range(length_c):
        sql = "update app_middleware set City  = '%s' where id = '%s'" % (citys[i]['value'], i+1)
        executeSql(sql)
    for i in range(length_e):
        sql = "update app_middleware set Education  = '%s' where id = '%s'" % (education[i]['value'], i+1)
        executeSql(sql)