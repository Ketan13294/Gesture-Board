import cv2
import imutils
import numpy as np
import threading
from scipy.spatial import distance as dist
from pynput.mouse import Controller, Button
import wx

# Snapshot - 2 colours distance < c & diagonal > K
# Click & Hold -  Right hand pointer - mouse, Left hand colour dist < c - Click & hold, Release - release

# Right Hand - Index - RED
# Right Hand - Thumb - BLUE
# Left Hand - Index - YELLOW
# Left Hand - Thumb - GREEN

mouse=Controller()

app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)

def IdentifyGesture():

    # Green Color Limits
    LowG = np.array([33,80,50]);
    UpG = np.array([80,255,255]);
    # Yellow Color Limits
    LowY = np.array([20,80,50]);
    UpY = np.array([30,255,155]);
    # Red Colour Limits
    LowR = np.array([0,80,50]);
    UpR = np.array([10,255,255]);
    # Blue Cot1lor Limits
    LowB = np.array([100,80,50]);
    UpB = np.array([120,255,255]);

    snap_count = 0
    cam= cv2.VideoCapture(0)
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
            if radius > 15 :
                cv2.circle(img,(int(x),int(y)),int(radius),colHSV,2)
                cv2.circle(img,center,5,colHSV,-1)
                return center
            return (0,0)

    def distance(c1, c2):
        return dist.euclidean(c1,c2)
    i=0
    # print "distane", distance((243, 123), (111,673))
    while True:
        ret, img=cam.read()


        # img=cv2.resize(img,(sx,sy))
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

        # ### Take snapshot Gesture - Create rectangle from fingers ###
        # if R1 is not None and R2 is not None and L2 is not None and L1 is not None:
        #     if(distance(R1, L2) < 15 and distance(R2, L1) < 15 and distance(R1, L1) > 20):
        #         path = "./snapshots/"
        #         img_filename = "snap%d.jpg"
        #         cv2.imwrite(os.path.join(path,img_filename) %snap_count, img)
        #         snap_count += 1
        #
        # ### Click - Hold and Release ###
        # hold = False
        # if(distane(L1, L2) < 15)
        #     if(hold):
        #
        #     else:
        #         # click and hold
        #         hold = True
        if centerG is not None and centerB is not None:
            mouse.position = centerG
            while mouse.position != centerG:
                pass

            if(dist.euclidean(centerG, centerB) < 5 0):
                print "Less",i
                i+=1


        cv2.imshow("img", img)
        # cv2.imshow("maskOpen", maskOpen)

        # cv2.imshow("cam", img)

        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

gesture_t = threading.Thread(target = IdentifyGesture)
gesture_t.start()


gesture_t.join()
cv2.destroyAllWindows()
