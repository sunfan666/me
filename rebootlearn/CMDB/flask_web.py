from flask import Flask,request,render_template,redirect,session
import json
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX Rasdasdasdsa~XHH!jmN]LWX/,?RT'

import MySQLdb as mysql
conn = mysql.connect(user='woniu',passwd='123456',host='59.110.12.72',db='woniu')
conn.autocommit(True)
cur = conn.cursor()
#cur.execute('select * from woniu_user')
#print cur.fetchall()


@app.route('/pc')
def index():
	return render_template('pc.html')
@app.route('/idc')
def b():
	return render_template('idc.html')


if __name__=='__main__':
	app.run(host='0.0.0.0',port=9092,debug=True)



