# coding:utf-8
from django.db import connection,transaction
import json
import re


# sql语言帮助
class SqlHelper(object):
    # 元组向其他类型转换
    def tupleToOther(self, tup):
        for i in tup:
            if isinstance(i[0], long):
                return int(i[0])

    # 执行一条sql语句
    def executeSql(self, sql):
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(sql)
            raw = cursor.fetchall()
            return raw

    # 查询salary情况，返回相关结果
    def executeGroupSalary(self, args):
        # flag = 0（有上限有下限） flag=1(上限) flag=2(下限 ) flag=3(面议)
        def execute_salary(flag, args):
            if len(args) > 4 or len(args) < 0:
                return None
            if flag == 0:
                sql = "select count(url) from app_zpinfo where salary >= %s and salary <= %s" % (args[0], args[1])
            elif flag == 1:
                sql = "select count(url) from app_zpinfo where salary <= %s " % (args[0])
            elif flag == 2:
                sql = "select count(url) from app_zpinfo where salary >= %s" % (args[0])
            elif flag == 3:
                sql = "select count(url) from app_zpinfo where salary = %s" % (u'"面议"')
            return self.executeSql(sql)
        ls = []
        for i in args:
            ls.append(self.tupleToOther(execute_salary(i[0], i[1:])))
        return ls

    # 关键字查询情况
    def executeGroupAsk(self, flag, args):
        la = []
        def executeLan(args):
            sql = "select count(job) from app_zpinfo where lower(job) like '%%%s%%'" % args.lower()
            return self.executeSql(sql)
        def executeKey(args):
            sql = "select count(ask) from app_asks where ask like '%%%s%%'" % args
            return self.executeSql(sql)
        # 语言
        if 1 == flag:
            for i in args:
                la.append({"value" : self.tupleToOther(executeLan(i)), "name" : i})
                #la[i] = self.tupleToOther(executeLan(i))
        # 关建字
        if 2 == flag:
            for i in args:
                la.append({"value" : self.tupleToOther(executeKey(i)), "name" : i})
        return la

    # 城市查询情况
    def executeGroupCity(self, args):
        def executeCity(arg):
            sql = "select count(city) from app_citys where city = '%s'" % (arg)
            return self.executeSql(sql)
        lc = []
        for i in args:
            lc.append({"value" : self.tupleToOther(executeCity(i)), "name" : i})
        return lc


class BaseOnSqlHelper(object):
    # 配置你想要获取的信息
    def __init__(self):
        self.sqlHelper = SqlHelper()
        # flag = 0（有上限有下限） flag=1(上限) flag=2(下限 ) flag=3(面议)
        self.salary = [[0,2000,4000], [0,4000,6000], [0, 6000, 8000], [0,8000,10000], [2, 10000], [3]]
        self.lan = ['java','c++', 'python', 'linux', 'php', 'ios', 'android', 'hadoop', 'asp', 'go']
        self.app_citys = [u'武汉', u'广州', u'北京', u'深圳', u'上海', u'天津', u'重庆', u'石家庄', u'沈阳', u'哈尔滨', '杭州',
             u'福州',u'济南',u'成都', u'昆明', u'兰州', u'南宁', u'银川', u'长春', u'南京', u'合肥', u'南昌',
             u'郑州', u'长沙',u'海口',u'贵阳', u'西安', u'呼和浩特', u'拉萨', u'乌鲁木齐']
        self.keyWords = [u'经验', u'数据库', u'态度认真',u'责任',u'执行力',u'吃苦耐劳',u'设计',
                    u'团队', u'事业进取心',u'管理能力',u'沟通', u'协调',u'算法',
                    u'压力',u'测试',u'硬件', u'云计算', u'物联网', u'大数据', u'安全', u'架构师',
                    u'数据挖掘', u'数据']
        self.educatioinBg = [u'中专', u'大专',  u'应届毕业生', u'本科', u'研究生', u'博士']
    # 二维元祖转换列表
    def tuple_to_list(self, tuples):
        ls = []
        for i in tuples:
            if isinstance(i[0], long):
                ls.append(int(i[0]))
        return ls

    # 拿到薪水值
    def getSalary(self):
        return self.sqlHelper.executeGroupSalary(self.salary)
    # 借用映射数据库拿到薪水值
    def getMiddleSalary(self):
        sql = "select salary from app_middleware limit %s" % len(self.salary)
        return self.tuple_to_list(self.sqlHelper.executeSql(sql))

    # 拿到语言值
    def getLan(self):
        return self.sqlHelper.executeGroupAsk(1, self.lan)
    # 借用映射数据库拿到语言值
    def getMiddleLan(self):
        sql = "select Lan from app_middleware limit %s" % len(self.lan)
        values = self.tuple_to_list(self.sqlHelper.executeSql(sql))
        result = []
        for i in range(len(values)):
            result.append({'name' : self.lan[i], 'value' : values[i]})
        return json.dumps(result)


    # 拿到城市值
    def getCity(self):
        return self.sqlHelper.executeGroupCity(self.app_citys)
    # 借用映射数据库拿到城市值
    def getMiddleCity(self):
        sql = "select City from app_middleware limit %s" % len(self.app_citys)
        values = self.tuple_to_list(self.sqlHelper.executeSql(sql))
        result = []
        for i in range(len(values)):
            result.append({'name' : self.app_citys[i], 'value' : values[i]})
        return json.dumps(result)

    # 拿到关键字
    def getKeyWords(self):
        return self.sqlHelper.executeGroupAsk(2, self.keyWords)
    # 借用映射数据库拿到关键字
    def getMiddleKeyWords(self):
        sql = "select KeyWords from app_middleware limit %s" % len(self.keyWords)
        values = self.tuple_to_list(self.sqlHelper.executeSql(sql))
        result = []
        result.append({ 'name': ' ', 'value': 0,
                         'textStyle': {'normal': { 'color': 'black'},
                         'emphasis': { 'color': 'red'}}})
        for i in range(len(values)):
            result.append({'name' : self.keyWords[i], 'value' : values[i]})
        return json.dumps(result)

    # 拿到教育情况
    def getEducation(self):
        return self.sqlHelper.executeGroupAsk(2, self.educatioinBg)
    # 借用映射数据库拿到教育情况
    def getMiddleEducation(self):
        sql = "select Education from app_middleware limit %s" % len(self.educatioinBg)
        values = self.tuple_to_list(self.sqlHelper.executeSql(sql))
        result = []
        for i in range(len(values)):
            result.append({'name' : self.educatioinBg[i], 'value' : values[i]})
        return json.dumps(result)

    # 二维元祖转换为字典列表
    def tuple_dict_list(self, tuples):
        ls = []
        #注意 ，要与getSearchData一一对应
        keys = ['url', 'job', 'salary', 'company', 'working_place', 'datetime']
        for tuple in tuples:
            ls.append({keys[0]:tuple[0],keys[1]:tuple[1],keys[2]:tuple[2],keys[3]:tuple[3]
                          ,keys[4]:tuple[4],keys[5]:tuple[5]})
        return ls
    # 搜索函数
    def getSearchData(self, key):
        # 一次查询限制返回100条
        sql = "select url, job, salary, company, working_place, datetime  \
              from app_zpinfo where lower(job) like '%%%s%%'  order by datetime desc limit 100" % key.lower()
        result = self.tuple_dict_list(self.sqlHelper.executeSql(sql))

        return result

    # 将城市需求结果以字典列表形式返回
    def city_list_dict(self, ll, app_citys):
        la = []
        for i in range(len(app_citys)):
            la.append({'name' : app_citys[i], 'value' : ll[i]})
        return la


    # 不同语言在各个城市之间的需求
    def getLanEachOfCity(self, key, app_citys):
        la = []
        l = {"c++" : u'c\+\+', "java" : u'java',"linux":u'linux',
             "php":u'php',"python":u'python', "数据库":u'\u6570\u636e\u5e93',
             "r":u'r', "c":u'c\u8bed\u8a00', "web" : u'web',
              "大数据":u'\u5927\u6570\u636e'
        }
        analyse = {
            'java' : u'从人才需求方面看，目前我国软件人才缺口极其严重，其中java人才最为缺乏，对java软件工程师的需求达到全部需求量的60%-70%。从薪资水平看，java软件工程师的薪资相对较高，具备3-5年工作经验的开发人员年薪在10万元以上的很正常的一个薪酬水平。',
            'php' : u'今年各类企业发布招聘PHP人才信息，对人才的需求量极大，但是因为国内PHP人才贮备的不足、培训体系的不健全以及国内Web开发人员对PHP的价值认识不够，造成 PHP人才非常稀缺...... \
       在最近几年年我们可以看到企业对PHP使用更加广泛，与此同时对PHP相关的Web开发人才需求更是急速升温。分析中国不同行业的网站，我们可以看到国内，包括Google、百度、网易、新浪、搜狐、阿里巴巴、奇虎、eBay、腾讯、Yahoo、金山等的各大网站都在寻求PHP高手。   \
       因此，在IT业和互联网的超速发展的时代，企业对PHP程序员的需求也大量增加，PHP程序员和招聘岗位的供求比例是1：40，很多公司半年都招不到一个合适的PHP程序员。这个岗位是程序员中最火的，这种严重供不应求的局面在未来几年中也将愈演愈烈。',
            'python' : 'Python薪酬是大幅度上升的，加上互联网行业正在进入成长爆发期，所以现在开始学习python的小伙伴果然是明智滴。',
            '大数据' : u'大数据产业发展很快，市场上预测在2014-2019年间年增长率可达23.1%。因此，市场上对数据分类、管理、处理的人才需求量很大，在大数据的背景下，来自各大数据相关高校的从业人员都有望实现自己的价值。',
            'c语言' : u'C语言运用范围广、人才缺口大，恰好蹴就了C语言人才的广阔就业前景，且在微软的强大支撑下，C语言学习已成热潮。另一方面，行业的高薪待遇也吸引了大批C语言学习者。薪资调查数据显示，一般的初级或者中级C语言软件工程师目前的年薪为5万-15万，而高级C语言软件工程师的年薪已达15万-30万，相对java软件工程师及.net软件开发工程师薪资都要高。随着信息化迅猛发展，不仅IT专业企业需要C语言开发工程师，众多非IT企业也表示对开发工程师有很大的需求，IT行业目前在国内为朝阳产业，C语言工程师便是这朝阳产业中具发展潜力的岗位之一。',
            'linux' : u'十年前所有的公司都注重网络技术，所以那个时候网络工程师大热。如今大公司的网络都早已成形，市场上的CCIE到处可见，网络技术的门槛越来越低。linux行业的崛起，又燃起了互联网人的新希望，在云计算大环境下，市场上对linux运维人员的需求越来越大。虽然linux运维前景大好，但人才也不是批量生产的，linux高级运维也不是想做就可以做的。一个职位最怕的是从事其他职位的人可以轻松取代你，如果是这样，这个职位就不值钱。如果你是不可取的的，那么薪资自然也是不可取代的。在Linux运维的初级阶段，其实是可以取代的，Linux毕竟是一个操作系统，只是一个工具。一个经常在linux下做开发的开发人员就可以取代一个linux初级运维人员。但如果高级运维，开发人员是无法取代运维人员的。高级运维是一个非常专业职位，高级运维需要掌握相当多的知识，包括但不限于网络技术、系统编程、运维流程及思想、虚拟化、自动化运维体系构建、数据库管理，云计算平台应用，大数据等。一个运维人员需要具备有开发人员的思想，但一个开发人员是否能够掌握常年积累下来的运维流程、思想和经验体系就不是一朝一夕的事情了，所以高级linux运维绝对是目前大公司的稀缺人才。',
            'web' : u'同等工作年限，前端开发岗在北京地区的平均薪资水平最高，广州地区的平均薪资水平最低；北上广三地前端开发工程师的薪资起点都比当地的平均收入高。随着工作经验的增加，前端开发岗在北上广三地的薪资水平均呈快速增长的趋势，相比之下，北京地区的薪资涨幅最大，广州最小。并且都在工作资历到第4、5年左右有一个跳跃式的增长',
        }
        value = str()
        flag = True
        for x in l:
            if re.search(l[x], key, re.I):
                flag = False
                value = analyse[x]
        if flag:
            value = u'在目前的行业发展状况来看，在近十年中，国内发展呈增长趋势，各大中小型企业的需求日益增长，要有很好的项目经验，对于这个行业，要有全局认识，工作选择的机会就越大。'
        # 没有勾选任何城市
        if len(app_citys) < 1:
            app_citys = [u'北京', u'上海', u'广州', u'深圳']
            for city in app_citys:
                sql = "select count(job) from app_zpinfo where lower(job) like '%%%s%%' and working_place like '%%%s%%'" % (key.lower(), city)
                la.append(self.sqlHelper.tupleToOther(self.sqlHelper.executeSql(sql)))
            best_city = app_citys[la.index(max(la))]
            return json.dumps(self.city_list_dict(la, app_citys)), best_city, value
        else:
            for city in app_citys:
                sql = "select count(job) from app_zpinfo where lower(job) like '%%%s%%' and working_place like '%%%s%%'" % (key.lower(), city)
                la.append(self.sqlHelper.tupleToOther(self.sqlHelper.executeSql(sql)))
            best_city = app_citys[la.index(max(la))]
            return json.dumps(self.city_list_dict(la, app_citys)), best_city, value