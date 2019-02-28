#!/usr/bin/python
#coding:utf-8

from flask import Flask,jsonify
from flask import request

app = Flask(__name__)
import json
import requests

import sys
import MySQLdb

import os
import re

import logging
import logging.handlers

def  get_hostid_ip(ip):
     sql = "select hostid from zabbix.interface where ip='%s'"%(ip)
     db = MySQLdb.connect("192.168.10.61","zabbix","zabbix","zabbix") 
     cursor = db.cursor()
     cursor.execute(sql)
     hostid = cursor.fetchall()[0][0] 
     db.close()
     return  hostid

def  get_hostname(hostid):
     sql = "select ip from zabbix.interface where hostid='%s'"%(hostid)
     db = MySQLdb.connect("192.168.10.61","zabbix","zabbix","zabbix") 
     cursor = db.cursor()
     cursor.execute(sql)
     ip = cursor.fetchall()[0][0] 
     db.close()
     return  "%s"%(ip)


def get_hostname1(hostid):
     sql = "select host from zabbix.hosts where hostid='%s'"%(hostid)
     db = MySQLdb.connect("192.168.10.61","zabbix","zabbix","zabbix")
     cursor = db.cursor()
     cursor.execute(sql)
     host = cursor.fetchall()[0][0]
     db.close()
     return  "%s"%(host)

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
     result = result[0]
     hostid = result.get("hostid")
     return hostid

def get_trigger(hostname,triggername):
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
                "hostid": get_hostid(hostname),"description": triggername

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
    result = result[0]
    triggerid = result.get("triggerid")
    return triggerid

def change_status(hostname, service_name, status):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    print "----------------"
    change = json.dumps(
                {
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": {
                "hostid":get_hostid(hostname),
                "triggerid":get_trigger(hostname,service_name),
                "status": status
            },
            "auth": "e40f54a7efb0671b54073832e51693de",
            "id": 1
            }
            )

    e = requests.post(url, data=change, headers=headers)

def change_status1(hostid, triggerid, status):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    change = json.dumps(
                {
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": {
                "hostid":hostid,
                "triggerid":triggerid,
                "status": status
            },
            "auth": "e40f54a7efb0671b54073832e51693de",
            "id": 1
            }
            )

    e = requests.post(url, data=change, headers=headers)
def check_status(hostname,service_name):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    change = json.dumps(
                {
                        "jsonrpc": "2.0",
                        "method": "trigger.get",
                        "params": {
                            "host": hostname,
                            "output": "extend",
                            "filter": {
                                      "description": [
                                         service_name 
                                      ]

                                  }
                },
                "auth": "e40f54a7efb0671b54073832e51693de",
                "id": 1
                }
                )
    e = requests.post(url, data=change, headers=headers)
    return e.text

def get_host_triggerid(hostid):
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    change = json.dumps(
               {
                   "jsonrpc": "2.0",
                   "method": "trigger.get",
                   "params": {
                        "hostids": hostid,
                        "output": "extend"
                    },
                   "auth": "e40f54a7efb0671b54073832e51693de",
                   "id": 1
               }
        )
    e = requests.post(url, data=change, headers=headers)
    result1 = e.text
    result1 = result1.encode("utf-8")
    result1=eval(result1)
    result = result1.get("result")
    dic = {}
    for h in result:
        dic[h['description']] = h['triggerid']
    return dic


def loger(ip,hostname, servicename, action):
    msg = "%s : %s: %s : %s"%(ip, hostname, servicename, action)
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    
    logging.basicConfig(filename='zabbix.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
    
    logging.info(msg)

@app.route('/api',methods=['POST','GET'])
def login():
    try:
    	hostname = request.form.get('hostname',default=None)
    	service_name = request.form.get('service_name',default=None)
    	action = request.form.get('action',default=None)
    	url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    	headers = {'content-type': 'application/json'}
    	
	if  action != "start" and action != "stop" and action != "status":
	    loger(request.remote_addr,hostname,service_name,action)
	    result = {"status": 1,"msg": 'fail',"data":"Null"}
            return json.dumps(result)

	if hostname is None:
           hostid = get_hostid_ip(request.remote_addr)
	   hostname = get_hostname1(hostid)
           triggeridlist = []
           for servicename,triggerid in get_host_triggerid(hostid).items():
		if re.search('disk',servicename) is not  None:
		   continue 
		if re.search('load',servicename) is not  None:
		   continue 
		if re.search('walle',servicename) is not  None:
		   continue 
		if re.search('{HOST.NAME}',servicename) is not  None:
		   continue 
		if re.search('服务器',servicename) is not  None:
		   continue 
		if re.search('mem-check',servicename) is not  None:
		   continue 
		if re.search('u670d',servicename) is not  None:
		   continue 
		if re.search('SE',servicename) is not  None:
		   continue 
		tirgger_status=check_status(hostname,servicename)

        	tirgger_status = json.loads(tirgger_status)
        	tirgger_status = str(tirgger_status['result'][0]['status'])
		test="enabled"
        	if tirgger_status == "1":
           		test="disabled"
                change_status1(hostid,triggerid,0)
		triggeriddic={"hostname":hostname,"servicename":servicename,"status":test}
		triggeridlist.append(triggeriddic)
	   
	   status_code = 0
           msg = "success"
	   result = {
                        "status": status_code,
                        "msg": msg,
                        "data":triggeridlist

                 }
	   loger(request.remote_addr,hostname,service_name,action)

           return json.dumps(result)

 	f = open("./whilelist","r")
	whilelist = []
	for ipaddr in f.readlines():
		ipaddr = ipaddr.strip('\n')
		whilelist.append(ipaddr)
	f.close()

	#whilelist.append(request.remote_addr)
	
	status = 0 
    	ip  = get_hostname(get_hostid(hostname)) 

	#print 'ip',ip,'request.remote_addr',request.remote_addr
	if request.remote_addr != ip:
	    status = 1
    	
	if request.remote_addr not  in whilelist:
            status = 1
	else:
	    status = 0

	if  action != "start" and action != "stop" and action != "status":
            status = 1

    	action_code = 0
    	if action == "stop":
    	    action_code = 1

	if status == 1:
           result = {"status": 1,"msg": 'fail',"data":"Null"}
           return json.dumps(result)
	
	if action == "status":
           check_status(hostname,service_name)
	else:
	   change_status(hostname,service_name, action_code)




	tirgger_status=check_status(hostname,service_name)

	tirgger_status = json.loads(tirgger_status)
	tirgger_status = str(tirgger_status['result'][0]['status'])
	
	print tirgger_status,type(tirgger_status)
	print "1",type("1")
	test="enabled"
	if tirgger_status == "1":
	   test="disabled"
	status_code = 0
	msg = "success"
	result = {
			"status": status_code,
			"msg": msg,
			"data":{
				  "status":test,
				  "hostname":"%s"%(hostname),
				  "servicename":"%s"%(service_name)
			       }
			
		 }	
	loger(request.remote_addr,hostname,service_name,action)
	return json.dumps(result)
    except Exception, e:
	print e
	loger(request.remote_addr,hostname,service_name,action)
	result = {"status": 1,"msg": 'fail',"data":"Null"}
	return json.dumps(result)

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.errorhandler(404)
def errorhandler(e):
    result = {"status": 1,"msg": 'fail',"data":"Null"}
    return json.dumps(result)    
@app.route("/status", methods=["POST"])
def get_host_status():
    hostname = request.form['hostname']
    service_name = request.form['service_name'] 
    
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    change = json.dumps(
	{
    		"jsonrpc": "2.0",
    		"method": "trigger.get",
    		"params": {
    		    "host": hostname,
    		    "output": "extend",
    		    "filter": {
    		              "description": [
    		                  service_name
    		              ]

    		          }
        },
    	"auth": "e40f54a7efb0671b54073832e51693de",
    	"id": 1
	}
	)
    e = requests.post(url, data=change, headers=headers) 
    status=json.loads(e.text)
    status = status['result'][0]['status']
    return status

if __name__ == "__main__":
	
    app.run(host= '192.168.9.11', port = 9000,debug = True)




