#!/usr/bin/python
#coding:utf-8
import requests
import json
import MySQLdb
import time
import datetime

def SEARCH():
    #date = time.strftime('%Y-%m-%d ',time.localtime(time.time())) 
    #date = date - datetime.timedelta(days=1)    
    today = datetime.date.today()
    date = today - datetime.timedelta(days=1)
    #date = today 
    #date = datetime.date.today()
    projeck_list = ['url','sanguo','sg2','hhw','daomu','vnsg2','thsg2','twsg2','jpsg2','bdx','dasheng','match','krsg2','tw-sg','fkdwc','shipgirl'] 

    db = MySQLdb.connect("192.168.7.74","rd","admin","uninotify")
    cursor = db.cursor()
    #sql = "select *,from_unixtime(created) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
    sql1 = "select count(*) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
    cursor.execute(sql1)
    data1 = cursor.fetchall()[0][0] 
    projeck_num = {}
    sum1 = 0
    for projeck in projeck_list:
    	sql_projeck = "select count(*) from notify_log_success  where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone' and msg like  '%%%s%%'"%(date,projeck)
        if projeck == 'sg2':
	   sql_projeck = "select count(*) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone' and msg like '%%%s%%' and msg like '%%yz%%'"%(date,projeck)
	cursor.execute(sql_projeck)
   	data = cursor.fetchall()[0][0]
        if data == 0:
           continue

	sum1 += data 
        projeck_num[projeck] = data

    sum1 = data1 - sum1
    projeck_num['other']= sum1
    db.close()
    return [data1,projeck_num]

def test():
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    change = json.dumps(
	{
		"jsonrpc": "2.0",
    		"method": "trigger.get",
    		"params": {
    		    "output": [
    		        "triggerid",
    		        "lastchange",
    		        "priority"
    		    ],            
    		    "monitored":1,    
    		    "skipDependent":1,        
    		    "sortfield": "lastchange",
    		    "limit":1001, 
    		    "only_true": 1
    		},                                         
    		"auth": "e40f54a7efb0671b54073832e51693de",
    		"id":1                                        
	  }
	)
    e = requests.post(url, data=change, headers=headers)
    result1 = e.text
    result1 = result1.encode("utf-8")
    result1=eval(result1)
    result = result1.get("result")
    Not_classified = []
    Information = []
    Warning = []
    Average = []
    High = []
    Disaster = []
    for h in result:
	if h['priority'] == "0":
	      Not_classified.append(h['triggerid'])
	if h['priority'] == "1":
	      Information.append('triggerid')
	if h['priority'] == "2":
	      Warning.append('triggerid')
	if h['priority'] == "3":
	      Average.append('triggerid')
	if h['priority'] == "4":
	      High.append('triggerid')
	if h['priority'] == "5":
	      Disaster.append('triggerid')
    dic = {"Not_classified":len(Not_classified),"Information":len(Information),"Warning":len(Warning),"Average":len(Average),"High":len(High),"Disaster":len(Disaster)}
    return dic

def POST1():
    #苏庆宾,王少峰,韩涛组
    #url = 'https://oapi.dingtalk.com/robot/send?access_token=dbdb7b79ed257530b98a1f818075d1f69efc32c6641b5e2f22d3ec9f91ceb535'
    #OPS-监控报警讨论组
    #url = 'https://oapi.dingtalk.com/robot/send?access_token=b4d6158fac9e6fde20163ce08d7347d37eef9f0860e7ee9656679c17bfcc3842'
    #运维部
    today = datetime.date.today()
    date = today - datetime.timedelta(days=1)
    #date = today 
    url = 'https://oapi.dingtalk.com/robot/send?access_token=8950183cf29b1d977c053dea1255bfb63f94700960ea5ffa3afa8fa1a905a09d'
    headers = {'content-type': 'application/json'}
    
    add_list = []
    DIC = test()
    for k,v in DIC.items():
         add_list.append('%s: %s \n\n >'%(k,v))
    STR = ''.join(add_list)

    #print 'STR:',STR
    d = json.dumps({
         "msgtype": "markdown",
         "markdown": {"title":"报警",
              		"text":"#### %s报警未处理数  \n > \n >%s  "%(date,STR)
          	     },
    		      "at": {
                      "atMobiles": [
                            "13717854786"
                      ],
                     }
 	})
    #print d

    r = requests.post(url, data=d,headers=headers)

    print r.text

def POST():
    #苏庆宾,王少峰,韩涛组
    #url = 'https://oapi.dingtalk.com/robot/send?access_token=dbdb7b79ed257530b98a1f818075d1f69efc32c6641b5e2f22d3ec9f91ceb535'
    #OPS-监控报警讨论组
    #url = 'https://oapi.dingtalk.com/robot/send?access_token=b4d6158fac9e6fde20163ce08d7347d37eef9f0860e7ee9656679c17bfcc3842'
    #运维部
    today = datetime.date.today()
    date = today - datetime.timedelta(days=1)
    #date = today 
    url = 'https://oapi.dingtalk.com/robot/send?access_token=8950183cf29b1d977c053dea1255bfb63f94700960ea5ffa3afa8fa1a905a09d'
    headers = {'content-type': 'application/json'}
    
    add_list = []
    for k,v in SEARCH()[1].items():
         add_list.append('%s: %s \n\n >'%(k,v))
    STR = ''.join(add_list)

    #print 'STR:',STR
    d = json.dumps({
         "msgtype": "markdown",
         "markdown": {"title":"报警",
              "text":"#### %s发出报警数  \n >总报警数:%s  \n >%s  "%(date,SEARCH()[0],STR)
          },
    "at": {
        "atMobiles": [
            "13717854786"
        ], 
        #"isAtAll": false
    }
 })
    #print d
    
    r = requests.post(url, data=d,headers=headers)
    
    print r.text
 
    #print d

POST()
POST1()
#print test()
#print SEARCH()

