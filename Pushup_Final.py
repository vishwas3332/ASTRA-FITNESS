import cv2
import mediapipe as mp
import numpy as np
import time


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
    else:
        return angD


def live_pushups():
    ptime = 0
    ctime = 0
    landmarks = []

    dir = 0
    global cnt
    cnt = 0

    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while True:
            ret, img = cap.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img.flags.writeable = False

            results = pose.process(img)

            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
            except:
                pass

            # print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
            lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            langle = calc_angle(lshoulder,lelbow,lwrist)
            rangle = calc_angle(rshoulder,relbow,rwrist)

            ctime = time.time()
            fps = 1/(ctime-ptime)
            ptime = ctime
            cv2.putText(img,f'FPS : {int(fps)}',(245,420),1,2,color=(0,0,0),thickness=2)

            cv2.putText(img,str(langle),
                    tuple(np.multiply(lelbow,[640,400]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                    )
            cv2.putText(img,str(rangle),
                    tuple(np.multiply(relbow,[640,400]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                    )

    # Percentage value of the angles
            per_val_langle = int(np.interp(langle,(75,175),(100,0)))
            per_val_rangle = int(np.interp(rangle,(75,175),(100,0)))

    # Bar values of angles so that the bar is filled 
            bar_langle = int(np.interp(per_val_langle,(0,100),(40+350,40)))
            bar_rangle = int(np.interp(per_val_rangle,(0,100),(40+350,42)))

    # Outer-rect & Inner-rect for left hand
            cv2.rectangle(img,(590,40),(590+30,40+350),(0,0,0),3)
            cv2.rectangle(img,(595,bar_langle),(595+20,36+350),(0,0,255),cv2.FILLED)

    # Outer-rect & Inner-rect for right hand
            cv2.rectangle(img,(20,40),(20+30,40+350),(0,0,0),3)
            cv2.rectangle(img,(25,bar_rangle),(25+20,36+350),(0,0,255),cv2.FILLED)

    # Percentage values of bar_left and bar_right
            cv2.putText(img,f'{per_val_langle}%',(560,25),1,2,color=(255,0,0),thickness=3)
            cv2.putText(img,f'{per_val_rangle}%',(25,25),1,2,color=(255,0,0),thickness=3)

            if (per_val_langle-per_val_rangle)>10:
                print("Right Hand is too low , cannot count the rep")
            elif(per_val_rangle-per_val_langle)>10:
                print("Left Hand is too low , cannot count the rep")
            else:
                print("Correct")
        
            if per_val_langle >= 97 and per_val_rangle >= 97:
                if dir==0:
                    cnt += 0.5
                    dir = 1
            elif per_val_langle <= 3 and per_val_rangle <= 3:
                if dir==1:
                    cnt += 0.5
                    dir = 0
    # Put count on the screen
            cv2.rectangle(img,(480,5),(200,40),(255,255,255),cv2.FILLED)
            cv2.putText(img,f'PUSH-UPS : {int(cnt)}',(225,30),1,2,color=(0,0,0),thickness=3)

    # Display Hand names
            cv2.putText(img,'Left-Hand',(12,350+60),1,2,color=(0,255,255),thickness=2)
            cv2.putText(img,'Right-Hand',(438,350+60),1,2,color=(0,255,255),thickness=2)
        

            mp_drawing.draw_landmarks(img,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            cv2.imshow("Pushups",img)

    # Exit loop when 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break
