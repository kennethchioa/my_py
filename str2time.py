# -*- coding: utf-8 -*-
import time
import sys
def timestamp_datetime(value):
	    format = '%Y-%m-%d %H:%M:%S'
	    value = time.localtime(value)
	    dt = time.strftime(format, value)
	    return dt
def datetime_timestamp(dt):
	  time.strptime(dt, '%Y-%m-%d %H:%M:%S')
if __name__ == '__main__':
	while 1:
	    s = timestamp_datetime(int(raw_input("请输入时间戳:")))
            print s
