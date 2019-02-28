#!/usr/bin/python
#coding:utf-8

# Create your views here.
import sys

reload(sys) 
sys.setdefaultencoding('utf8')
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate
from django.http.response import HttpResponse
import sqlite3
import MySQLdb
import re
import html_helper

def polls(request):
    
    conn = sqlite3.connect('/home/pirate/opbak/zabbix_alert_alias')
    cursor = conn.cursor()
    sql = "select * from mapping"
    cursor.execute(sql)
    data1 = cursor.fetchall()
    zabbix_trigger_name_mapping = []
    for item in data1:
        zabbix_trigger_name = item[1]
        mapping = item[2]
        tmp = {'zabbix_trigger_name':zabbix_trigger_name,'mapping':mapping}
        zabbix_trigger_name_mapping.append(tmp)
    cursor.close()
    ret = {'zabbix_trigger_name_mapping':zabbix_trigger_name_mapping}
    #conn.close()
    print ret
    return render_to_response('polls/zhanshi.html',ret)    
    #return HttpResponse(ret)

def select_data(request,page1,page):
    #print 'page:',page
    try:
        page = int(page)
    except Exception, e:
        page = 1
    per_item = 50
    start = (page - 1) * per_item
    end = page * per_item

    zabbix_nanme = request.POST.get("zabbix_name", None)
    status = request.POST.get("status", None)


    #print 'zabbix_nanme:',zabbix_nanme
    #print 'status',status
    #print type(status)

    if status is  None:
       status = "4" 
    db = MySQLdb.connect("192.168.10.61","admin","BabelTime","zabbix")
    cursor = db.cursor()
    #cursor.execute("select description from triggers where status != 1 and state != 1 group by description ;")
    cursor.execute("select description   from triggers  where status != 1 and state != 1 and description not like '%disk-check[/home/pirate/dev/disk%' and description not like '%Switcher%' group by description")
    data = cursor.fetchall()
    old_list = []
    for item in data:
	 if zabbix_nanme is None:
	    old_list.append(item[0])
	 else: 
            if re.search(zabbix_nanme,item[0]):
	       old_list.append(item[0])
	    else:
	       continue
	 #print '-------------------' 
         #old_list.append(item[0])
    db.close()
	
    #print 'old_list',old_list
    #------------------------------------------------------
    conn = sqlite3.connect('/home/pirate/opbak/zabbix_alert_alias')
    cursor = conn.cursor()
    sql = "select * from mapping"
    cursor.execute(sql)
    data1 = cursor.fetchall()
    tmp = {}
    item_status = {}
    for item in data1:
	     
              zabbix_trigger_name = item[1]
              mapping = item[2]
	      if mapping is None:
 		 mapping = ""
	      if status is None:
		 tmp[zabbix_trigger_name] = mapping
                 item_status[zabbix_trigger_name] = item[3]
                 continue
	      if int(status.encode("utf-8")) == 4:
                 tmp[zabbix_trigger_name] = mapping
		 item_status[zabbix_trigger_name] = item[3]
		 continue
	      if int(status.encode("utf-8")) == item[0]:
		 tmp[zabbix_trigger_name] = mapping
                 item_status[zabbix_trigger_name] = item[3]
		 continue
	      if int(status.encode("utf-8")) == item[3]:
		 tmp[zabbix_trigger_name] = mapping
                 item_status[zabbix_trigger_name] = item[3]
                 continue
	    #  if int(status.encode("utf-8")) is not  None:
	    #      if int(status.encode("utf-8")) != item[3]:
	    #	      continue
	      if zabbix_nanme is not None:
                  if re.search(zabbix_nanme,item[2]) is not  None:
	             tmp[zabbix_trigger_name] = mapping
 	             item_status[zabbix_trigger_name] = item[3]
                     continue
	      #tmp[zabbix_trigger_name] = mapping
	      #item_status[zabbix_trigger_name] = item[3]
		 
    cursor.close()
    #print 'tmp:',tmp
    dic_fa = []
    for old_son in old_list:
	 if status is None:
             
             if tmp.has_key(old_son):
                continue
	     dic_sun = {}
             dic_sun['name'] = old_son
             alias = tmp.get(old_son)
             dic_sun['alias'] = alias
             dic_sun['status'] = 4 
             dic_fa.append(dic_sun)
	     continue
         if int(status.encode("utf-8")) == 0:

	    continue
	 if int(status.encode("utf-8")) == 1:  
            if tmp.get(old_son) is None:
                dic_sun = {}
                dic_sun['name'] = old_son
                alias = tmp.get(old_son)
                dic_sun['alias'] = alias
                dic_sun['status'] = 4
                dic_fa.append(dic_sun)
            continue
	 if int(status.encode("utf-8")) == 3:  
            if item_status.get(old_son) == 3:
                dic_sun = {}
                dic_sun['name'] = old_son
                alias = tmp.get(old_son)
                dic_sun['alias'] = alias
                dic_sun['status'] = 4
                dic_fa.append(dic_sun)
            continue
         if int(status.encode("utf-8")) == 4:
	     #if tmp.has_key(old_son):
             #   continue
	     dic_sun = {}
             dic_sun['name'] = old_son
             alias = tmp.get(old_son)
	     #print "=======================%s=========================%s"%(old_son,alias) 
             dic_sun['alias'] = alias
             dic_sun['status'] = 4
             dic_fa.append(dic_sun)
	 
    #print 'dic_fa:',dic_fa
    for k,v in tmp.items():
	  #if  zabbix_nanme is not None:
	  #    continue
    	  itemsStatus = item_status.get(k)
    	  d = {'name':k,'alias':v,'status':itemsStatus}
	  #print int(status.encode("utf-8")),item_status.get(k)
	  if int(status.encode("utf-8")) == item_status.get(k):
             
    	  	dic_fa.append(d)
		continue
    #print 'dic_fa:',dic_fa
    #if zabbix_nanme == "4":
    #    for k,v in tmp.items():
    #         itemsStatus = item_status.get(k)
    #         d = {'name':k,'alias':v,'status':itemsStatus}
    #         dic_fa.append(d)
    #All_list = len(dic_fa)
    #dic_fa = dic_fa[start:end]
    #all = divmod(All_list, per_item)
    #if all[1] == 0:
    #    all_page_count = all[0]
    #else:
    #    all_page_count = all[0] + 1
    #page_string = html_helper.Pager(page, all_page_count)
    #ret = {'result':dic_fa,'page': page_string}
    ret = {'result':dic_fa}
    return render_to_response('polls/zhanshi.html',ret)

def err_trigger(request):
    pass
    
    
def api(request):
    #zabbix_trigger_name = request.POST.get('zabbix_trigger_name',None)
    #mapping = request.POST.get('mapping',None)
    ##return HttpResponse({'zabbix_trigger_name':zabbix_trigger_name,'mapping':mapping}
    #return HttpResponse('OK')
    
    zabbix_trigger_name = request.GET['zabbix_trigger_name']
    conn = sqlite3.connect('/home/pirate/opbak/zabbix_alert_alias')
    cursor = conn.cursor()
    sql = "select mapping_name from mapping where zabbix_trigger_name = '%s'"%(zabbix_trigger_name)
    print sql
    cursor.execute(sql)
    data1 = cursor.fetchall()
    cursor.close()
    return HttpResponse(str(data1))

def edit(request,zabbix_trigger_name,mapping_name):
    ret = {'zabbix_trigger_name':zabbix_trigger_name,'mapping_name':mapping_name}
    if request.method == 'POST':
        zabbix_trigger_name = request.POST.get('zabbix_trigger_name', None)
        mapping_name = request.POST.get('mapping_name', None)
    	conn = sqlite3.connect('/home/pirate/opbak/zabbix_alert_alias')
    	cursor = conn.cursor()
    	sql = "insert into mapping (zabbix_trigger_name,mapping_name,status) values ('%s','%s',%s)"%(zabbix_trigger_name,mapping_name,0)
    	cursor.execute(sql)
    	data1 = cursor.fetchall()
    	conn.commit()
        #------------------------------------------------
	sql = "select * from mapping"
    	cursor.execute(sql)
    	data1 = cursor.fetchall()
    	zabbix_trigger_name_mapping = []
    	for item in data1:
    	    zabbix_trigger_name1 = item[1]
    	    mapping = item[2]
	    if mapping is None:
		mapping = ""
	    status = item[3]
    	    tmp = {'zabbix_trigger_name':zabbix_trigger_name1,'mapping':mapping,'status':status}
    	    zabbix_trigger_name_mapping.append(tmp)
    	#ret = {'result':zabbix_trigger_name_mapping}
    	cursor.close() 
	db = MySQLdb.connect("192.168.10.61","admin","BabelTime","zabbix")
    	cursor = db.cursor()
    	cursor.execute("select description   from triggers  where status != 1 and state != 1 and description not like '%disk-check[/home/pirate/dev/disk%' and description not like '%Switcher%' group by description")
    	data = cursor.fetchall()
    	old_list = []
    	for item in data:
    	    old_list.append(item[0])
    	db.close()
    	ret = {'result':old_list,'zabbix_trigger_name_mapping':zabbix_trigger_name_mapping}
        return render_to_response('polls/zhanshi.html',ret)
    return render_to_response('polls/edit.html',ret)
#------------------------------------------------------------------------
def  get_hostname(ip):
     sql = "select hostid from zabbix.interface where ip='%s'"%(ip)
     db = MySQLdb.connect("192.168.10.61","zabbix","zabbix","zabbix") 
     cursor = db.cursor()
     cursor.execute(sql)
     hostid = cursor.fetchall()[0][0] 
     db.close()
     return  hostid     

def  get_hostid(hostname):
     url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
     headers = {'content-type': 'application/json'}
     get_host = json.dumps(
          {
              "jsonrpc": "2.0",
              "method": "host.get",
              "params": {
                  "output": "extend",
                  "filter": {
                      "host": [
                          hostname,
                      ]
                  }
              },
              "auth": 'e40f54a7efb0671b54073832e51693de',
              "id": 1
          }
     )
     e = requests.post(url, data=get_host, headers=headers)
     result1 = e.text
     result1 = result1.encode("utf-8")
     result1 = eval(result1)
     result = result1.get("result")
     print result
     result = result[0]
     hostid = result.get("hostid")
     return hostid

def get_trigger(ip,triggername):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    get_trigger = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
            "output": [
                "triggerid"
            ],
            "filter": {
                "hostid": get_hostname(ip),"description": triggername

            },
            "sortorder": "DESC"
            },
            "auth": "e40f54a7efb0671b54073832e51693de",
            "id": 1
       }
    )
    e = requests.post(url, data=get_trigger, headers=headers)
    result1 = e.text
    result1 = result1.encode("utf-8")
    result1 = eval(result1)
    result = result1.get("result")
    print result
    result = result[0]
    triggerid = result.get("triggerid")
    return triggerid

def change_trigger_status(hostname,triggername,status):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    change = json.dumps(
        {
    "jsonrpc": "2.0",
    "method": "trigger.update",
    "params": {
        "hostid":get_hostid(hostname),
        "triggerid": get_trigger(hostname,triggername),
        "status": status
    },
    "auth": "e40f54a7efb0671b54073832e51693de",
    "id": 1
    }
    )

    e = requests.post(url, data=change, headers=headers)
    result1 = e.text

def trigger_adddependencies(ip,dependsOnTriggerid):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    triggername="服务器"
    adddependencies = json.dumps(
        {
         "jsonrpc": "2.0",
         "method": "trigger.adddependencies",
         "params": {
             "triggerid":get_trigger(ip,triggername),
             "dependsOnTriggerid": dependsOnTriggerid
         },
         "auth": "e40f54a7efb0671b54073832e51693de",
         "id": 1
     })
    e = requests.post(url, data=adddependencies, headers=headers)
    result1 = e.text
#def disable_trigger(environ,start_response):
#    def login():
#    json_data ={ 'success':'true' }
#    url = "http://35.200.48.182/api_jsonrpc.php"
#    headers = {'content-type': 'application/json'}
#    change = json.dumps(
#            {
#        "jsonrpc": "2.0",
#        "method": "trigger.update",
#        "params": {
#            "hostid":'10258',
#            "triggerid": '16318',
#            "status": 1
#        },
#        "auth": "519eb89b1471c6263f62d30da63af70d",
#        "id": 1
#        }
#        )
#
#    e = requests.post(url, data=change, headers=headers)
#    print "e",e
#    return jsonify(json_data)

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
