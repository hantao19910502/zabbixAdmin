#!/usr/bin/env  python
#coding:utf

# Create your views here.
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate
from django.http.response import HttpResponse
import MySQLdb
import time
import html_helper
def SELECT(request):
    db = MySQLdb.connect("192.168.7.74","rd","admin","uninotify")
    cursor = db.cursor()
    cursor.execute("select * from notify_log_success limit 2")
    data = cursor.fetchall()
    ret = []
    for item in data:
	timeArray = time.localtime(item[6])
	otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        DATA={ 'to':item[1].strip('[').strip(']'),'msg':item[2],'appid':item[3],'type':item[4],'ip':item[5],'created':otherStyleTime,'tag':item[7],'sum_num':item[8],'result':item[9]}
	ret.append(DATA)
	#print item[1].strip('[').strip(']'),item[3],item[4]
    #print "Database version : %s " % data
    #version = "Database version : %s " % data
    db.close()
    ret1 = {'result':ret}
    return render_to_response('sms/zhanshi.html',ret1)
    #return HttpResponse('OK')

def SEARCH(request,page):
    #localtime = time.strftime('%Y-%m-%d ',time.localtime(time.time())) 
    try:
        page = int(page)
    except Exception, e:
        page = 1
    per_item = 50
    start = (page - 1) * per_item
    end = page * per_item
    date = request.POST.get('date', None)
    #date = str(date)
    #print type(date)
    #print date
    #tm = time.strptime(date, '%Y-%m-%d')
    #timeArray = time.strptime(date, "%Y-%m-%d")
    #timeStamp = int(time.mktime(timeArray))
     
    db = MySQLdb.connect("192.168.7.74","rd","admin","uninotify")
    cursor = db.cursor()
    sql = "select *,from_unixtime(created) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
    sql1 = "select count(*) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.execute(sql1)
    data1 = cursor.fetchall()[0][0] 
    ret = []
    for item in data:
        timeArray = time.localtime(item[6])
        otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        DATA={ 'to':item[1].strip('[').strip(']'),'msg':item[2],'appid':item[3],'type':item[4],'ip':item[5],'created':item[10],'tag':item[7],'sum_num':item[8],'result':item[9]}
        ret.append(DATA)
    db.close()
    All_list = len(ret)
    ret = ret[start:end]
    all = divmod(All_list, per_item)
    if all[1] == 0:
       all_page_count = all[0]
    else:
       all_page_count = all[0] + 1
    page_string = html_helper.Pager(page, all_page_count)
    ret1 = {'result':ret,'page': page_string,'count':data1,'localtime':date}
    return render_to_response('sms/zhanshi.html',ret1)

def timeStamp(timeStamp):
    date =  time.localtime(timeStamp)
    date = time.strftime("%Y-%m-%d", date)
    return date

def LIULIANG(request):
    localtime1 = time.strftime('%Y-%m-%d ',time.localtime(time.time())) 
    localtime1 = localtime1.split("-")
    localtime1 = localtime1[0]+localtime1[1]+localtime1[2]
    projeck_list = ['sanguo','sg2','hhw','daomu','vnsg2','thsg2','twsg2','jpsg2','bdx','dasheng','match','krsg2','tw-sg','fkdwc','shipgirl'] 
    #ret = {'result':[{'dt':'20180801','data':100}]}
    if request.method == 'GET':
       #stat = 1533081600 
       stat = 1533052800 
       date = timeStamp(stat)
       localtime = time.strftime('%Y-%m-%d ',time.localtime(time.time()))
       #tod = '%s 00:00:00'%(localtime)
       #timeArray = time.strptime(tod, "%Y-%m-%d %H:%M:%S")
       #timeStamp1 = int(time.mktime(timeArray))
       timeStamp1 = 1542902400
       print 'stat:',stat,'timeStamp1:',timeStamp1
       db = MySQLdb.connect("192.168.7.74","rd","admin","uninotify")
       cursor = db.cursor()
       result = []
       while stat <= timeStamp1:   
           projeck_num = {}
           for projeck in projeck_list:
	   	sql_projeck = "select count(*) from notify_log_success  where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone' and msg like  '%%%s%%'"%(date,projeck)
           	cursor.execute(sql_projeck)
           	data = cursor.fetchall()[0][0]

           	projeck_num[projeck] = data
       	   	#sql = "select *,from_unixtime(created) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
	   print 'projeck_num:',projeck_num
       	   sql1 = "select count(*) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
       	   cursor.execute(sql1)
       	   data1 = cursor.fetchall()[0][0] 
           #timeStamp1 = timeStamp1 - 86400
	   date = date.split("-")
	   print date
	   date = date[0]+date[1]+date[2]
           print date
           ret1 = {"dt":date,"data1":data1,"projeck_num":projeck_num}
	   print 'ret1:',ret1
           result.append(ret1)
	   print 'result:',result
	   stat = stat + 86400
           date = timeStamp(stat)
       	   #result.append({'projeck_num':projeck_num})
       #projeck_num1 = {}
       #for projeck in projeck_list:
       #         sql_projeck = "select count(*) from notify_log_success  where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone' and msg like  '%%%s%%'"%(date,projeck)
       #         cursor.execute(sql_projeck)
       #         data = cursor.fetchall()[0][0]

       #         projeck_num1[projeck] = data
       #sql1 = "select count(*) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
       #cursor.execute(sql1)
       #data1 = cursor.fetchall()[0][0]
       ##
       #result.append({'dt':localtime1,'data':data1,"projeck_num1":projeck_num1})
       db.close()
       ret = {"result":result,"projeck_list":projeck_list}
       print ret
       return render_to_response('sms/liuliang.html',ret)
    return render_to_response('sms/liuliang.html')



def event_acknowledge(request, token , hostname , eventids):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    #uri = request.get_full_path()   
    #url = "192.168.2.199:8000/%s"%(uri)
    key="BabelTime"
    if request.method == 'POST':
        eventids = request.POST.get('eventids', None)
        info = request.POST.get('info', None)
        print info

        #hostname = hostnane.encode("utf8").strip("\n").split()
        set_acknowledge = json.dumps(
                {
                  "jsonrpc": "2.0",
                  "method": "event.acknowledge",
                  "params": {
                      "eventids": eventids,
                      "message": "%s"%(info)
                  },
                  "auth": "e40f54a7efb0671b54073832e51693de",
                  "id": 1
              }
        )
        e = requests.post(url, data=set_acknowledge, headers=headers)
        result1 = e.text
        return render_to_response('web/success.html')
    user_token=generate_token(key=key)
    if not user_token:
       return "error"
    else:
       ret = {'eventids':eventids, 'hostname':hostname}
       return render_to_response('web/acknowledge.html',ret)
