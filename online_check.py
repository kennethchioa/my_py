#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author kenneth.chioa
#date 2015-01-30


import os
import sys
import re
import time
import Queue
import paramiko
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

def online_run(zone_ip,zone_id,shell):
    username = 'root'
    port = 10090
	## password = 'guaiwu_Yunwei;{}' + ip.split('.')[3]
    keyfile = '/root/.ssh/id_rsa'
    key = paramiko.RSAKey.from_private_key_file(keyfile)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = zone_ip,port = port,username = username,pkey = key)
    stdin,stdout,stderr = ssh.exec_command(shell)
#	stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;sh %s" % (zone_id,shell))
	## stdin,stdout,stderr = ssh.exec_command("cd /mxm/mxm%s/bin;ls" % (zone_id))
    print  stdout.read()
    ssh.close()

def plantform_run(plt):
    xml_file = select_xml(plt)
    all_list = get_All_ZoneID_and_IP(xml_file)
    for zone in all_list.keys():
        print  "Platform:%s" % plt.upper() + " " + "IP:" +  str(all_list[zone])  + " " +  "ZONE:" + str(zone)
        check_version_shell = 'echo "Current Version is:`cat /mxm/mxm%s/server_patch/new_server_patch_packet/update_patch_list`"' % zone
        online_run(all_list[zone],zone,check_version_shell)

#def run(plt):
#    xml_file = select_xml(plt)
#    all_list = get_All_ZoneID_and_IP(xml_file)
#    for zone in all_list.keys():
#        conn = "ssh -p10090 %s \"" % all_list[zone]
##       run_cmd = "cat /mxm/mxm%s/server_patch/new_server_patch_packet/update_patch_list \""   %  zone
#        run_cmd = "grep CWBattle /mxm/mxm%s/conf/Zone*.conf \""   %  zone
##       run_cmd = "sed -i -e 's/ActivityInfo%s.dat/ActivityInfo.dat/g' /mxm/mxm%s/Gate*.conf /mxm/mxm%s/Manager.conf /mxm/mxm%s/Zone*.conf\""   %  (zone,zone,zone,zone)
##       print  conn + " " +run_cmd
#        print   "ip:" +  str(all_list[zone])  + " " +  "zone:" + str(zone)
##       print (conn   +  run_cmd)
#        os.system(conn +" " +  run_cmd)
#        print "\n"


if __name__=="__main__":
    if len(sys.argv) == 2 and \
    (sys.argv[1] in ['android','ios','appstore']):
        print (" Starting......")
        try:
            plantform_run(sys.argv[1])
        except:
            sys.exit(1)
    else:
        print ("Paramerer Wrong!!...")
        print ("Parameter1 (format: Platform: android or ios or appstore)")
        sys.exit(0)
