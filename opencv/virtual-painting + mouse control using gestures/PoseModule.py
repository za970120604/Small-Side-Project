import cv2
import mediapipe as mp
import time

class poseDetector():
    def __init__(self , mode = False , modelC = 1 , upBody = False , smooth = True , detectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode
        self.modelC = modelC
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode , self.modelC , self.upBody , self.smooth , self.detectionCon , self.trackCon)
        self.mpDraw= mp.solutions.drawing_utils
    
    def findPose(self , img , draw = True):
        imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img , self.results.pose_landmarks , self.mpPose.POSE_CONNECTIONS)
        return img   

    def findPosition(self , img , draw = True):
        lmList = []
        for id , lm in enumerate(self.results.pose_landmarks.landmark):
            h , w , channel = img.shape
            cx , cy = int(lm.x*w) , int(lm.y*h)
            lmList.append([id , cx , cy])
            if draw:
                cv2.circle(img , (cx , cy) , 10 , (255 , 0 , 0) , cv2.FILLED)
        return lmList

# while(True):
#     ret, img = cap.read()
#     img = cv2.resize(img , (960, 540))
#     imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
#     results = pose.process(imgRGB)
#     # print(results.pose_landmarks)
#     if results.pose_landmarks:
#         mpDraw.draw_landmarks(img , results.pose_landmarks , mpPose.POSE_CONNECTIONS)
#         for id , lm in enumerate(results.pose_landmarks.landmark):
#             h , w , channel = img.shape
#             cx , cy = int(lm.x*w) , int(lm.y*h)
#             cv2.circle(img , (cx , cy) , 5 , (255 , 0 , 255) , cv2.FILLED)

def main():
    cap = cv2.VideoCapture("PoseVideo/1.mp4")
    detector = poseDetector()
    pTime = 0
    cTime = 0
    while(True):
        ret, img = cap.read()
        img = cv2.resize(img , (960, 540))
        img = detector.findPose(img)
        lmList = detector.findPosition(img) 
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3) 
        cv2.imshow('image' , img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()