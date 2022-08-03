import threading
import cv2
import time
from datetime import datetime

from matplotlib.pyplot import pause


from . import Object_Detector
from .detection_utils import draw_polly_and_check_isin

class VideoCamera(object):
    def __init__(self, cameraip="10.16.223.253"):
        # self.video = cv2.VideoCapture('rtsp://admin:Abc1234*@10.16.223.253/')
        self.cameraip = cameraip
        self.video = cv2.VideoCapture(f'rtsp://admin:Abc1234*@{self.cameraip}/cam/realmonitor?channel=1&subtype=0.')
        # self.video.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        #self.video = None
        #self.frame = None
        #self.grabbed = None
        (self.grabbed, self.frame) = self.video.read()
        self.jpeg = self.frame
        self.image = self.frame
        self.predictiontime = None
        self.detect = Object_Detector.ObjectDetection()
        # self.detect.setDaemon(True)
        self.start_time = time.time()
        self.display_time = 1
        self.fc = 0
        self.FPS = 0
        self.FLAG_1 = 0
        threading.Thread(target=self.get_video, args=()).start()
        threading.Thread(target=self.get_frame, args=()).start()

    def __del__(self):
        # sys.exit()
        self.video.release()

    def get_video(self):
        while True:
            try:
                (self.grabbed, self.frame) = self.video.read()
                if not self.grabbed:
                    self.video = cv2.VideoCapture(f'rtsp://admin:Abc1234*@{self.cameraip}/cam/realmonitor?channel=1&subtype=0.')

                # time.sleep(0.2)
                # print(self.grabbed, self.frame)
            except:
                print("REad hata")
    def get_frame(self):
        while True:
            try:
                # (self.grabbed, self.frame) = self.video.read()
                # self.frame = cv2.resize(self.frame, [200,200])
                # if not(self.grabbed):
                #     self.video = cv2.VideoCapture('rtsp://admin:Abc1234*@10.16.223.253/cam/realmonitor?channel=1&subtype=0.', cv2.CAP_FFMPEG)
                #     continue
                image = self.frame
                image = cv2.resize(image, (720, 576))
                self.fc+=1
                TIME = time.time() - self.start_time
                
                if (TIME) >= self.display_time :
                    self.FPS = self.fc / (TIME)
                    self.fc = 0
                    self.start_time = time.time()

                fps_disp = "FPS: "+str(self.FPS)[:5]
                
                # _, orgimage = cv2.imencode('.jpg', image)
                image_detected,  boxes, scores, classes= self.detect.object_detection(image)
                image_detected = draw_polly_and_check_isin(image_detected, boxes, scores, classes)
                self.predictiontime = datetime.now()
                image = cv2.putText(image_detected, fps_disp, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # cv2.imshow("Frame", image_detected)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
                # _, jpeg = cv2.imencode('.jpg', image)
                # self.jpeg = jpeg.tobytes()
                # self.image = orgimage.tobytes()
                _, image = cv2.imencode('.jpg', image_detected)
                
                self.jpeg = image.tobytes()
                # yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + self.jpeg + b'\r\n\r\n')
                    
            except:
                print("Detection hata.")    
            
            
            
            
            
        #self.image = image.tobytes()
            

    def gen(self):  
        while True: 
            try:
                yield (b'--frame\r\n' 
                    b'Content-Type: image/jpeg\r\n\r\n' + self.jpeg + b'\r\n\r\n')
                    
            except:
                pass

