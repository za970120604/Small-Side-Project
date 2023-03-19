import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("FaceVideo/1.mp4")

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection()
mpDraw= mp.solutions.drawing_utils

pTime = 0
cTime = 0

while(True):
    ret, img = cap.read()
    img = cv2.resize(img , (960, 540))
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    # # print(results.detections)
    if results.detections:
        for id , detection in enumerate(results.detections):
            mpDraw.draw_detection(img , detection)
            # print(detection.score)
            # print(detection.location_data.relative_bounding_box)
            bboxC = detection.location_data.relative_bounding_box
            h , w , channel = img.shape
            bbox = int(bboxC.xmin * w) , int(bboxC.ymin * h) , int(bboxC.width * w) , int(bboxC.height * h)
            cv2.rectangle(img, bbox , (255 , 0 , 255) , 2)
            cv2.putText(img , str(int(detection.score[0]*100))+'%' , (bbox[0] , bbox[1]-20) , cv2.FONT_HERSHEY_PLAIN , 2 , (255 , 0 , 255) , 3) 

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3) 
    cv2.imshow('image' , img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break