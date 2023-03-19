import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy

pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)

frameR = 100
wCam , hCam = 640 , 480
wScreen , hScreen = autopy.screen.size()
smooth = 7

cap.set(3, wCam)
cap.set(4, hCam)
# print(wScreen , hScreen)

detector = htm.handDetector() 
preX , preY = 0 , 0
curX , curY = 0 , 0

cnt_change = 20
click_type = 1

while(True):
    ret, cur_frame = cap.read()
    # cur_frame = cv2.flip(cur_frame , 1)
    cur_frame = detector.findHands(cur_frame)
    lmList, bbox = detector.findPosition(cur_frame)
    cv2.rectangle(cur_frame , (frameR , frameR) , (wCam - frameR , hCam - frameR) , (255 , 255 , 0) , 2)
    if len(lmList) != 0:
        x1 , y1 = lmList[8][1:]
        x2 , y2 = lmList[12][1:]
        fingers , fingercount = detector.FingerCount()
        if fingers[1] == 1 and fingers[2] == 0:  # mouse movement
            x3 = np.interp(x1 , (frameR , wCam-frameR) , (0 , wScreen))
            y3 = np.interp(y1 , (frameR , hCam-frameR) , (0 , hScreen))
            curX = preX + (x3 - preX) / smooth
            curY = preY + (y3 - preY) / smooth
            autopy.mouse.move(curX , curY)
            cv2.circle(cur_frame , (x1 , y1) , 10 , (255 , 0 , 0) , cv2.FILLED)
            preX = curX
            preY = curY
        if fingers[1] == 1 and fingers[2] == 1 and fingercount != 5:
            dist , cur_frame , coords = detector.findDistance(8 , 12 , cur_frame)
            if dist < 40:
                cv2.circle(cur_frame , (coords[-2], coords[-1]),15, (0, 255, 0), cv2.FILLED)
                if click_type == 1:
                    autopy.mouse.click()
                elif click_type == 0:
                    autopy.mouse.click(autopy.mouse.Button.RIGHT)
        if fingercount == 5:
            if cnt_change == 0:
                # print("what" , click_type == 1 , click_type == 0)
                if click_type == 1:
                    click_type = 0
                    cnt_change = 20
                else:
                    click_type = 1
                    cnt_change = 20
        if fingercount == 0:
            autopy.key.tap(autopy.key.Code.RETURN)

        cnt_change -= 1
        cnt_change = max(0 , cnt_change)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(cur_frame , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 0) , 3)
    cv2.imshow('frame' , cur_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()