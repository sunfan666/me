#!/usr/bin/env python 
#coding:utf-8
#判断闰年

print '\033[1;31;42m'
while True:
	x = int(raw_input("please input year "))
	if   x % 100 == 0   and x % 400 == 0:
		print "%d 年是 闰年" % x
		break
	elif x % 100 != 0   and x % 4 == 0:
		print "%d 年是 闰年" % x
		break
	else:
		print "%d 年不是 闰年" % x
print '\033[0m'
