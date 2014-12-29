#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import sys
import xml.dom.minidom   
import string
import os
import tarfile
import shutil


def startServer(zone_id):
	print "startServer "+zone_id
	dirpath = "/mj/mj"+zone_id+"/bin"
	os.chdir(dirpath)	
	cmd = "./start_release.sh &"
	os.system( cmd )
	cmd = "sleep 3"
	os.system( cmd )

if len(sys.argv)!=2:
	sys.exit(0)
	
startServer(sys.argv[1])	