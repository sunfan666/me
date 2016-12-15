#coding:utf-8
f = open('./userinfo.txt','r+')
sf = f.readlines()
login_method = raw_input('Please select the login method:(name,id): ')
#定义用户密码ID等数组
user_list = []
pwd_list = []
id_list = []
#遍历文件每行内容,将用户密码ID等追加到单独的数组中
for i in sf:
    temp =  i.split(':')
    user_list.append(temp[1])
    pwd_list.append(temp[2].split('\n')[0])
    id_list.append(temp[0])
    # print user_list,pwd_list,id_list
#选择登陆方式为name,让其输入name和pwd
if login_method == 'name':
    _input_name = raw_input('please input your name: ')
    _input_passwd = raw_input('please input your password ')
#判断name和pwd正确与否
    if _input_name in user_list:
        if _input_passwd == pwd_list[user_list.index(_input_name)]:
            print 'ok'
        else:
            print 'key error'
    else:
        print 'user not exists.'
#选择方式为ID,让其输入ID和pwd
else:
    _input_id = raw_input('please input your id: ')
    _input_passwd = raw_input('please input your password ')
#判断ID和pwd正确与否
    if _input_id in id_list:
        if _input_passwd == pwd_list[id_list.index(_input_id)]:
            print 'ok'
        else:
            print 'key error'
    else:
        print 'id not exists.'
f.close()
