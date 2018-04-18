#coding:utf-8
from flask import Flask,session,redirect,render_template,request
import fileutil
fileutil.read_file()
app = Flask(__name__)
app.secret_key = 'sunfanA0Zr98j/3yX R~XHH!jmN]LWX/,?RTsunfan'

@app.route('/list')
def userlist():
    if "username" in session:
        return render_template('user_list.html',userlist = fileutil.user_dict.items())
    else:
        return redirect('/login')

@app.route('/login')
def index():
    if 'username' in session:
        return redirect('/list')
    return render_template('login.html')

@app.route('/loginaction')
def loginaction():
    user = request.args.get("user")
    pwd = request.args.get("pwd")
    err_msg = ''
    if user and pwd:
        if user == 'sunfan' and pwd == 'admin':
            session['username'] = 'admin'
            return redirect('/list')
        else:
            err_msg = 'user or pwd is wrong'
    else:
        err_msg = 'need user and pwd'
    return render_template('login.html',err_msg=err_msg)

@app.route('/adduser')
def add():
    user = request.args.get('user')
    pwd = request.args.get('pwd')
    if user in fileutil.user_dict:
        return redirect('/list')
    else:
        fileutil.user_dict[user] = pwd
        fileutil.write_file()
        return redirect('/list')

@app.route('/del')
def del_user():
    user = request.args.get('user')
    fileutil.user_dict.pop(user)
    fileutil.write_file()
    return redirect('/list')

@app.route('/update')
def update():
    user = request.args.get('user')
    pwd = fileutil.user_dict.get(user)
    return render_template('update.html',user = user,pwd = pwd)

@app.route('/updateaction')
def updateaction():
    user = request.args.get('user')
    new_pwd = request.args.get('new_pwd')
    fileutil.user_dict[user] = new_pwd
    fileutil.write_file()
    return redirect('/list')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10001,debug=True)
