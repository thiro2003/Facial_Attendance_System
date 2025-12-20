from flask import Flask,redirect,render_template,session,request,flash,url_for
import os
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import face_recognition
import numpy as np
from datetime import datetime
import cv2
from io import BytesIO
from PIL import Image
from datetime import date


app=Flask(__name__)
app.secret_key="Thiro"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Face_recognition.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['UPLOAD_FOLDER']="static/uploads"

db=SQLAlchemy(app)

class User(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  full_name=db.Column(db.String(100),nullable=False)
  email=db.Column(db.String(100))
  password=db.Column(db.String(100),nullable=False)
  image=db.Column(db.String(200))
  face_encoding = db.Column(db.PickleType)
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    attendance = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref=db.backref('attendances', lazy=True))  

  
with app.app_context():
  db.create_all()
  
  
  
  



@app.route('/mark_attendance')
def mark_attendance():
    if 'user' not in session:
        flash("Please login first ❌🚫", 'danger')
        return redirect('/')

    users = User.query.all()
    known_encodings = []
    known_user_ids = []
    known_usernames = []

    for user in users:
        if user.face_encoding is not None:
            known_encodings.append(user.face_encoding)
            known_user_ids.append(user.id)
            known_usernames.append(user.full_name)

    
    if len(known_encodings) == 0:
        flash("No registered faces found. Please register first ❌🚫", "danger")
        return redirect('/home')

    video = cv2.VideoCapture(0)
    marked = False
    attendance_message = None
    attendance_category = None

    while True:
        ret, frame = video.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_encodings,
                face_encoding,
                tolerance=0.5
            )

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            if len(face_distances) == 0:
                continue

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                user_id = known_user_ids[best_match_index]
                username = known_usernames[best_match_index]

                today = datetime.utcnow().date()
                existing = Attendance.query.filter(
                    Attendance.user_id == user_id,
                    db.func.date(Attendance.date_time) == today
                ).first()

                if existing:
                    attendance_message = "Attendance Already Marked For Today ✨👍"
                    attendance_category = "info"
                else:
                    attendance = Attendance(
                        user_id=user_id,
                        username=username,
                        attendance=True,
                        date_time=datetime.utcnow()
                    )
                    db.session.add(attendance)
                    db.session.commit()
                    attendance_message = "Attendance marked successfully ✨👍"
                    attendance_category = "success"

                marked = True
                break

        cv2.imshow("Mark Attendance - Press Q to exit", frame)

        if marked or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    if not marked:
        flash("Face not recognized ❌🚫", "danger")
    else:
        flash(attendance_message, attendance_category)

    return redirect('/home')

  
  
@app.route('/home',methods=['POST','GET'])
def home():
    if 'user' not in session:
        return redirect('/')

    user = session['user']
    user_attendance = Attendance.query.filter_by(username=user).all()

    return render_template(
        'home.html',
        user=user,
        attendances=user_attendance
    )

 
  
@app.route('/', methods=['POST','GET'])
def login():
    if 'user' in session:
      return redirect(url_for('home'))
    if request.method == 'POST':
        full_name = request.form.get('fullname').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')

        
        user = User.query.filter_by(email=email).first()

        if user:  
            
            if check_password_hash(user.password, password) and user.full_name.strip() == full_name:
                session['user'] = user.full_name
                flash("Login Successful ✨👍",'success')
                return redirect(url_for('home'))
            else:
                flash("Incorrect full name or password.",'danger')
        else:
            flash("User Does Not exists, Please Signup ❌🚫",'danger')
    
    return render_template('login.html')
  



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        image_file = request.files['image']

      
        img = face_recognition.load_image_file(image_file)
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            flash("No face detected. Please upload a clear face image ❌🚫", "danger")
            return redirect('/register')

        face_encoding = encodings[0]  


        new_user = User(
            full_name=full_name,
            email=email,
            password=generate_password_hash(password),
            face_encoding=face_encoding
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful ✨👍", 'success')
        return redirect('/')

    return render_template('register.html')


@app.route('/logout')
def logout():
  session.pop('user',None)
  flash("Log out Successfull ✨👍",'success')
  return redirect('/')
    
      

















if __name__=='__main__':
  app.run(debug=True)
