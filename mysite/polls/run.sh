#!/bin/bash

run_num=`ps -ef |grep  trigger_switch | grep -v grep | awk '{print $2}' | wc -l`

if [[ $run_num -eq 0 ]];then
	cd /home/pirate/optool/mysite/polls/ && nohup python trigger_switch.py   >> myout.file 2>&1 &
else
	/bin/ps -ef |grep  trigger_switch | grep -v grep | awk '{print $2}'  | xargs kill -9 &>/dev/null
	cd /home/pirate/optool/mysite/polls/ && nohup python trigger_switch.py   >> myout.file 2>&1 &
fi
