#!/usr/bin/env python
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
	if par == 'appstore':
		xmlfile = 'ServerPatchConfig_APPSTORE.xml'
	return xmlfile

def select_status(status):
	if status == 'start':
		runshell = 'start_release.sh'
	if status == 'stop':
		runshell = 'stop_release.sh'
	return runshell

def remote_run(ip,zone,mxmshell):
	username = 'root'
	port = 10090
	## password = 'guaiwu_Yunwei;{}' + ip.split('.')[3]
	keyfile = '/root/.ssh/id_rsa'
	key = paramiko.RSAKey.from_private_key_file(keyfile)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname = ip,port = port,username = username,pkey = key)
	stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;./%s" % (zone,mxmshell))
	## stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;ls" % (zone))
	##print stdout.read()
	ssh.close()

if len(sys.argv) == 3 and (sys.argv[1] == 'android' or sys.argv[1] == 'ios' or sys.argv[1] == 'appstore') and (sys.argv[2] == 'start' or sys.argv[2] == 'stop'):
	print ("%s %s 所有游戏区..." % (sys.argv[2],sys.argv[1]))
else:
	print ("参数不对...")
	print ("参数1 为 game 平台(格式: android or ios or appstore)")
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
	t = threading.Thread(target=remote_run,args=(ServerIP_manager,Zone,runshell))
	t.start()

	#remote_run(ServerIP_manager,Zone,runshell)
	#time.sleep(0.1)
	
	## remote_run(ServerIP_manager,Zone,runshell)
	print ("%s mxm%s runing %s done... " % (ServerIP_manager,Zone,runshell))
	## time.sleep(0.1)
