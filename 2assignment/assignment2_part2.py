# ----------------------------------------
#                                        |
# CSCI 442 - Assignment 2 (Part 2)       |
# 02/15/2019                             |
# Written by Logan Davis & Joel Lechman  |
#                                        |
# ----------------------------------------

import numpy
import cv2

# helper function to increase brightness of a single frame
def increase_brightness(src, value):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    src = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return src


#capture camera and create windows
cap = cv2.VideoCapture(0)
cv2.namedWindow("normal",0)
#cv2.namedWindow("threechannel",0)

status, img = cap.read()
average = numpy.float32(img)

#process each frame
while True:
        status, img = cap.read()
        
        threeChannel = numpy.float32(img/255)

        #brighten the image slightly
        result = increase_brightness(img,50)
        
        #5x5 mask blur image 5x5 mask
        result = cv2.blur(result, (5,5))

        #accumulateWeighted (take running average)
        cv2.accumulateWeighted(result,average,0.01)
        result = cv2.convertScaleAbs(average)

        #take difference
        result = cv2.absdiff(result,img)
        
        #grayscale the image
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        #threshold the grayscale with low number
        ret1, result = cv2.threshold(result, 10,90, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        #blur again 5x5 mask
        result = cv2.blur(result,(5,5))

        #threshold again
        ret1, result = cv2.threshold(result, 110,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        #contours
        contours = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        for c in contours:
            #if the area is larger than 7500 then draw the rectangle for that group
            if(cv2.contourArea(c) > 7500): 
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


        #refresh all windows
        cv2.resizeWindow('normal', 900, 900)
        cv2.imshow("normal", img)
        cv2.imshow("test",result)
        #cv2.imshow("threechannel", threeChannel)


        #exit with escape key (kill program)
        k = cv2.waitKey(1)
        if k == 27:
                break


cv2.destroyAllWindows()
print("windows closed")