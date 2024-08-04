import numpy as np
import mediapipe as mp
import time
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

landmarks = []
dir = 0
squat_ctr = 0


def calc_Angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    rad = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angD = np.abs(rad*180.0/np.pi)

    if angD>180:
        angD = 360 - angD
        return angD
    else:
        return angD

cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as Pose:
    while True:
        ret,img = cap.read()

        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        
        results = Pose.process(img)
        
        img.flags.writeable = True
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

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

        left_leg_angle = int(calc_Angle(lhip,lknee,lankle))
        right_leg_angle = int(calc_Angle(rhip,rknee,rankle))

        cv2.putText(img,str(left_leg_angle),
                    tuple(np.multiply(lknee,[640,470]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                    )
        
        cv2.putText(img,str(right_leg_angle),
                    tuple(np.multiply(rknee,[640,470]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                    )

    # Percentage value of the angles
        per_val_left_leg = int(np.interp(left_leg_angle,(70,175),(100,0)))
        per_val_right_leg = int(np.interp(right_leg_angle,(70,175),(100,0))) 

    # Bar values of angles so that the bar is filled 
        bar_left_leg = int(np.interp(per_val_left_leg,(0,100),(40+350,40)))
        bar_right_leg = int(np.interp(per_val_right_leg,(0,100),(40+350,42)))   



        # Outer-rect & Inner-rect for left leg
        cv2.rectangle(img,(590,40),(590+30,40+350),(0,0,0),3)
        cv2.rectangle(img,(595,bar_left_leg),(595+20,36+350),(0,0,255),cv2.FILLED)
        
        # Outer-rect & Inner-rect for right leg
        cv2.rectangle(img,(20,40),(20+30,40+350),(0,0,0),3)
        cv2.rectangle(img,(25,bar_right_leg),(25+20,36+350),(0,0,255),cv2.FILLED)

    # Percentage values of bar_left and bar_right
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
        
    # Put count on screen 
        cv2.rectangle(img,(480,5),(200,40),(255,255,255),cv2.FILLED)
        cv2.putText(img,f'SQUATS : {int(squat_ctr)}',(225,30),1,2,color=(0,0,0),thickness=3)
    # Display Hand names
        cv2.putText(img,'Left-Leg',(12,350+60),1,2,color=(0,255,255),thickness=2)
        cv2.putText(img,'Right-Leg',(438,350+60),1,2,color=(0,255,255),thickness=2)

        mp_drawing.draw_landmarks(img,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=2))

        

        cv2.imshow("Squats",img)
        if cv2.waitKey(1)==ord('q'):
            break