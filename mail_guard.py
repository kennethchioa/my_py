#!/usr/bin/env python
# -*- coding: utf-8 -*-

#author kenneth.chioa
#date 2014-10-31

#导入smtplib和MIMEText
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import smtplib
import os
import socket
import time,datetime
from email.mime.text import MIMEText
def send_mail(sub,content):
#############
#要发给谁
    mailto_list={ \
                 "zhaoyichun" : "13816656813@139.com",
                 "guomeng"    : "18818061825@139.com",
                 "qianchen"   : "13601941126@139.com",
                 "zhangyongbo": "zhangyongbo@15166.com",
                 }
#####################
#设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.163.com"
    mail_user="mtj_alert"
    mail_pass="xxxxxxxxxxxxx"
    mail_postfix="163.com"
######################
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@qq.com","sub","content")
    '''
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content,_charset='utf8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.starttls()
        s.sendmail(me, mailto_list.values(), msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False



if __name__ == '__main__':

    LOCAL_HOST = socket.gethostname()
    LOCAL_IP = socket.gethostbyname(socket.gethostname())
    GUARD_DIR = '/mtj/fab/guard/'
    CHECK_FILE = '/root/.last_guard_file'
    TITLE = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())) +  u" CHECK GUARD "
    CONTENT = u"主机 : %s IP : %s 路径：%s 存在err文件 请登陆检查服务器！ " %  ( LOCAL_HOST , LOCAL_IP , GUARD_DIR )
    
    if  os.path.exists( GUARD_DIR ):
          l = os.listdir( GUARD_DIR )
          l.sort(key=lambda fn: os.path.getmtime( GUARD_DIR + fn) if  os.path.isdir( GUARD_DIR + fn ) else 0)
          d = datetime.datetime.fromtimestamp(os.path.getmtime( GUARD_DIR +l[-1]))
          if os.path.isfile( CHECK_FILE ):
              r = open( CHECK_FILE ,'r').read()
              f = open( CHECK_FILE ,'w').write(d.strftime("%Y年%m月%d日 %H时%M分%S秒"))
	      f_new = open( CHECK_FILE ,'r').read()
    	      if r == f_new:
		 t = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time.localtime(time.time()))     
    	         print(t + '上一次最后回传的文件的时间是 ' + r + ', 最后回传文件是' + l[-1] + "，时间:"+d.strftime("%Y年%m月%d日 %H时%M分%S秒") + '未改动')
    	      else:
		 t = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time.localtime(time.time()))
    	         print ( t +'最后回传的文件是' + l[-1] + ",时间:"+ d.strftime("%Y年%m月%d日 %H时%M分%S秒") + '有改动')
    	         print u'开始发送邮件>>>>>>>>>'
                 if send_mail( TITLE , CONTENT ):
                     print u'发送成功'
                 else:
                     print u'发送失败'
          else:
	      f = open( CHECK_FILE ,'w').write(l[-1])
	      t = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time.localtime(time.time()))
	      print (t + '最后回传的文件是' + l[-1] + ",时间:"+ d.strftime("%Y年%m月%d日 %H时%M分%S秒"))
	      if send_mail( TITLE , CONTENT ):
	          print u'发送成功'
	      else:
	          print u'发送失败'

    else:
        t = time.strftime('%Y年%m月%d日 %H时%M分%S秒',time.localtime(time.time())) 
        print u"%s %s目录不存在 没有err文件！正常!" % ( t , GUARD_DIR )
