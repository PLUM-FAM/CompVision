import cv2
import numpy

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



imgOne = cv2.imread("one.jpg", cv2.IMREAD_COLOR)
cv2.imshow("img", imgOne)

#Technique 1:

#increase brightness first?
imgOne= increase_brightness(imgOne,70)


#guassian blur (seems to work better) *** 2 blurs works well for img1, 2nd 5x5 mask blur sort of messes up images 3 and 4
blurOne = cv2.GaussianBlur(imgOne,(5,5),0)
blurOne = cv2.GaussianBlur(blurOne,(3,3),0)


#possibly dialating and eroding first
kernel = numpy.ones((5,5),numpy.uint8)

#canny edge detection
edgesOne = cv2.Canny(blurOne,5,150)

cv2.imshow("canny edges", edgesOne)

#finding clircles 
#started with circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
#parameters here: https://docs.opencv.org/3.1.0/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
circles = cv2.HoughCircles(edgesOne,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=20,minRadius=20,maxRadius=40) #leave max radius at 40 (perfect for img 4)
circles = numpy.uint16(numpy.around(circles))

for i in circles[0,:]:
    cv2.circle(edgesOne,(i[0],i[1]),i[2]-5,(255,255,255), -1) #-1 is to fill in the circles. 255's are for white. i[2]-5 is for drawing 5px smaller than orig circle. ensures circles are not overlapping.
    

cv2.imshow('detected circles',edgesOne)



cv2.waitKey(0)
cv2.destroyAllWindows()
