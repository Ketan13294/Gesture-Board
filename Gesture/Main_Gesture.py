# organize imports
# -*- coding: utf-8 -*-

import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
# import pyautogui


# global variables
bg = None

# This function finds the running average between background and curr frame
# accumulateWeighted has inbuilt formula -> dst(x,y)=(1−a).dst(x,y)+a.src(x,y)
# with a as accumWeight
def run_avg(frame, a):
    global bg

    if bg is None:
        bg = frame.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(frame, bg, a)

# Finds diffrence between background and current frame and then separates the foreground as white
# and background as black, Find contours and and the contour with the largest area is our hand,
# it is returned
def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)

    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

# Find convex hull of segmented hand. Then find the extreme left, right, top, bottom points to find
# the centre of the hand, little less than maximium distance from centre to extreme points is taken as radius,
# to cover all fingers. A circle is formed which when masked with thresholded value gives cuts used to find number of fingers
def count(thresholded, segmented):
	chull = cv2.convexHull(segmented)

	extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
	extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
	extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
	extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])

    # centre adjusted to account for thumb
	cX = int(extreme_left[0]*0.45 + extreme_right[0]*0.55)
	cY = int(extreme_top[1]*0.3 + extreme_bottom[1]*0.7)


	distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
	maximum_distance = distance[distance.argmax()]

	# calculate the radius of the circle with 80% of the max euclidean distance obtained
	radius = int(0.8 * maximum_distance)

	circumference = (2 * np.pi * radius)

	circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")

	cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

	circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

	(cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	# initalize the finger count
	count = 0

	# loop through the contours found
	for c in cnts:
		(x, y, w, h) = cv2.boundingRect(c)

		# increment the count of fingers only if -
		# 1. The contour region is not the wrist (bottom area)
		# 2. The number of points along the contour does not exceed
		#     10% of the circumference of the circular ROI
		if ((cY + (cY * 0.20)) > (y + h)) and ((circumference * 0.10) > c.shape[0]):
			count += 1

	return count

# Funtion used for callibrating the weighted average model, first 15 frames are used for callibrating with background
# After callibration any movement is captured as white in thres window
def calibrate(gray, accumWeight, num_frames):
    run_avg(gray, accumWeight)
    if num_frames == 1:
        print ("[STATUS] please wait! calibrating...")
    elif num_frames == 14:
        print ("[STATUS] calibration successfull...")
    num_frames += 1

def takeSnapshot():
    # im1 = pyautogui.screenshot()
    # im1.save('my_screenshot.png')
    return

# Exit App
def exitApp():
    # free up memory
    camera.release()
    cv2.destroyAllWindows()

#-------------------------------------------------------------------------------
# Main function
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    accumWeight = 0.5

    #Webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 470, 230, 690

    # initialize num of frames
    num_frames = 0

    calibrated = False

    while(True):
        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=700)

        #Take mirror image
        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)


        if num_frames < 15:
            calibrate(gray, accumWeight, num_frames)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                (thresholded, segmented) = hand
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))

                # count the number of fingers
                fingers = count(thresholded, segmented)

                cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                # # print "Fingers = ", fingers
                if fingers == 0 and num_frames > 100:
                    print ("Exiting Application..")
                    break
                if fingers == 2:
                    takeSnapshot()
                # show the thresholded image
                winname = "Thresholded"
                cv2.imshow(winname, thresholded)
                cv2.moveWindow(winname, 900, 100)

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

exitApp()
