#coding:utf-8
#分词模块
import re

class Datacleaning(object):
    def __init__(self):
        self.sign = []
        self.get_signs()
    def get_signs(self):
        self.sign.append(u'任职要求')
        self.sign.append(u'职位描述')
        self.sign.append(u'职位要求')
        self.sign.append(u'任职资格')
        
    def get_text_content(self,desc):
			length = len(desc)
			contents = str()
			for i in range(length):
				contents += desc[i].get_text().encode('utf-8')
			return contents

    def get_index(self, contentList):
        flag = False
        for content in contentList:
            for sign in self.sign:
                find = re.search(sign, content)
                if find is not None:
                    flag = True
                    return contentList.index(content) + 1
        if not flag:
            return None

    def get_job_description(self, desc):
        contentList = re.split(u'([\u4e00-\u9fa5]{2,7}\uff1a)', desc)
        index = self.get_index(contentList)
        if index is not None:
            return contentList[index]
        else:
            return None

    def get_sarlary_k(self, salary):			#形如7k-8k
		list = re.split('-', salary)
		num = str()
		flag = True
		for i in list:
			num1 = re.findall('[0-9]*', i)
			num += num1[0]+"000"
			if flag:
				num += '-'
				flag = False
		return num

    def get_salary_m(self, salary):			#形如￥500-
		list = re.split('-', salary)
		num = str()
		flag = True
		for i in list:
			num += re.sub("\D", "", i[1:])
			if flag:
				num += "-"
				flag = False
		return num

    def get_salary_y(self, salary):			#形如5000/月
		list = re.split('-', salary)
		num = str()
		flag = True
		for i in list:
			num += re.sub("\D", "", i)
			if flag:
				num += "-"
				flag = False
		return num

    def get_salary(self, salary):
		find1 = re.search('k', salary)
		find2 = re.search('[^\x00-\xff]\d+.+\d+$', salary)
		find3 = re.search('/', salary)
		find4 = re.search(r'[0-9]{1,6}-[0-9]{1,6}', salary)
		find5 = re.search(u'面议', salary)
		#print 'find5 = ' + find4
		if find1 is not None:
			return self.get_sarlary_k(salary)
		if find2 is not None:
			return self.get_salary_m(salary)
		if find3 is not None:
			return self.get_salary_y(salary)
		if find4 is not None:
			return salary
		if find5 is not None:
			return u'面议'
    def check_item(self, item):
		params = ['url', 'job', 'job_category', 'salary', 'company', 'working_place', 'experience', 'educational', 'job_description']
		for i in params:
			item[i] = ' '

