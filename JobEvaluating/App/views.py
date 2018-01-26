#coding:utf-8
from django.shortcuts import render
from handlesql import BaseOnSqlHelper
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import json
# Create your views here.

import sys

reload(sys)

sys.setdefaultencoding('utf-8')

helper = BaseOnSqlHelper()

def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)

def display(request):
    ctx = {}
    if request.is_ajax():
        val = request.POST.get('choose')
        if val in 'salary':
            salary = helper.getMiddleSalary()
            ctx['salary'] = salary
        if val in 'lan':
            lan = helper.getMiddleLan()
            ctx['lan'] = lan
        if val in 'ask':
            ask = helper.getMiddleKeyWords()
            ctx['ask'] = ask
        if val  in 'citys':
            citys = helper.getMiddleCity()
            ctx['citys'] = citys
        if val in 'education':
            education = helper.getMiddleEducation()
           # print education
            ctx['education'] = education
    else:
        salary = helper.getMiddleSalary()
        ctx['salary'] = salary
    return render(request, 'display.html', ctx)

def about(request):
    ctx = {}
    return render(request, 'about.html', ctx)

def search(request):
    limit = 7        #每页显示的记录数
    ctx = {}
    if request.GET.get('search'):
        search = request.GET.get('search')
        paginator = Paginator(helper.getSearchData(search), limit)
    else:
        paginator = Paginator(helper.getSearchData('java'), limit)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    ctx['result'] = result
    return render(request, 'search.html', ctx)

def analyse(request):
    ctx = {}
    citys = []
    if request.GET.get('beijing'):
        citys.append(u'北京')
    if request.GET.get('wuhan'):
        citys.append(u'武汉')
    if request.GET.get('shanghai'):
        citys.append(u'上海')
    if request.GET.get('guangzhou'):
        citys.append(u'广州')
    if request.GET.get('hangzhou'):
        citys.append(u'杭州')
    if request.GET.get('jinan'):
        citys.append(u'济南')
    if request.GET.get('shenzheng'):
        citys.append(u'深圳')
    if request.GET.get('nanjing'):
        citys.append(u'南京')
    if request.GET.get('hefei'):
        citys.append(u'合肥')
    if request.GET.get('changsha'):
        citys.append(u'长沙')
    if request.GET.get('guiyang'):
        citys.append(u'贵阳')
    if request.GET.get('xian'):
        citys.append(u'西安')

    if request.GET.get('search'):
        search = request.GET.get('search')
        heat_lan,best_city, value = helper.getLanEachOfCity(search, citys)
        ctx['heat_lan'] = heat_lan
        ctx['best_city'] = best_city
        ctx['title'] = json.dumps(search)
        ctx['analyse'] = value
    else:
        search = 'java开发工程师'
        heat_lan,best_city,value = helper.getLanEachOfCity(search, citys)
        ctx['heat_lan'] = heat_lan
        ctx['title'] =  json.dumps(search)
        ctx['best_city'] = best_city
        ctx['analyse'] = value
    return render(request, 'analyse.html', ctx)
