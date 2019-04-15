import numpy as np
import PIL
import imutils
import cv2
import time
from pymouse import PyMouse


l = 0   # average counter
a = 0   # mean x variable
b = 0   # mean y variable
hand_rect_one_y = None  # lower corner y coordinate
hand_rect_one_x = None  # lower corner x coordinate
hand_rect_two_x = None  # Upper corner x coordinate
hand_rect_two_y = None  # Upper corner y coordinate

###############Colour Ranges##############
# RED color limits
LowR = np.array([136,87,111]);
UpR = np.array([180,255,255]);

# Blue Color Limits
LowB = np.array([33,80,40]);
UpB = np.array([102,255,255]);

# Green Color Limits
LowG = np.array([22,60,6]);
UpG = np.array([60,255,255]);

# Yellow Color Limits
LowY = np.array([58,40,38]);
UpY = np.array([58,255,155]);

# morphology kernels
kernelOpen = np.ones((4,4))
kernelClose = np.ones((25,25))

#######mouse tracking function#########
def mouse_track(mse,x,y):
    global l,a,b
    if l == 2:
        a = a + x
        b = b + y
        x = int(a/l)
        y = int(b/l)
        l = 0
        a = 0
        b = 0
        size = mse.screen_size();
        size1 = np.array([640,480])
        x = int((x/1024)*size[0])
        y = int((y/768)*size[1])
        mse.move(x,y);
    else :
        a = a + x
        b = b + y
        l = l + 1




#extract the camera feed
vdcpt = cv2.VideoCapture(0)
time.sleep(1)
mse = PyMouse()
print("Press e to exit....")
while True :

    # extract colors from the images
    ret,img = vdcpt.read();     #read frame from video stream
    img = cv2.resize(img,(1024,768))     #resizing as it is easier to work on a standard size
    img=cv2.flip(img,1)
    imgHSV = cv2.GaussianBlur(img, (11, 11), 0)
    imgHSV = cv2.cvtColor(imgHSV,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV,LowG,UpG)     #create a mask for red color in the range specified

    #morphology
    imgerode = cv2.erode(mask,None,iterations=2)
    imgdilate = cv2.dilate(imgerode,None,iterations=2)
    imgfinal = imgdilate

    cont = cv2.findContours(imgfinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)

    if len(cont)>0 :

        cont = max(cont, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cont)
        M = cv2.moments(cont)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius > 15 :
            cv2.circle(img,(int(x),int(y)),int(radius),(0,255,0),2)
            cv2.circle(img,center,5,(0,255,0,-1))
            mouse_track(mse,int(x),int(y))

    mask1 = cv2.inRange(imgHSV,LowR,UpR)     #create a mask for red color in the range specified

    #morphology
    imgerode = cv2.erode(mask1,None,iterations=2)
    imgdilate = cv2.dilate(imgerode,None,iterations=2)
    imgfinal = imgdilate

    cont = cv2.findContours(imgfinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)

    if len(cont)>0 :
        cont = max(cont, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cont)
        M = cv2.moments(cont)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius > 22 :
            cv2.circle(img,(int(x),int(y)),int(radius),(255,0,0),2)
            cv2.circle(img,center,5,(255,0,0),-1)

    mask2 = cv2.inRange(imgHSV,LowB,UpB)     #create a mask for red color in the range specified

    #morphology
    imgerode = cv2.erode(mask2,None,iterations=2)
    imgdilate = cv2.dilate(imgerode,None,iterations=2)
    imgfinal = imgdilate

    cont = cv2.findContours(imgfinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)

    if len(cont)>0 :
        cont = max(cont, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cont)
        M = cv2.moments(cont)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius > 22 :
            cv2.circle(img,(int(x),int(y)),int(radius),(0,0,255),2)
            cv2.circle(img,center,5,(0,0,255),-1)

    mask3 = cv2.inRange(imgHSV,LowY,UpY)     #create a mask for red color in the range specified

    #morphology
    imgerode = cv2.erode(mask3,None,iterations=2)
    imgdilate = cv2.dilate(imgerode,None,iterations=2)
    imgfinal = imgdilate

    cont = cv2.findContours(imgfinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = imutils.grab_contours(cont)

    if len(cont)>0 :
        cont = max(cont, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cont)
        M = cv2.moments(cont)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius > 22 :
            cv2.circle(img,(int(x),int(y)),int(radius),(255,255,0),2)
            cv2.circle(img,center,5,(255,255,0),-1)

    cv2.imshow("cam",img)
    key = cv2.waitKey(10)
    if key == ord("e"):
        break
