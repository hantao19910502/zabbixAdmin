#!/usr/bin/python
#coding:utf-8
import urllib,urllib2,cookielib
from sys import argv

#print '''
#	1.Zabbix agent on {HOST.NAME} is unreachable for 3 minutes
#	2.{HOST.NAME} has just been restarted
#'''
#INPUT = input("input:")

#if INPUT == 1:
#   zabbix_trigger_name = "Zabbix agent on {HOST.NAME} is unreachable for 3 minutes"
#if INPUT == 2:
#   zabbix_trigger_name = "{HOST.NAME} has just been restarted"
#if INPUT == 3:
#   zabbix_trigger_name = "baidu"
#

zabbix_trigger_name = argv[1]
url = 'http://192.168.9.11:8088/polls/api?' 
headers = {
   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
headers = {'User-agent':'Mozilla/5.0'}
url_args = urllib.urlencode({ 
                            "zabbix_trigger_name":"%s"%(zabbix_trigger_name),
			    }) 

urls = '%s%s' %(url,url_args)
req = urllib2.Request(url=urls,headers=headers)
result_str =  urllib2.urlopen(req).read()
str = urllib2.urlopen(req).readlines()[0].strip('[').strip(']').strip('(').strip(')').split(',')[0]
print str.split("'")[1]
