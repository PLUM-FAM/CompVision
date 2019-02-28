import cv2
import numpy

blueCount = 0
greenCount = 0
yellowCount = 0
orangeCount = 0
brownCount = 0
redCount = 0
unknownCount = 0

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

# onclick event function for hsv window
def onClick(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # print out color values for current click x,y coords (to help figure out color thresholds)
            print(imgOne[y, x])  

whichImage = raw_input("Please enter a filename: ")
imgOne = cv2.imread(whichImage, cv2.IMREAD_COLOR)

cv2.imshow("OG",imgOne)




# increase brightness first
imgOne = increase_brightness(imgOne, 70) #70

# guassian blur (seems to work better) *** 2 blurs works well for img1, 2nd 5x5 mask blur sort of messes up images 3 and 4
blurOne = cv2.GaussianBlur(imgOne, (5, 5), 0)
blurOne = cv2.GaussianBlur(blurOne, (3, 3), 0)

# possibly dialating and eroding first
kernel = numpy.ones((5, 5), numpy.uint8)

# canny edge detection
edgesOne = cv2.Canny(blurOne, 5, 150)
# finding circles 
# initally started with: circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)

circles = cv2.HoughCircles(edgesOne, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=20, minRadius=6, maxRadius=20)

# min radius for houghCircles has to be a max of 13, any higher and img1 wont detect
# param 2 = 20 initially, but working better for all images at 25

circles = numpy.uint16(numpy.around(circles))
listOfCircleImages = []
count = 0

for i in circles[0, :]:
    
    # current image to be added to list of circle images
    currentImg = numpy.zeros((imgOne.shape[0], imgOne.shape[1]), numpy.uint8) 

    # -1 is to fill in the circles. 255's are for white. i[2]-5 is for drawing 5px smaller than orig circle. ensures circles are not overlapping.
    cv2.circle(currentImg,(i[0], i[1]), i[2]-5, (255, 255, 255), -1) 
    cv2.circle(edgesOne,(i[0], i[1]), i[2]-5, (255, 255, 255), -1) #draw one on detected circles window
    listOfCircleImages.append(currentImg)

    # show an individual window for each m&m ##DEBUGING##
    # cv2.imshow(str(len(listOfCircleImages)), currentImg)
    
for img in listOfCircleImages:
    rgb_data = cv2.mean(imgOne, mask = img)
    count += 1
    currentCircle = circles[0,count-1]
  
    cv2.circle(edgesOne, (currentCircle[0], currentCircle[1]), currentCircle[2]-5, (255, 255, 255), -1) #DEBUG draw circles over edges

    # check blue
    if(int(rgb_data[0]) in range(250, 256) and int(rgb_data[1]) in range(155, 239) and int(rgb_data[2]) in range(0, 20)):
        blueCount += 1
        cv2.circle(imgOne, (currentCircle[0], currentCircle[1]), currentCircle[2], (255, 180, 10), -1)
    # check orange
    elif(int(rgb_data[0]) in range(32, 120) and int(rgb_data[1]) in range(98, 160) and int(rgb_data[2]) in range(245, 256)):
        orangeCount += 1
        cv2.circle(imgOne, (currentCircle[0], currentCircle[1]), currentCircle[2], (35, 100, 250), -1)
    # check red
    elif(int(rgb_data[0]) in range(90, 170) and int(rgb_data[1]) in range(75, 140) and int(rgb_data[2]) in range(230, 256)):
        redCount += 1
        cv2.circle(imgOne, (currentCircle[0],currentCircle[1]), currentCircle[2],(0, 0, 255), -1)
    # check yellow
    elif(int(rgb_data[0]) in range(0, 70) and int(rgb_data[1]) in range(220, 256) and int(rgb_data[2]) in range(245, 256)):
        yellowCount += 1
        cv2.circle(imgOne,(currentCircle[0], currentCircle[1]),int(currentCircle[2]),(0,255,255),-1)
    # check green
    elif(int(rgb_data[0]) in range(70, 250) and int(rgb_data[1]) in range(98, 256) and int(rgb_data[2]) in range(0, 50)):
        greenCount += 1
        cv2.circle(imgOne, (currentCircle[0], currentCircle[1]), currentCircle[2], (80, 180, 0), -1)
    # check brown
    elif(int(rgb_data[0]) in range(100, 215) and int(rgb_data[1]) in range(94, 181) and int(rgb_data[2]) in range(105, 161)):
        brownCount += 1
        cv2.circle(imgOne, (currentCircle[0], currentCircle[1]), currentCircle[2], (0, 75, 150), -1)
    else:
        unknownCount += 1


textY = len(imgOne) - 160
# draw total counts on OG window/img
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(imgOne,("Yellow: " + str(yellowCount)), (10, textY), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(imgOne,("Blue: " + str(blueCount)), (10, textY + 30), font, 0.75,(255,255,255),2,cv2.LINE_AA)
cv2.putText(imgOne,("Green: " + str(greenCount)), (10, textY + 60), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(imgOne,("Red: " + str(redCount)), (10, textY + 90), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(imgOne,("Brown: " + str(brownCount)), (10, textY + 120), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(imgOne,("Orange: " + str(orangeCount)), (10, textY + 150), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)

cv2.imshow("img", imgOne)
cv2.setMouseCallback('img', onClick)


cv2.imshow("canny edges", edgesOne) #debug show canny edges and circles overlayed on them.

print(yellowCount, " yellow")
print(blueCount , " blue")
print(greenCount , " green")
print(redCount , " red")
print(brownCount , " brown")
print(orangeCount , " orange")
print(unknownCount , " unknown")



cv2.waitKey(0)
cv2.destroyAllWindows()
