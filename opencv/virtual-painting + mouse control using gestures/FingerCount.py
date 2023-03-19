import cv2
import time
import HandTrackingModule as htm

# Cam_width = 640
# Cam_height = 480


pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)
# cap.set(3 , Cam_width)
# cap.set(4 , Cam_height)
detector = htm.handDetector(detectionCon=0.7)
while(True):
    ret, cur_frame = cap.read()
    cur_frame = cv2.flip(cur_frame , 1)
    cur_frame = detector.findHands(cur_frame)
    landmarks = detector.findPosition(cur_frame , draw = False)
    if len(landmarks) != 0:
        fingers , fingercount = detector.FingerCount()
        print(fingers)
        
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(cur_frame , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3)
    cv2.imshow('frame' , cur_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()