# import cv2
# import numpy as np
# import time
#
# #   RED color limits
# LowR=np.array([136,87,111]);
# UpR=np.array([180,255,255]);
#
# #   Blue Color Limits
# LowB=np.array([99,115,150]);
# UpB=np.array([110,255,255]);
#
# #   Green COlor Limits
# LowG=np.array([22,60,200]);
# UpG=np.array([60,255,255]);

import cv2
import numpy as np

#   RED color limits
LowR=np.array([136,87,111]);
UpR=np.array([180,255,255]);

#   Blue Color Limits
LowB=np.array([33,80,40]);
UpB=np.array([102,255,255]);

#   Green COlor Limits
LowG=np.array([22,60,200]);
UpG=np.array([60,255,255]);

#
# lowerBound=np.array([33,80,40])
# upperBound=np.array([102,255,255])

cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))


while True:
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # create the Mask
    # mask1=cv2.inRange(imgHSV,LowR,UpR)
    mask=cv2.inRange(imgHSV,LowB,UpB)
    # mask3=cv2.inRange(imgHSV,LowG,UpG)
    # mask=mask1+mask2+mask3

    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        # cv2.cv.PutText(cv2.cv.fromarray(img), str(i+1),(x,y+h),font,(0,255,255))
    cv2.imshow("maskClose",maskClose)
    cv2.imshow("maskOpen",maskOpen)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.waitKey(10)
