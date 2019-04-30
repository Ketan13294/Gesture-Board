import cv2
import imutils
import numpy as np
import threading
from scipy.spatial import distance as dist
from pynput.mouse import Controller, Button
from pynput.keyboard import Key, Controller as KeyController
from subprocess import call
import screeninfo
import os

# Right Hand - Index - RED
# Right Hand - Thumb - BLUE
# Left Hand - Index - YELLOW
# Left Hand - Thumb - GREEN

mouse=Controller()
keyboard = KeyController()


# app=wx.App(False)
# (sx,sy)=mse.screen_size()
screen = screeninfo.get_monitors()[0]
size = (screen.width, screen.height)

(camx,camy)=(320,240)

def IdentifyGesture():

    # Green Color Limits
    LowG = np.array([33,80,50]);
    UpG = np.array([80,255,255]);
    # Yellow Color Limits
    LowY = np.array([20,80,80]);
    UpY = np.array([40,255,255]);
    # Red Colour Limits
    LowR = np.array([0,100,80]);
    UpR = np.array([10,255,255]);
    # Blue Cot1lor Limits
    LowB = np.array([100,80,50]);
    UpB = np.array([120,255,255]);

    snap_count = 0
    snap_flag = 0
    tab_flag=0
    pinch = 0
    i=0
    lastR =0

    cam= cv2.VideoCapture(1)
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((5,5))

    def colourCenter(imgHSV, low, high, colHSV):
        mask = cv2.inRange(imgHSV,low,high)
        #morphology
        # maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        # maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

        #morphology
        maskOpen = cv2.erode(mask,None,iterations=4)
        maskClose = cv2.dilate(maskOpen,None,iterations=2)

        cont = cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cont = imutils.grab_contours(cont)

        if len(cont)>0 :
            cont = max(cont, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(cont)
            M = cv2.moments(cont)
            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
            if radius > 15 and radius < 100:
                cv2.circle(img,(int(x),int(y)),int(radius),colHSV,2)
                cv2.circle(img,center,5,colHSV,-1)
                return center

    def distance(c1, c2):
        return dist.euclidean(c1,c2)

    # print "distane", distance((243, 123), (111,673))
    while True:
        ret, img=cam.read()

        img=cv2.resize(img,size)
        img = cv2.flip(img,1)

        clone = img.copy()

        imgHSV = cv2.GaussianBlur(img, (7, 7), 0)
        imgHSV = cv2.cvtColor(imgHSV,cv2.COLOR_BGR2HSV)

            # cv2.imshow("maskClose", maskClose)
            # cv2.moveWindow("maskClose", 900, 100)

        R1 = centerR = colourCenter(imgHSV,LowR,UpR, (0, 0, 255))
        R2 = centerB = colourCenter(imgHSV,LowB,UpB, (255, 0, 0))
        L1 = centerG = colourCenter(imgHSV,LowG,UpG, (0, 255, 0))
        L2 = centerY = colourCenter(imgHSV,LowY,UpY, (0, 255, 255))

        # print "center R", centerR
        # print "center B", centerB
        # print "center G", centerG
        # print "center Y", centerY

        if centerB is not None:
                ### Mouse pointer Tracking ###
                mouse.position = centerB
                while mouse.position != centerB:
                    pass

        if centerR is not None and centerG is not None and centerB is not None and centerY is not None:

            # ### Mouse pointer Tracking ###
            # mouse.position = centerB
            # while mouse.position != centerB:
            #     pass

            ### Left Click - Hold and Release ###
            if(dist.euclidean(centerG, centerR) < 65):

                if pinch == 0:
                    # click and pinch
                    pinch = 1
                    mouse.press(Button.left)
                    # print(centerR[0], size[0])
            else:
                if pinch == 1:
                    pinch = 0
                    mouse.release(Button.left)

            ### Snapshot ###
            if(dist.euclidean(centerY, centerG) < 95 and dist.euclidean(centerR, centerB) < 95 and dist.euclidean(centerB, centerG) > 20):
                if snap_flag == 0:
                    path = "./snapshots/"
                    img_filename = "snap%d.jpg"
                    cv2.imwrite(os.path.join(path,img_filename) %snap_count, img)
                    snap_count += 1
                    snap_flag = 1
                if(dist.euclidean(centerY, centerG) > 75 and dist.euclidean(centerR, centerB) > 75):
                    snap_flag = 0

        ### Volume Function ###
        if centerB is not None and centerY is not None:

            if centerB[0] > size[0]/2 and centerY[0] > size[0]/2 and dist.euclidean(centerY, centerB) < 65:
                # raise by 2 %
                if centerB[1] < lastR:
                    call(["amixer", "-D", "pulse", "sset", "Master", "2%+"])
                    lastR = centerB[1]
                #lower by 2 %
                elif centerB[1] > lastR:
                    call(["amixer", "-D", "pulse", "sset", "Master", "2%-"])
                    lastR = centerB[1]

            ### Switch b/w apps ###
            # if(dist.euclidean(centerY, centerB) < 80):
            #     keyboard.press(Key.cmd_l)
            #     if dist.euclidean(centerG, centerB) < 65:
            #         if tab_flag == 1:
            #             keyboard.press(Key.tab)
            #             tab_flag = 0
            #         else:
            #             keyboard.release(Key.tab)
            #             tab_flag = 1
            # else:
            #     keyboard.release(Key.cmd_l)
            #     keyboard.release(Key.tab)


        ### Quit ###
        if centerR is not None and centerY is not None :
            if(dist.euclidean(centerR, centerY)) < 40:
                break


        # cv2.imshow("img", img)

        # cv2.imshow("maskOpen", maskOpen)

        # cv2.imshow("cam", img)

        keypress = cv2.waitKey(1) & 0xFF
        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

IdentifyGesture()
cv2.destroyAllWindows()
