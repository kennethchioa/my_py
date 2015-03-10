#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author kenneth.chioa
#date 2015-01-30


import os
import sys
import re
import time
import Queue
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

def getAllZoneID(xml_file):
    resList = []
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    serverlist=root.getElementsByTagName("serverInfo")
    for serverID in serverlist:
        zoneID = serverID.getAttribute("Zone");
        resList.append(zoneID)
    return resList;

def auto_split(plt):
    xml_file = select_xml(plt)
    split_list =  getAllZoneID(xml_file)

    return split_list



### Threading run
class Threadrun(threading.Thread):
    def __init__(self,path,script,func,queue):
         threading.Thread.__init__(self)
         self.path = path
         self.script = script
         self.func = func
         self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                break
            foo = self.queue.get()
            os.chdir("%s" % (self.path))
            print self.getName(),':', foo
            print ("fab -f %s %s:%s" % (self.script,self.func,foo))
            time.sleep(2)
            self.queue.task_done()

def thunder_fab(plt,func):
    Threading_Count = 10
    path = '/root/packet/server_patch'
#   func = 'update_server'
    script = select_fab_script(plt)
    split_list = auto_split(plt)
    queue = Queue.Queue()
    for lst in split_list:
        print lst
        queue.put(str(lst))
    for th_num in range(Threading_Count):
        print 'Thread' + str(th_num)
        t = Threadrun(path,script,func,queue)
        t.start()
    queue.join()

if __name__=="__main__":
    if len(sys.argv) == 3 and \
    (sys.argv[1] in ['android','ios','appstore']) and \
    (sys.argv[2] in ['update_server']):
        print (" Starting......")
        try:
            thunder_fab(sys.argv[1],sys.argv[2])
        except:
            sys.exit(1)
    else:
        print ("Paramerer Wrong!!...")
        print ("Parameter1 (format: Plantform: android or ios or appstore)")
        print ("Parameter2 (format: Fuction: update_server or hello)")
        sys.exit(0)
