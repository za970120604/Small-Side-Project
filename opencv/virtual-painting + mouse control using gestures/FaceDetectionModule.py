import cv2
import mediapipe as mp
import time

class faceDetector():
    def __init__(self , minDetectionCon = 0.6):
        self.minDetectionCon = minDetectionCon
        
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)
        self.mpDraw= mp.solutions.drawing_utils
    
    def findFaces(self , img , draw = True):
        imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxes = []
        if self.results.detections:
            for id , detection in enumerate(self.results.detections):
                self.mpDraw.draw_detection(img , detection)
                bboxC = detection.location_data.relative_bounding_box
                h , w , channel = img.shape
                bbox = int(bboxC.xmin * w) , int(bboxC.ymin * h) , int(bboxC.width * w) , int(bboxC.height * h)
                bboxes.append([id, bbox, detection.score])
                if draw:
                    l = 30
                    t = 5
                    rt = 1
                    x , y , w , h = bbox
                    x1 , y1 = x+w , y+h
                    cv2.rectangle(img, bbox , (255 , 0 , 255) , rt) 
                    # top , left
                    cv2.line(img , (x,y) , (x+l , y) , (255 , 0 , 255) , t)
                    cv2.line(img , (x,y) , (x , y+l) , (255 , 0 , 255) , t)
                    # top right
                    cv2.line(img , (x1,y) , (x1-l , y) , (255 , 0 , 255) , t)
                    cv2.line(img , (x1,y) , (x1 , y+l) , (255 , 0 , 255) , t)
                    # bottom , left
                    cv2.line(img , (x,y1) , (x+l , y1) , (255 , 0 , 255) , t)
                    cv2.line(img , (x,y1) , (x , y1-l) , (255 , 0 , 255) , t)
                    # top right
                    cv2.line(img , (x1,y1) , (x1-l , y1) , (255 , 0 , 255) , t)
                    cv2.line(img , (x1,y1) , (x1 , y1-l) , (255 , 0 , 255) , t)

                    cv2.putText(img , str(int(detection.score[0]*100))+'%' , (bbox[0] , bbox[1]-20) , cv2.FONT_HERSHEY_PLAIN , 2 , (255 , 0 , 255) , 3) 
        return img , bboxes  


def main():
    cap = cv2.VideoCapture("FaceVideo/1.mp4")
    detector = faceDetector(0.9)
    pTime = 0
    cTime = 0
    while(True):
        ret, img = cap.read()
        img = cv2.resize(img , (960, 540))
        img , bboxes = detector.findFaces(img)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img , str(int(fps)) , (10 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 255) , 3) 
        cv2.imshow('image' , img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()