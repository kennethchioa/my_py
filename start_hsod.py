#!/usr/bin/env python
# -*- coding:utf-8 -*-
#author kenneth.chioa
#date 2015-03-13

'''
Written for HSOD Servers starting.
Game Process order priority int 1-8,
1 is the first start process
if you set the the value = or < 0 
this process won't start

'''

import os 
import sys
import time
import subprocess

APP_HOME = '/home/hsod/'

PROCESS_ORDER = { 
        'dbgate50000'    : 1,
	'dbgate51000'    : 2, 
	'nodeserver'     : 3,
	'chatserver'     : 4,
	'relationserver' : 5,
	'gatewaysvrd'    : 6,
	'oaserver'       : 7,
	'dispatchsvrd'   : 8
	}


def appfile_check(f_h,f_l):
    f_list = [f for f in f_l if f_l[f] > 0 ]
    j_lst = []
    for f in f_list:
        if os.path.isfile(os.path.join(f_h + f,f)):
            j_lst.append(f)
    ret = [ l for l in f_list if l not in j_lst ]
    if ret == []:
	    return True
    else:
        return ret

        

def start_hsod(app_home,process_order):
    judge_res = appfile_check(app_home,process_order)
    order_keys = sorted(process_order, key= lambda k: process_order[k])
    if  judge_res == True:
        print "Process List setting is %s" % ([p  for p in  process_order if process_order[p] > 0])
        for proc in order_keys:
                        print "Now Execuding process %s" % proc
                        if proc == "dbgate50000" or proc == "dbgate51000":
                            exe_sh = "./" + proc.split('5')[0] + '.sh &'
                        else:
                            exe_sh = "./" + proc + ".sh &"
                        try:
                            print "Starting %s ......" % proc
                            os.chdir(app_home + proc)
                            retcode = subprocess.check_call(exe_sh,shell=True)
	                    if retcode < 0:
                                print >>sys.stderr, "Child Process % was terminated by signal" % proc ,  -retcode
		            else:
                                print >>sys.stderr, "Child Process %s returned" % proc , retcode
		                print "Sleep 5 Seconds......"
                                time.sleep(5)
	                except OSError, e:
                            print >>sys.stderr, "Execution failed:", e
    else:
	for lost_file in judge_res:
            print "Lost File!!! : %s " %  lost_file
            
if __name__ == '__main__':
    start_hsod(APP_HOME,PROCESS_ORDER)
