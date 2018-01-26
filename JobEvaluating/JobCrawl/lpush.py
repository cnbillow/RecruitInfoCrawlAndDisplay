# coding:utf-8
import redis

try:
    r = redis.Redis(host='localhost', port=6379)
    r.lpush('baicai:start_urls', 'http://beijing.baicai.com/jobs/xiaoshoujingli/16799463/')
    r.lpush('chinahr:start_urls', 'http://www.chinahr.com/job/5149152252723715.html')
    r.lpush('wyjob:start_urls', 'http://jobs.zhaopin.com/000645187251845.htm')
    r.lpush('zlzp:start_urls', 'http://jobs.zhaopin.com/000645187251845.htm')
    print "压入url成功!"
except Exception:
    print "压入失败"