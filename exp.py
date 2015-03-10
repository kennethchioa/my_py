# -*- coding: utf-8 -*-

def expnu():
	newnu = int(raw_input("请给出宠物当前经验值 : "))
	oldnu = int(raw_input("请给出宠物转生前经验值 : "))
	lowerexp = newnu*0.00007 + oldnu*0.00003
	print (format(lowerexp,'.0f'))

if __name__ == '__main__':
	while 1:
		expnu()
input()
