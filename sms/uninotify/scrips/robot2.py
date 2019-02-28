#!/usr/bin/python
#coding:utf-8
import requests
import json
import MySQLdb
import time
import datetime
import sys

def SEARCH(projeck):
    #date = time.strftime('%Y-%m-%d ',time.localtime(time.time())) 
    #date = date - datetime.timedelta(days=1)    
    today = datetime.date.today()
    date = today - datetime.timedelta(days=1)
    #date = today 
    #date = datetime.date.today()
    #projeck_list = ['url','sanguo','sg2','hhw','daomu','vnsg2','thsg2','twsg2','jpsg2','bdx','dasheng','match','krsg2','tw-sg','fkdwc','shipgirl'] 

    db = MySQLdb.connect("192.168.7.74","rd","admin","uninotify")
    cursor = db.cursor()
    #sql = "select *,from_unixtime(created) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
    #sql1 = "select count(*) from notify_log_success where from_unixtime(created) like '%%%s%%' and tag = 'zabbixNone'"%(date)
    sql_projeck = "select count(*) from notify_log_success  where from_unixtime(created) like '%%%s%%' and  tag = 'zabbixNone' and msg like  '%%%s%%'"%(date,projeck)
    cursor.execute(sql_projeck)
    data = cursor.fetchall()[0][0]
    db.close()
    return data

if __name__ == "__main__":
	project= sys.argv[1]
	print SEARCH(project)

