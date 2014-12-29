# -*- coding: utf-8 -*-
#### 全区启动...

import os
import sys
import re
import time
import threading
import xml.dom.minidom
import paramiko

def select_gamepar(par):
	if par == 'android':
		xmlfile = 'ServerPatchConfig.xml'
	if par == 'ios':
		xmlfile = 'ServerPatchConfig_IOS.xml'
	return xmlfile

def select_status(status):
	if status == 'start':
		runshell = 'start_release.sh'
	if status == 'stop':
		runshell = 'stop_release.sh'
	return runshell

def remote_run(ip,zone,mjshell):
	username = 'root'
        if len(ip.split(".")[-1])==3:
	 port=int("1009"+ip.split(".")[-1][0])
        else:
	 port = 10090
	password = "fangcun#13MJ()" + ip.split(".")[-1]
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname = ip,port = port,username = username,password = password)
	stdin,stdout,stderr = ssh.exec_command("cd /mj/mj%s/bin;./%s" % (zone,mjshell))
	## stdin,stdout,stderr = ssh.exec_command("cd /mj/mj%s/bin;ls" % (zone))
	## print stdout.read()
	ssh.close()

if len(sys.argv) == 3 and (sys.argv[1] == 'android' or sys.argv[1] == 'ios') and (sys.argv[2] == 'start' or sys.argv[2] == 'stop'):
	print ("%s %s 所有游戏区..." % (sys.argv[2],sys.argv[1]))
else:
	print ("参数不对...")
	print ("参数1 为 game 平台(格式: android or ios)")
	print ("参数2 为进程状态(格式: start or stop)")
	sys.exit(0)

xmlpath = '/root/packet/server_patch/'
xmlfile = select_gamepar(sys.argv[1])
### 判断 start or stop
runshell = select_status(sys.argv[2])
print runshell
dom = xml.dom.minidom.parse('%s%s' % (xmlpath,xmlfile))
xmllist = dom.documentElement
serverlist = xmllist.getElementsByTagName("serverInfo")
for i in serverlist:
	## print i
	Zone = i.getAttribute("Zone")
	ServerIP_manager = i.getAttribute("ServerIP_manager")
	print ServerIP_manager + " ---- " + Zone

	### 调用远程执行
	print ("\n -------现在执行-----------")
	## 线程执行
	## t = threading.Thread(target=remote_run,args=(ServerIP_manager,Zone,runshell))
	## t.start()

	remote_run(ServerIP_manager,Zone,runshell)
	time.sleep(0.1)
	
	## remote_run(ServerIP_manager,Zone,runshell)
	print ("%s mj%s runing %s done... " % (ServerIP_manager,Zone,runshell))
	## time.sleep(0.1)
