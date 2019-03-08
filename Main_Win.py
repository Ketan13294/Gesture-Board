#!/usr/bin/python
import Tkinter
from Tkinter import *
import os
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:

    def __init__(self, master, video_source=0):
        self.master = master
        self.video_source = video_source

        #################
        #Frame Main Menu
        MainM = Frame(master, bd = "1px",width= "200px", height= "240px")
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

        StartRec = Button(M1, text = "Start Record", command = self.StartRec)
        StartRec.grid(row=2,column=1,padx=(20,20),pady=(12,12))

        StopRec =Button(M1 , text = "Stop Record", command = self.StopRec)
        StopRec.grid(row=2,column=2,padx=(20,20),pady=(12,12))

        ShowMark =Button(M1 , text = "Show Markers", command = self.ShowMar)
        ShowMark.grid(row=3,column=1,padx=(20,20),pady=(12,12))

        tex = Text(M1, height=5, width=25)
        tex.grid(row=4, column=1, columnspan=20, padx=(20,20),pady=(5,5))

        CamProp = Button(M1 , text = "Adjust Camera Properties", command = self.CameraAdjust)
        CamProp.grid(row=5,column=1,columnspan=2, padx=(20,20),pady=(10,5))


        ###############################
        #Apps Menu
        AppsM = Frame(gboard, bd = "1px",width= "200px", height= "135px")
        M2 = LabelFrame(AppsM,text="Apps")
        M2.pack(fill="both",expand="yes")
        AppsM.pack_propagate(0)
        AppsM.place(x=0,y=319)

        #Buttons in Apps
        Test = Button(M2, text = "Test", command = self.Testmark, width=9, height=2)
        Test.grid(row=1,padx=(80,20),pady=(20,20))

        Draw = Button(M2, text = "Draw", command = self.Draw, width=9, height=2)
        Draw.grid(row=2,padx=(80,20),pady=(15,15))



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
        self.canvas = Tkinter.Canvas(self.M3, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        # self.btn_snapshot=Tkinter.Button(master, text="Snapshot", width=50, command=self.takeSnapshot)
        # self.btn_snapshot.pack(anchor=Tkinter.CENTER, expand=True)
        self.btn_snapshot =Button(M1 , text = "Take Snapshot", command = self.takeSnapshot)
        self.btn_snapshot.grid(row=3,column=2,padx=(15,15),pady=(12,12))

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

    def delaySnapshot(self, t_sec):
        self.t_sec = t_sec
        self.M3.after(1000*self.t_sec)

    def takeSnapshot(self):

       #Delay for 3 seconds
       # self.delaySnapshot(3)
       # Get a frame from the video source
       # i = 0;
       # for i in range(90000000):
       #      continue;
       ret, frame = self.vid.get_frame()

       # Saves the snapshot into snapshots folder in current directory
       if ret:
           path = "./snapshots/"
           # img_filename = "frame-" + time.strftime("%d-%m-%Y@%H:%M:%S") + ".jpg"
           img_filename = "snap.jpg"
           cv2.imwrite(os.path.join(path,img_filename), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
       # Get a frame from the video source
       ret, frame = self.vid.get_frame()

       if ret:
           self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
           self.canvas.create_image(0, 0, image = self.photo, anchor = Tkinter.NW)

       self.M3.after(self.delay, self.update)


    def MarkerAdd(self):
        os.system('python AddMarker.py')

    def MarkerEd(self):
        os.system('python EdMarker.py')

    def StartRec(self):
        os.system('python StartRec.py')

    def StopRec(self):
        os.system('python StopRec.py')

    def ShowMar(self):
        os.system('python ShowMar.py')

    def CameraAdjust(self):
        os.system('python CameraAdjust.py')

    def Testmark(self):
        os.system('python Testmark.py')

    def Draw(self):
        os.system('python Draw.py')

    def EditMark1(self):
        os.system('python EditMark1.py')

    def EditMark2(self):
        os.system('python EditMark2.py')

    def EditMark3(self):
        os.system('python EditMark3.py')

    def EditMark4(self):
        os.system('python EditMark4.py')


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
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


gboard=Tk()

gboard.title("Gesture Board Controls")
gboard.update_idletasks()
width = 1000
height = 500

gboard.geometry("{}x{}+20+20".format(width,height))
gboard.resizable(0,0)

app = App(gboard)

gboard.mainloop()









# SixthSense = Tk()
# SixthSense.title("Gesture Board")
# SixthSense.geometry("800x600")
# SixthSense.resizable(0,0)
#
# SixthSense.option_add("*Button.Background", "black")
# SixthSense.option_add("*Button.Foreground", "red")
# SixthSense.option_add("*Button.Foreground", "whop")op# frame1 = Frame(SixthSense, width=200,height=300)
# Label(frame1, text = 'Main Menu', width=200, height=20,bg='white', fg='black').pack(side="left")
# frame1.pack_propagate(0)
# frame1.pack(anchor="nw")
#
# #Buttons and Boxes in Main Menu
# AddM = Button(frame1, text="Add Marker",bg="red",fg="black").pack()
#
#
# frame2 = Frame(SixthSense,width=200,height=300)
# Label(frame2, text = 'Apps', width=200, height=20,bg='red', fg='white').pack(side="left")
# frame2.pack_propagate(0)
# frame2.pack(anchor="sw")
#
# #Buttons and Boxes in Apps
#
# frame3 = Frame(SixthSense, width = 600, height = 600)
# Label(frame3, text = "Camera Input", bg = 'black', fg='red').pack(side="top")
# frame3.pack(anchor="e")
#
# SixthSense.mainloop()
