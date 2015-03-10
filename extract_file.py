import sys
import xml.dom.minidom   
import string
import os
import tarfile
import shutil

def extract_dbfile(file_dir,file_name):

	tar = tarfile.open(os.path.join(file_dir,file_name))
	file_dir=os.path.join(file_dir,"mxm")
	names = tar.getnames()
	for name in names:
		tar.extract(name,path=file_dir)	
		
if len(sys.argv)!=3:
	sys.exit(0)
	
extract_dbfile(sys.argv[1],sys.argv[2])	