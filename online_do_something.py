#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#author kenneth.chioa
#date 2015-01-27

import os
import re
import sys 
import time
import threading
import xml.dom.minidom
import paramiko




def getZoneIDList( ip ):			
	resList = []
	dom = xml.dom.minidom.parse( cnf_name)
	root = dom.documentElement
	serverlist=root.getElementsByTagName("serverInfo")
	for serverID in serverlist:
		tmpip = serverID.getAttribute("ServerIP_zone");      
		if tmpip == ip:
			res = serverID.getAttribute("Zone")
			resList.append(res)
		else:
			tmpip = serverID.getAttribute("ServerIP_manager"); 	
			if tmpip == ip:
				res = serverID.getAttribute("Zone")
				resList.append(res)
	return resList			

def getAllDiffIP( cnf_name ):
	resList = []
	dom = xml.dom.minidom.parse( cnf_name )
	root = dom.documentElement
	serverlist=root.getElementsByTagName("serverInfo")
	for serverID in serverlist:
		zoneIP = serverID.getAttribute("ServerIP_zone");
		bFindZoneIP = False
		for res in resList:
			if res==zoneIP:
				bFindZoneIP = True
				break
		if bFindZoneIP == False:	
			resList.append(zoneIP)	
			
		managerIP = serverID.getAttribute("ServerIP_manager");
		bFindManagerIP = False
		for res in resList:
			if res==managerIP:
				bFindManagerIP = True
				break
		if bFindManagerIP == False:	
		 	resList.append(managerIP)	
	return resList	

def get_platform( plt ):
	if plt == 'android':
		xmlfilename = 'ServerPatchConfig.xml'
	if plt == 'ios':
		xmlfilename = 'ServerPatchConfig_IOS.xml'
	if plt == 'appstore':
		xmlfilename = 'ServerPatchConfig_APPSTORE.xml'
	return xmlfilename

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

def check_update_patch_list():
    for i in  getAllDiffIP():
#            run_cmd = "scp -P10090 %s cp /usr/local/nagios/etc/nrpe.cfg{,_bak}" % str(i)
             run_cmd = 'mysql -umxm -pmxm@Yun@wei -h%s "use mxm%s;select * from mail where g_cash=0 and m_cash=0 and item=0;"' % str(i,zone)
	         os.system( run_cmd )
#	    run_cmd = "ssh -p10090 %s \"pkill nrpe;/usr/local/nagios/bin/nrpe -c /usr/local/nagios/etc/nrpe.cfg -d\"" % str(i)

def main_do_list():
	if __name__=="__main__":
        if len(sys.argv) == 3 and (sys.argv[1] in ['android','ios','appstore']) and (sys.argv[2] in ['check','status']):
			get_platform(sys.argv[1])
	        print ("%s %s ..." % (sys.argv[2],sys.argv[1]))
        else:
	        print ("Wrong parameter!!!")
	        print ("paramerer1 game platform(format: android or ios or appstore)")
	        print ("paramerer2 Method List()")
	        sys.exit(0)
