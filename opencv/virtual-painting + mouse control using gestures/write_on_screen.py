import cv2
import numpy as np
import time
import HandTrackingModule as htm


brushThickness = 10
eraserThickness = 30

drawColor = (255 , 191 , 0)
cnt_draw = 20
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.8)
xp , yp = 0 , 0 
while(True):
    ret, cur_frame__ = cap.read()
    cur_frame_ = cv2.flip(cur_frame__ , 1)
    cur_frame = cv2.flip(cur_frame__ , 1)
    for i in range(1 , 100):
        cur_frame[0:i , 100:200] = (51 , 128 , 255)
        cur_frame[0:i , 400:500] = (0 , 128 , 0)
        cur_frame[0:i , 700:800] = (255 , 191 , 0)
        cur_frame[0:i , 1000:1100] = (0 , 0 , 0)

    cur_frame = detector.findHands(cur_frame , draw = False)
    landmarks = detector.findPosition(cur_frame , draw = False)

    if len(landmarks) != 0:
        x1 , y1 = landmarks[8][1:] # index finger
        x2 , y2 = landmarks[12][1:] # middle finger
        fingers , fingercount = detector.FingerCount()
    
        # selection mode
        if fingers[1] == 1 and fingers[2] == 1:
            cnt_draw = 30
            xp , yp = 0 , 0
            if y1 < 100:
                if 100 < x1 < 200:
                    drawColor = (51 , 128 , 255)
                elif 400 < x1 < 500:
                    drawColor = (0 , 128 , 0)
                elif 700 < x1 < 800:
                    drawColor = (255 , 191 , 0)
                elif 1000 < x1 < 1100:
                    drawColor = (0 , 0 , 0)
            cv2.rectangle(cur_frame, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # drawing mode
        if fingers[1] == 1 and fingers[2] == 0:
            if cnt_draw < 0:
                cv2.circle(cur_frame , (x1, y1) , brushThickness , drawColor , cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    cv2.line(cur_frame , (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                
                else:
                    cv2.line(cur_frame , (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1
            else:
                cnt_draw -= 1
        
       
        
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _,imgBinary = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV) # getting image that is draw by black line
        imgInv = cv2.cvtColor(imgBinary,cv2.COLOR_GRAY2BGR)
        cur_frame = cv2.bitwise_and(cur_frame,imgInv)
        cur_frame = cv2.bitwise_or(cur_frame,imgCanvas)
        if fingercount == 0:
            imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
            _,imgBinary = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV) # getting image that is draw by black line
            imgInv = cv2.cvtColor(imgBinary,cv2.COLOR_GRAY2BGR)
            cur_frame_ = cv2.bitwise_and(cur_frame_,imgInv)
            cur_frame_ = cv2.bitwise_or(cur_frame_,imgCanvas)
            cv2.imwrite("out.jpg" , cur_frame_)
        
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(cur_frame , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3)
    cv2.imshow('frame' , cur_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()