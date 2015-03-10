#!/usr/bin/env python
# -*- coding: utf-8 -*-
# machine_status.py  ��ȡ������Դʹ����Ϣ������״̬���������
# created by vince67 (nuovince@gmail.com)
# May 2014
 
 
import datetime
import os
import psutil as ps                       # psutil�� ��Ԥ�Ȱ�װ
from pymongo import Connection
import time
import socket
import uuid
 
 
class MachineStatus(object):
 
    #   ��ʼ��
    def __init__(self):
        self.MAC = None
        self.IP = None
        self.cpu = {}
        self.mem = {}
        self.process = {}
        self.network = {}
        self.status = []                    #  [cpuʹ���ʣ� �ڴ�ʹ���ʣ� ������Ŀ�� established������]
        self.get_init_info()
        self.get_status_info()
 
    #  ���������״̬
    def run(self):
        self.get_status_info()
        self.save_status_to_db()
 
    def save_status_to_db(self):
        print self.status
 
    #  �����ռ�
    def get_init_info(self):
        self.cpu = {'cores' : 0,            #  cpu�߼�����
                    'percent' : 0,          #  cpuʹ����
                    'system_time' : 0,      #  �ں�̬ϵͳʱ��
                    'user_time' : 0,        #  �û�̬ʱ��
                    'idle_time' : 0,        #  ����ʱ��
                    'nice_time' : 0,        #  niceʱ�� (�����ڵ����������ȼ��ϵ�ʱ��)
                    'softirq' : 0,          #  ����ж�ʱ��
                    'irq' : 0,              #  �ж�ʱ��
                    'iowait' : 0}           #  IO�ȴ�ʱ��
        self.mem = {'percent' : 0,
                    'total' : 0,
                    'vailable' : 0,
                    'used' : 0,
                    'free' : 0,
                    'active' : 0}
        self.process = {'count' : 0,        #  ������Ŀ
                        'pids' : 0}         #  ����ʶ���
        self.network = {'count' : 0,        #  ��������
                        'established' : 0}  #  established������
        self.status = [0, 0, 0, 0]          #  cpuʹ���ʣ��ڴ�ʹ���ʣ� �������� established������
        self.get_mac_address()
        self.get_ip_address()
 
    #  ��ȡ״̬�б�
    def get_status_info(self):
        self.get_cpu_info()
        self.get_mem_info()
        self.get_process_info()
        self.get_network_info()
        self.status[0] = self.cpu['percent']
        self.status[1] = self.mem['percent']
        self.status[2] = self.process['count']
        self.status[3] = self.network['established']
 
    #  ��ȡmac
    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.MAC = ":".join([mac[e : e+2] for e in range(0, 11, 2)])
 
    #  ��ȡip
    def get_ip_address(self):
        tempSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tempSock.connect(('8.8.8.8', 80))
        addr = tempSock.getsockname()[0]
        tempSock.close()
        self.IP = addr
 
    #  ���cpu��Ϣ
    def get_cpu_info(self):
        self.cpu['cores'] = ps.cpu_count()
        self.cpu['percent'] = ps.cpu_percent(interval=2)
        cpu_times = ps.cpu_times()
        self.cpu['system_time'] = cpu_times.system
        self.cpu['user_time'] = cpu_times.user
        self.cpu['idle_time'] = cpu_times.idle
        self.cpu['nice_time'] = cpu_times.nice
        self.cpu['softirq'] = cpu_times.softirq
        self.cpu['irq'] = cpu_times.irq
        self.cpu['iowait'] = cpu_times.iowait
 
    #  ���memory��Ϣ
    def get_mem_info(self):
        mem_info = ps.virtual_memory()
        self.mem['percent'] = mem_info.percent
        self.mem['total'] = mem_info.total
        self.mem['vailable'] = mem_info.available
        self.mem['used'] = mem_info.used
        self.mem['free'] = mem_info.free
        self.mem['active'] = mem_info.active
 
    #  ��ȡ������Ϣ
    def get_process_info(self):
       pids = ps.pids()
       self.process['pids'] = pids
       self.process['count'] = len(pids)
 
    #  ��ȡ��������
    def get_network_info(self):
        conns = ps.net_connections()
        self.network['count'] = len(conns)
        count = 0
        for conn in conns:
           if conn.status is 'ESTABLISHED':
               count = count + 1
        self.network['established'] = count
 
if __name__ == '__main__':
    MS = MachineStatus()
    print MS.IP, '\n', MS.MAC, '\n', MS.cpu, '\n', MS.mem, '\n', MS.status