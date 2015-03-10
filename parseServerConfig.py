#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import os
import re
import sys
import xml.dom.minidom
import string
#从结点中得到特定子元素集合
def getElementZoneIP(zone_id):
	res = []
	dom = xml.dom.minidom.parse("ServerPatchConfig.xml")
	root = dom.documentElement
	serverlist=root.getElementsByTagName("serverInfo")
	for serverID in serverlist:
		tmpzoneid = serverID.getAttribute("Zone");   
		#print ("tmpzoneid"+tmpzoneid)
		strZoneID = "%i"%zone_id
		#print ("ZoneID"+d)         
		if tmpzoneid == strZoneID:
			res = serverID.getAttribute("ServerIP_zone")
			return res
       

def getElementManagerIP(zone_id):
	res = []
	dom = xml.dom.minidom.parse("ServerPatchConfig.xml")
	root = dom.documentElement
	serverlist=root.getElementsByTagName("serverInfo")
	for serverID in serverlist:
		tmpzoneid = serverID.getAttribute("Zone");   
		#print ("tmpzoneid"+tmpzoneid)
		strZoneID = "%i"%zone_id
		#print ("ZoneID"+d)         
		if tmpzoneid == strZoneID:
			res = serverID.getAttribute("ServerIP_manager")
			return res

#返回配置文件中不同的ip地址
def getAllDiffIP():
	resList = []
	dom = xml.dom.minidom.parse("ServerPatchConfig.xml")
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

def getAllZoneID():
	resList = []
	dom = xml.dom.minidom.parse("ServerPatchConfig.xml")
	root = dom.documentElement
	serverlist=root.getElementsByTagName("serverInfo")	
	for serverID in serverlist:
		zoneID = serverID.getAttribute("Zone");
		resList.append(zoneID)	
	return resList;
			
#返回配置文件中所有涉及到传入ip地址的zoneID
def getZoneIDList(ip):			
	resList = []
	dom = xml.dom.minidom.parse("ServerPatchConfig.xml")
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
