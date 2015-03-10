#-*- coding: utf-8 -*-
###kenneth.chioa###
###update newest goagent iplist###

import re,os
import requests


iplist=[]
source_url='http://cb.e-fly.org:81/archives/goagent-iplist.html'
goagent_dir='d:\\Program Files\goagent-3.2.0\local'
r = requests.get(source_url)
data = r.text
link_list =re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" ,data)
for url in link_list:
    if re.match(r"/usr/uploads/*", url):
         iplist.append(url)
newest_dir = iplist[0]
newest_url= "http://" + source_url.split('/')[2] + newest_dir
print newest_url
newest_iplist = os.popen('curl '  +  newest_url).read()
print  newest_iplist
print type(newest_iplist)

if re.match(r'[0-9].+', newest_iplist):

    os.chdir(goagent_dir)

    if not os.path.exists('proxy.ini'):
        exit(-1)

    lines = open('proxy.ini').readlines()

    os.rename('proxy.ini','proxy_bak.ini')

    open('proxy_new.ini', 'w').write(re.sub(r'[^\n]*google_cn = [0-9].+', 'google_cn = ' + newest_iplist.strip(), open('proxy_bak.ini').read()))

    open('proxy.ini', 'w').write(re.sub(r'[^\n]*google_hk = [0-9].+', 'google_hk = ' + newest_iplist.strip(), open('proxy_new.ini').read()))

    os.remove('proxy_bak.ini')
else:
    print "VALUES ERROR!!"
input()
