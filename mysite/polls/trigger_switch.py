from flask import Flask,jsonify
from flask import request

app = Flask(__name__)
import json
import requests

import sys
import MySQLdb

import os
import logging

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

def loger(ip,hostname, servicename, action):
    msg = "%s : %s: %s : %s"%(ip, hostname, servicename, action)
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

    logging.basicConfig(filename='zabbix.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    logging.info(msg)

@app.route('/api',methods=['POST','GET'])
def login():
    try:
    	json_data = {}
    	#json_data['hostname']= request.form['hostname']
    	json_data['hostname'] = request.form['hostname']
    	json_data['service_name']= request.form['service_name']
    	json_data['action']= request.form['action']
    	#print json_data
    	json_data['ip']  = request.remote_addr
    	url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    	headers = {'content-type': 'application/json'}
    	
    	#whilelist = ['172.31.0.55','172.31.0.16','172.31.0.16','172.31.0.6','172.31.0.18','172.31.0.41','172.31.0.51','172.31.0.56','172.31.0.43','172.31.0.49','172.31.0.39','172.31.0.24','172.31.0.17','172.31.252.135']
 	f = open("./whilelist","r")
	whilelist = []
	for ip in f.readlines():
		ip = ip.strip('\n')
		whilelist.append(ip)
	f.close()

    	ip = os.popen("/sbin/ifconfig eth0 | awk -F'[: ]+' 'NR==2{print $4}'").read()
    	ip = ip.split("\n")
    	whilelist.append(ip[0])

    	##print whilelist
    	if json_data['ip'] not  in whilelist or json_data['action'] != "start" and json_data['action'] != "stop" and json_data['action'] != "status": 
    	    json_data['status'] = 1
    	    #return jsonify(json_data)
	    loger(request.remote_addr,json_data['hostname'],json_data['service_name'],json_data['action'])
    	    return "1"
	print json_data['action']
	print "======================="
	if json_data['action'] == "status":
		change = json.dumps(
        	{
        	        "jsonrpc": "2.0",
        	        "method": "trigger.get",
        	        "params": {
        	            "host": json_data['hostname'],
        	            "output": "extend",
        	            "filter": {
        	                      "description": [
        	                          json_data['service_name']
        	                      ]

        	                  }
        	},
        	"auth": "e40f54a7efb0671b54073832e51693de",
        	"id": 1
        	}
        	)
		print 'change',change
    		e = requests.post(url, data=change, headers=headers)
    		status=json.loads(e.text)
    		status = status['result'][0]['status']
		loger(request.remote_addr,json_data['hostname'],json_data['service_name'],json_data['action'])
    		return status
    	action = 0
    	if json_data['action'] == "stop":
    	    action = 1

    	change = json.dumps(
    	        {
    	    "jsonrpc": "2.0",
    	    "method": "trigger.update",
    	    "params": {
    	        "hostid":get_hostid(json_data['hostname']),
    	        "triggerid":get_trigger(json_data['hostname'],json_data['service_name']),
    	        "status": action 
    	    },
    	    "auth": "e40f54a7efb0671b54073832e51693de",
    	    "id": 1
    	    }
    	    )
    	e = requests.post(url, data=change, headers=headers) 
    	#print "e",e
	loger(request.remote_addr,json_data['hostname'],json_data['service_name'],json_data['action'])
    	return "0" 
    except Exception, e:
	print e
	#loger(request.remote_addr,json_data['hostname'],json_data['service_name'],json_data['action'])
	return "1"

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200

@app.errorhandler(404)
def errorhandler(e):
    return '1'

if __name__ == "__main__":
	
    app.run(host= '192.168.9.11', port = 10000,debug = True)




