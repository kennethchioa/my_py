import os
import sys
import re
import time
import Queue
import threading
import xml.dom.minidom


def getAllZoneID_IP(xml_file):
    resList = {}
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    serverlist=root.getElementsByTagName("serverInfo")
    for serverID in serverlist:
        zoneID = serverID.getAttribute("Zone");
        zoneIP = serverID.getAttribute("ServerIP_manager");
        resList[int(zoneID)] = str(zoneIP)
    return resList

a = getAllZoneID_IP('ServerPatchConfig.xml')
for i in a:
   b= [i,a[i]]
   print b[0]
