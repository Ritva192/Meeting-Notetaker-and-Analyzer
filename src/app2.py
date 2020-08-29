import os
from flask import Flask, render_template, json, request, url_for, redirect, session, send_from_directory
from flaskext.mysql import MySQL
from werkzeug import secure_filename

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'spooky action at a distance-Einstein'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'meetingdata'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def main():
    return render_template('login.html')



@app.route('/showSignin')
def showSignin():
    return render_template('login.html')



@app.route('/showSignin',methods=['POST','GET'])
def validateLogin():
    try:
        _username = request.form['email']
        _password = request.form['password']
        print("valid")       
        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT * FROM member where email= '"+ _username +"' and password='"+  _password +"'"
        print(sql) 

   # Execute the SQL command
        cursor.execute(sql)
   # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        #print("Total number of rows in python_developers is - ", cursor.rowcount)
        r = cursor.rowcount
        if r > 0:
            return render_template('header.html')
        else:
                return render_template('login.html')
                

    except:
           print ("Error: unable to fecth data")
           return render_template('login.html')
    finally:
        cursor.close()
        con.close()
    
    
		
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignUp',methods=['POST','GET'])
def signUp():
    
    r = request.files.getlist('file')
    print(r)
    count=1
    for file in r:
       
      
        
        file.index(1).save(secure_filename(file.filename))
        s = file.filename
   
       
        #print(s)
        
        
      
    return render_template('signup.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/orgdata')       
def display_data():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM organization"
        cursor.execute(query)

        rows = cursor.fetchall()
        print(rows)
        conn.close()

        #return rows

        return render_template('orgdata.html', data = rows)

    except Exception as e:
        return (str(e))	
        
if __name__ == "__main__":
    app.run()
