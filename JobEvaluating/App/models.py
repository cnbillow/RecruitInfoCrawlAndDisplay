# coding: utf-8
from django.db import models
from datetime import datetime

# 招聘
class ZpInfo(models.Model):
    id = models.AutoField(primary_key=True)  # id
    url = models.CharField(max_length=100)  # 网址
    job = models.CharField(max_length=100)  # 工作
    job_category = models.CharField(max_length=100)  # 工作类别
    salary = models.CharField(max_length=100)  # 薪水
    company = models.CharField(max_length=100)  # 公司
    working_place = models.CharField(max_length=100)  # 工作地点
    experience = models.CharField(max_length=100) # 工作经验
    educational = models.CharField(max_length=100)  # 学历
    job_description = models.CharField(max_length=1024)  # 工作描述
    datetime = models.DateTimeField(auto_now_add=True,  blank=True)  # 时间戳


# 需求
class Asks(models.Model):
    id = models.AutoField(primary_key=True)  # id
    ask = models.CharField(max_length=100)  # 需求


# 城市
class Citys(models.Model):
    id = models.AutoField(primary_key=True)  # id
    city = models.CharField(max_length=100)  # 城市


# 中间结果
class Middleware(models.Model):
    id = models.AutoField(primary_key=True)
    Salary = models.IntegerField()
    Lan = models.IntegerField()
    City = models.IntegerField()
    KeyWords = models.IntegerField()
    Education = models.IntegerField()