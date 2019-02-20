# ----------------------------------------
#                                        |
# CSCI 442 - Assignment 2 (Part 1)       |
# 02/15/2019                             |
# Written by Logan Davis & Joel Lechman  |
#                                        |
# ----------------------------------------

import cv2
import numpy

#global window height and width for every drawn video window.
windowHeight = 500
windowWidth = 800

#numpy array order: hue, saturation, value
mins = numpy.zeros(3)
maxs = numpy.zeros(3)

#onclick event function for hsv window
def onClick(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
                print(hsv[y,x]) #print out hsv values for current click x,y coords

#adjust mins functions
def adjust_hue_MIN(value):
        mins[0] = value

def adjust_sat_MIN(value):
        mins[1] = value

def adjust_val_MIN(value):
        mins[2] = value

#adjust maxs functions
def adjust_hue_MAX(value):
        maxs[0] = value

def adjust_sat_MAX(value):
        maxs[1] = value

def adjust_val_MAX(value):
        maxs[2] = value


#capture camera and create 3 windows for part 1
cap = cv2.VideoCapture(0)
cv2.namedWindow("hsv",0)
cv2.namedWindow("Video",0)
cv2.namedWindow("track",0)


#creating min/max sliders on hsv window
cv2.createTrackbar('Hue MIN','hsv',0,180,adjust_hue_MIN)
cv2.createTrackbar('Hue MAX','hsv',0,180,adjust_hue_MAX)

cv2.createTrackbar('Sat MIN','hsv',0,255,adjust_sat_MIN)
cv2.createTrackbar('Sat MAX','hsv',0,255,adjust_sat_MAX)

cv2.createTrackbar('Val MIN','hsv',0,255,adjust_val_MIN)
cv2.createTrackbar('Val MAX','hsv',0,255,adjust_val_MAX)

#process each frame
while True:
        status, img = cap.read()

        #display normal video window
        cv2.imshow("Video", img)

        #convert img to HSV and save to hsv
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #display hsv window
        cv2.imshow("hsv", hsv)

        #on click on hsv window, call onClick function
        cv2.setMouseCallback('hsv',onClick)

        #loop through picture and apply object tracking math logic
        track = cv2.inRange(hsv, (mins[0], mins[1], mins[2]), (maxs[0], maxs[1], maxs[2]))

        #Dilate, erode the grayscale image to get a better representation of the object you are tracking.
        kernel = numpy.ones((5,5),numpy.uint8)

        #dialate
        afterDialation = cv2.dilate(track,kernel,iterations = 1)
        #erode
        afterErosion = cv2.erode(afterDialation,kernel,iterations = 1)

        #display final object tracking video window (erosion is after dialating the og grayscale image and then eroding it)
        cv2.imshow("track", afterErosion)

        cv2.resizeWindow('Video', windowWidth,windowHeight)
        cv2.resizeWindow('hsv', windowWidth,windowHeight)
        cv2.resizeWindow('track', windowWidth,windowHeight)

        k = cv2.waitKey(1)
        if k == 27:
                break


cv2.destroyAllWindows()
print("windows closed")

