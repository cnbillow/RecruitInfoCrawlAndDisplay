# 基于Web爬虫的IT行业需求信息分析系统
------

临近毕业，找工作不易，所以对行业内的招聘信息做了个简单的分析，主要面向学历、城市、工作要求关键字等进行数据分析，并将其结果展示在Web端。该项目主要采用Python27、Django、Scrapy、Redis、Celery、Mysql、jieba分词、echarts、Bootstrap、jQuery等，其中Redis、Celery主要将Scrapy框架和Django框架结合，起到每隔一段时间更新相关分析图。


## 环境依赖
> * Python环境： Django1.8以上+Beatuifulsoup4(4.5.1)+Celery(3.1.25)+Django-celery(3.1.17)+lxml+MysqlDB+redis(2.10.5)+Scrapy(1.2.0)+scrapy-redis(0.6.3)+Unipath(1.1)+Twisted(16.6.0)
> * 数据库环境：MySQL5以上、Redis 3以上
> * 操作系统： Windows XP以上

## 数据来源
> * [百才招聘网](http://wuhan.baicai.com/)
> * [中华英才网](http://www.chinahr.com/wuhan/)
> * [前程无忧](http://www.51job.com/)
> * [智联招聘](https://www.zhaopin.com/)

## 信息格式

**网址**、**工作**、**工作类别**、**平均月薪**、**公司名称**、**工作地点**、**工作经验**、**学历**、**学位**、**职业描述**


## 项目架构图
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/frame.png)
## 部署方式
### 1. 安装所需要的库
+ bs4
+ scrapy
+ redis
+ scrapy-redis
+ pywin32
+ jieba
+ MySQLdb
+ django
+ celery（3.1.25）[ **windows不支持4**]
+ unipath
+ django-celery

## 2. 启动相关服务
> **Redis服务**
> **MySQL服务**

### 3. 配置相关环境
+  配置数据库环境
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/mysql_django.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/scrapy_databases.png)
+  配置爬虫定时执行时间
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/celery_django.png)
+  压入初始URL到Redis中(JobCrawl/lpush.py)


### 4. 启动程序
+ 启动定时任务
  + **celery -A JobEvaluating worker --loglevel=INFO**
  + **celery -A JobEvaluating beat -s celerybeat-schedule**
+ 同步数据库
  + **python manage.py makemigrations**
  + **python manage.py migrate**
+ 启动Django(python manage.py runserver)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/index.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/index1.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/index2.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/display.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/search.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/analyse.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/asks.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/job_hot.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/lan.png)
![](https://github.com/CaryXiang/Information-Analysis-system-of-IT-Industry-requirement-based-on-Web-crawler/blob/master/imgs/salary.png)
