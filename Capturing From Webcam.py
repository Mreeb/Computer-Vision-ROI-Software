import cv2                        ## OpenCV library for Image Processing 
import time                       ## For Time

print("-----WELCOME TO VIDEO CAPTURNING PROGRAM------")
print("=> INSTUCTIONS:")
print("=> THEN PRESS ENTER TO END COLLECTING FRAMES ")

fps_start_time = 0
fps = 0

capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)      ## this opnes the camera and "0" for just one camera
 
while(True):      

    lower_fps_value = 0          ## Contolling the FPS Customize if you want you can slow it too.                 
    time.sleep(lower_fps_value)                             

    (grabbed,frame) = capture.read()    ## Reading the captured frames from the video

    if not grabbed:                ## if does not grab the frames some how programm will end 
        break                          

    fps_end_time = time.time()          ## Calculating FPS   
    time_diff = fps_end_time - fps_start_time
    fps = 0.1/(time_diff)
    fps_start_time = fps_end_time
    fps_text = "FPS : {:.2f}".format(fps)

    cv2.putText(frame,fps_text, (5,30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255,255), 1)
    cv2.imshow('Frame', frame)          ## shows the live video on the screen
    

    key = cv2.waitKey(1) & 0xFF         ## this binds your code with the keyboard
    if key == 13:                       ## key == 13 is used for the Enter key which is used to end the program
	    break                          
    
capture.release()                       ## Closes video file or capturing device
cv2.destroyAllWindows()                 ## simply destroys all the windows we created. 
