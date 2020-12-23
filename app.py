from flask import Flask
from flask import render_template
from flask import request,session
import sqlite3
from flask import Flask, redirect, url_for, request
app = Flask(__name__)
app.secret_key = "hello"


@app.route('/')
def home():
   return redirect(url_for('login'))
@app.route('/dashboard')
def dashboard():

   return render_template('all_crop.html')
@app.route('/cropdec')
def cropdec():

   return render_template('price.html')
   

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      usr_email=request.form['log_email']
      usr_password=request.form['log_password']
      conn = sqlite3.connect('frameland.db')
      c=conn.cursor()
      query1="SELECT * FROM USER S WHERE S.Email=\'"+ usr_email+"\'" +" AND S.Password={p}".format(e=usr_email,p=usr_password)
      rows=c.execute(query1)
      rows=rows.fetchall()
      conn.commit()
      conn.close()
      if len(rows)==1:
         return redirect(url_for('dashboard'))
      else:
         return redirect(url_for('signup'))
   else:
      return render_template('login2.html')

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
   if request.method == 'POST':
      u_name=request.form['user_name']
      u_email = request.form['user_email']
      u_password = request.form['user_password']
      if(u_name and u_email and u_password):    
         conn = sqlite3.connect('frameland.db')
         c=conn.cursor()
         c.execute('INSERT INTO USER (Username,Email,Password) VALUES (?,?,?)',(u_name,u_email,u_password))
         conn.commit()
         conn.close()
         return redirect(url_for('login'))
   else:
      return render_template('login2.html')

if __name__ == '__main__':
   app.run(debug = True)