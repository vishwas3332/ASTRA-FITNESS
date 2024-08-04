from flask import Flask ,render_template,url_for, Response, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import mediapipe as mp
import numpy as np
import time
import os
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Darahas1'
app.config['MYSQL_DB'] = 'Astra'

mysql = MySQL(app)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calc_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angD = np.abs(rad * 180.0 / np.pi)

    if angD > 180:
        angD = 360 - angD
    return angD

def generate_frames():
    ptime = 0
    ctime = 0
    dir = 0
    cnt = 0

    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while True:
            ret, img = cap.read()
            if not ret:
                break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img.flags.writeable = False

            results = pose.process(img)

            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                langle = calc_angle(lshoulder, lelbow, lwrist)
                rangle = calc_angle(rshoulder, relbow, rwrist)

                ctime = time.time()
                fps = 1 / (ctime - ptime)
                ptime = ctime
                cv2.putText(img, f'FPS : {int(fps)}', (245, 420), 1, 2, color=(0, 0, 0), thickness=2)

                cv2.putText(img, str(langle),
                            tuple(np.multiply(lelbow, [640, 400]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )
                cv2.putText(img, str(rangle),
                            tuple(np.multiply(relbow, [640, 400]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                per_val_langle = int(np.interp(langle, (75, 175), (100, 0)))
                per_val_rangle = int(np.interp(rangle, (75, 175), (100, 0)))

                bar_langle = int(np.interp(per_val_langle, (0, 100), (40 + 350, 40)))
                bar_rangle = int(np.interp(per_val_rangle, (0, 100), (40 + 350, 42)))

                cv2.rectangle(img, (590, 40), (590 + 30, 40 + 350), (0, 0, 0), 3)
                cv2.rectangle(img, (595, bar_langle), (595 + 20, 36 + 350), (0, 0, 255), cv2.FILLED)

                cv2.rectangle(img, (20, 40), (20 + 30, 40 + 350), (0, 0, 0), 3)
                cv2.rectangle(img, (25, bar_rangle), (25 + 20, 36 + 350), (0, 0, 255), cv2.FILLED)

                cv2.putText(img, f'{per_val_langle}%', (560, 25), 1, 2, color=(255, 0, 0), thickness=3)
                cv2.putText(img, f'{per_val_rangle}%', (25, 25), 1, 2, color=(255, 0, 0), thickness=3)

                if per_val_langle == 100 and per_val_rangle == 100:
                    if dir == 0:
                        cnt += 0.5
                        dir = 1
                elif per_val_langle == 0 and per_val_rangle == 0:
                    if dir == 1:
                        cnt += 0.5
                        dir = 0

                cv2.rectangle(img, (480, 5), (200, 40), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, f'PUSH-UPS : {int(cnt)}', (225, 30), 1, 2, color=(0, 0, 0), thickness=3)

                cv2.putText(img, 'Left-Hand', (12, 350 + 60), 1, 2, color=(0, 255, 255), thickness=2)
                cv2.putText(img, 'Right-Hand', (438, 350 + 60), 1, 2, color=(0, 255, 255), thickness=2)

                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            except:
                pass

            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()

            if cv2.waitKey(1)==ord('q'):
                break

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

def generate_frames_squats():
    cap = cv2.VideoCapture(0)
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, img = cap.read()

            if not ret:
                break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img.flags.writeable = False

            results = pose.process(img)

            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
            except:
                pass
            
            lhip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            lknee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            lankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            rhip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            rknee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            rankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            left_leg_angle = int(calc_angle(lhip,lknee,lankle))
            right_leg_angle = int(calc_angle(rhip,rknee,rankle))

            cv2.putText(img,str(left_leg_angle),
                        tuple(np.multiply(lknee,[640,470]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                        )
            
            cv2.putText(img,str(right_leg_angle),
                        tuple(np.multiply(rknee,[640,470]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                        )

            per_val_left_leg = int(np.interp(left_leg_angle,(70,175),(100,0)))
            per_val_right_leg = int(np.interp(right_leg_angle,(70,175),(100,0)))

            bar_left_leg = int(np.interp(per_val_left_leg,(0,100),(40+350,40)))
            bar_right_leg = int(np.interp(per_val_right_leg,(0,100),(40+350,42)))

            cv2.rectangle(img,(590,40),(590+30,40+350),(0,0,0),3)
            cv2.rectangle(img,(595,bar_left_leg),(595+20,36+350),(0,0,255),cv2.FILLED)

            cv2.rectangle(img,(20,40),(20+30,40+350),(0,0,0),3)
            cv2.rectangle(img,(25,bar_right_leg),(25+20,36+350),(0,0,255),cv2.FILLED)

            cv2.putText(img,f'{per_val_left_leg}%',(560,25),1,2,color=(255,0,0),thickness=3)
            cv2.putText(img,f'{per_val_right_leg}%',(25,25),1,2,color=(255,0,0),thickness=3)

            if per_val_left_leg >= 97 and per_val_right_leg >= 97:
                if dir == 0:
                    squat_ctr += 0.5
                    dir = 1
            elif per_val_left_leg <= 5 and per_val_right_leg <= 5:
                if dir == 1:
                    squat_ctr += 0.5
                    dir = 0

            cv2.rectangle(img,(480,5),(200,40),(255,255,255),cv2.FILLED)
            cv2.putText(img,f'SQUATS : {int(squat_ctr)}',(225,30),1,2,color=(0,0,0),thickness=3)

            cv2.putText(img,'Left-Leg',(12,350+60),1,2,color=(0,255,255),thickness=2)
            cv2.putText(img,'Right-Leg',(438,350+60),1,2,color=(0,255,255),thickness=2)

            mp_drawing.draw_landmarks(img,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=2))

            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO signup_details (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cur.close()

        flash('You have successfully signed up!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')  # Render the signup page on GET request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM signup_details WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    return render_template('login.html') 


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Squats')
def squats():
    return render_template("squats.html")

@app.route('/Pushups')
def pushups():
    return render_template("pushups.html")


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_squats')
def video_feed_squats():
    return Response(generate_frames_squats(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)