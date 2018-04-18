#coding:utf-8
#author:sunfan
def tailf():
    with open('access_201612201700.log') as f:
        f.seek(0,2)
        while True:
            last_pos = f.tell()
            line = f.readline()
            if line:
                print line
tailf()
