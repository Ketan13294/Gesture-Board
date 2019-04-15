# from tkinter import *
# import cv2
# import PIL
# from PIL import ImageTk
#
# ref_point = []
# crop = False
#
# class AdMarker:
#     def __init__(self, master):
#         self.master = master
#
#
#         ## Edit Marker Frame ##
#         M1 = Frame(master)
#         M1.pack()
#         ## Display Image in Frame ##
#         self.path = "./snapshots/snap.jpg"
#          # Load an image using OpenCV
#         cv_img = cv2.cvtColor(cv2.imread(self.path), cv2.COLOR_BGR2RGB)
#
#         # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
#         self.height, self.width, self.no_channels = cv_img.shape
#
#         # Create a canvas that can fit the above image
#         self.canvas = Canvas(M1, width = self.width, height = self.height)
#         self.canvas.pack()
#
#         # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
#         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
#
#         # Add a PhotoImage to the Canvas
#         self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
#
#         M1.bind("<Button-1>",mouclick)
#         M1.bind("<B1-Motion>",moumove)
#         M1.bind("<ButtonRelease-1>",mouend)
#         self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
#
#
# def mouclick(event):
#     ref_point = [(event.x, event.y)]
# def moumove(event):
#     ref_point[1]=(event.x, event.y)
# def mouend(event):
#     ref_point[1]=(event.x, event.y)
#     cv2.rectangle(self.photo, ref_point[0], ref_point[1], (0, 255, 0), 2)
#
#
#
#
# # def shape_selection(event, x, y, flags, param):
# #     # grab references to the global variables
# #     global ref_point, crop
# #
# #     # if the left mouse button was clicked, record the starting
# #     # (x, y) coordinates and indicate that cropping is being performed
# #     if event == cv2.EVENT_LBUTTONDOWN:
# #         ref_point = [(x, y)]
# #
# #     # check to see if the left mouse button was released
# #     elif event == cv2.EVENT_LBUTTONUP:
# #         # record the ending (x, y) coordinates and indicate that
# #         # the cropping operation is finished
# #         ref_point.append((x, y))
# #
# #         # draw a rectangle around the region of interest
# #         cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
# #         cv2.imshow("image", image)
#
#
#
#
# Addmark = Tk()
# admark = AdMarker(Addmark)
# Addmark.title("Add Marker")
# # Addmark.geometry("800x600)
# Addmark.resizable(0,0)
#
# Addmark.mainloop()




import cv2
import os

ref_point = []
mark_count=[]
crop = False

def markcheck():

    exists = os.path.isfile('./markers/marker1.jpg')
    if exists:
        mark_count.append(1)
    else :
        mark_count.append(0)
    exists = os.path.isfile('./markers/marker2.jpg')
    if exists:
        mark_count.append(1)
    else:
        mark_count.append(0)
    exists = os.path.isfile('./markers/marker3.jpg')
    if exists:
        mark_count.append(1)
    else:
        mark_count.append(0)
    exists = os.path.isfile('./markers/marker4.jpg')
    if exists:
        mark_count.append(1)
    else:
        mark_count.append(0)
    if mark_count == [1,1,1,1]:
        exit(4);




def shape_selection(event, x, y, flags, param):
	# grab references to the global variables
	global ref_point, crop

	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being performed
	if event == cv2.EVENT_LBUTTONDOWN:
		ref_point = [(x, y)]

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		ref_point.append((x, y))

		# draw a rectangle around the region of interest
		cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
		cv2.imshow("image", image)



markcheck()
# load the image, clone it, and setup the mouse callback function
path = "./snapshots/snap.jpg"
# Load an image using OpenCV
image = cv2.imread(path)
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", shape_selection)


# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	# press 'r' to reset the window
	if key == ord("r"):
		image = clone.copy()

	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

if len(ref_point) == 2:
    crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]

path = "./markers/"
if mark_count[0] == 0 :
    img_filename = "marker1.jpg"
    cv2.imwrite(os.path.join(path,img_filename,),crop_img)
elif mark_count[1] == 0:
    img_filename = "marker2.jpg"
    cv2.imwrite(os.path.join(path,img_filename,),crop_img)
elif mark_count[2] == 0:
    img_filename = "marker3.jpg"
    cv2.imwrite(os.path.join(path,img_filename,),crop_img)
elif mark_count[3] == 0:
    img_filename = "marker4.jpg"
    cv2.imwrite(os.path.join(path,img_filename,),crop_img)

# close all open windows
cv2.destroyAllWindows()
exit(0)
