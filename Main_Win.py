#!/usr/bin/python
import tkinter
from tkinter import *
from functools import partial
import os
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
import PIL
import imutils
from pymouse import PyMouse
from pynput.keyboard import Key, Controller
import threading

keyboard = Controller()
l = 0   # average counter
a = 0   # mean x variable
b = 0   # mean y variable
active = "n"

class App:

    def __init__(self, master, video_source=0):
        self.master = master
        self.video_source = video_source

        #################
        #Frame Main Menu
        MainM = Frame(master, bd = "1px",width= "240px", height= "240px")
        M1 = LabelFrame(MainM,text="Main Menu")
        # , width= "800px", height= "200px"
        # MainM.grid(row=0, column=0, columnspan=2)
        M1.pack(fill="both",expand="yes")
        MainM.pack_propagate(0)
        MainM.place(anchor="nw")

        # Buttons in Main Menu
        AddM = Button(M1, text = "Add Marker", command = self.MarkerAdd)
        AddM.grid(row=1,column=1,padx=(20,20))

        EditM = Button(M1, text = "Edit Marker", command = self.MarkerEd)
        EditM.grid(row=1,column=2,padx=(20,20),pady=(12,12))

        StartRec = Button(M1, text = "Start Tracking", command = self.StartTrack)
        StartRec.grid(row=2,column=1,padx=(20,20),pady=(12,12))

        StopRec =Button(M1 , text = "Stop Tracking", command = self.StopTrack)
        StopRec.grid(row=2,column=2,padx=(20,20),pady=(12,12))

        ShowMark =Button(M1 , text = "Show Markers", command = self.ShowMar)
        ShowMark.grid(row=3,column=1,padx=(20,20),pady=(12,12))

        self.tex = Text(M1, height=5, width=25)
        self.tex.grid(row=4, column=1, columnspan=2, padx=(20,20),pady=(5,5))

        CamProp = Button(M1 , text = "Adjust Camera Properties", command = self.CameraAdjust)
        CamProp.grid(row=5,column=1,columnspan=2, padx=(20,20),pady=(10,5))


        ###############################
        #Apps Menu
        AppsM = Frame(gboard, bd = "2px",width= "240px", height= "135px")
        M2 = LabelFrame(AppsM,text="Apps")
        M2.pack(fill="both",expand="yes")
        AppsM.pack_propagate(0)
        AppsM.place(x=0,y=319)

        #Buttons in Apps
        Quit = Button(M2, text = "Quit", command = partial(self.QuitApp, master), width=9, height=2)
        Quit.grid(row=1,padx=(90,20),pady=(20,20))


        # Draw = Button(M2, text = "Draw", command = self.Draw, width=9, height=2)
        # Draw.grid(row=2,padx=(90,20),pady=(15,15))



        ########################################
        #Camera frame
        self.CamF = Frame(gboard, bd = "5px", relief="raised",width= "500px", height= "450px")
        self.M3 = LabelFrame(self.CamF,text="Camera Feed")
        self.M3.pack(fill="both",expand=True, anchor=E)
        self.CamF.pack_propagate(0)
        # self.CamF.place(x=350,y=0)
        self.CamF.pack(anchor=E)

        # open video source (by default this will try to open the computer webcam)
        self.vid = CaptureVideo(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.M3, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        # self.btn_snapshot=tkinter.Button(master, text="Snapshot", width=50, command=self.takeSnapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_snapshot =Button(M1 , text = "Take Snapshot", command = self.takeSnapshot)
        self.btn_snapshot.grid(row=3,column=2,padx=(15,15),pady=(12,12))

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

    def delaySnapshot(self, t_sec):
        self.t_sec = t_sec
        self.M3.after(1000*self.t_sec)

    # Take snapshot in between live camera feed. The video stream pauses for a moment
    # Snapshot is saved in the snapshots folder, replaces the old snapshot.
    def takeSnapshot(self):

       #Delay for 3 seconds

       mil = 3000
       while mil>0 :
           ret, frame = self.vid.get_frame()

           mil = mil-30
           # cv2.imshow("f", frame)
           if cv2.waitKey(10) & 0xFF == ord('q'):
               #this method holds execution for 10 milliseconds, which is why we
               #reduce millis by 10
               break

       # Saves the snapshot into snapshots folder in current directory
       if ret:
           path = "./snapshots/"
           img_filename = "snap.jpg"
           cv2.imwrite(os.path.join(path,img_filename), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    # Update video feed as new frame received
    def update(self):
       # Get a frame from the video source
       ret, frame = self.vid.get_frame()

       if ret:
           self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
           self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

       self.M3.after(self.delay, self.update)


    def MarkerAdd(self):
        os.system('python AddMarker.py')
        self.tex.delete("1.0", END)

    def MarkerEd(self):
        os.system('python EdMarker.py')
        self.tex.delete("1.0", END)

    # Intitiates with input of a frame from the videostream object,
    # masks the unwanted region using the color HSV ranges. After the
    # required region has been found out, largest contour of the particular
    # color is selected and center of area is found out using moment of area
    # which then is highlighted by circular markers. The coordinates of the
    # center of contours is used to scale on the screen size which is then
    # used to move the mouse to the scaled coordinates
    #
    def StartTrack(self):
        global active
        #print(active)
        active = "y"
        # Function which is called when the thread is initiated
        def StTrack():
            # os.system('python StartTrack.py')
            global active
            hand_rect_one_y = None  # lower corner y coordinate
            hand_rect_one_x = None  # lower corner x coordinate
            hand_rect_two_x = None  # Upper corner x coordinate
            hand_rect_two_y = None  # Upper corner y coordinate
            ###############Colour Ranges##############
            # RED color limits
            LowR = np.array([136,87,111]);
            UpR = np.array([180,255,255]);

            # Blue Cot1lor Limits
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
            # the function calculates the coordinates of the center of contour
            # and then scales it to the screen and moves the mouse pointer to
            # the calculated coordinates.
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
            # vdcpt = cv2.VideoCapture(0)
            time.sleep(1)
            mse = PyMouse()
            #print("Press e to exit....")

            while True :

                # extract colors from the images
                ret,img = self.vid.get_frame();     #read frame from video stream
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                img = cv2.resize(img,(1024,768))     #resizing as it is easier to work on a standard size

                # img=cv2.flip(img,1)
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

                # cv2.imshow("cam",img)
                key = cv2.waitKey(10)
                if key == ord("e") or active == "n":
                    #print(active,"waitKey")
                    active = "y"
                    break


        global t1
        t1 = threading.Thread(target=StTrack)
        t1.start()

    # The stop function changes the flag of tracking function to break the
    # tracking function out of the infinite loop and exit the tracking script.
    def StopTrack(self):
        # os.system('python StopTrack.py')
        global active
        global t1
        keyboard.press('e')
        keyboard.release('e')
        active = "n"
        t1.join();

    def ShowMar(self):
        # os.system('python ShowMar.py')
        # For evry marker file, check if exists, then display in text field
        for i in range(4):
            marker_file = "./markers/marker" + str(i+1) + ".txt"
            if os.path.exists(marker_file):
                info =  "Marker " + str(i+1) + " Added\n"
                self.tex.insert(END, info)
            else:
                info = "Marker "+ str(i+1) + " Not Added\n"
                self.tex.insert(END, info)

        # self.tex.delete("1.0", END)


    def CameraAdjust(self):
        os.system('python CameraAdjust.py')

    def Testmark(self):
        os.system('python Testmark.py')

    # Quit App, Before that terminate thread adn release resources
    def QuitApp(self, master):
        # t1.join()
        if active == "y":
            self.StopTrack()
        cv2.destroyAllWindows()
        master.destroy()

    def Draw(self):
        os.system('python Draw.py')


# Class with functions to capture video from the webcam
# get stream frame by frame to perform operations on each frame.
class CaptureVideo:

    def __init__(self, video_source=0):
    # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # cv2.imshow("M3", frame)
                # k = cv2.waitKey(1)
                #
                # if k%256 == 27:
                #     #ESC pressed, dont Save the image
                #     break
                # elif k%256 == 32:
                #     # SPACE pressed
                # Return a boolean success flag and the current frame converted to BGR
                frame = cv2.flip(frame,1)
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Main window props
gboard=Tk()

gboard.title("Gesture Board Controls")
gboard.update_idletasks()
width = 1000
height = 500

gboard.geometry("{}x{}+250+100".format(width,height))
gboard.resizable(0,0)

app = App(gboard)

gboard.mainloop()
