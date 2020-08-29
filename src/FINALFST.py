from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import cv2
import os
import numpy as np
import mysql.connector as mc
import pyttsx3
from os import path
import unittest
from summa.summarizer import summarize
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from tkinter import messagebox
#from summa.summarizer import utils
#from utils import get_text_from_test_data
import os.path
import sys
from PIL import ImageTk
import speech_recognition as sr
meeting=0
t=(24,11)

conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
cur = conn.cursor()
#num=cur.execute ("""UPDATE meeting_member SET status=%s WHERE member_id= %s""", (t))
#res=cur.fetchall()


conn.commit()

#print(res)

r = sr.Recognizer()
#FILENAME = 'F:\project fair\FINAL PROJECT CODE\FR(Version 2)\myimage.png'
def detect_face(img):
    #convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('D:\SEM-8\FINAL PROJECT CODE\FR(Version 2)\lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    #cv2.resize(gray, (640, 360))
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]


def prepare_training_data(data_folder_path):
    
    dirs = os.listdir(data_folder_path)
    
    faces = []
    
    labels = []

    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue;
            
       
        label = int(dir_name.replace("s", ""))
        
        subject_dir_path = data_folder_path + "/" + dir_name
        
        #get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            
            #ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;
            image_path = subject_dir_path + "/" + image_name

            #read image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #display an image window to show the image 
            cv2.imshow("Training on image...", cv2.resize(gray, (400, 500)))
            cv2.waitKey(100)
            
            #detect face
            face, rect = detect_face(image)
            
            #------STEP-4--------
            #for the purpose of this tutorial
            #we will ignore faces that are not detected
            if face is not None:
                #add face to list of faces
                cv2.resize(face, (640, 360))
                faces.append(face)
                #add label for this face
                labels.append(label)
    print(labels)        
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels



#create our LBPH face recognizer 



def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
     
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(test_img):
    print("Predictions ")
    img = test_img.copy()
    #cv2.imshow('my image',img)
    face, rect = detect_face(img)
    print("Len ",len(face))
    if (len(face) == 0):
         print("not detect")
    #if not face:
    #    print("error")
    #cv2.imshow('my image',face)
    label, confidence = face_recognizer.predict(face)
    print(label)
    print(confidence)
    if not label:
        print("not found!!")

    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    engine = pyttsx3.init()
    engine.say("Hello and welcome"+label_text+ "into meeting ")
    engine.setProperty('rate',100)  
    engine.runAndWait()
    conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
    cur = conn.cursor()
    #sql1="SELECT concat(concat(fname,' '),lname) as username FROM "
#sql2="SELECT lname FROM member"
    #print(sql1)
    #query = " SELECT member_id FROM member WHERE organization_id = %s "
 
    #print(label_text)
    data = (label_text, )
    #result=cur.execute(query,data)
    #print(result)
    numrows = cur.execute("SELECT member_id FROM member where concat(concat(fname,' '),lname)= %s",data)
    print ("Selected %s rows" % numrows )     
    print ("Selected %s rows" % cur.rowcount)
    result=cur.fetchall()
    print(result)
    #c=result.split('(')
    #print(c)
    #bi=tuple(result)
    b=[]
    #for i in result:
        #b.append(i)
        #b=', '.join(i)
    #print(b)
    t = ''.join(str(n) for n in result)
    
    #t=t.remove(",")
    t=t.replace(',', '')
    print(t)
    t=t.replace('(', '')
    t=t.replace(')', '')
    print("new value:",t)
    aList = list(t)
    #print(bi)
    #num=cursor.execute("INSERT INTO member WHERE name IN (%s, %s, %s), ["name1", "name2", "name3", id, pid])
    sql_update_query = """UPDATE meeting_member SET (status)=%s WHERE member_id= %s"""
    #sql="UPDATE meeting_member SET status = 1, WHERE member_id = 24"
    sql="UPDATE meeting_member SET status = %s WHERE member_id = %s"

    ram = 1
    member_id = [24,11]
    inp = (1,)
    #inp[1]=24
    aabb = (1,t)
    #aabb = list(aabb)
    #aabb.insert(1, t)
    #aabb = tuple(aabb)
    print(aabb)
    res=cur.execute(sql,aabb)
    print(res)

    
    return img


conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
cur = conn.cursor()
sql1="SELECT concat(concat(fname,' '),lname) as username FROM member"
#sql2="SELECT lname FROM member"
print(sql1)
cur.execute(sql1)

result=cur.fetchall()
result = list(sum(result, ()))
#print( subjects)
print(result) 
subjects=[""]
for i in result:
    print(i)
    #subjects.insert(i)
    subjects.append(i)
print(subjects)    
#subjects = ["", "YALE","elvis","bilin","krishna bhadja","krishna ahire","ritva","not found!!"]
data_folder_path=r"D:\SEM-8\FINAL PROJECT CODE\FR(Version 2)\training-data"
window = Tk()
 
window.title("Welcome to LikeGeeks app")
 
window.geometry('3500x2000')

#canvas =Canvas(window, width=250, height=250)
#canvas.pack()
#tk_img = ImageTk.PhotoImage(file = FILENAME)
#canvas.create_image(125, 125, image=tk_img)

lbl = Label(window, text="Hello")
lbl2 = Label(window,text="select meeting name:")
conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
cur = conn.cursor()
sql="SELECT concat(concat(meeting_id,' '),meeting_topic) as meetingname FROM meeting"
#sql2="SELECT  FROM member"
print(sql)
cur.execute(sql)
result=cur.fetchall()
print(result)
option=[]
for row in result:
    print(row)
    option.append(row)
#combo = Combobox(window)
#combo['values']= option
#lab=Label(window,text="Select Meeting Topic:")
#lab.place(relx="0.1",rely="0.1")
cmb = ttk.Combobox(window, width="20", values=option)
#cmb.place(relx="0.1",rely="0.1")
#cmb.grid(column=2, row=2)
text1 = Text(window)
text1.grid(column=3, row=3)
#text1.pack_forget()
text1.grid_remove()
text2 = Text(window)
text2.grid(column=4, row=4)
#text1.pack_forget()
text2.grid_remove()
#text1.insert(END,"aa")

##def call2():
##            text="Hello USers"
##            
##            f=open("F:\web interface\workspace\ritva2.txt","w+")
##            print(text)
##            f.write(text)
##            f.close()
           
def call():
    #text1.insert(END,"ZZZZ")
#while True:
    print(cmb.get())
    meeting=cmb.get()
    meeting=meeting.split(" ")
    print(meeting)
    me=cmb.get()
    me=me.split(" ")
    print("printed:",me)
    print(me[1])
    fname="STT"+me[1]+".txt"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)  
        print("SAY SOMETHING");
        audio=r.listen(source)
        try:
            print("TEXT : "+r.recognize_google(audio,language = 'US-IN'))
            text=r.recognize_google(audio,language = 'US-IN')
             #text1.pack()
            #text1.grid(column=0, row=3,visible ='yes')
            f=open(fname,"w+")
            #print(text)
            f.write(text)
            f.close()
            with open(r"D:\SEM-8\FINAL PROJECT CODE\FR(Version 2)\rr.wav", "wb") as f:
                f.write(audio.get_wav_data())
            sleep()
        except:
            pass;
        #reply=input('Press s to stop ')
    #if reply == 's':
            #break
        print("TIME OVER, THANKS")
        text1.lift()
        text1.insert(END,text)
        text1.grid(column=3,row=3)
        bt.grid(column=1, row=4)
    lbl.configure(text="start recording... !!")
    

 


print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")
print("Predicting images...")
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
#face_recognizer = **cv2.face.LBPHFaceRecognizer_create()**
#face_recognizer = cv2.face.LBPHFaceRecognizer_create()
#face_recognizer = cv2.face.createLBPHFaceRecognizer()
face_recognizer.train(faces, np.array(labels))
faceCascade = cv2.CascadeClassifier('HAAR/haarcascade_frontalface_default.xml')

def clicked():
    lbl.configure(text="Button was clicked !!")
    conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
    cur = conn.cursor()
    sql="SELECT face_image_1 FROM member where member_id=23"
    print(sql)
    cur.execute(sql)
    result=cur.fetchall()
    print(result)
    conn.close()

    cap = cv2.VideoCapture(0)
    lbl.configure(text="Button was clicked !!")
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    while True:
        ret, img = cap.read()
        if not img is None: 
            if not ret: continue
            img = cv2.flip(img, 1)
            cv2.resize(img, (640, 360))
            gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.resize(gray, (640, 360))
            face = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
             )
        #print(face)
        #predicted_img1 = predict(img)
        #test_img1 = cv2.imread(img)
        
            for (x,y,w,h) in face:
                cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
            
                roi_color = img[y:y+h, x:x+w]
        cv2.resize(img, (320, 243))
        #k1=predict(img)
        #print(k1)
        cv2.imshow('video',gray)
        
        
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    #test_img1 = cv2.imread("test-data/test1.png")
    #test_img2 = cv2.imread("test-data/test2.png")

#perform a prediction
    predicted_img1 = predict(img)
    cv2.imshow('Image',predicted_img1)
    btnn.grid(column=1, row=3)
    lbl2.grid(column=1, row=2)
    cmb.grid(column=2, row=2)
def summary():
    filename=r'D:\SEM-8\FINAL PROJECT CODE\FR(Version 2)\testing.txt'
    f = open(filename, "r")
    #print(f.read())
    text=f.read()
    print(text)
    data=summarize(text,  ratio=0.2)
    print(summarize(text, ratio=0.2))
    #print(summarize(text, words=50))
    #print(summarize(text, language='english'))
    #print(summarize(text, split=True))
    text2.lift()
    text2.insert(END,data)
    text2.grid(column=3,row=4)
    me=cmb.get()
    me=me.split(" ")
    new=me[1].replace('}','')
    print("printed: ",new)
    print(me[1])
    fname=new+".txt"
    print(fname)
    file1=open(fname,"w")
    file1.write(data)
    file1.close()
    
    conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
    cur = conn.cursor()
    print(meeting)
    sql="SELECT * FROM meeting_member"
    #sql2="SELECT  FROM member"
    print(sql)
    #cur.execute(sql,(meeting))
    cur.execute(sql)
    result=cur.fetchall()
    print(result)
    fromaddr = "meetingnotetake14@gmail.com"
    #toaddr = "ritu234.fetr@gmail.com"
    to = ('krishnaahire24@gmail.com', 'ritu234.fetr@gmail.com','bilin478@gmail.com','krishnabhadja369@gmail.com','ajtank18@gmail.com')
    #toaddr=', '.join(result)
    toaddr=to
    
    msg = MIMEMultipart()   
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr )
    #msg['To'] = toaddr 
    msg['Subject'] = "Meeting text summarization"
    body = "Meeting document is attached here!!\n Meeting ID and Name :"+cmb.get()
    msg.attach(MIMEText(body, 'plain'))  
    filename = "myfile.txt"
    attachment = open("D:\SEM-8\FINAL PROJECT CODE\FR(Version 2)\myfile.txt", "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "Project@1234") 
    text = msg.as_string()  
    s.sendmail(fromaddr, toaddr, text) 
    s.quit()
    messagebox.showinfo("Mail Notification", "THANK YOU FOR ATTENDING THE MEETING\n DOCUMENTS OF THE MEEETINGS ARE SENDED!!!")
    conn = mc.connect(user="root", password="", host="localhost", database="meetingdata")
    cur = conn.cursor()
##    #print(meeting)
##    sql="SELECT * FROM meeting_member"
##    #sql2="SELECT  FROM member"
##    print(sql)
##    #cur.execute(sql,(meeting))
##    cur.execute(sql)
##    result=cur.fetchall()
##    print(result)
    
    #print(me[1].split('}'))
    data = (0, cmb.get(), filename)
##    print(cmb.get())
##    asdf=cmb.get()
##    a=asdf.joint('.txt')
##    print(a)
    sql = """ INSERT INTO meeting_summary (report_id, meeting_id_name, summary_report) VALUES (%s, %s, %s) """  
    print(sql, data)
    cursor = conn.cursor()
    cursor.execute(sql, data)
#cmb.grid(column=2, row=2)
btn = Button(window, text="Face Recognition", command=clicked)
btnn = Button(window, text="Start Recording", command=call)
bt = Button(window, text="Text Summarization", command=summary)
#bt.grid(column=1, row=4) 
#cmb.grid(column=2, row=2)
btn.grid(column=1, row=1)









