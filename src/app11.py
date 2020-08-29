import os
import smtplib
import requests
from flask import Flask, flash, render_template, json, request, url_for, redirect, session, send_from_directory
from flaskext.mysql import MySQL
from werkzeug import secure_filename
from flask import send_file

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

@app.route('/download/<fname>')
def file_downloads(fname):
    try:        
        return send_file(fname, as_attachment=True)# attachment_filename='aa.txt')
    except Exception as e:
        return str(e)

@app.route('/dashboard')
def main():
    return render_template('header.html')
    
		
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
		
@app.route('/showSignUp',methods=['POST','GET'])
def signUp():
    try:
     
        conn = mysql.connect()
        cursor = conn.cursor()
        # validate the received values
               
        
        print(request.form["fname"])
        print(request.form['mname'])
        print(request.form['lname'])
        print(request.form['gender'])
        print(request.form['email'])
        print(request.form['dob'])
        print(request.form['address'])
        print(request.form['country'])
        print(request.form['state'])
        print(request.form['city'])
        print(request.form['pincode'])
        print(request.form['contact_no_1'])
        print(request.form['contact_no_2'])
        print(request.form['department'])
        print(request.form['designation'])
        #r = request.files['file']
        #r.save(secure_filename(r.filename))
        r = request.files.getlist('file')
        count=1
        s=""
        for file in r:
            file.save(secure_filename(file.filename))
            s="s"+str(count)
            globals()[s] = file.filename
            count+=1
        #print(s1)
        #print(s2)	
        
       
        a = request.form["fname"]
        b = request.form['mname']
        c = request.form['lname']
        d = request.form['gender']
        e = request.form['email']
   
        h = request.form['dob']
        i = request.form['address']
        j = request.form['country']
        k = request.form['state']
        l = request.form['city']
        m = request.form['pincode']
        n = request.form['contact_no_1']
        o = request.form['contact_no_2']
        p = request.form['department']
        q = request.form['designation']
        #s = r.filename
			   
        
        data = (0, 0, a, b, c, d, e, h, i, j, k, l, m, n, o, p, q, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10)
                        
        sql = """ INSERT INTO member (member_id, organization_id, fname, mname, lname, gender, email, dob, address_line_1, country, state, city, pincode, contact_no_1, contact_no_2, department, designation, face_image_1, face_image_2, face_image_3, face_image_4, face_image_5, face_image_6, face_image_7, face_image_8, face_image_9, face_image_10) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        
 
        print(sql, data)
        
        # Execute the SQL command
        
        cursor.execute(sql, data)
        # Fetch all the rows in a list of lists.
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
             return render_template('signup.html')
       

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
@app.route('/meeting_agenda')       
def display_meeting_agenda():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM meeting_agendas"
        cursor.execute(query)

        rows = cursor.fetchall()
        print(rows)
        conn.close()

        #return rows

        return render_template('meeting_agenda.html', data = rows)

    except Exception as e:
        return (str(e))
@app.route('/agenda')
def agenda_meeting():
     try:
        conn = mysql.connect()
        cursor = conn.cursor()
        query1 = "SELECT * FROM meeting"
        cursor.execute(query1)
        myrows = cursor.fetchall()
        print(myrows)
        conn.close()

        #return rows
        return render_template('agenda.html',mydata = myrows)

     except Exception as e:
         return (str(e))


@app.route('/agenda',methods=['POST','GET'])
def saveagenda():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        # validate the received values
               
        
        print(request.form["meeting"])
        print(request.form["agenda"])
       
        
            # will basicaly show on the browser the uploaded file
             # Load an html page with a link to each uploaded file
        a = request.form["meeting"]
        b = request.form["agenda"]
        
        data = (0, a, b, 0)
                        
        sql = """ INSERT INTO meeting_agendas (agenda_id, meeting_id, agenda_name, covered) VALUES (%s, %s, %s, %s) """
        
        result = cursor.execute(sql,data)
        print(result);
        print(sql, data)

        result=cursor.execute(sql, data)
        print(result)
        # Fetch all the rows in a list of lists.
        #if len(data) is 0:

        conn.commit()
    
        return render_template('agenda.html')

        #else:
            #return json.dumps({'error':str(data[0])})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    #file = request.files['file']
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', filenames=filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/register')
def register():
    return render_template('register.html')
	
@app.route('/register',methods=['POST','GET'])
def orgregister():
    try:
        print("Hello") 
        conn = mysql.connect()
        cursor = conn.cursor()
        # validate the received values
        
        
                        
        sql = "INSERT INTO organization(organization_id,organization_name,organization_type,organization_email,password) " \
               "VALUES(%s, %s, %s, %s, %s)"
        #print(sql)
        #print(request.form["organization_id"])
        print(request.form["organization_name"])
        print(request.form["organization_type"])
        print(request.form["organization_email"])
        print(request.form["organization_password"])
		  
        data = (0,request.form["organization_name"],request.form["organization_type"],request.form["organization_email"],request.form["organization_password"])
        #data = (0,"aaa","bb","ss","sd","sd","2013-04-04","aaa",2323,233,"wq",1)
        
        # Execute the SQL command
        print(data)
        result = cursor.execute(sql,data)
        print(result);
        # Fetch all the rows in a list of lists.
		
        if len(data) is 0:
            return json.dumps({'error':str(data[0])})   
        else:
            conn.commit()
            #return json.dumps({'message':'organization account created successfully !'})
            return render_template('org_login.html')
       

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
@app.route('/org_login')
def OrgLogin():
    return render_template('org_login.html')
    
@app.route('/org_login',methods=['POST','GET'])
def ValidateOrgLogin():
    try:
        print(request.form['organization_email'])
        _username = request.form['organization_email']
        _password = request.form['organization_password']
        print("valid")       
        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT * FROM organization where organization_email= '"+ _username +"' and password='"+  _password +"'"
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
            return render_template('org_login.html')
                

    except:
        print ("Error: unable to fecth data")
           #return render_template('org_login.html')
    finally:
        cursor.close()
        con.close()
@app.route('/schedule')
def schedule_meeting():
    return render_template('schedule.html')

@app.route('/schedule',methods=['POST','GET'])
def meetinggggg():
    try:
     
        conn = mysql.connect()
        cursor = conn.cursor()
        # validate the received values
               
        
        print(request.form["meeting_topic"])
        print(request.form["date"])
        print(request.form["start_time"])
        
        print(request.form["location"])
        print(request.form["country"])
        print(request.form["state"])
        print(request.form["city"])
        print(request.form["description"])
       
        
            # will basicaly show on the browser the uploaded file
             # Load an html page with a link to each uploaded file
        a = request.form["meeting_topic"]
        b = request.form["date"]
        c = request.form["start_time"]
     
        e = request.form["location"]
        g = request.form["country"]
        h = request.form["state"]
        i = request.form["city"]
        j = request.form["description"]
        
        data = (0, a, b, c, e, g, h, i, j,0)
                        
        sql = """ INSERT INTO meeting (meeting_id, meeting_topic, date, start_time, location, country, state, city, description,organization_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
        
        result = cursor.execute(sql,data)
        print(result);
        print(sql, data)
        
        # Execute the SQL command
        
        cursor.execute(sql, data)
        # Fetch all the rows in a list of lists.
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'Meeting scheduled successfully !'})
            
        else:
            return render_template('schedule.html')
       

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
        

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

@app.route('/summary')       
def display_summary():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM meeting_summary"
        cursor.execute(query)

        rows = cursor.fetchall()
        
        print(rows)
        conn.close()

        #return rows

        return render_template('summary.html', data = rows)

    except Exception as e:
        return (str(e))
    
@app.route('/dashboard',methods=['POST','GET'])       
def count_org():
    try:
        conn = mysql.connect()
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn.cursor()

       

        query1 = "SELECT * FROM member"
        cursor1.execute(query1)
        rows1 = cursor1.fetchall()
        r1 = cursor1.rowcount
        

        query2 = "SELECT * FROM meeting"
        cursor2.execute(query2)
        rows2 = cursor2.fetchall()
        r2 = cursor2.rowcount

        query3 = "SELECT * FROM meeting_summary"
        cursor3.execute(query3)
        rows2 = cursor3.fetchall()
        r3 = cursor3.rowcount


        conn.close()
        return render_template('header.html', r1 = cursor1.rowcount, r2 = cursor2.rowcount, r3=cursor3.rowcount)

    except Exception as e:
        return (str(e))
    

@app.route('/members')       
def des_member():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM member"
        cursor.execute(query)

        rows = cursor.fetchall()

  
        conn.close()

        

        return render_template('displaymember.html', data = rows)

    except Exception as e:
        return (str(e))

    
@app.route('/newdata')
def display_meetingmember():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM member"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        query1 = "SELECT * FROM meeting"
        cursor.execute(query1)
        myrows = cursor.fetchall()
        print(myrows)
        conn.close()

        #return rows
        return render_template('newdata.html', data = rows,mydata = myrows)

        #return render_template('meetingmember.html', data = rows)

    except Exception as e:
        return (str(e))


@app.route('/newdata',methods=['POST','GET'])
def notification():
     try:
        conn = mysql.connect()
        cursor = conn.cursor()
        emails = request.form.getlist("email")
        meeting = request.form["meeting"]
        #member_id = request.form.getlist("email.id")
        #emails = request.form.getlist("email.emails")
        #query = "SELECT * FROM member"
        #cursor.execute(query)
        #rows = cursor.fetchall()
        #print(member_id)
        print(emails)
        

        sql = "INSERT INTO meeting_member(meeting_member_id,meeting_id,member_id,status) " \
               "VALUES(%s, %s, %s, %s)"
        #query1 = "SELECT * FROM meeting"
        #cursor.execute(query1)
        #myrows = cursor.fetchall()
        data = (0,meeting,11,1)
        
        print(data)
        result = cursor.execute(sql,data)
        print(result);
        print(meeting)
        query1 = "SELECT * FROM meeting WHERE meeting_id = %s"
        print(query1)
        cursor.execute(query1,(meeting))
        details = cursor.fetchall()
        print(details)
        
        #print(details[1])
        for row in details :
            print(row[0],row[1],row[2],row[3],row[4])
        #print(details['meeting_topic'])
        
        gmail_user = 'meetingnotetake14@gmail.com'  
        gmail_password = 'Project@1234'

        sent_from = gmail_user
        to = emails
       # to = ['krishnaahire24@gmail.com', 'ajtank18@gmail.com']  
        subject = 'New Meeting Scheduled!!'
        body = 'Hello member!! You are invited for the meeting and details are listed below:\n Topic Name:'+row[1]+'\n Date:'+row[2]+'\nTime:'+row[3]+'\n Location: '+row[4]
        email_text = """\  
        From: %s  
        To: %s  
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)
        message = 'Subject: {}\n\n{}'.format(subject, email_text)

        try:
             server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
             server.ehlo()
             server.login(gmail_user, gmail_password)
             server.sendmail(sent_from, to, message)
             server.close()
             print("Email sent!")
        except:
            print("Something went wrong...")
        print("inserted")
        conn.close()

        #return rows
        return render_template('newdata.html')

        #return render_template('meetingmember.html', data = rows)
     except Exception as e:
        return (str(e))
    

@app.route('/meetingmember',methods=['POST','GET'])
def meeetingmember():   
    try:
        print("Hello") 
        conn = mysql.connect()
        cursor = conn.cursor()
        # validate the received values
        member_id = request.form.getlist("email.id")
        emails = request.form.getlist("email.emails")
        print(emails)
        print(member_id)
                        
        sql = "INSERT INTO meeting_member(meeting_member_id,meeting_id,status) " \
               "VALUES(%s, %s, %s, %s)"
        #print(sql)
        #print(request.form["organization_id"])
        print(request.form["meeting_member_id"])
        print(request.form["meeting_id"])
        #print(request.form["status"])
		  
        data = (0,11)
        #data = (0,"aaa","bb","ss","sd","sd","2013-04-04","aaa",2323,233,"wq",1)
        
        # Execute the SQL command
        print(data)
        result = cursor.execute(sql,data)
        print(result);
        # Fetch all the rows in a list of lists.
		
        if len(data) is 0:
            return json.dumps({'error':str(data[0])})   
        else:
            conn.commit()
            #return json.dumps({'message':'organization account created successfully !'})
            return render_template('meetingmember.html')
       

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
@app.route('/meetingdata')
def display_meetingdata():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM meeting"
        cursor.execute(query)

        rows = cursor.fetchall()
        print(rows)
        conn.close()

        #return rows

        return render_template('meetingdata.html', data = rows)

    except Exception as e:
        return (str(e))




    
@app.route('/meeting_member')       
def display_meeting_member():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        query = "SELECT * FROM meeting_member"
        cursor.execute(query)

        rows = cursor.fetchall()
        print(rows)
        conn.close()

        #return rows

        return render_template('meeting_member.html', data = rows)

    except Exception as e:
        return (str(e))	      
        
if __name__ == "__main__":
    app.run()
