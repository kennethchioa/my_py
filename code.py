#-*- coding:utf-8 -*-
'''
��̵�����������룬������Сд��ĸ�����֣�����ָ�����볤��
'''
#�����������
from random import choice
import string

#python3��Ϊstring.ascii_letters,��python2�������ʹ��string.letters��string.ascii_letters

def GenPassword(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

if __name__=="__main__":
    #����10���������    
    for i in range(10):
        #����ĳ���Ϊ8
        print(GenPassword(8))
        input()