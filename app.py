from flask import Flask
from flask import render_template
from flask import request,session
import sqlite3
from flask import Flask, redirect, url_for, request
app = Flask(__name__)
app.secret_key = "hello"

conn = sqlite3.connect('FarmEasy.db')
c=conn.cursor()
#c.execute('CREATE TABLE PRICE(CROP_ID INTEGER PRIMARY KEY AUTOINCREMENT,CROP_NAME TEXT NOT NULL,VARUTY TEXT,LOCATION TEXT,MARKET TEXT,MIN_PRICE TEXT,MAX_PRICE TEXT)')
#c.execute('INSERT INTO PRICE (CROP_NAME,VARUTY,LOCATION,MARKET,MIN_PRICE,MAX_PRICE) VALUES (?,?,?,?,?,?)',('jola','Loacl','panakaje','pmarket','550','650'))
#c.execute('ALTER TABLE USER ADD COLUMN ROLE INTEGER ')
#c.execute('UPDATE USER SET ROLE=1 WHERE Password={U}'.format(U=123))
#c.execute('CREATE TABLE NEWS(NEWS_ID INTEGER PRIMARY KEY AUTOINCREMENT,NEWS_TITLE TEXT NOT NULL,NEWS_URL TEXT NOT NULL)')


@app.route('/')
def home():
   return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():

   return render_template('admin_home.html')

@app.route('/price', methods=['GET'])
def price():
   conn = sqlite3.connect('FarmEasy.db')
   d=conn.cursor()
   rows=d.execute('SELECT * FROM PRICE')
   rows=rows.fetchall()
   conn.commit()
   conn.close()
   if session['role']==1:
      return render_template('admin_price.html',crop=rows)
   else:
      return render_template('price.html',crop=rows)


   
@app.route('/news')
def news():
   conn = sqlite3.connect('FarmEasy.db')
   d=conn.cursor()
   rows=d.execute('SELECT * FROM NEWS')
   rows=rows.fetchall()
   conn.commit()
   conn.close()
   return render_template('news.html',role=session['role'],news=rows)

@app.route('/logout')
def logout():
   session.pop('username',None)
   return render_template('login2.html')
   

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      usr_email=request.form['log_email']
      usr_password=request.form['log_password']
      conn = sqlite3.connect('FarmEasy.db')
      c=conn.cursor()
      query1="SELECT * FROM USER S WHERE S.Email=\'"+ usr_email+"\'" +" AND S.Password={p}".format(e=usr_email,p=usr_password)
      rows=c.execute(query1)
      rows=rows.fetchall()
      conn.commit()
      conn.close()
      if len(rows)==1:
         session['username']=usr_email
         session['role']=rows[0][3]
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
         conn = sqlite3.connect('FarmEasy.db')
         c=conn.cursor()
         c.execute('INSERT INTO USER (Username,Email,Password) VALUES (?,?,?)',(u_name,u_email,u_password))
         conn.commit()
         conn.close()
         return redirect(url_for('login'))
   else:
      return render_template('login2.html')

@app.route('/price/update',methods = ['POST', 'GET'] )
def price_update():
   if request.method == 'POST':
       c_id=request.form.get('id')
       c_min=request.form.get('min_price')
       c_max=request.form.get('max_price')
       conn = sqlite3.connect('FarmEasy.db')
       e=conn.cursor()
       e.execute('UPDATE PRICE SET MIN_PRICE={m},MAX_PRICE={mm} WHERE CROP_ID={i} '.format(m=c_min,mm=c_max,i=c_id))
       conn.commit()
       rows=e.execute('SELECT * FROM PRICE')
       rows=rows.fetchall()
       conn.commit()
       conn.close()
       return redirect(url_for('price'))
       

@app.route('/price/delete/<id>',methods = ['POST', 'GET'] )
def price_delete(id):
   if request.method == 'GET':
      conn = sqlite3.connect('FarmEasy.db')
      e=conn.cursor()
      e.execute('DELETE FROM PRICE WHERE CROP_ID={i}'.format(i=id))
      conn.commit()
   rows=e.execute('SELECT * FROM PRICE')
   rows=rows.fetchall()
   conn.commit()
   conn.close()
   return redirect(url_for('price'))

@app.route('/crop/add',methods = ['POST', 'GET'] )
def addcrop():
   return redirect(url_for('dashboard'))

@app.route('/subcrop/add',methods = ['POST', 'GET'] )
def addsubcrop():
   return redirect(url_for('dashboard'))

@app.route('/news/add',methods = ['POST', 'GET'])
def newsadd():
   if request.method == 'POST':
      n_title=request.form.get('news_title')
      n_url=request.form.get('news_url')
      conn = sqlite3.connect('FarmEasy.db')
      c=conn.cursor()
      c.execute('INSERT INTO NEWS (NEWS_TITLE,NEWS_URL) VALUES(?,?)',(n_title,n_url))
      conn.commit()
      conn.close()
      return redirect(url_for('news'))
      



conn.commit()
conn.close()

if __name__ == '__main__':
   app.run(debug = True)