#coding:utf-8
#
from flask import Flask,request,render_template,redirect,session
import json
#python 2.7 版本中文字符编码问题的神解决方案 URL:http://blog.csdn.net/mindmb/article/details/7898528
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#ASCII不支持中文字符编码，UNICODE支持中文字符编码，二者主要区别。python 3 版本中解决了这个问题 比较赞
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX Rasdasdasdsa~XHH!jmN]LWX/,?RT'

import MySQLdb as mysql
conn = mysql.connect(user='sunfan',passwd='123456',host='localhost',db='flask_learn')
conn.autocommit(True)
cur = conn.cursor()
#cur.execute('select * from woniu_user')
#print cur.fetchall()

@app.context_processor
def inject_user():
    return {'user':'Admin'}

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect('/')
    else:
        return redirect('/')

@app.route('/')
def index():
        return redirect('/login')

@app.route('/login')
def userlogin():
    if 'username' in session:
        return redirect('/pc')
    return render_template('login.html')

@app.route('/loginaction')
def loginaction():
    user = request.args.get('username')
    pwd  = request.args.get('password')
    print request.method
    error_msg = ''
    if user and pwd:
        if user == 'sunfan' and pwd == 'sunfan':
            session['username'] = 'sunfan'
            return redirect('/pc')
        else:
            error_msg = 'wrong user or pssword'
    else:
        error_msg = 'Need user and pwd'
    return render_template('login.html', error_msg = error_msg)

#@app.route('/loginaction', methods=['GET', 'POST'])
#def loginaction():
#    error_msg = ''
#    print request.method
#    if request.method == 'GET':
#        return render_template('login.html')
#    elif request.method == 'POST':
#        username = request.form.get('username')
#        password = request.form.get('password')
#        print username,password
#        if username and password:
#            if username == 'admin' and password == 'admin':
#                session['username'] = 'admin'
#                return redirect('/pc')
#            else:
#                error_msg = 'wrong user or pssword'
#        else:
#            error_msg = 'Need user and pwd'
#        return render_template('login.html', error_msg = error_msg)
@app.route('/idc')
def indexhtml():
    return render_template('idc.html')

@app.route('/addidc',methods=['post'])
def addidc():
    idc_name = request.form.get('name')
    sql = 'insert into idc (name) values ("%s")'%(idc_name)
    print '*'*100
    print sql
    cur.execute(sql)
    return 'ok'

@app.route('/idclist')
def idclist():
    cur.execute('select * from idc')
    res =  cur.fetchall()
    return json.dumps(res)

@app.route('/pc')
def pc():
    return render_template('pc.html')


@app.route('/updatepc',methods=['post'])
def updatepc():
    pc_id = request.form.get('id')
    ip = request.form.get('ip')
    mem = request.form.get('mem')
    idc_id = request.form.get('idc_id')
    create_time = request.form.get('create_time')
    sql='update pc set ip="%s",mem=%s,idc_id=%s,create_time="%s" where id=%s'%(ip,mem,idc_id,create_time,pc_id)
    print sql
    cur.execute(sql)
    return 'ok'
@app.route('/pclist')
def pclist():
    id = request.args.get('id')
    sql = 'select pc.id,pc.ip,pc.mem,idc.name,pc.create_time, pc.idc_id from pc,idc where pc.idc_id=idc.id'
    if id:
        sql += ' and pc.id=%s'%(id)

    print sql   
    cur.execute(sql)
    res = cur.fetchall()
    return json.dumps(res)

@app.route('/addpc',methods=['post'])
def addpc():
    ip = request.form.get('ip')
    mem = request.form.get('mem')
    idc_id = request.form.get('idc_id')
    create_time = request.form.get('create_time')
    sql = 'insert into pc (ip,mem,idc_id,create_time) values ("%s",%s,%s,"%s")'%(ip,mem,idc_id,create_time)
    print '*'*100
    print sql
    cur.execute(sql)
    return 'ok'

@app.route('/delpc',methods=['post'])
def delpc():
    id = request.form.get('id')
    if not id:
        return 'error'
    sql = 'delete from pc where id=%s'%(id)
    cur.execute(sql)
    return 'ok'



if __name__=='__main__':
    app.run(host='0.0.0.0',port=9093,debug=True)

