import cv2
import mediapipe as mp
import numpy as np
import time
import pose_module as pm

width = 1200
height = 780
dim = (width, height)

pTime = 0
dir = 0
count = 0

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()

def bicep_curls(arm='right'):

    global width, height, dim, pTime, dir, count, cap, detector

    while True:
        success, img = cap.read()

        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        img = detector.find_pose(img)
        lmList = detector.find_position(img)

        if len(lmList) != 0:
            
            if arm == 'right':
                angle = detector.find_angle(img, 12, 14, 16)
            elif arm == 'left':
                angle = detector.find_angle(img , 11, 13, 15)

            per = np.interp(angle, (60, 145), (100, 0))
            #print(per, angle)

            if per == 100:
                if dir == 0:
                    count+= 0.5
                    dir = 1
            if per == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0

            fill = np.interp(per, (0, 100), (750, 150))

            cv2.putText(img, f'{str(int(per))}%', (1030, 145), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            cv2.rectangle(img, (1040, 750), (1115, int(fill)), (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (1040, 150), (1115, 750), (0, 255, 0), 3)

            cv2.putText(img, str(int(count)), (10, 750), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5) 

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
def shoulder_press():
    
    global width, height, dim, pTime, dir, count, cap, detector

    while True:
        success, img = cap.read()

        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        img = detector.find_pose(img)
        lmList = detector.find_position(img)

        if len(lmList) != 0:
            
            aleft = detector.find_angle(img, 11, 12, 14)
            aright = detector.find_angle(img, 12, 11, 13)

            aleft_per = np.interp(aleft, (105, 170), (100, 0))
            aright_per = np.interp(aright, (105, 170), (100, 0))

            fleft = detector.find_angle(img, 11, 13, 15)
            fright = detector.find_angle(img, 12, 14, 16)

            fleft_per = np.interp(fleft, (70, 150), (0, 100))
            fright_per = np.interp(fright, (70, 150), (0, 100))

            if aleft_per == 100 and aright_per == 100 and fleft_per == 100 and fright_per == 100:
                if dir == 0:
                    count+= 0.5
                    dir = 1
            if aleft_per == 0 and aright_per == 0 and fleft_per == 0 and fright_per == 0:
                if dir == 1:
                    count += 0.5
                    dir = 0

            #l_fill = np.interp(left_per, (0, 100), (750, 150))
            #r_fill = np.interp(right_per, (0, 100), (750, 150))

            #cv2.putText(img, f'{str(int(left_per))}%', (1030, 145), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            #cv2.rectangle(img, (1040, 750), (1115, int(l_fill)), (0, 255, 0), cv2.FILLED)
            #cv2.rectangle(img, (1040, 150), (1115, 750), (0, 255, 0), 3)

            cv2.putText(img, str(int(count)), (10, 750), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5) 

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)