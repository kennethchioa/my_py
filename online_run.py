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

def run(plt):
    xml_file = select_xml(plt)
    all_list = get_All_ZoneID_and_IP(xml_file)
    for zone in all_list.keys():
        conn = "mysql -umxm -pmxm@Yun@wei -h%s -Dmxm%s_log -e" % (all_list[zone],str(zone))
#       run_cmd = "\"delete from character_activity where activity_id=156;\"" 
        sql_cmd="\"select b.item_id,count(b.change_number) from log_context_relationship a ,item_change_log b where a.log_id = b.id and context_type=3 and log_type=0 and change_number >0 and b.item_id in (61100,61101,61102,61103) group by item_id;\""
        print  "mxm%s" % str(zone)
#       os.system (conn + " " + run_cmd)
#       print conn + " " + sql_cmd
        os.system (conn + " " + sql_cmd)


if __name__=="__main__":
    if len(sys.argv) == 2 and \
    (sys.argv[1] in ['android','ios','appstore']):
        print (" Starting......")
        try:
            run(sys.argv[1])
        except:
            sys.exit(1)
    else:
        print ("Paramerer Wrong!!...")
        print ("Parameter1 (format: Plantform: android or ios or appstore)")
        sys.exit(0)
