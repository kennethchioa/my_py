#!/bin/sh
# -*- coding: utf-8 -*-
#### 多线程程并发执行恢复数据库

import os
import sys
import re
import time
import Queue
import threading


def listdir(date):
	files = []
	androidlist = []
	ioslist = []
	appstorelist = []

	list = os.listdir('/root/log/%s' % date)
	## print list
	for line in list:
		if re.search('tar.gz',line):
			files.append(line)

	for pack in files:
		if re.search('ios',pack,re.I):
			ioslist.append(pack)
		elif re.search('appstore',pack,re.I):
			appstorelist.append(pack)
		else:
			androidlist.append(pack)

	return files,androidlist,ioslist,appstorelist

def selectscript(date,gamepar):
	### 获取游戏平台数据库包
	(files,androidlist,ioslist,appstorelist) = listdir(date)
	if gamepar == 'android':
		packlist = androidlist
		print ("导入 android 的游戏区包...")
	if gamepar == 'ios':
		packlist = ioslist
		print ("导入 ios 的游戏区包...")
	if gamepar == 'appstore':
		packlist = appstorelist
		print ("导入 appstore 的游戏区包...")

	return packlist

def importscript(par):
	if par == "android":
		importscript = 'recover_backup_dbfile.py'
	if par == "ios":
		importscript = 'recover_backup_dbfile_IOS.py'
	if par == "appstore":
		importscript = 'recover_backup_dbfile_APPSTORE.py'
	
	return importscript

### 线程执行
class Threadrun(threading.Thread):
	def __init__(self,date,script,queue):
		 threading.Thread.__init__(self)
		 self.date = date
		 self.script = script
		 ## self.pack = pack
		 self.queue = queue

	def run(self):
		while True:
			if self.queue.empty():
				break
			foo = self.queue.get()
			os.chdir("/root/log/%s" % (self.date))
			os.system("python %s /root/log/%s %s" % (self.script,self.date,foo))
			## print ("cd /root/log/%s" % (self.date))
			## print ("python %s /root/log/%s %s" % (self.script,self.date,foo))
			print self.getName(),':', foo
			time.sleep(2)
			self.queue.task_done()

def importdb(date,gamepar):
	script = importscript(gamepar)
	packlist = selectscript(date,gamepar)

#	print script
#	print packlist

	queue = Queue.Queue()
	for pack in packlist:
		queue.put(pack)
	for num in range(5):
		## os.chdir("/root/log/%s" % (date))
		## os.system("python %s /root/log/%s %s" % (script,date,pa))
		## print ("cd /root/log/%s" % (date))
		## print ("python %s /root/log/%s %s" % (script,date,pa))
		print 'Thread' + str(num)
		t = Threadrun(date,script,queue)
		t.start()
		## t = threading.Thread(target=runpro,args=(date,script,pa))
		## t.start()
		## time.sleep(2)
	queue.join()


if len(sys.argv) == 3 and re.match('\d\d\d\d-[0-1]\d-[0-3]\d','%s' % (sys.argv[1])) != None and (sys.argv[2] == 'android' or sys.argv[2] == 'ios' or sys.argv[2] == 'appstore'):
	print ("执行备份恢复...")
else:
	print ("参数不对...")
	print ("参数1 为时间 (格式为: %s)" % (time.strftime('%Y-%m-%d')))
	print ("参数2 为 game 平台(格式: android or ios or appstore)")
	sys.exit(0)

importdb(sys.argv[1],sys.argv[2])
## (files,androidlist,ioslist) = listdir(sys.argv[1])
