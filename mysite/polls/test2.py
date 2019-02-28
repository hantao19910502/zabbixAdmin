from flask import Flask,jsonify
from flask import request

app = Flask(__name__)
import json
import requests

import sys
import MySQLdb

import os


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

@app.route('/api',methods=['POST','GET'])
def login():
    json_data = {}
    #json_data['hostname']= request.form['hostname']
    json_data['hostname'] = request.form['hostname']
    json_data['servername']= request.form['servername']
    json_data['switch']= request.form['switch']
    #print json_data
    json_data['ip']  = request.remote_addr
    url = "http://192.168.10.61:8088/zbx/api_jsonrpc.php"
    headers = {'content-type': 'application/json'}
    
    whilelist = ['172.31.0.16','172.31.0.16,172.31.0.6,172.31.0.18,172.31.0.41,172.31.0.51,172.31.0.56,172.31.0.43,172.31.0.55,172.31.0.49,172.31.0.39,172.31.0.24,172.31.0.17,172.31.252.135']
 
    ip = os.popen("/sbin/ifconfig eth0 | awk -F'[: ]+' 'NR==2{print $4}'").read()
    ip = ip.split("\n")
    whilelist.append(ip[0])
    
    ##print whilelist
    if json_data['ip'] not  in whilelist: 
        json_data['status'] = 1
        #return jsonify(json_data)
        return "1"
 
    switch = 0
    if json_data['switch'] == "stop":
	switch = 1

    change = json.dumps(
            {
        "jsonrpc": "2.0",
        "method": "trigger.update",
        "params": {
            "hostid":get_hostid(json_data['hostname']),
            "triggerid":get_trigger(json_data['hostname'],json_data['servername']),
            "status": switch 
        },
        "auth": "e40f54a7efb0671b54073832e51693de",
        "id": 1
        }
        )

    e = requests.post(url, data=change, headers=headers) 
    #print "e",e

    #return jsonify(json_data)
    return "0" 

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200
if __name__ == "__main__":
	
    app.run(host= '192.168.9.11', port = 7777,debug = True)
