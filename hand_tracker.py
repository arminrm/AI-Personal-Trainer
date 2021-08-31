import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)  #video capture object, argument is the device index

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils #MediaPipe Hands

pTime = 0
cTime = 0

while True:
    success, img = cap.read()   #if frame is read correctly, success=true. img would be the frame.

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #convert image from colourspace to rgb (2nd argument is colourspace conversion code)
    results = hands.process(imgRGB)  #Processes an RGB image and returns the hand landmarks and handedness of each detected hand.

    if results.multi_hand_landmarks:   #if hand landmarks exist; (none if nothing)
        for handLms in results.multi_hand_landmarks: 
            for id, lm in enumerate(handLms.landmark): #returns x, y, z coordinates for specific hand landmark
                h, w, c = img.shape  #returns height, width, channels (pixels)

                cx, cy = int(lm.x * w), int(lm.y * h)

                print(cx, cy)
        
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)  #Draws the landmarks and the connections on the image.

    #calculating fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    
    cv2.imshow("Image", img)  #display image in a window
    cv2.waitKey(1) #wait 1 ms