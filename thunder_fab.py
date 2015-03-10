#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author kenneth.chioa
#date 2015-01-30


'''
This script is written for 
multithreaded update/patch and restart

'''


import os
import sys
import re
import time
import Queue
import paramiko
import threading
import xml.dom.minidom


def select_fab_script(plt):
    if plt == "android":
        fab_script = 'fabfile.py'
    if plt == "ios":
        fab_script = 'fabfile_IOS.py'
    if plt == "appstore":
        fab_script = 'fabfile_APPSTORE.py'

    return fab_script

def select_xml(plt):
    if plt == "android":
        xml_file = 'ServerPatchConfig.xml'
    if plt == "ios":
        xml_file = 'ServerPatchConfig_IOS.xml'
    if plt == "appstore":
        xml_file = 'ServerPatchConfig_APPSTORE.xml'

    return  xml_file

def get_All_ZoneID_and_IP(xml_file):
    resDict = {}
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    serverlist=root.getElementsByTagName("serverInfo")
    for serverID in serverlist:
        zoneID = serverID.getAttribute("Zone");
        zoneIP = serverID.getAttribute("ServerIP_manager");
        resDict[int(zoneID)] = str(zoneIP)
    return resDict


def auto_split(plt):
    xml_file = select_xml(plt)
    split_dict = get_All_ZoneID_and_IP(xml_file)
    return split_dict

def remote_run(zone_ip,zone_id,shell):
    username = 'root'
    port = 10090
	## password = 'guaiwu_Yunwei;{}' + ip.split('.')[3]
    keyfile = '/root/.ssh/id_rsa'
    key = paramiko.RSAKey.from_private_key_file(keyfile)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = zone_ip,port = port,username = username,pkey = key)
    stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;sh %s" % (zone_id,shell))
#	stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;sh %s" % (zone_id,shell))
	## stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;ls" % (zone_id))
    print stdout.read()
    ssh.close()


### Threading run
class Threadrun(threading.Thread):
    def __init__(self,path,script,func,queue):
         threading.Thread.__init__(self)
         self.path = path
         self.script = script
         self.func = func
         self.queue = queue

    def run(self):
        if self.func == 'update_server':
            while True:
                if self.queue.empty():
                    break
                zone_id = self.queue.get()[0]
                os.chdir("%s" % (self.path))
                print self.getName(),':', zone_id
                os.system("fab -f %s %s:%s" % (self.script,self.func,zone_id))
                time.sleep(2)
                self.queue.task_done()
        elif self.func == 'thunder_patch':
            while True:
                if self.queue.empty():
                    break
                zone_info = self.queue.get()
                zone_id = zone_info[0]
                zone_ip = zone_info[1]
                os.chdir("%s" % (self.path))
                print self.getName(),':', zone_id,zone_ip
                os.system("fab -f %s %s:%s" % (self.script,self.func,zone_id))
                remote_run(zone_ip,zone_id,"start_release.sh")
                time.sleep(2)
                self.queue.task_done()
            

def thunder_fab(plt,func):
    path = '/root/packet/server_patch'
    Threading_Count = 10
    script = select_fab_script(plt)
    split_dict = auto_split(plt)
    start = True
    queue = Queue.Queue()
    for dct in split_dict.keys():
        queue.put([str(dct),split_dict[dct]])
    for th_num in range(Threading_Count):
        print 'Thread' + str(th_num)
        t = Threadrun(path,script,func,queue)
        t.start()
    queue.join()

if __name__=="__main__":
    if len(sys.argv) == 3 and \
    (sys.argv[1] in ['android','ios','appstore']) and \
    (sys.argv[2] in ['update_server','thunder_patch']):
        print (" Starting......")
        try:
            thunder_fab(sys.argv[1],sys.argv[2])
        except:
            sys.exit(1)
    else:
        print ("Paramerer Wrong!!...")
        print ("Parameter1 (format: Plantform: android or ios or appstore)")
        print ("Parameter2 (format: Fuction: update_server or thunder_patch)")
        sys.exit(0)
