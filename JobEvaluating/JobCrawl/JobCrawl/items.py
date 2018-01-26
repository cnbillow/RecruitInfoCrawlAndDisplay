# -*- coding: utf-8 -*-


import scrapy


# 招聘
class ZpItem(scrapy.Item):
	url = scrapy.Field()				# 网址
	job = scrapy.Field()				# 工作
	job_category = scrapy.Field()		# 工作类别
	salary = scrapy.Field()				# 平均月薪
	company = scrapy.Field()			# 公司名称
	working_place  = scrapy.Field()		# 工作地点
	experience = scrapy.Field()			# 工作经验
	educational = scrapy.Field()		# 学历
	job_description = scrapy.Field()	# 职位描述