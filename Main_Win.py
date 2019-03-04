#!/usr/bin/python
from Tkinter import *
import os


gboard=Tk()
gboard.title("Gesture Board Controls")
gboard.geometry("800x600")
gboard.resizable(0,0)

def MarkerAdd():
    os.system('python AddMarker.py')

def MarkerEd():
    os.system('python EdMarker.py')

def StartRec():
    os.system('python StartRec.py')

def StopRec():
    os.system('python StopRec.py')

def ShowMar():
    os.system('python ShowMar.py')

def CameraAdjust():
    os.system('python CameraAdjust.py')

def Testmark():
    os.system('python Testmark.py')

def Draw():
    os.system('python Draw.py')

def EditMark1():
    os.system('python EditMark1.py')

def EditMark2():
        os.system('python EditMark2.py')

def EditMark3():
    os.system('python EditMark3.py')

def EditMark4():
    os.system('python EditMark4.py')

#################
#Frame Main Menu
MainM = Frame(gboard, bd = "5px", relief="raised",width= "200px", height= "250px")
M1 = LabelFrame(MainM,text="Main Menu")
M1.pack(fill="both",expand="yes")
MainM.pack_propagate(0)
MainM.place(anchor="nw")

# Buttons in Main Menu
AddM = Button(M1, text = "Add Marker", command = MarkerAdd)
AddM.grid(row=1,column=1,padx=(20,20))

EditM = Button(M1, text = "Edit Marker", command = MarkerEd)
EditM.grid(row=1,column=2,padx=(20,20),pady=(12,12))

StartRec = Button(M1, text = "Start Record", command = StartRec)
StartRec.grid(row=2,column=1,padx=(20,20),pady=(12,12))

StopRec =Button(M1 , text = "Stop Record", command = StopRec)
StopRec.grid(row=2,column=2,padx=(20,20),pady=(12,12))

ShowMark =Button(M1 , text = "Show Markers", command = ShowMar)
ShowMark.grid(row=3,column=1,padx=(20,20),pady=(12,12))

tex = Text(M1, height=5, width=25)
tex.grid(row=4, column=1, columnspan=20, padx=(20,20),pady=(5,5))

CamProp = Button(M1 , text = "Adjust Camera Properties", command = CameraAdjust)
CamProp.grid(row=5,column=1,columnspan=2, padx=(20,20),pady=(10,5))

###############################
#Apps Menu
AppsM = Frame(gboard, bd = "5px", relief="raised",width= "200px", height= "200px")
M2 = LabelFrame(AppsM,text="Apps")
M2.pack(fill="both",expand="yes")
AppsM.pack_propagate(0)
AppsM.place(x=0,y=330)

#Buttons in Apps
Test = Button(M2, text = "Test", command = Testmark, width=10, height=2)
Test.grid(row=6,column=1,padx=(20,20),pady=(20,20))

Draw = Button(M2, text = "Draw", command = Draw, width=10, height=2)
Draw.grid(row=6,column=2,padx=(20,20),pady=(20,20))

Marker1 = Button(M2, text = "Edit Marker 1", command = EditMark1, height=2)
Marker1.grid(row=7,column=1,padx=(20,20),pady=(20,20))

Marker2 = Button(M2, text = "Edit Marker 2", command = EditMark2, height=2)
Marker2.grid(row=7,column=2,padx=(20,20),pady=(20,20))

Marker3 = Button(M2, text = "Edit Marker 3", command = EditMark3, height=2)
Marker3.grid(row=8,column=1,padx=(20,20),pady=(20,20))

Marker4 = Button(M2, text = "Edit Marker 4", command = EditMark4, height=2)
Marker4.grid(row=8,column=2,padx=(20,20),pady=(20,20))

########################################
#Camera frame
CamF = Frame(gboard, bd = "5px", relief="raised",width= "390px", height= "450px")
M3 = LabelFrame(CamF,text="Camera Feed")
M3.pack(fill="both",expand=True, anchor=E)
CamF.pack_propagate(0)
CamF.place(x=280,y=0)


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
