import cv2                        ## OpenCV library for Image Processing 
import time                       ## For Time
import argparse                   ## It's what you use to get command line arguments into your program. Adds Flexibility.
import numpy as np                ## Numpy library is used to work with arrays.
import tkinter as tk              ## For GUI
from tkinter import simpledialog  ## For Dialogue Box 


print("-----WELCOME TO VIDEO CAPTURNING ROI PROGRAM------")
print("=> INSTUCTIONS:")
print("=> STEP 1: WE NEED TO STOP THE ON A SINGLE FRAME WITH 'C'. ")
print("=> STEP 2: SELECT THE ROI ON THE FRAME THROUGH MOUSE. ")
print("=> STEP 3: PRESS 'C' TO CONFIRM THE ROI SELECTED. ")
print("=> STEP 4: GIVE AN ID TO ROI ON THE POP UP MENUE. ")
print("=> STEP 5: PRESS OKAY TO SAVE THE FILE. ")
print("=> STEP 6: NOW PRESS 'R' RESUME THE CAPTURING. ")
print("=> STEP 7: PRESS 'Q' QUIT. ")
print("=> NOTE: YOU CAN CAPTURE AGAIN AS WELL AFTER RESUME. ")

class staticROI(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0) # For Laptop Camera
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # For any external Camera other than laptop.
        

        # Bounding box reference points and boolean if we are extracting coordinates
        self.image_coordinates = []
        self.extract = False
        self.selected_ROI = False
        self.img_counter = 0
        self.fps_start_time = 0
        self.fps = 0
        self.im_coordinates = ""

        self.update()

    def FPS(self):
        self.fps_end_time = time.time()          ## Calculating FPS   
        self.time_diff = self.fps_end_time - self.fps_start_time
        self.fps = 1/(self.time_diff)
        self.fps_start_time = self.fps_end_time
        self.fps_text = "FPS : {:.2f}".format(self.fps)

    def update(self):
        while True:

            lower_fps_value = 0         ## Contolling the FPS Customize if you want.                 
            time.sleep(lower_fps_value)        


            if self.capture.isOpened():
                # Read frame
                (self.status, self.frame) = self.capture.read()

                if not self.status:                ## if does not grab the frames some how programm will end 
                    break   

                self.FPS()
                cv2.putText(self.frame,self.fps_text, (5,30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255,255), 1) 

                # This code right Here is used to resize if you want 

                # (height, width) = self.frame.shape[:2]
                # self.frame = cv2.resize(self.frame, (700, 500),interpolation=cv2.INTER_AREA)
                # numPixels = np.prod(self.frame.shape[:2])

                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('Grayscale', self.gray)

                cv2.imshow('image', self.frame)
                key = cv2.waitKey(2)

                # Crop image
                if key == ord('c'):
                    self.clone = self.frame.copy()
                    cv2.namedWindow('image')
                    cv2.setMouseCallback('image', self.extract_coordinates)
                    while True:
                        key = cv2.waitKey(2)
                        cv2.imshow('image', self.clone)
                        

                        # Crop and display cropped image
                        if key == ord('c'):
                            self.crop_ROI()
                            self.show_cropped_ROI()
                            self.save_croped_image()

                        # Resume video
                        if key == ord('r'):
                            cv2.destroyWindow('cropped image')
                            break
                # Close program with keyboard 'q'
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit(1)
            else:
                pass

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False
            self.selected_ROI = True

            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0,255,0), 2)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.frame.copy()
            self.selected_ROI = False

    def crop_ROI(self):
        if self.selected_ROI:
            self.cropped_image = self.frame.copy()

            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]

            x3 = min(x1,x2)
            y3 = min(y1,y2)
            x4 = max(x1,x2)
            y4 = max(y1,y2)

            self.cropped_image = self.cropped_image[y3:y4, x3:x4]
            self.im_coordinates = '({}), ({})'.format(self.image_coordinates[0], self.image_coordinates[1])
            print(f"Coordinates of Cropped Image {self.im_coordinates}")
        else:
            print('Select ROI to crop before cropping')

    def show_cropped_ROI(self):
        cv2.putText(self.cropped_image,self.im_coordinates, (5,30), cv2.FONT_HERSHEY_COMPLEX, 0.3, (0, 255,255), 1) 
        cv2.imshow('cropped image', self.cropped_image)

    def save_croped_image(self):
        ROOT = tk.Tk()
        ROOT.withdraw()
        ROI_ID = simpledialog.askstring(title="Popup",prompt="ENTER ROI_ID:")
        img_name = "ROI_{}.png".format(ROI_ID)
        cv2.imwrite(img_name, self.cropped_image)
        print("{} Saved!".format(img_name))
        self.img_counter += 1

if __name__ == '__main__':
    static_ROI = staticROI()
