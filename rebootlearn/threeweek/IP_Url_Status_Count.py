#coding:utf-8
res_str = '<table border="1">'
tmp = '''
  <tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
  </tr>'''
dict = {}

with open('www_access_20140823.log') as f:
    for line in f.read().strip().split('\n'):
        L = line.split()
        dict[(L[0],L[6],L[8])] = dict.get((L[0],L[6],L[8]),0) + 1

# f = open('www_access_20140823.log')
# for line in f.read().strip().split('\n'):#将整个文件切换成每行为一个元素的列表
#     file = line.split()
#     dict[(file[0],file[6],file[8])] = dict.get((file[0],file[6],file[8]),0)+1 #将需要展示的元素统计出来多少次
    # dict.setdefault((file[0],file[6],file[8]),0)#第二种方法,格式为{(x,y,z):count}
    # dict[(file[0],file[6],file[8])]+=1
    #print dict
res_list = dict.items()#将字典转换成list,格式为[(x,y,z),count]
#冒泡排序
length=len(res_list)
count=0
res_str += tmp %('NO','IP','url','state','count')
for i in range(length-1):
    for j in range(length-1-i):
        if res_list[j][1] > res_list[j+1][1]:
            res_list[j],res_list[j+1]=res_list[j+1],res_list[j]
    now_max,pre_max = res_list[-(i+1)],res_list[-i]
    if now_max[1]== pre_max[1]:
        count = count +1
    else:
        count =0
        if i>10:
            break
#print '第%s名，IP%s,访问url %s ,状态码%s, 次数%s '%(i+1-count,now_max[0][0],now_max[0][1],now_max[0][2],now_max[1])
    res_str += tmp % (i+1-count,now_max[0][0],now_max[0][1],now_max[0][2],now_max[1])  

#写入到html中

res_str+='</table>'
ff = open('sunfan.html','w')
ff.write(res_str)
ff.close

f.close()
print "finish"


