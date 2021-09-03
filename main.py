from ast import copy_location
import cv2
import numpy as np
import argparse
from sklearn.cluster import KMeans
import drawcircle

class camera_Sign():
    def __init__(self):
        self.filename = "LocationData.txt"
        self.cap = cv2.VideoCapture("./WIN_20210818_15_37_30_Pro.mp4")
        self.Led_Box = []
        self.label_sum = []
        self.Location_Read()
        self.run()

    def Location_Read(self):
        with open(self.filename, "r", encoding = "utf-8") as f:
            data = f.readlines()
            data = [x for x in data if(len (x)>0)]
            data = [x.strip().split(',') for x in data]
            for d in data:
                self.Led_Box.append([int(x) for x in d])

    def Led_State_Judge(self, image):
        ledmeans_list = []
        block_flag = []
        for bbox in self.Led_Box: 
            ledimage = image[int(bbox[2]):int(bbox[3]), int(bbox[0]):int(bbox[1]), :]
            ledmeans = np.mean(np.mean(ledimage, axis=0), axis=0)
        #    print(ledmeans)
            ledmeans_list.append(ledmeans)
        #    cv2.imshow("led", ledimage)

        kmeans = KMeans(n_clusters=2).fit(ledmeans_list)
        centers = kmeans.cluster_centers_
        y_pred = kmeans.labels_
        centerMeans = np.mean(centers, axis=1)
        ratio = 50
        resLabel = None
        if(centerMeans[0] > ratio and centerMeans[1] > ratio):
            # all on
            resLabel = [True for x in y_pred]
        elif(centerMeans[0] < ratio and centerMeans[1] < ratio) :
            resLabel = [False for x in y_pred]
            # all off
        else:
            # have on and off
            print(centerMeans)
            if(centerMeans[0] > centerMeans[1]):
                # lables[0] on
                resLabel = [x == 0 for x in y_pred]
            else: 
                # lables[1] on
                resLabel = [x == 1 for x in y_pred]
        if(self.label_sum == []):
            self.label_sum = resLabel
        # for x in self.label_sum:

        self.label_sum = [self.label_sum[x] or resLabel[x] for x in range(len(resLabel))]
        print(self.label_sum)
        return self.label_sum


    def run(self):       
        cv2.namedWindow("led show")
        led_locat_flag = [0 for x in range(100)]
        while(True):
            _, frame = self.cap.read()
            
            #copyimg = frame.copy()
            #copyimg = cv2.cvtColor(copyimg, cv2.COLOR_BGR2GRAY)
            led_state = self.Led_State_Judge(frame)
            
            for bbox, label in zip(self.Led_Box, led_state):
            #    print(bbox)
                cv2.rectangle(
                    frame, (bbox[0], bbox[2]), (bbox[1], bbox[3]), (255, 255, 0), thickness = 1)
#                print(len(led_stateflag))
                if label:
                    cv2.putText(
                        frame, 'O', (bbox[0], bbox[2]-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
                    print(bbox[0] + bbox[2]-10)
                    
#                elif  :
                else:
                    cv2.putText(
                        frame, 'X', (bbox[0], bbox[2]-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

            cv2.imshow("led show", frame) 

            if(cv2.waitKey(100) == ord('q')):
#                cv2.imwrite("img.jpg", copyimg)
                cv2.destroyAllWindows();
                break

if __name__ == "__main__":
    camera_sign = camera_Sign()

