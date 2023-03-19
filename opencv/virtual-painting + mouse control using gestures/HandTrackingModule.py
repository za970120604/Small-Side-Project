import cv2
import mediapipe as mp
import time # to check the frame rate
import math

class handDetector():
    def __init__(self , mode = False , max_hand = 2 , modelC = 1 , detectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode
        self.max_hand = max_hand
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode , self.max_hand , self.modelC , self.detectionCon , self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self , frame , draw = True):
        frameRGB = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB) # mediapipe only support RGB image
        self.results = self.hands.process(frameRGB)
        #  print(results.multi_hand_landmarks) # check if the hand is detected by mediapipe
        if self.results.multi_hand_landmarks:
            for single_hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame , single_hand , self.mpHands.HAND_CONNECTIONS) # draw 21 landmarks and handlines on the current frame which is shown
        return frame
    
    def findPosition(self , frame, handNumber = 0 , draw = True):
        self.landmarks = []
        xmin = 200000
        xmax = -1 
        ymin = 200000
        ymax = -1
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id , landmark in enumerate(myHand.landmark):
                # print(id , landmark)
                h , w , channel = frame.shape
                cx , cy = int(landmark.x*w) , int(landmark.y*h) # convert the 2D coordinate in the scene into pixel value , which is integer
                xmin = min(xmin , cx)
                xmax = max(xmax , cx)
                ymin = min(ymin , cy)
                ymax = max(ymax , cy)
                self.landmarks.append([id , cx , cy])
                # if draw:
                #     cv2.circle(frame , (cx , cy) , 10 , (255 , 0 , 255) , cv2.FILLED)
            if draw:
                cv2.rectangle(frame , (xmin - 20, ymin - 20) , (xmax + 20, ymax + 20) , (0, 255, 0), 2)

        return self.landmarks , [xmin , ymin , xmax , ymax]
    
    def FingerCount(self , is_left_hand = True):
        fingers = []
        if self.landmarks:
            tipIds = [4, 8, 12, 16, 20]
            # Thumb : 
            if self.landmarks[tipIds[0]][1] < self.landmarks[tipIds[0] - 1][1]:
                if is_left_hand:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if is_left_hand:
                    fingers.append(0)
                else:
                    fingers.append(1)
            # Rest of the fingers
            for id in range(1, 5):
                if self.landmarks[tipIds[id]][2] < self.landmarks[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers , fingers.count(1)
    
    def drawTip(self , frame , handNumber = 0 , tipID = -1 , color = (255 , 0 , 255)):
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id , landmark in enumerate(myHand.landmark):
                # print(id , landmark)
                h , w , channel = frame.shape
                cx , cy = int(landmark.x*w) , int(landmark.y*h) # convert the 2D coordinate in the scene into pixel value , which is integer
                self.landmarks.append([id , cx , cy])
                if (id == tipID) or tipID == -1:
                    cv2.circle(frame , (cx , cy) , 8 , color , cv2.FILLED)
        return frame
    
    def findDistance(self , p1 , p2 , img , draw = True , r = 15 , t = 3):
        x1, y1 = self.landmarks[p1][1:]
        x2, y2 = self.landmarks[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


        


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while(True):
        ret, cur_frame = cap.read()
        cur_frame = detector.findHands(cur_frame)
        landmarks = detector.findPosition(cur_frame)
        # if len(landmarks) != 0:
        #     print(landmarks[4])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(cur_frame , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3)
        cv2.imshow('frame' , cur_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()