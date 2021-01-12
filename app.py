from flask import Flask
from flask import render_template
from flask import request,session
import sqlite3
from flask import Flask, redirect, url_for, request
app = Flask(__name__)
app.secret_key = "hello"

conn = sqlite3.connect('FarmEasy.db')
c=conn.cursor()

#c.execute('CREATE TABLE CROP(CROP_ID TEXT PRIMARY KEY ,CROP_NAME TEXT NOT NULL,CROP_IMG TEXT,CROP_DURATION INTEGER,CROP_REGION TEXT,CROP_TEMP INTEGER,CROP_IRRIGATION TEXT,CROP_SOIL TEXT,CROP_DESC TEXT)')
#c.execute('CREATE TABLE SUBCROPS_FOR_CROP(CROP_ID TEXT NOT NULL,SUBCROP_ID TEXT NOT NULL,PRIMARY KEY(CROP_ID,SUBCROP_ID),FOREIGN KEY (CROP_ID) REFERENCES CROP (CROP_ID),FOREIGN KEY (SUBCROP_ID) REFERENCES SUBCROP (SUBCROP_ID))')
#c.execute('CREATE TABLE PRICE(CROP_ID TEXT PRIMARY KEY,CROP_IMG TEXT,CROP_NAME TEXT NOT NULL,VARUTY TEXT,LOCATION TEXT,MARKET TEXT,MIN_PRICE TEXT,MAX_PRICE TEXT,FOREIGN KEY (CROP_ID) REFERENCES CROP (CROP_ID))')
#c.execute('CREATE TABLE SUBCROP(SUBCROP_ID TEXT PRIMARY KEY ,SUBCROP_NAME TEXT NOT NULL,SUBCROP_DESC TEXT,SUBCROP_PERACER INTEGER)')
#c.execute('CREATE TABLE FERTILIZER(FERTILIZER_ID TEXT PRIMARY KEY ,ORG_FERTILIZER TEXT NOT NULL,CHE_FERTILIZER TEXT NOT NULL,FOREIGN KEY (FERTILIZER_ID) REFERENCES SUBCROP (SUBCROP_ID) )')
#c.execute('INSERT INTO PRICE (CROP_NAME,VARUTY,LOCATION,MARKET,MIN_PRICE,MAX_PRICE) VALUES (?,?,?,?,?,?)',('jola','Loacl','panakaje','pmarket','550','650'))
#c.execute('ALTER TABLE USER ADD COLUMN ROLE INTEGER ')
#c.execute('UPDATE USER SET ROLE=1 WHERE Password={U}'.format(U=123))
#c.execute('CREATE TABLE NEWS(NEWS_ID INTEGER PRIMARY KEY AUTOINCREMENT,NEWS_TITLE TEXT NOT NULL,NEWS_URL TEXT NOT NULL)')
#c.execute('DROP TABLE SUBCROP')
#c.execute('DROP TABLE CROP')
#c.execute('DROP TABLE PRICE')
#c.execute('DROP TABLE SUBCROPS_FOR_CROP')
#c.execute('DROP TABLE FERTILIZER')
#c.execute('DROP TRIGGER ADDPRICE')


#c.execute('''CREATE TRIGGER ADDPRICE AFTER INSERT ON CROP 
#            BEGIN 
#          INSERT INTO PRICE (CROP_ID,CROP_IMG,CROP_NAME,VARUTY,LOCATION,MARKET,MIN_PRICE,MAX_PRICE) VALUES (cp_id,cp_img,cp_name,'LOCAL',cp_region,'','0','0');
#          END;'''
#           )


@app.route('/')
def home():
   return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
   conn = sqlite3.connect('FarmEasy.db')
   c=conn.cursor()
   rows=c.execute('SELECT SUBCROP_ID,SUBCROP_NAME FROM SUBCROP')
   rows=rows.fetchall()
   return render_template('admin_home.html',subcrop=rows)

@app.route('/allcrop')
def allcrop():
   conn = sqlite3.connect('FarmEasy.db')
   c=conn.cursor()
   rows=c.execute('SELECT * FROM CROP')
   rows=rows.fetchall()
   return render_template('all_crop.html',crops=rows)

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
       c_market=request.form.get('market')
       c_max=request.form.get('max_price')
       conn = sqlite3.connect('FarmEasy.db')
       e=conn.cursor()
       e.execute("UPDATE PRICE SET MARKET=\'" + c_market+"\',"+"MIN_PRICE=\'" + c_min+"\',"+"MAX_PRICE=\'" + c_max+"\'"+"WHERE CROP_ID=\'" + c_id +"\'")
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
      e.execute("DELETE FROM PRICE WHERE CROP_ID=\'" + id +"\'")
      conn.commit()
   rows=e.execute('SELECT * FROM PRICE')
   rows=rows.fetchall()
   conn.commit()
   conn.close()
   return redirect(url_for('price'))

@app.route('/cropdec/<id>',methods = ['POST', 'GET'])
def cropdesc(id):
   if request.method == 'GET':
      conn = sqlite3.connect('FarmEasy.db')
      e=conn.cursor()
      rows=e.execute("SELECT DISTINCT C.*,F.* FROM CROP C,FERTILIZER F,SUBCROP S WHERE C.CROP_ID=F.FERTILIZER_ID AND C.CROP_ID=\'" + id +"\'")
      rows=rows.fetchall()
      sub=e.execute("SELECT * FROM SUBCROP WHERE SUBCROP_ID IN (SELECT S1.SUBCROP_ID FROM SUBCROP S1,SUBCROPS_FOR_CROP SS WHERE S1.SUBCROP_ID=SS.SUBCROP_ID AND SS.CROP_ID=\'" + id +"\')")
      sub=sub.fetchall()
      print(rows)
      print(sub)
      return render_template('crop_decription.html', des=rows,sdes=sub)


@app.route('/crop/add',methods = ['POST', 'GET'] )
def addcrop():
   if request.method == 'POST':
       crop_name=request.form.get('crop_name')
       crop_id=request.form.get('crop_id')
       crop_img=request.form.get('crop_img')
       crop_duration=request.form.get('crop_duration')
       crop_region=request.form.get('crop_region')
       crop_temp=request.form.get('crop_temp')
       crop_irrigation=request.form.get('crop_irrigation')
       crop_soil=request.form.get('crop_soil')
       crop_desc=request.form.get('crop_desc')
       subcrops=request.form.getlist('subcrop')
       crop_of=request.form.get('crop_of')
       crop_cf=request.form.get('crop_cf')

       try:
         conn = sqlite3.connect('FarmEasy.db')
         e=conn.cursor()
         e.execute('INSERT INTO CROP (CROP_ID,CROP_NAME,CROP_IMG,CROP_DURATION,CROP_REGION,CROP_TEMP,CROP_IRRIGATION,CROP_SOIL,CROP_DESC) VALUES(?,?,?,?,?,?,?,?,?)',(crop_id,crop_name,crop_img,crop_duration,crop_region,crop_temp,crop_irrigation,crop_soil,crop_desc))          
         conn.commit()
         for subcrop in subcrops:
            e.execute('INSERT INTO SUBCROPS_FOR_CROP (CROP_ID,SUBCROP_ID) VALUES(?,?)',(crop_id,subcrop))
            conn.commit()
         e.execute('INSERT INTO FERTILIZER (FERTILIZER_ID,ORG_FERTILIZER,CHE_FERTILIZER) VALUES(?,?,?)',(crop_id,crop_of,crop_cf))
         e.execute('INSERT INTO PRICE (CROP_ID,CROP_IMG,CROP_NAME,VARUTY,LOCATION,MARKET,MIN_PRICE,MAX_PRICE) VALUES(?,?,?,?,?,?,?,?)',(crop_id,crop_img,crop_name,'LOCAL',crop_region,' ','0','0'))
         conn.commit()
         conn.close()
         return redirect(url_for('dashboard'))
       except:
          return redirect(url_for('dashboard'))

@app.route('/subcrop/add',methods = ['POST', 'GET'] )
def addsubcrop():
   if request.method == 'POST':
      scrop_name=request.form.get('subname')
      scrop_id=request.form.get('subid')
      scrop_yield=request.form.get('yield')
      scrop_desc=request.form.get('subdesc')
      scrop_of=request.form.get('subof')
      scrop_cf=request.form.get('subcf')
      conn = sqlite3.connect('FarmEasy.db')
      c=conn.cursor()
      rows=c.execute("SELECT * FROM SUBCROP WHERE SUBCROP_ID=\'"+ scrop_id+"\' ")
      rows=rows.fetchall()
      try:
         c.execute('INSERT INTO SUBCROP (SUBCROP_ID,SUBCROP_NAME,SUBCROP_DESC,SUBCROP_PERACER) VALUES(?,?,?,?)',(scrop_id,scrop_name,scrop_desc,scrop_yield))
         conn.commit()

      except:
         return redirect(url_for('dashboard'))
      try:
         c.execute('INSERT INTO FERTILIZER (FERTILIZER_ID,ORG_FERTILIZER,CHE_FERTILIZER) VALUES(?,?,?)',(scrop_id,scrop_of,scrop_cf))
         conn.commit()
         #r=c.execute(' PRAGMA foreign_keys = ON')
         #r=r.fetchall()
         #print(r)
         return redirect(url_for('dashboard'))

      except:
         return "my"
      conn.commit()
      conn.close()   


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