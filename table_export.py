#!/usr/bin/env python
#encoding=utf8
import sys
import xml.dom.minidom
import string
import os
import tarfile
import shutil

mysql_bin="mysql -uroot -pfangcun@d.cn"
mysqldump_bin="mysqldump -uroot -pfangcun@d.cn"
cmd=mysql_bin + " -e\"show databases like 'mxmtmp%_log_2013-08-27'\" > 8_db_list.txt"
#print cmd
os.system(cmd)
count = len(open("8_db_list.txt").readlines())-1
fp = open("8_db_list.txt") 
currentCount = 1
for line in fp:
        content = line.replace('\n','')
        temp = content.split("tmp")
        if len(temp) != 2:
                continue
        print "export %s...(%d/%d)" % (content,currentCount,count)
        currentCount += 1
        cmd = "%s %s player_login  > %s%s_player_login.sql" % (mysqldump_bin,content,temp[0],temp[1]);
        print cmd
        #os.system(cmd)
        cmd = "%s %s petexp_change_log  > %s%s_petexp_change_log.sql" % (mysqldump_bin,content,temp[0],temp[1]);
        #os.system(cmd)