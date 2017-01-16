from flask import Flask,request,render_template,redirect,session
#import fileutil
#fileutil.read_file()
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX Rasdasdasdsa~XHH!jmN]LWX/,?RT'

import MySQLdb as mysql
conn = mysql.connect(user='woniu',passwd='123456',host='59.110.12.72',db='reboot12')
conn.autocommit(True)
cur = conn.cursor()
#cur.execute('select * from woniu_user')
#print cur.fetchall()


#@app.route('/login',methods=['GET','POST'])
#def login():
#	if request.method=='GET':
#		return render_template('login.html')
#	elif request.method=='POST':
#		user = request.form.get('user')

@app.route('/')
def index():
	if 'username' in session:
		return redirect('/list')
	return render_template('login.html')
@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
@app.route('/loginaction',methods=['GET','POST'])
def loginaction():
	if request.method=='GET':
		user = request.args.get('user')
                pwd  = request.args.get('pwd')
        elif request.method=='POST':
                user = request.form.get('user')
		pwd  = request.form.get('pwd')
	error_msg = ''
	if user and pwd:
		if user=='admin' and pwd=='admin':
			session['username'] = 'admin'
			return redirect('/list')
		else:
			error_msg ='wrong user or password'
	else:
		error_msg ='need user and pwd'
	return render_template('login.html',error_msg=error_msg)
@app.route('/del')
def del_user():
	user = request.args.get('user')
	sql = 'delete from sunfan_user where user = "%s"' % user
	cur.execute(sql)
	# fileutil.file_dict.pop(user)
	# fileutil.write_file()
	return redirect('/list')
@app.route('/update')
def update():
	user = request.args.get('user')
	pwd = request.args.get('pwd')
#	sql = "select pwd from sunfan_user where user = '%s'" % user 
#        cur.execute(sql)
#	print cur.fetchall()
	return render_template('update.html',user=user,pwd=pwd)
@app.route('/updateaction')
def updateaction():
	if 'GET' == request.method:
        	user = request.args.get('user')
        	pwd = request.args.get('pwd')
    	else:
        	user = request.form.get('user')
        	pwd = request.form.get('pwd')
	new_pwd = request.args.get('new_pwd')
	sql = "update sunfan_user set pwd = '%s' where user = '%s'"%(new_pwd,user)
	cur.execute(sql)
	# fileutil.file_dict[user] = new_pwd
	# fileutil.write_file()
	return redirect('/list')
@app.route('/adduser')
def adduser():
	if 'GET' == request.method:
            user = request.args.get('user')
            pwd = request.args.get('pwd')
        else:
            user = request.form.get('user')
            pwd = request.form.get('pwd')
	num_msg =''
        if user =='':
            num_msg = 'please input your name'
            return redirect('/list')
	sql = "select user from sunfan_user where user = '%s'" % user
	cur.execute(sql)
        users=cur.fetchall()
        if users ==():
        #    num_msg ='user is not exist'
         #   return redirect('/list')
	#else:
	    sql = 'insert into sunfan_user values ("%s","%s")'%(user,pwd)
	    cur.execute(sql)
	    return redirect('/list')
		#fileutil.file_dict[user] = pwd
		#fileutil.write_file()
        if users !=():
	    num_msg ='user is not exist'
	    return redirect('/list')
@app.route('/list')
def userlist():
	res = cur.execute('select user,pwd from sunfan_user')
	print res
	all_res = cur.fetchall()
	print all_res
	if 'username' in session:
		return render_template('list.html',userlist=all_res)
	else:
		return redirect('/')
if __name__=='__main__':
	app.run(host='0.0.0.0',port=11111,debug=True)
