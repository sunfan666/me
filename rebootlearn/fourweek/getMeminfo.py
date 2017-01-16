#coding:utf-8
import time
def getMem(filename,r):
    count = 0
    res_dict = {}
    with open(filename) as f:
        for line in f:
            if line == '\n':
                continue
            temp = line.split()
            res_dict[temp[0]] = temp[1]
            count += 1
            if count >= 4:
                break
    return res_dict
def calculate_Mem():
    res_dict = getMem('/proc/meminfo')
    memused = int(res_dict['MemTotal:'])-int(res_dict['MemFree:'])-int(res_dict['Buffers:'])-int(res_dict['Cached:'])
    return memused

NO = 0
while NO < 50:
    print calculate_Mem()
    NO += 1
    time.sleep(1)
