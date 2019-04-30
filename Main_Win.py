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
from pynput.keyboard import Key, Controller as KeyController
import threading
keyboard = KeyController()

# mouse = Cont()
active = "n"


class App:

    def __init__(self, master, video_source=1):
        self.master = master
        self.video_source = video_source

        #################
        #Frame Main Menu
        MainM = Frame(master, bd = "1px",width= "200px", height= "360px")
        M1 = LabelFrame(MainM,text="Main Menu")
        M1.pack(fill="both",expand="yes")
        MainM.pack_propagate(0)
        MainM.place(anchor="nw")

        # Buttons in Main Menu
        # AddM = Button(M1, text = "Add Marker", command = self.MarkerAdd)
        # AddM.grid(row=1,column=1)
        #
        # EditM = Button(M1, text = "Edit Marker", command = self.MarkerEd)
        # EditM.grid(row=1,column=2,padx=(20,20),pady=(12,12))

        StartRec = Button(M1, text = "Start Tracking", command = self.StartTrack)
        StartRec.grid(row=2,column=1,padx=(10,10),pady=(12,12))

        StopRec =Button(M1 , text = "Stop Tracking", command = self.StopTrack)
        StopRec.grid(row=2,column=2,padx=(10,10),pady=(12,12))
        #
        # ShowMark =Button(M1 , text = "Show Markers", command = self.ShowMar)
        # ShowMark.grid(row=3,column=1,padx=(20,20),pady=(12,12))

        # Button that lets the user take a snapshot
        self.btn_snapshot =Button(M1 , text = "Take Snapshot", command = self.takeSnapshot)
        self.btn_snapshot.grid(row=3,column=1,columnspan = 2,padx=(15,15),pady=(12,12))

        self.tex = Text(M1, height=5, width=25)
        self.tex.grid(row=4, column=1, columnspan=2, padx=(20,20),pady=(5,5))

        # CamProp = Button(M1 , text = "Adjust Camera Properties", command = self.CameraAdjust)
        # CamProp.grid(row=5,column=1,columnspan=2, padx=(20,20),pady=(10,5))

        #Buttons in Apps
        Quit = Button(M1, text = "Quit", command = partial(self.QuitApp, master), width=9, height=2)
        Quit.grid(row = 7, column = 1,columnspan = 2, padx=(20,20),pady = (12,12))


        ########################################
        #Camera frame
        self.CamF = Frame(gboard, bd = "5px", relief="raised",width= "500px", height= "450px")
        self.M3 = LabelFrame(self.CamF,text="Camera Feed")
        self.M3.pack(fill="both",expand=True, anchor=E)
        self.CamF.pack_propagate(0)
        self.CamF.pack(anchor=E)

        # open video source (by default this will try to open the computer webcam)
        self.vid = CaptureVideo(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.M3, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

    def delaySnapshot(self, t_sec):
        self.t_sec = t_sec
        self.M3.after(1000*self.t_sec)

    # Take snapshot in between live camera feed. The video stream pauses for a moment
    # Snapshot is saved in the snapshots folder, replaces the old snapshot.
    def takeSnapshot(self):
       # Delay for 3 seconds
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

########################################
# Marker Addition
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
        global t1
        def startt():
            self.vid.__del__()
            os.system('python StartTracking.py')

        t1 = threading.Thread(target = startt)
        t1.start()


    # The stop function changes the flag of tracking function to break the
    # tracking function out of the infinite loop and exit the tracking script.
    def StopTrack(self):
        # os.system('python StopTrack.py')
        global active,keyboard
        global t1
        print(self.vid.isOpen())
        if self.vid.isOpen() == 0 :
            # print(self.vid.isOpen())
            self.vid = CaptureVideo(self.video_source)
        keyboard.press('q')
        keyboard.release('q')
        t1.join()
        active = "n"
        # t1.join();

        # gesture_t.join()

    def ShowMar(self):
        # os.system('python ShowMar.py')
        # For evry marker file, check if exists, then display in text field
        for i in range(4):
            marker_file = "./markers/marker" + str(i+1) + ".jpg"
            if os.path.exists(marker_file):
                info =  "Marker " + str(i+1) + " Added\n"
                self.tex.insert(END, info)
            else:
                info = "Marker "+ str(i+1) + " Not Added\n"
                self.tex.insert(END, info)

    def CameraAdjust(self):
        os.system('python CameraAdjust.py')

    # Quit App, Before that terminate thread adn release resources
    def QuitApp(self, master):
        # t1.join()
        if active == "y":
            self.StopTrack()
        cv2.destroyAllWindows()
        master.destroy()


# Class with functions to capture video from the webcam
# get stream frame by frame to perform operations on each frame.
class CaptureVideo:

    def __init__(self, video_source):
    # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def isOpen(self):
         if not self.vid.isOpened():
             return 0
         else:
             return 1

    def get_frame(self):
        ret = False
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
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
