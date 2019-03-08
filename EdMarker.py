from Tkinter import *
from functools import partial
import PIL
import cv2
import os
from PIL import ImageTk, Image


class EdMarker:
    def __init__(self, master):
        self.master = master


        ## Edit Marker Frame ##
        M1 = LabelFrame(master,text="Edit Marker 1")
        M1.grid(row=0, column=0, padx=(70,20))
        M2 = LabelFrame(master,text="Edit Marker 2")
        M2.grid(row=0, column=1, padx=(20,20))
        M3 = LabelFrame(master,text="Edit Marker 3")
        M3.grid(row=0, column=2, padx=(20,20))
        M4 = LabelFrame(master,text="Edit Marker 4")
        M4.grid(row=0, column=3)

        M5 = LabelFrame(master,text = "Snapshot")
        M5.grid(row=1, columnspan=10, padx=(20,20))


        ## Buttons Edit Marker ##
        replaceM1 = Button(M1, text = "Replace", command = partial(self.ReplaceMarker, 1) ,width=9, height=2)
        replaceM1.grid(row=0,column=0,padx=(12,12),pady=(7,7))
        deleteM1 = Button(M1, text = "Delete", command = partial(self.DeleteMarker, 1),width=9, height=2)
        deleteM1.grid(row=1,column=0,padx=(12,12),pady=(7,7))

        replaceM2 = Button(M2, text = "Replace", command = partial(self.ReplaceMarker, 2),width=9, height=2)
        replaceM2.grid(row=0,column=1,padx=(13,13),pady=(7,7))
        deleteM2 = Button(M2, text = "Delete", command = partial(self.DeleteMarker, 2),width=9, height=2)
        deleteM2.grid(row=1,column=1,padx=(12,12),pady=(7,7))

        replaceM3 = Button(M3, text = "Replace", command = partial(self.ReplaceMarker, 3),width=9, height=2)
        replaceM3.grid(row=0,column=2,padx=(12,12),pady=(7,7))
        deleteM3 = Button(M3, text = "Delete", command = partial(self.DeleteMarker, 3),width=9, height=2)
        deleteM3.grid(row=1,column=2,padx=(12,12),pady=(7,7))

        replaceM4 = Button(M4, text = "Replace", command = partial(self.ReplaceMarker, 4),width=9, height=2)
        replaceM4.grid(row=0,column=3,padx=(13,13),pady=(7,7))
        deleteM4 = Button(M4, text = "Delete", command = partial(self.DeleteMarker, 4),width=9, height=2)
        deleteM4.grid(row=1,column=3,padx=(12,12),pady=(7,7))

        ## Display Image in Frame ##
        self.path = "./snapshots/snap.jpg"
         # Load an image using OpenCV
        cv_img = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB)

        # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
        self.height, self.width, self.no_channels = cv_img.shape

        # Create a canvas that can fit the above image
        self.canvas = Canvas(M5, width = self.width, height = self.height)
        self.canvas.pack()

        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))

        # Add a PhotoImage to the Canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)




    def ReplaceMarker(self, id):
        print "Replace marker ", id

    def DeleteMarker(self, id):

        file_path = "./markers/marker" + str(id) + ".txt"
        if(os.path.exists(file_path)):
            os.remove(file_path)
        else:
            print "Marker not added !, File DNE"
        # print "Delete marker ", id

Edmark=Tk()

edMarker = EdMarker(Edmark)

Edmark.title("Edit Markers")
Edmark.geometry("700x650+400+60")
Edmark.resizable(0,0)

Edmark.mainloop()
