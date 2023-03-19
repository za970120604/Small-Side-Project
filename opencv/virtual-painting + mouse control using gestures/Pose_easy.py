import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture("PoseVideo/1.mp4")

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw= mp.solutions.drawing_utils

pTime = 0
cTime = 0

while(True):
    ret, img = cap.read()
    img = cv2.resize(img , (960, 540))
    imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img , results.pose_landmarks , mpPose.POSE_CONNECTIONS)
        for id , lm in enumerate(results.pose_landmarks.landmark):
            h , w , channel = img.shape
            cx , cy = int(lm.x*w) , int(lm.y*h)
            cv2.circle(img , (cx , cy) , 5 , (255 , 0 , 255) , cv2.FILLED)

    # frameRGB = cv2.cvtColor(cur_frame , cv2.COLOR_BGR2RGB) # mediapipe only support RGB image
    # results = hands.process(frameRGB)
    # #  print(results.multi_hand_landmarks) # check if the hand is detected by mediapipe
    # if results.multi_hand_landmarks:
    #     for single_hand in results.multi_hand_landmarks:
    #         for id , landmark in enumerate(single_hand.landmark):
    #             # print(id , landmark)
    #             h , w , channel = cur_qframe.shape
    #             cx , cy = int(landmark.x*w) , int(landmark.y*h) # convert the 2D coordinate in the scene into pixel value , which is integer
    #             if id == 0:
    #                 cv2.circle(cur_frame , (cx , cy) , 25 , (255 , 0 , 255) , cv2.FILLED)
    #         mpDraw.draw_landmarks(cur_frame , single_hand , mpHands.HAND_CONNECTIONS) # draw 21 landmarks and handlines on the current frame which is shown
    # cTime = time.time()
    # fps = 1/(cTime - pTime)
    # pTime = cTime
    # cv2.putText(cur_frame , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3) 
    cv2.imshow('image' , img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break