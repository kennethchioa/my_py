#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import sys
import xml.dom.minidom   
import string
import os
import tarfile
import shutil

GLOBAL_SERVER_IP = []
def checkCreateDir(dst_path):
	hasDstDir = os.path.exists(dst_path)
	if(hasDstDir == False):
		os.makedirs(dst_path)	



		
def copyFile(src_dir,dst_dir):
		for srcFile in os.listdir(src_dir): 
			 sourcefile_path = os.path.join(src_dir, srcFile)
			 if os.path.isfile(sourcefile_path):
#			 	print sourcefile
				if sourcefile_path.find("svn")<0:
					print "do file "+sourcefile_path
					print "do dst_dir "+os.path.join(dst_dir, srcFile)
			 		shutil.copy(sourcefile_path,os.path.join(dst_dir, srcFile))
			 else:	
			 	if os.path.isdir(sourcefile_path): 
			 		#print sourcefile_path
			 		#print dst_dir+"/"+srcFile	
			 		#checkCreateDir(dst_dir+"/"+srcFile) 
			 		#copyFile(sourcefile_path, dst_dir+"/"+srcFile)
			 		checkCreateDir(os.path.join(dst_dir, srcFile))
			 		copyFile(sourcefile_path, os.path.join(dst_dir, srcFile))
					


				
def choose_server_patch(zone_id,system_type):
	first_patch_file_name = ""
	smallest_version = 0
	root_path = "/hf/hf"+zone_id
#	root_path = "root/hf/hf"+zone_id;
	
	update_file_path = os.path.join(root_path,"server_patch")
	update_file_path = os.path.join(update_file_path,"new_server_patch_packet")
	
	#检测有没有更新日志文件
	update_patch_list_file = os.path.join(update_file_path, "update_patch_list")
	if os.path.isfile(update_patch_list_file):
		handle_update_file = open(os.path.join(update_file_path, "update_patch_list"), 'r')
		#last_line = []
		#fileList = handle_update_file.readlines()
		#for fileLine in fileList:
		#	if not fileLine:
		#		last_line = fileLine	
		#		break;
		last_patch_version = handle_update_file.readline()
		handle_update_file.close()
		first_patch_file_name = choos_patch_file(update_file_path,last_patch_version)
	else:	
		#handle_update_file = open(os.path.join(update_file_path, "update_patch_list"), 'w')
		#handle_update_file.close()
		first_patch_file_name = choos_patch_file(update_file_path,"0")
	
	#print "this time patch_file_name "+first_patch_file_name	
	return first_patch_file_name;
	#if not first_patch_file_name.strip():
	#	print "choos update tar file error"
	#	return IndexError
	
	#start_copy(root_path,update_file_path,first_patch_file_name,system_type)




	
def start_copy(root_path,patch_file_path,patch_file_name,system_type,zone_id):	
	#开始解压缩包
	print  root_path
	hasupdateTmpDir = os.path.exists(os.path.join(root_path,"updateTmp"))
	if(hasupdateTmpDir == True):
		print "remove "+os.path.join(root_path,"updateTmp")
		shutil.rmtree(os.path.join(root_path,"updateTmp"),True)
	checkCreateDir(os.path.join(root_path,"updateTmp"))
	tar = tarfile.open(os.path.join(patch_file_path,patch_file_name))
	names = tar.getnames()
	for name in names:
		tar.extract(name,path=root_path+"/updateTmp")	
			
	# bin
	#拷贝的目标位置是不是存在对应目录
	checkCreateDir(root_path+"/bin")
	#拷贝源是不是存在对应目录
	hasSrcPatchBinDir = os.path.exists(root_path+"/updateTmp/bin")
	if(hasSrcPatchBinDir == True):
		print os.listdir(root_path+"/updateTmp/bin")
		for srcFile in os.listdir(root_path+"/updateTmp/bin"): 
			sourcefile_path = os.path.join(root_path+"/updateTmp/bin", srcFile)
			print "sourcefile_path"+sourcefile_path
		copyFile(root_path+"/updateTmp/bin",root_path+"/bin")

	# inks
	#拷贝的目标位置是不是存在对应目录
	checkCreateDir(root_path+"/inks")
	#拷贝源是不是存在对应目录
	hasSrcPatchBinDir = os.path.exists(root_path+"/updateTmp/inks")
	if(hasSrcPatchBinDir == True):
		print os.listdir(root_path+"/updateTmp/inks")
		for srcFile in os.listdir(root_path+"/updateTmp/inks"): 
			sourcefile_path = os.path.join(root_path+"/updateTmp/inks", srcFile)
			print "sourcefile_path"+sourcefile_path
		copyFile(root_path+"/updateTmp/inks",root_path+"/inks")
		
# etc		
	checkCreateDir(root_path+"/etc")
	hasSrcPatchEtcIOSDir = os.path.exists(root_path+"/updateTmp/etc")
	if(hasSrcPatchEtcIOSDir == True):	
		copyFile(root_path+"/updateTmp/etc",root_path+"/etc")

# database
	checkCreateDir(root_path+"/database")
	hasSrcPatchDatabaseDir = os.path.exists(root_path+"/updateTmp/database")
	if(hasSrcPatchDatabaseDir == True):	
		copyFile(root_path+"/updateTmp/database",root_path+"/database")
	os.environ["mysql_bin"]="/usr/local/mysql/bin/mysql -umj -pfangcun#13MJ"
	print os.environ.get('mysql_bin')
	os.chdir(os.path.join(root_path,"database"))
	cmd = "python "+"installalldb.py"+" mj"+zone_id
	print cmd
	os.system( cmd )
	os.chdir("/root");
		
# conf		
	checkCreateDir(root_path+"/conf")
	hasSrcPatchEtcDir = os.path.exists(root_path+"/updateTmp/conf")
	if(hasSrcPatchEtcDir == True):	
		copyFile(root_path+"/updateTmp/conf",root_path+"/conf")		

	if os.path.isfile(os.path.join(root_path+"/updateTmp","run_once.py")):
		print "has run_once.py"	
		global GLOBAL_SERVER_IP
		cmd = "python "+os.path.join(root_path+"/updateTmp","run_once.py")+" "+zone_id+" "+GLOBAL_SERVER_IP
		print cmd
		os.system( cmd )
			




def choos_patch_file(patch_file_path,last_patch_version):
	print "last_patch_version "+last_patch_version
	smallest_version = 0
	first_patch_file_name = ""
	for patch_file in os.listdir(patch_file_path): 
		if patch_file.find("tar")<0:
			continue
		list_split_underline = patch_file.split('_')  #server_full_2013-03-05-4897.tar.gz
		#print list_split_underline   ['server', 'full', '2013-03-05-4897.tar.gz']
		list_split_dot = list_split_underline[-1].split('.')
		#print list_split_dot					['2013-03-05-4897', 'tar', 'gz']	
		list_split_midline = list_split_dot[0].split('-')
		#print list_split_midline			['2013', '03', '05', '4897']
		#patch_version = string.atol(list_split_midline[-1])
		patch_version = string.atol(list_split_midline[-1])+string.atol(list_split_midline[-2])*100000+string.atol(list_split_midline[1])*10000000+string.atol(list_split_midline[0])*1000000000
		if (patch_version<smallest_version or smallest_version == 0) and (patch_version>string.atol(last_patch_version)):
			smallest_version = patch_version
			first_patch_file_name = patch_file
	return first_patch_file_name



	
def update_all_server_patch(zone_id,system_type):
	root_path = "/hf/hf"+zone_id;
	#关闭进程
	dirpath = "/hf/hf"+zone_id+"/bin"
	os.chdir(dirpath)
	os.system("sh "+"./stop_release.sh");
	os.chdir("/root");
	
	update_file_path = os.path.join(root_path,"server_patch")
	update_file_path = os.path.join(update_file_path,"new_server_patch_packet")
	patch_file_name = choose_server_patch(zone_id,system_type)	
	while(patch_file_name.strip()):
		print "this time patch_file_name "+patch_file_name
		start_copy(root_path,update_file_path,patch_file_name,system_type,zone_id)	
		
		update_patch_list_file = os.path.join(update_file_path, "update_patch_list")	
		handle_update_file = open(update_patch_list_file, 'w')
		list_split_underline = patch_file_name.split('_')  #server_full_2013-03-05-4897.tar.gz
		#print list_split_underline   ['server', 'full', '2013-03-05-4897.tar.gz']
		list_split_dot = list_split_underline[-1].split('.')
		#print list_split_dot					['2013-03-05-4897', 'tar', 'gz']	
		list_split_midline = list_split_dot[0].split('-')
		#patch_version = string.atol(list_split_midline[-1])
		patch_version = string.atol(list_split_midline[-1])+string.atol(list_split_midline[-2])*100000+string.atol(list_split_midline[1])*10000000+string.atol(list_split_midline[0])*1000000000
		handle_update_file.write("%d"%patch_version)	
		handle_update_file.close()
		patch_file_name = choose_server_patch(zone_id,system_type)
	else:
		print "no patch need do"		
	
	
	
if len(sys.argv)!=4:
	sys.exit(0)	
GLOBAL_SERVER_IP = sys.argv[3]			
update_all_server_patch(sys.argv[1],sys.argv[2])	
						
